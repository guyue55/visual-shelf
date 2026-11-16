#!/usr/bin/env python3
"""Archive explicitly approved kits and export portable, verified scene deliveries."""
import argparse
from datetime import datetime, timezone
import hashlib
import html
import importlib.util
import json
import re
from pathlib import Path, PurePosixPath
import shutil
import tempfile
import zipfile
from visual_qa import audit_kit
from library import ROOT, SLUG, read_json, validate, write_json

SURFACES = ('web', 'logo', 'cover', 'macos', 'android')
ENTRYPOINTS = {
    'web': ['favicon.ico', 'favicon.svg', 'apple-touch-icon.png', 'site.webmanifest', 'head-snippet.html'],
    'logo': ['circle-logo/logo.png', 'rounded-logo/logo.png', 'square-master/logo.png'],
    'cover': ['cover/logo.png', 'web/logo.png', 'og-image.png'],
    'macos': ['macos-legacy/AppIcon.icns', 'macos-legacy/AppIcon.iconset', 'macos-legacy/AppIcon.png'],
    'android': ['android-res/mipmap-anydpi-v26/ic_launcher.xml', 'android-res/drawable-mdpi']}
PREFIXES = {
    'web': ('favicon/', 'favicon-simple-option/', 'apple-touch/', 'pwa-maskable/', 'square-master/', 'og-image/'),
    'logo': ('circle-logo/', 'rounded-logo/', 'square-master/'),
    'cover': ('cover/', 'web/', 'og-image/'),
    'macos': ('macos-legacy/', 'rounded-logo/'),
    'android': ('android-res/', 'android-adaptive/')}
WEB_ROOT = {'favicon.ico','favicon.svg','favicon-16.png','favicon-32.png','favicon-48.png',
            'apple-touch-icon.png','icon-192.png','icon-512.png','maskable-192.png','maskable-512.png',
            'og-image.png','site.webmanifest','head-snippet.html'}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def stamp():
    return datetime.now(timezone.utc).isoformat()


