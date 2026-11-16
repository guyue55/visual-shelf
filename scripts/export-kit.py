#!/usr/bin/env python3
"""Build a review-only multi-surface design kit; never writes assets/catalog/site."""
import argparse
import hashlib
import html
import json
from pathlib import Path
import shutil
import struct
import subprocess
import sys
from library import ROOT


def ico_from_pngs(files):
    if not files:
        raise ValueError('ICO 至少需要一帧')
    blobs = [p.read_bytes() for p in files]
    offset = 6 + 16*len(files)
    entries = []
    for data in blobs:
        if data[:8] != b'\x89PNG\r\n\x1a\n':
            raise ValueError('ICO 仅封装实际 PNG')
        w,h = struct.unpack('>II',data[16:24])
        if w!=h or not 1<=w<=256:
            raise ValueError('ICO 帧须为 1～256 正方形')
        entries.append(struct.pack('<BBBBHHII',w%256,h%256,0,0,1,32,len(data),offset))
        offset += len(data)
    return struct.pack('<HHH',0,1,len(files)) + b''.join(entries) + b''.join(blobs)


def build(args):
    out=args.output.resolve()
    if out.exists() or not out.is_relative_to((ROOT/'.drafts').resolve()):
        raise ValueError('输出必须为仓库 .drafts/ 下的新目录，不覆盖或自动部署')
    if not args.text.strip() or len(args.text)>2:
        raise ValueError('全套包含浏览器标签，请提供 1～2 字短标记；长封面另行创建')
    out.mkdir(parents=True)
    profiles=['circle-logo','rounded-logo','square-master','favicon','apple-touch','pwa-maskable','android-adaptive','og-image','cover','web']
    for profile in profiles:
        subprocess.run([str(ROOT/'scripts/render-logo.sh'),'--background',str(args.background.resolve()),'--text',args.text,'--profile',profile,'--theme',args.theme,'--output',str(out/profile)],check=True)
    # Alternative only. Sealed design stays the default until a user chooses otherwise.
    subprocess.run([str(ROOT/'scripts/render-logo.sh'),'--background',str(args.background.resolve()),'--text',args.text,'--profile','favicon','--theme',args.theme,'--no-seal','--output',str(out/'favicon-simple-option')],check=True)
    for variant in ('favicon','favicon-simple-option'):
        folder=out/variant
        (folder/'favicon.ico').write_bytes(ico_from_pngs([folder/f'preview-{s}.png' for s in (16,32,48)]))
        svg=(folder/'foreground.svg').read_text()
        end=svg.index('>')+1
        bg='102334' if args.theme=='dark' else 'EAE2D2'
        svg=svg[:end]+f'<rect width="256" height="256" fill="#{bg}"/>'+svg[end:]
        (folder/'favicon.svg').write_text(svg)
    for name,source in {'favicon.ico':'favicon/favicon.ico','favicon.svg':'favicon/favicon.svg','favicon-16.png':'favicon/preview-16.png','favicon-32.png':'favicon/preview-32.png','favicon-48.png':'favicon/preview-48.png','apple-touch-icon.png':'apple-touch/logo.png','icon-192.png':'square-master/preview-192.png','icon-512.png':'square-master/preview-512.png','maskable-192.png':'pwa-maskable/preview-192.png','maskable-512.png':'pwa-maskable/preview-512.png','og-image.png':'og-image/logo.png'}.items():
        shutil.copyfile(out/source,out/name)
    manifest={'name':args.name or args.text,'short_name':args.text,'icons':[{'src':f'icon-{s}.png','sizes':f'{s}x{s}','type':'image/png','purpose':'any'} for s in (192,512)]+[{'src':f'maskable-{s}.png','sizes':f'{s}x{s}','type':'image/png','purpose':'maskable'} for s in (192,512)]}
    (out/'site.webmanifest').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
    (out/'head-snippet.html').write_text('''<!-- Paths are relative examples. Integrate against your real base path and route. -->
<link rel="icon" href="favicon.ico" sizes="16x16 32x32 48x48">
<link rel="icon" href="favicon.svg" type="image/svg+xml" sizes="any">
<link rel="apple-touch-icon" href="apple-touch-icon.png" sizes="180x180">
<link rel="manifest" href="site.webmanifest">
<!-- Replace the following with the real absolute URL before publishing. -->
<meta property="og:image" content="https://YOUR_DOMAIN/og-image.png">
''')
    android=out/'android-res'
    for density,px in [('mdpi',108),('hdpi',162),('xhdpi',216),('xxhdpi',324),('xxxhdpi',432)]:
        folder=android/f'drawable-{density}';folder.mkdir(parents=True)
        for layer in ('foreground','background'):
            subprocess.run(['sips','-z',str(px),str(px),str(out/'android-adaptive'/f'{layer}-layer.png'),'--out',str(folder/f'ic_launcher_{layer}.png')],check=True,stdout=subprocess.DEVNULL)
    xml=android/'mipmap-anydpi-v26';xml.mkdir(parents=True)
    (xml/'ic_launcher.xml').write_text('''<?xml version="1.0" encoding="utf-8"?>
<adaptive-icon xmlns:android="http://schemas.android.com/apk/res/android">
  <background android:drawable="@drawable/ic_launcher_background"/>
  <foreground android:drawable="@drawable/ic_launcher_foreground"/>
</adaptive-icon>
''')
    subprocess.run([str(ROOT/'scripts/export-macos.sh'),str(out/'rounded-logo/logo.png'),str(out/'macos-legacy')],check=True)
    cards=''.join(f'<figure><img src="{p}/logo.png" alt="{p}"><figcaption>{p}</figcaption></figure>' for p in profiles)
    (out/'preview.html').write_text(f'''<!doctype html><html lang="zh-CN"><meta charset="utf-8"><title>{html.escape(args.text)} · 模板套件草稿</title><link rel="icon" href="favicon.ico"><style>body{{font-family:serif;background:#eee8df;color:#252d32;margin:40px}}main{{display:grid;grid-template-columns:repeat(3,1fr);gap:24px}}figure{{margin:0;background:#fff;padding:16px}}img{{width:100%;height:230px;object-fit:contain}}p{{line-height:1.8}}.sizes img{{width:auto;height:auto;margin:12px}}</style><h1>{html.escape(args.text)} · 场景模板草稿</h1><p>全部待确认，未部署、未收录。默认带古月章；简化标签图标只是备选，不自动替换。</p><div class="sizes">'''+''.join(f'<img src="favicon/preview-{s}.png" alt="带章{s}px">' for s in (16,32,48))+''.join(f'<img src="favicon-simple-option/preview-{s}.png" alt="简化备选{s}px">' for s in (16,32,48))+f'</div><main>{cards}</main></html>')
    files={p.relative_to(out).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in out.rglob('*') if p.is_file()}
    (out/'kit.json').write_text(json.dumps({'state':'draft','text':args.text,'font':'MaShanZheng-Regular','default_seal':'古月','simplified_tab_option':'需用户选择，不自动启用','profiles':profiles,'files':files,'limitations':['manifest 只提供图标信息，不含 Service Worker 或完整安装配置','Android XML/密度资源未在设备安装验证，无 monochrome 自动资源','现代 Apple .icon 仍需 Icon Composer','OG 绝对 URL 占位符需接入时替换','全部生成文件需要逐用途视觉确认']},ensure_ascii=False,indent=2)+'\n')
    print(f'DRAFT KIT：{out}/preview.html；{len(files)} 个文件，未批准、未收录、未部署')


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--background',type=Path,required=True)
    parser.add_argument('--text',required=True)
    parser.add_argument('--name',default='')
    parser.add_argument('--theme',choices=['light','dark'],default='dark')
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    try:build(args)
    except (ValueError,OSError,subprocess.SubprocessError) as exc:parser.exit(1,f'失败：{exc}\n')

if __name__=='__main__':main()
