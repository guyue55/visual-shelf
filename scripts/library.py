#!/usr/bin/env python3
"""Visual Shelf: validate, import, create and build with Python 3.11+ stdlib."""
import argparse
import hashlib
import json
import math
import re
import shutil
import sys
import xml.etree.ElementTree as ET
from datetime import date
from pathlib import Path
from xml.sax.saxutils import escape
from organization import registry, validate_organization, public_registry

ROOT = Path(__file__).resolve().parents[1]
KINDS = ('logos', 'icons', 'legends', 'covers')
EXTENSIONS = {'.svg', '.png', '.jpg', '.jpeg', '.webp'}
SLUG = re.compile(r'^[a-z0-9]+(?:-[a-z0-9]+)*$')
# Deliberately restricted static SVG profile; not a general SVG sanitizer.
SVG_TAGS = set('svg g defs path rect circle ellipse line polyline polygon title desc linearGradient radialGradient stop clipPath mask text tspan'.split())
SVG_ATTRS = set('xmlns id viewBox width height x y x1 y1 x2 y2 cx cy r rx ry d points fill fill-rule fill-opacity stroke stroke-width stroke-linecap stroke-linejoin stroke-opacity opacity transform gradientUnits gradientTransform offset stop-color stop-opacity clip-path mask font-family font-size font-weight letter-spacing text-anchor dominant-baseline preserveAspectRatio role aria-label'.split())


def read_json(path):
    return json.loads(path.read_text(encoding='utf-8'))