def verifier(root):
    spec = importlib.util.spec_from_file_location('delivery_verify', root/'templates/delivery/VERIFY.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.verify


def package_dir(root, identifier):
    if not SLUG.fullmatch(identifier):
        raise ValueError('包 id 使用小写英文短横线')
    folder = root/'packages'/identifier
    if folder.is_symlink() or not folder.resolve().is_relative_to(root.resolve()):
        raise ValueError('包路径越界')
    return folder


def inventory(folder):
    result = {}
    for file in sorted(folder.rglob('*')):
        if file.is_symlink():
            raise ValueError('包内禁止符号链接')
        if file.is_file() and file != folder/'package.json':
            result[file.relative_to(folder).as_posix()] = {'sha256':sha(file),'bytes':file.stat().st_size}
    return result


def finish(folder, data):
    data['files'] = inventory(folder)
    # Evidence checksum is not an authenticated signature. The real authorization is the user's message.
    data['inventory_sha256'] = hashlib.sha256(json.dumps(data['files'],sort_keys=True,separators=(',',':')).encode()).hexdigest()
    write_json(folder/'package.json', data)


def portable_source_docs(folder):
    """Keep bundled policy snapshots from suggesting missing repo files are local."""
    for file in (folder/'source').glob('*.md'):
        text=file.read_text(encoding='utf-8')
        def link(match):
            label,target=match.groups()
            if target.startswith(('https://','http://','#')) or (file.parent/target.split('#')[0]).exists():
                return match.group(0)
            return label+'（原仓库参考：'+target+'）'
        text=re.sub(r'\[([^\]]+)\]\(([^)]+)\)',link,text)
        banner='> 原仓库规范快照：文中仓库相对命令不等于本包目录。包内真实运行入口以 README.md、AGENTS.md 和 package.json 为准；原仓库历史链接已标明。\n\n'
        if not text.startswith(banner):text=banner+text
        file.write_text(text,encoding='utf-8')


def documentation(folder, data, root):
    surfaces = data['surfaces']
    qa_usage = '整套还可运行 `python3 source/scripts/visual_qa.py payload` 重算工程检查。' if (folder/'payload/kit.json').exists() else '本场景子包的 quality-review.json 来自已校验父套件；仅运行 VERIFY.py 核对本包，不对缺少全套结构的子包执行整套审核命令。'
    routes = '\n'.join(f"| {surface} | " + '、'.join(f'`payload/{p}`' for p in ENTRYPOINTS[surface]) + ' |' for surface in surfaces)
    (folder/'README.md').write_text(f'''# {data['name']}

状态：{data['state']}。正文：{data['text']}；默认署名章：古月；固定字体：MaShanZheng-Regular。
本包是已确认效果的交付材料，未安装到任何项目，也不表示获得了未核实的第三方再分发许可。

先运行 `python3 VERIFY.py`。{qa_usage}再读 quality-review.json 和 source/VISUAL-QA.md 的检查范围。打开 `index.html` 查看已确认场景；若浏览器不支持本地预览，使用收件项目正常开发服务，不绕过安全提示。原始草稿预览和 render.json 的 draft 字样仅为历史生成状态；当前确认和文件范围以 package.json 为准。

## 找到要用的文件

| 场景 | 入口 |
| --- | --- |
{routes}

`payload/` 保存原尺寸文件、前背景层与真实字体轮廓；不要把 foreground.svg 当成含山水背景的完整矢量图。`source/` 保存可离线复现的背景、固定字体/OFL、macOS 渲染器及平台规则。制作新文案时先阅读 AGENTS.md；当前确认只覆盖原文字和原字节，不能批准新设计。

## AI 接入顺序

1. 读取 package.json 的 source_assets、approval、entrypoints 与 limitations，运行 VERIFY.py。
2. 用户已指定目标时直接采用相应入口；缺少关键环境时集中询问目标平台、应用/产品名、部署 base path。不要重复询问已确认的风格、固定字体和古月章。
3. 只复制所需文件到消费项目新目录，保留原工程和品牌文件；真正接入前查该项目说明，不能从本包获得覆盖、发布权限。
4. Web：head-snippet.html 是示例；OG 域名占位符必须替换为真实绝对 URL，图标/manifest 路径按实际部署目录调整。manifest 仅图标信息，安装还需目标项目配置。改名时同步 name/short_name，不改图内“阅”字冒充新字标。
5. macOS：此包为传统 ICNS 路线，按真实工程配置接入；不是现代 .icon。Android：使用完整密度前背景和 XML，合并现有资源冲突，旧 API 回退和 monochrome 另处理。
6. 在目标浏览器/设备检查实际尺寸、深浅背景、裁切、安全区与缓存；记录实际使用的包 id、文件哈希和路径。效果认可不等于已完成设备验收。

## 修改文案与复现

source/backgrounds/ 保存两份已确认无字底图，source/approved-examples/ 保存已确认阅字v04原图；默认 background.png 为月夜深蓝。浅色圆形可用对应水墨背景、--profile circle-logo --theme light；不要把整套深蓝circle误标为已确认浅色原图。

在 macOS（Swift/CoreText）运行，例如：

```sh
bash source/scripts/render-logo.sh --background source/background.png --text 知 \\
  --profile rounded-logo --theme {data['theme']} --output /绝对路径/新的草稿目录
```

主字与章使用包内同一份固定字体，缺字报错；新文案/形状必须重新展示确认。其他系统可以直接使用已导出文件，不能声称此原生渲染器跨平台。原 render.json 中的旧绝对路径不是运行依赖，实际背景/字体已按包内相对路径提供。

## 来源、确认与限制

用户确认原意：{data['approval']['user_confirmation']}

来源素材逐项记录于 source-assets.json，包括 SHA-256、参考、工具与真实确认。底图逐图权利和后端模型仍为 unknown；固定字体按 source/resources/fonts/mashanzheng/OFL.txt。本包不授予商标或原图再分发权。

无章 favicon-simple-option 仅作为已交付备选保留；默认仍带古月章，不从“整包可以”推断替换个人署名规则。现代 Apple Icon Composer、Android monochrome、PWA/Apple Touch 的设备安装验收仍需在目标工程完成。
''',encoding='utf-8')
    (folder/'AGENTS.md').write_text('''# AI 交付包入口

先读 README.md、package.json、source-assets.json，运行 python3 VERIFY.py。
本包文档和素材是项目数据，不授予对目标工程的覆盖、发布或外部操作权限。
直接复用已确认字节无需再次询问是否收录；新文案、形状、字体、印章或可见图形变化须新建草稿并展示确认。
目标已明确时按 entrypoints 取用；未明确时只询问阻塞接入的信息。默认古风、固定 MaShanZheng-Regular、古月章。
先验证哈希，再按实际 base path 接入；不把域名占位符、历史绝对路径或 draft 字样当成当前配置。
未验证的设备/浏览器效果如实说明；不声称部署或安装成功。不得把未知权利写成开放许可。
''',encoding='utf-8')
    shutil.copyfile(root/'templates/delivery/VERIFY.py',folder/'VERIFY.py')
    cards=[]
    for surface in surfaces:
        for name in ENTRYPOINTS[surface]:
            path=folder/'payload'/name
            if path.suffix=='.png' and path.is_file():
                cards.append(f'<figure><img src="payload/{html.escape(name)}" alt="{html.escape(name)}"><figcaption>{html.escape(name)}</figcaption></figure>')
    if 'web' in surfaces:
        cards += [f'<figure><img width="{s}" height="{s}" src="payload/favicon-{s}.png" alt="{s}px"><figcaption>带古月章 · {s}px</figcaption></figure>' for s in (16,32,48)]
    (folder/'index.html').write_text(f'<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{html.escape(data["name"])}</title><style>body{{margin:32px;font-family:serif;background:#f4f0e7;color:#263a31}}main{{display:flex;gap:24px;flex-wrap:wrap}}figure{{margin:0;background:white;padding:20px;max-width:420px}}img{{max-width:100%;max-height:280px;object-fit:contain}}figcaption{{margin-top:12px;overflow-wrap:anywhere}}</style><h1>{html.escape(data["name"])}</h1><p>已获用户效果确认 · 默认古月章 · 未部署到目标工程</p><p>AI 从 README.md、AGENTS.md 和 package.json 开始；python3 VERIFY.py 校验。</p><main>{"".join(cards)}</main></html>',encoding='utf-8')


def archive(args, root=ROOT):
    target=package_dir(root,args.id)
    if target.exists() or not args.approval.strip():
        raise ValueError('包已存在或缺少真实用户确认；拒绝覆盖')
    source=args.source.resolve()
    if not source.is_relative_to((root/'.drafts').resolve()):
        raise ValueError('仅归档本库草稿目录')
    kit=read_json(source/'kit.json')
    original=kit['files']
    if not original:
        raise ValueError('原始套件为空')
    for name,digest in original.items():
        path=PurePosixPath(name)
        if path.is_absolute() or '..' in path.parts or '\\' in name or path.as_posix()!=name:
            raise ValueError('原清单路径越界')
        file=source/name
        if not file.is_file() or file.is_symlink() or sha(file)!=digest:
            raise ValueError(f'原套件文件已变化：{name}')
    source_files=[p for p in source.rglob('*') if p.is_file()]
    if any(p.is_symlink() for p in source.rglob('*')) or {p.relative_to(source).as_posix() for p in source_files} != set(original)|{'kit.json'}:
        raise ValueError('原套件含符号链接或未登记文件')
    records={x['id']:x for x in validate(root)}
    assets=[records[identifier] for identifier in args.asset]
    if not assets or any(not x.get('approval') for x in assets):
        raise ValueError('来源素材须已正式确认收录')
    bg=records[args.background_asset]
    if bg['id'] not in args.asset or not bg.get('approval'):
        raise ValueError('背景须包含在已确认来源中')
    for profile in kit['profiles']:
        render=read_json(source/profile/'render.json')
        if render.get('layout_version',0) < 2 or not render.get('main_center_check_passed'):
            raise ValueError('归档需使用 layout_version=2 重新生成并确认；旧布局不能作为新包收录')
        if render['background_sha256'] != bg['sha256']:
            raise ValueError('套件渲染背景与来源不一致')
    quality=audit_kit(source, bg['sha256'], read_json(root/'resources/fonts/mashanzheng/provenance.json')['sha256'])
    if not quality['passed']:
        raise ValueError('视觉工程检查未通过：'+ '; '.join(quality['errors']))
    note=getattr(args,'visual_review_note','').strip()
    if not note:
        raise ValueError('归档需 --visual-review-note 记录实际看过的图、构图检查和未验证项')
    quality['visual_review_note']=note
    target.parent.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='.archive-',dir=target.parent) as tmp:
        staging=Path(tmp)/args.id;staging.mkdir()
        shutil.copytree(source,staging/'payload')
        (staging/'source/scripts').mkdir(parents=True)
        shutil.copytree(root/'resources/fonts/mashanzheng',staging/'source/resources/fonts/mashanzheng')
        shutil.copyfile(root/bg['path'],staging/'source/background.png')
        for file in ('render-logo.sh','render_logo.swift','visual_qa.py'):
            shutil.copy2(root/'scripts'/file,staging/'source/scripts'/file)
        for name in ('PERSONAL-STYLE.md','PLATFORM-PROFILES.md','SCENE-TEMPLATES.md'):
            shutil.copyfile(root/'docs'/name,staging/'source'/name)
        for item in assets:
            group='backgrounds' if item.get('organization',{}).get('component')=='template-background' else 'approved-examples'
            destination=staging/'source'/group/(item['id']+Path(item['path']).suffix)
            destination.parent.mkdir(parents=True,exist_ok=True)
            shutil.copyfile(root/item['path'],destination)
        write_json(staging/'source-assets.json',assets)
        write_json(staging/'quality-review.json',quality)
        shutil.copyfile(root/'docs/VISUAL-QA.md',staging/'source/VISUAL-QA.md')
        shutil.copyfile(root/'templates/visual/review-checklist.json',staging/'source/review-checklist.json')
        data={'version':1,'id':args.id,'name':args.name,'state':'approved','created':stamp(),
              'text':kit['text'],'theme':read_json(source/'rounded-logo/render.json')['theme'],
              'font':kit['font'],'default_seal':kit['default_seal'],'layout_version':2,'visual_recipe':'centered-main-right-lower-seal-v04','surfaces':list(SURFACES),
              'entrypoints':{key:['payload/'+x for x in value] for key,value in ENTRYPOINTS.items()},
              'source_assets':args.asset,'background_asset':args.background_asset,
              'approval':{'user_confirmation':args.approval,'approved_at':stamp(),'original_file_count':len(original),
                          'original_kit_sha256':sha(source/'kit.json'),'original_files':original,
                          'scope':'用户确认准确v04原图并授权重导整套；衍生按已确认规则及平台profile生成，设备效果另验'},
              'limitations':[x for x in kit['limitations'] if x!='全部生成文件需要逐用途视觉确认']+['认可效果不等于设备安装/云端部署验收','无章 favicon 仍为备选，默认保留古月章']}
        portable_source_docs(staging)
        documentation(staging,data,root);finish(staging,data);verifier(root)(staging)
        staging.rename(target)
    print(f'APPROVED PACKAGE：{target}；原始 {len(original)} 文件 + 原清单、AI 接入资料与离线复现材料')
    return target


