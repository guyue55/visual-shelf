#!/usr/bin/env python3
"""Prepare image tasks outside the public catalog; review exact bytes before acceptance."""
import argparse
import hashlib
import json
import re
from pathlib import Path
import shutil
import sys
from datetime import datetime, timezone
from library import ROOT, SLUG, add, check_file, read_json, write_json


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def job_dir(job):
    if not SLUG.fullmatch(job):
        raise ValueError('任务 id 须为小写英文短横线')
    directory = ROOT / '.drafts' / job
    if directory.is_symlink() or not directory.resolve().is_relative_to(ROOT.resolve()):
        raise ValueError('草稿路径越界')
    return directory


def save(path, data):
    temporary = path.with_suffix('.tmp')
    write_json(temporary, data)
    temporary.replace(path)


def prepare(args):
    styles = read_json(ROOT / 'templates' / 'visual' / 'styles.json')
    style = styles[args.style]
    reference = read_json(ROOT / 'catalog' / (style['reference'] + '.json'))
    directory = job_dir(args.job)
    directory.mkdir(parents=True, exist_ok=False)
    file = ROOT / reference['path']
    check_file(file)
    reference_file = 'reference' + file.suffix.lower()
    shutil.copyfile(file, directory / reference_file)
    task = dict(job=args.job, style=args.style, purpose=args.purpose, text=args.text,
                owner=args.owner, instructions=args.instructions, reference=style['reference'],
                reference_file=reference_file, reference_sha256=digest(file), state='prepared', created=datetime.now(timezone.utc).isoformat())
    save(directory / 'task.json', task)
    sizes = {'web':'横幅构图；未指定尺寸时先以 1600×600 探索，布局需重新设计，不拉伸圆角图标',
             'cover':'16:9，1600×900 探索；真实平台尺寸另核对，保留标题安全区域',
             'logo':'以 1:1 探索；保留识别主体，复杂纹理可建议简化，位图不冒充矢量',
             'app-icon':'1:1，1024×1024 探索；保留透明圆角，检查缩小后的辨识度'}
    prompt = f'''# 制作任务 {args.job}

- 已确认喜欢的风格：{style['name']}；{style['direction']}。
- 本次用途：{args.purpose}；{sizes[args.purpose]}。
- 准确主文案：{args.text or 'unknown；若涉及准确字标需补充'}。
- 主要归属：{args.owner}。它与参考图来源产品不是同一概念，不自动署名 MacRightClick。
- 本次附加要求：{args.instructions or '无'}。
- 实际参考：{reference_file}；source asset id：{style['reference']}。

## 执行要求

先查看参考，再使用当前可用图像编辑工具处理。原图文字已栅格化；换大字需局部重绘或重建字形，不直接覆盖旧字造成残影。图形与标题可分层排版，精确中文逐字核对。古月印章不自动迁移到新项目，默认移除或按明确要求替换。保留用户指定不变项。

如果任务是介绍 MacRightClick 且未要求改 Logo，原标识保持原样；若明确要求换字或跨产品创作，本任务制作衍生稿，不替换原项目图标。web/封面需要重构横向版式，不能靠拉伸源图实现。

本文件是参考与需求，不是生成成功证据。候选保存在本任务目录或明确的工作位置，生成后用 review 登记准确文件。AI 检查文字、残影、比例、边缘、透明区域、目标尺寸后向用户展示。用户未明确满意，不允许 accept 或底层 add/create 入正式库。

## 建议补充（不重复询问已有信息）

真实归属、准确文案、用途、目标比例为优先项；背景/印章文字有歧义且影响结果时集中问一次。可选补充：别名、主题标签、可编辑源、模型与参考来源、字体与许可。未知可以记 unknown，不阻塞探索稿。
'''
    (directory / 'prompt.md').write_text(prompt, encoding='utf-8')
    print(f'PREPARED：{directory}\n已复制原图；尚未生成或编辑。执行建议见 prompt.md')