def write_json(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def metadata_path(root, slug):
    if not SLUG.fullmatch(slug):
        raise ValueError('id 使用英文小写短横线')
    matches = list((root / 'catalog').rglob(slug + '.json'))
    if len(matches) != 1:
        raise ValueError(f'素材 {slug} 元数据不存在或不唯一')
    return matches[0]


def check_svg(data):
    text = data.decode('utf-8')
    if re.search(r'<!|<\?', text):
        raise ValueError('SVG 不接受 DTD、实体、注释或处理指令；请先导出纯静态 SVG')
    svg = ET.fromstring(text)
    if svg.tag != '{http://www.w3.org/2000/svg}svg':
        raise ValueError('SVG 根元素必须声明标准 xmlns')
    box = svg.attrib.get('viewBox', '').replace(',', ' ').split()
    if len(box) != 4 or not all(math.isfinite(float(n)) for n in box) or any(float(n) <= 0 for n in box[2:]):
        raise ValueError('SVG 需要有效的 viewBox')
    for node in svg.iter():
        tag = node.tag.removeprefix('{http://www.w3.org/2000/svg}')
        if tag not in SVG_TAGS:
            raise ValueError(f'SVG 不支持元素: {tag}')
        for key, value in node.attrib.items():
            if key not in SVG_ATTRS:
                raise ValueError(f'SVG 不支持属性: {key}')
            if re.search(r'url\s*\(', value, re.I) and not re.fullmatch(r'url\(#[A-Za-z0-9_-]+\)', value):
                raise ValueError('SVG 禁止外部资源引用')
            if '\\' in value or re.search(r'javascript:|data:|https?:|@import', value, re.I):
                raise ValueError('SVG 禁止外部或可执行内容')
    return [float(box[2]), float(box[3])]


def check_file(path):
    if path.suffix.lower() not in EXTENSIONS:
        raise ValueError('仅支持 SVG、PNG、JPG、WebP')
    if path.is_symlink() or not path.is_file():
        raise ValueError('素材必须是普通文件，禁止符号链接')
    data = path.read_bytes()
    if not data or len(data) > 5 * 1024 * 1024:
        raise ValueError('单个素材须在 1 byte～5 MiB；大型源文件请另存')
    suffix = path.suffix.lower()
    if suffix == '.svg':
        check_svg(data)
    elif not ((suffix == '.png' and data.startswith(b'\x89PNG\r\n\x1a\n')) or
              (suffix in {'.jpg', '.jpeg'} and data.startswith(b'\xff\xd8\xff')) or
              (suffix == '.webp' and data[:4] == b'RIFF' and data[8:12] == b'WEBP')):
        raise ValueError('文件格式与扩展名不符')
    return hashlib.sha256(data).hexdigest()


def validate(root=ROOT):
    records, ids, paths, hashes = [], set(), set(), set()
    groups = registry(root)
    for entry in (root / 'catalog').rglob('*'):
        if entry.is_symlink():
            raise ValueError('catalog 禁止符号链接')
    for meta in sorted((root / 'catalog').rglob('*.json')):
        if meta.is_symlink():
            raise ValueError('元数据禁止符号链接')
        item = read_json(meta)
        for key in ('id', 'name', 'kind', 'path', 'tags', 'source', 'license', 'author', 'created', 'description', 'sha256'):
            if key not in item:
                raise ValueError(f'{meta.name} 缺少 {key}')
        if not isinstance(item['id'], str) or not SLUG.fullmatch(item['id']) or meta.stem != item['id'] or item['id'] in ids:
            raise ValueError(f'无效或重复 id: {meta.name}')
        if item['kind'] not in KINDS:
            raise ValueError('无效分类')
        for key in ('name', 'source', 'license', 'author', 'description'):
            if not isinstance(item[key], str) or not item[key].strip():
                raise ValueError(f'{key} 必须为非空文本；未知信息请填 unknown')
        if item['source'] not in ('original', 'unknown') and not re.fullmatch(r'https?://\S+', item['source']):
            raise ValueError('来源须为 http(s) URL、original 或 unknown')
        date.fromisoformat(item['created'])
        if not isinstance(item['tags'], list) or not item['tags'] or not all(isinstance(t, str) and t.strip() for t in item['tags']):
            raise ValueError('tags 须为非空字符串数组')
        if 'organization' in item:
            validate_organization(item['organization'], groups)
        if not isinstance(item['path'], str):
            raise ValueError('素材路径必须为字符串')
        rel = Path(item['path'])
        if rel.is_absolute() or not 3 <= len(rel.parts) <= 8 or rel.parts[:2] != ('assets', item['kind']) or '..' in rel.parts or not SLUG.fullmatch(rel.stem) or not all(SLUG.fullmatch(p) for p in rel.parts[2:-1]):
            raise ValueError('素材路径须为 assets/<分类>/[分组目录/]<kebab-case>.<格式>')
        path = root / rel
        if not path.resolve().is_relative_to((root / 'assets').resolve()):
            raise ValueError('路径越界')
        digest = check_file(path)
        if digest != item['sha256']:
            raise ValueError(f'{item["id"]} 内容哈希不符；确认修改后更新元数据')
        if 'approval' in item:
            approval = item['approval']
            if not isinstance(approval, dict) or not isinstance(approval.get('user_confirmation'), str) or not approval['user_confirmation'].strip() or approval.get('reviewed_sha256') != digest:
                raise ValueError(f'{item["id"]} 用户确认记录缺失或不匹配当前文件；需重新确认')
        if digest in hashes or str(rel) in paths:
            raise ValueError('重复素材内容或路径')
        ids.add(item['id']); paths.add(str(rel)); hashes.add(digest)
        records.append(item)
    for path in (root / 'assets').rglob('*'):
        if path.is_symlink():
            raise ValueError('assets 禁止符号链接')
        if path.is_file() and path.name != '.gitkeep' and path.relative_to(root).as_posix() not in paths:
            raise ValueError(f'未登记素材: {path.relative_to(root)}')
    return records


def add(file, slug, name, kind, tags, source, license_name, author, description, root=ROOT, organization=None, folder=None):
    if not SLUG.fullmatch(slug) or kind not in KINDS:
        raise ValueError('id 使用英文小写短横线；kind 使用 logos/icons/legends/covers')
    records = validate(root)
    digest = check_file(file)
    if organization is not None:
        validate_organization(organization, registry(root))
        if folder is None:
            owner = organization['owner']
            prefix = owner.replace('product:', 'products/').replace('project:', 'projects/')
            folder = prefix + '/' + (organization.get('series') or 'general')
            if organization.get('component'):
                folder += '/' + organization['component']
    group = Path(folder) if folder else Path()
    if group.is_absolute() or any(not SLUG.fullmatch(p) for p in group.parts) or len(group.parts) > 5:
        raise ValueError('分组目录使用小写英文短横线，最多五层，禁止越界')
    dest = root / 'assets' / kind / group / (slug + file.suffix.lower())
    meta = root / 'catalog' / group / (slug + '.json')
    if not dest.resolve().is_relative_to((root/'assets').resolve()) or not meta.resolve().is_relative_to((root/'catalog').resolve()):
        raise ValueError('分组路径越界')
    if dest.exists() or meta.exists() or any(x['sha256'] == digest or x['id'] == slug for x in records):
        raise ValueError('id、路径或内容已存在，拒绝覆盖')
    item = dict(id=slug, name=name, kind=kind, path=dest.relative_to(root).as_posix(), tags=tags,
                source=source, license=license_name, author=author, created=date.today().isoformat(),
                description=description, sha256=digest)
    if organization is not None:
        item['organization'] = organization
    # Validate all metadata in isolation before making any repository change.
    import tempfile
    with tempfile.TemporaryDirectory() as tmp:
        candidate = Path(tmp)
        (candidate / 'catalog').mkdir()
        if (root/'organization.json').exists():
            shutil.copyfile(root/'organization.json',candidate/'organization.json')
        target = candidate / 'assets' / kind / group
        target.mkdir(parents=True)
        shutil.copyfile(file, target / dest.name)
        candidate_meta = candidate / 'catalog' / group / meta.name
        candidate_meta.parent.mkdir(parents=True, exist_ok=True)
        write_json(candidate_meta, item)
        validate(candidate)
    dest.parent.mkdir(parents=True, exist_ok=True)
    meta.parent.mkdir(parents=True, exist_ok=True)
    with dest.open('xb') as stream:
        stream.write(file.read_bytes())
    try:
        with meta.open('x', encoding='utf-8') as stream:
            stream.write(json.dumps(item, ensure_ascii=False, indent=2) + '\n')
    except Exception:
        dest.unlink()
        raise
    return item


def create_svg(kind, title, color, subtitle='VISUAL NOTES'):
    if not re.fullmatch(r'#[0-9a-fA-F]{6}', color):
        raise ValueError('颜色须为 #RRGGBB')
    title, subtitle = escape(title), escape(subtitle)
    if kind == 'covers':
        return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1600 900"><rect width="1600" height="900" fill="#f3f0e9"/><circle cx="1420" cy="150" r="310" fill="{color}"/><path d="M1120 900V480h480" fill="none" stroke="#161e29" stroke-width="2"/><text x="96" y="130" font-family="sans-serif" font-size="24" letter-spacing="6" fill="#58616d">{subtitle}</text><text x="96" y="490" font-family="sans-serif" font-size="88" font-weight="700" fill="#161e29">{title}</text><path d="M96 570h150" stroke="{color}" stroke-width="10"/><text x="96" y="800" font-family="sans-serif" font-size="24" fill="#58616d">PERSONAL COLLECTION / 16:9</text></svg>'''
    if kind == 'legends':
        return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 640 240"><rect width="640" height="240" rx="24" fill="#f3f0e9"/><circle cx="64" cy="88" r="12" fill="{color}"/><text x="96" y="98" font-family="sans-serif" font-size="28" fill="#161e29">{title}</text><path d="M52 166h70" stroke="{color}" stroke-width="6" stroke-linecap="round"/><text x="148" y="175" font-family="sans-serif" font-size="24" fill="#58616d">{subtitle}</text></svg>'''
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect x="8" y="8" width="48" height="48" rx="14" fill="{color}"/><path d="M20 32l8 8 16-16" fill="none" stroke="#ffffff" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/></svg>'''


def build(root=ROOT):
    records = validate(root)
    out = root / 'dist'
    # Only this generated directory is replaceable.
    if out.is_symlink():
        raise ValueError('dist 不得为符号链接')
    if out.exists():
        shutil.rmtree(out)
    shutil.copytree(root / 'site', out)
    shutil.copytree(root / 'assets', out / 'assets')
    write_json(out / 'catalog.json', records)
    write_json(out / 'organization.json', public_registry(root, records))
    index = out / 'index.html'
    markup = index.read_text(encoding='utf-8')
    for name in ('app.js','catalog-model.js','style.css'):
        file = out / name
        if file.is_file():
            version = hashlib.sha256(file.read_bytes()).hexdigest()[:12]
            markup = markup.replace('\"'+name+'\"', '\"'+name+'?v='+version+'\"')
    index.write_text(markup, encoding='utf-8')
    (out / '.nojekyll').touch()
    print(f'构建完成：{len(records)} 项 → dist/')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    sub.add_parser('validate'); sub.add_parser('build')
    for command in ('add', 'create'):
        p = sub.add_parser(command)
        if command == 'add':
            p.add_argument('file', type=Path)
            p.add_argument('--source', required=True)
            p.add_argument('--license', required=True)
        else:
            p.add_argument('--color', default='#d96b45')
            p.add_argument('--subtitle', default='VISUAL NOTES')
            p.add_argument('--license', default='LicenseRef-All-Rights-Reserved')
        p.add_argument('--id', required=True)
        p.add_argument('--name', required=True)
        p.add_argument('--kind', choices=KINDS if command == 'add' else ('icons', 'legends', 'covers'), required=True)
        p.add_argument('--tags', required=True, help='逗号分隔，中英文均可')
        p.add_argument('--author', default='unknown')
        p.add_argument('--description', default='unknown')
        p.add_argument('--owner', help='organization.json 中已登记的归属')
        p.add_argument('--series')
        p.add_argument('--component')
        p.add_argument('--function', action='append', default=[])
        p.add_argument('--platform', action='append', default=[])
        p.add_argument('--folder', help='可选本地分组目录；已有 URL 不会自动迁移')
        if command == 'add':
            p.add_argument('--approval-note', required=True, help='用户对当前文件/版本的实际收录确认；AI 不得代签')
    args = parser.parse_args()
    try:
        if args.command == 'validate':
            print(f'校验通过：{len(validate())} 项')
        elif args.command == 'build':
            build()
        else:
            if args.command == 'create':
                if not SLUG.fullmatch(args.id):
                    raise ValueError('id 使用英文小写短横线')
                if args.folder:
                    raise ValueError('create 只生成草稿，不接受 --folder；正式收录时自动确定目录')
                org = dict(owner=args.owner, series=args.series, component=args.component, functions=args.function, platforms=args.platform) if args.owner else None
                if not args.owner and (args.series or args.component or args.function or args.platform):
                    raise ValueError('设置结构化信息时须指定 --owner')
                if org:
                    validate_organization(org, registry(ROOT))
                svg = create_svg(args.kind, args.name, args.color, args.subtitle)
                check_svg(svg.encode())
                directory = ROOT / '.drafts' / args.id
                directory.mkdir(parents=True, exist_ok=False)
                (directory / 'template.svg').write_text(svg, encoding='utf-8')
                write_json(directory / 'task.json', dict(job=args.id, style='parameterized',
                    purpose=args.kind, kind=args.kind, text=args.name, owner=args.owner or 'unknown', proposed_organization=org,
                    reference=None, reference_sha256=None, state='prepared'))
                print(f'草稿已创建：{directory / "template.svg"}；尚未收录。用 studio.py review 后展示给用户确认。')
                return
            if not args.approval_note.strip():
                raise ValueError('必须记录用户的实际收录确认')
            org = dict(owner=args.owner, series=args.series, component=args.component, functions=args.function, platforms=args.platform) if args.owner else None
            if not args.owner and (args.series or args.component or args.function or args.platform):
                raise ValueError('设置系列/组件等结构化信息时须指定 --owner')
            item = add(args.file, args.id, args.name, args.kind, [x.strip() for x in args.tags.split(',') if x.strip()], args.source, args.license, args.author, args.description, organization=org, folder=args.folder)
            item['approval'] = dict(user_confirmation=args.approval_note, reviewed_sha256=item['sha256'])
            write_json(metadata_path(ROOT, args.id), item)
            print(f'已登记 {item["id"]}；运行 build 更新预览')
    except (ValueError, OSError, KeyError, TypeError, ET.ParseError) as exc:
        parser.exit(1, f'失败：{exc}\n')


if __name__ == '__main__':
    main()