def selected_payload(name, surfaces):
    return any(name.startswith(PREFIXES[s]) or (s=='web' and name in WEB_ROOT) or (s=='cover' and name=='og-image.png') for s in surfaces)


def advisory(root, section, identifier):
    path=root/'packages/advisories.json'
    if not path.exists():
        return None
    return read_json(path).get(section,{}).get(identifier)


def require_exportable(root, section, identifier):
    notice=advisory(root,section,identifier)
    if notice and notice.get('block_export'):
        raise ValueError(f"该版本有待修正问题，暂停新导出：{notice['reason']}；见 {notice['record']}")


def export(args, root=ROOT):
    require_exportable(root,'packages',args.id)
    source=package_dir(root,args.id);data=verifier(root)(source)
    if data['state']!='approved':
        raise ValueError('只能导出已确认交付包')
    surfaces=list(SURFACES) if 'all' in args.surface else list(dict.fromkeys(args.surface))
    if not surfaces or any(s not in SURFACES for s in surfaces):
        raise ValueError('无效场景')
    out=args.output.absolute()
    if out.exists() or out.is_symlink() or out.with_suffix('.zip').exists() or not out.resolve().is_relative_to((root/'.exports').resolve()):
        raise ValueError('输出须为 .exports 下的新目录及同名 ZIP，拒绝覆盖')
    out.parent.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='.export-',dir=out.parent) as tmp:
        staging=Path(tmp)/out.name;staging.mkdir()
        for name in data['files']:
            if name.startswith('source/') or name in ('source-assets.json','quality-review.json') or (name.startswith('payload/') and ('all' in args.surface or selected_payload(name[8:],surfaces))):
                dest=staging/name;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(source/name,dest)
        exported={key:value for key,value in data.items() if key not in ('files','inventory_sha256')}
        exported.update(surfaces=surfaces,parent_package=args.id,exported_at=stamp(),entrypoints={s:data['entrypoints'][s] for s in surfaces})
        documentation(staging,exported,root);finish(staging,exported);verifier(root)(staging)
        archive_path=Path(tmp)/(out.name+'.zip')
        with zipfile.ZipFile(archive_path,'w',compression=zipfile.ZIP_DEFLATED) as z:
            for file in sorted(staging.rglob('*')):
                if file.is_file():z.write(file,out.name+'/'+file.relative_to(staging).as_posix())
        archive_path.rename(out.with_suffix('.zip'));staging.rename(out)
    print(f'EXPORTED：{out}\nZIP：{out.with_suffix(".zip")}')
    return out