def review(args):
    directory = job_dir(args.job)
    task = read_json(directory / 'task.json')
    if task['state'] == 'accepted':
        raise ValueError('已收录任务不再修改；新建任务或修订')
    original = args.file.resolve()
    check_file(original)
    if digest(original) == task['reference_sha256']:
        raise ValueError('这是未修改的参考图，不作为新的衍生成品收录')
    if not args.checks.strip():
        raise ValueError('需记录实际检查与未验证项')
    target = directory / ('candidate' + original.suffix.lower())
    if original != target.resolve():
        shutil.copyfile(original, target)
    task.update(state='awaiting-user', candidate=target.name, candidate_sha256=digest(target),
                checks=args.checks, tool=args.tool)
    task.pop('approval', None)
    save(directory / 'task.json', task)
    print(f'AWAITING_USER：{target}\nSHA256={task["candidate_sha256"]}\n需展示此文件并等待用户确认；更改文件后必须重新 review')


def accept(args):
    directory = job_dir(args.job)
    task = read_json(directory / 'task.json')
    if task['state'] != 'awaiting-user':
        raise ValueError('任务须先 review 并等待用户确认')
    if not args.approval.strip():
        raise ValueError('必须记录用户对该版本的实际确认，不得由 AI 自行批准')
    candidate = directory / task['candidate']
    if args.sha256 != task['candidate_sha256'] or digest(candidate) != args.sha256:
        raise ValueError('文件或确认哈希已变化，需重新 review 并让用户确认当前版本')
    if args.owner == 'unknown':
        raise ValueError('正式入库前请补充真实 owner（探索阶段可 unknown）')
    if not (args.owner == 'shared' or re.fullmatch(r'(product|project):[a-z0-9]+(?:-[a-z0-9]+)*', args.owner)):
        raise ValueError('owner 使用 product:<slug>、project:<slug> 或 shared')
    if not SLUG.fullmatch(args.family) or not SLUG.fullmatch(args.variant) or not re.fullmatch(r'v[0-9]{2,}', args.revision):
        raise ValueError('family/variant 须为英文短横线标识，revision 使用 v01 等编号')
    if not all(t.strip() for t in args.tags.split(',')):
        raise ValueError('补充标签不能含空值')
    note = dict(user_confirmation=args.approval, reviewed_sha256=args.sha256, task=args.job,
                checks=task['checks'], tool=task['tool'], template=task['style'],
                reference=task['reference'], approved_at=datetime.now(timezone.utc).isoformat())
    kind = task.get('kind') or ('covers' if task['purpose'] in ('web','cover') else 'logos')
    item = add(candidate, args.id, args.name, kind,
               [f'owner:{args.owner}', f'family:{args.family}', f'variant:{args.variant}',
                f'revision:{args.revision}', 'status:ready', '用户已确认', task['purpose'], *args.tags.split(',')],
               'original', args.license, args.author, args.description, root=ROOT)
    item['approval'] = note
    save(ROOT / 'catalog' / (args.id + '.json'), item)
    task.update(state='accepted', asset_id=args.id, approval=note)
    save(directory / 'task.json', task)
    print(f'ACCEPTED：{args.id}；请同步实体卡、品牌决策与制作记录，然后 restart 更新预览')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    sub.add_parser('list')
    p = sub.add_parser('prepare')
    p.add_argument('--job', required=True)
    p.add_argument('--style', choices=['ink-light-a','ink-light-b','moonlit-blue'], required=True)
    p.add_argument('--purpose', choices=['web','cover','logo','app-icon'], required=True)
    p.add_argument('--text', default='')
    p.add_argument('--owner', default='unknown')
    p.add_argument('--instructions', default='')
    p = sub.add_parser('review')
    p.add_argument('--job', required=True); p.add_argument('--file', type=Path, required=True)
    p.add_argument('--checks', required=True); p.add_argument('--tool', default='unknown')
    p = sub.add_parser('accept')
    for key in ('job','sha256','approval','id','name','owner','family','variant','revision','description'):
        p.add_argument('--'+key, required=True)
    p.add_argument('--tags', default='常用'); p.add_argument('--license', default='unknown'); p.add_argument('--author', default='unknown')
    args = parser.parse_args()
    if args.command == 'list':
        for key, style in read_json(ROOT / 'templates' / 'visual' / 'styles.json').items():
            print(key, style['name'], style['direction'])
    else:
        globals()[args.command](args)


if __name__ == '__main__':
    try:
        main()
    except (ValueError, OSError, KeyError) as exc:
        print(f'失败：{exc}', file=sys.stderr)
        sys.exit(1)