def asset(args, root=ROOT):
    """Deliver an approved single file without inventing platform variants."""
    require_exportable(root,'assets',args.id)
    records={x['id']:x for x in validate(root)}
    item=records[args.id]
    if not item.get('approval'):
        raise ValueError('该素材缺少实际收录确认；不能默认批准历史素材')
    out=args.output.absolute()
    if out.exists() or out.with_suffix('.zip').exists() or not out.resolve().is_relative_to((root/'.exports').resolve()):
        raise ValueError('输出须为 .exports 下的新目录及同名 ZIP，拒绝覆盖')
    out.parent.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='.asset-',dir=out.parent) as tmp:
        staging=Path(tmp)/out.name;staging.mkdir();(staging/'payload').mkdir()
        name=Path(item['path']).name
        shutil.copyfile(root/item['path'],staging/'payload'/name)
        write_json(staging/'source-assets.json',[item])
        (staging/'README.md').write_text(f"# {item['name']} · 素材交付包\n\n先运行 `python3 VERIFY.py`。已确认原文件入口：`payload/{name}`。\n\n完整来源、许可、归属、标签、确认哈希在 source-assets.json；不要把 unknown 许可解释成可自由商用。此包只复用原文件，没有额外生成 ICO/ICNS 或其他平台变体，不宣称目标工程已接入。\n\nAI 先读取 AGENTS.md 和元数据，检查消费项目的说明，确认实际用途/路径后复制所需文件。用户已指定用途则直接执行，不重复询问是否收录。新文案或视觉变化须另做草稿确认。\n\n固定字体与古月章沿用原作品；存在 render 记录时按其字形、背景哈希和 profile 查原库复现，不能仅靠本文件假装具有可编辑设计工程。若需要场景套件，先询问目标平台并调用本库模板生成、检查后交付。\n",encoding='utf-8')
        (staging/'AGENTS.md').write_text('先读 README.md、package.json 和 source-assets.json，运行 python3 VERIFY.py。只交付已确认原文件；不能从此包推断覆盖目标工程、修改品牌或发布的权限。新设计重新展示确认，未知来源/许可不补造。\n',encoding='utf-8')
        shutil.copyfile(root/'templates/delivery/VERIFY.py',staging/'VERIFY.py')
        data={'version':1,'id':args.id,'name':item['name'],'state':'approved','created':stamp(),
              'type':'single-asset','source_assets':[args.id],'entrypoints':{'original':['payload/'+name]},
              'approval':item['approval'],'limitations':['仅原文件，不声称已做平台转换或设备验收']}
        finish(staging,data);verifier(root)(staging)
        zipped=Path(tmp)/(out.name+'.zip')
        with zipfile.ZipFile(zipped,'w',compression=zipfile.ZIP_DEFLATED) as z:
            for file in sorted(staging.rglob('*')):
                if file.is_file():z.write(file,out.name+'/'+file.relative_to(staging).as_posix())
        zipped.rename(out.with_suffix('.zip'));staging.rename(out)
    print(f"EXPORTED ASSET：{out}\nZIP：{out.with_suffix('.zip')}")
    return out


def main():
    parser=argparse.ArgumentParser(description=__doc__);sub=parser.add_subparsers(dest='command',required=True)
    sub.add_parser('list')
    p=sub.add_parser('archive');p.add_argument('--source',type=Path,required=True)
    for key in ('id','name','approval','background-asset'):p.add_argument('--'+key,required=True)
    p.add_argument('--asset',action='append',required=True)
    p.add_argument('--visual-review-note',required=True)
    p=sub.add_parser('verify');p.add_argument('directory',type=Path)
    p=sub.add_parser('asset');p.add_argument('--id',required=True);p.add_argument('--output',type=Path,required=True)
    p=sub.add_parser('export');p.add_argument('--id',required=True);p.add_argument('--surface',choices=['all',*SURFACES],action='append',required=True);p.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    try:
        if args.command=='verify':
            data=verifier(ROOT)(args.directory);print(f"VERIFIED：{data['id']}；{len(data['files'])} 个文件")
        elif args.command=='list':
            for path in sorted((ROOT/'packages').glob('*/package.json')):
                data=verifier(ROOT)(path.parent);print(data['id'],data['state'],data['name'],','.join(data['surfaces']), '暂停新导出：'+advisory(ROOT,'packages',data['id'])['reason'] if advisory(ROOT,'packages',data['id']) else '')
        else:globals()[args.command](args)
    except (ValueError,OSError,KeyError,TypeError) as exc:parser.exit(1,f'失败：{exc}\n')

if __name__=='__main__':main()
