#!/usr/bin/env python3
"""Deterministic geometry/recipe/file checks. Does not replace optical or device review."""
import argparse
import hashlib
import json
import math
from pathlib import Path
import struct
import xml.etree.ElementTree as ET

DIMENSIONS={'circle-logo':(1024,1024),'rounded-logo':(1024,1024),'square-master':(1024,1024),'favicon':(256,256),'apple-touch':(180,180),'pwa-maskable':(1024,1024),'android-adaptive':(1080,1080),'og-image':(1200,630),'cover':(1600,900),'web':(1600,600)}
GENERIC={'circle-logo','rounded-logo','square-master','apple-touch'}

def sha(file):return hashlib.sha256(file.read_bytes()).hexdigest()

def png_size(file):
    raw=file.read_bytes()
    if len(raw)<24 or raw[:8]!=b'\x89PNG\r\n\x1a\n':raise ValueError('PNG header 无效')
    return struct.unpack('>II',raw[16:24])

def inside_shape(x,y,profile,w,h):
    if profile=='circle-logo':return math.hypot(x-w/2,y-h/2)<=w*0.475+1e-6
    if profile=='rounded-logo':
        lo_x,hi_x,lo_y,hi_y=w*0.045,w*0.955,h*0.045,h*0.955
        radius=w*0.19
        return lo_x<=x<=hi_x and lo_y<=y<=hi_y and math.hypot(max(lo_x+radius-x,0,x-(hi_x-radius)),max(lo_y+radius-y,0,y-(hi_y-radius)))<=radius+1e-6
    return 0<=x<=w and 0<=y<=h

def corners(g):
    return [(g['x'],g['y']),(g['x']+g['width'],g['y']),(g['x'],g['y']+g['height']),(g['x']+g['width'],g['y']+g['height'])]

def inspect_geometry(data):
    errors=[];profile=data['profile'];w,h=DIMENSIONS[profile]
    if data.get('layout_version',0)<2:errors.append('旧布局版本')
    if (data['width'],data['height'])!=(w,h):errors.append('画布尺寸与profile不符')
    glyphs=data['glyphs'];main=[g for g in glyphs if g['role']=='main']
    if ''.join(g['text'] for g in main)!=data['text']:errors.append('实际正文与文案不符')
    if not main: return errors+['缺少正文轮廓']
    for g in glyphs:
        if not all(isinstance(g[k],(int,float)) and math.isfinite(g[k]) for k in ('x','y','width','height')):return errors+['轮廓坐标非有限数值']
        if g['width']<=0 or g['height']<=0:errors.append('空轮廓')
        if g['x']<0 or g['y']<0 or g['x']+g['width']>w or g['y']+g['height']>h:errors.append('字形超出画布')
        if not all(inside_shape(x,y,profile,w,h) for x,y in corners(g)):errors.append('字形边界超出目标形状')
    left=min(g['x'] for g in main);right=max(g['x']+g['width'] for g in main)
    bottom=min(g['y'] for g in main);top=max(g['y']+g['height'] for g in main)
    if profile in GENERIC: expected=(w/2,h/2)
    elif profile=='favicon':expected=(w*(0.5 if data['seal']=='none' else 0.43),h/2)
    else:expected=(w/2,h*0.54)
    if abs((left+right)/2-expected[0])>0.5 or abs((bottom+top)/2-expected[1])>0.5:errors.append('正文实际轮廓未居中于目标')
    if not data.get('main_center_check_passed') or not data.get('all_glyph_bounds_inside_shape'):errors.append('中心/形状检查未通过')
    sealed=data['seal']!='none';seal=[g for g in glyphs if g['role']=='seal']
    if sealed and ''.join(g['text'] for g in seal)!='古月':errors.append('印章文字不准确')
    if sealed and not data.get('seal_frame_inside_shape'):errors.append('印章含描边未通过形状边界检查')
    if sealed and profile in GENERIC and data.get('seal_placement')!='right-lower':errors.append('通用Logo未使用已确认右下章位')
    if sealed and 'seal_bounds' in data:
        s=data['seal_bounds']
        if not all(isinstance(s[k],(int,float)) and math.isfinite(s[k]) for k in ('x','y','width','height')):return errors+['章框坐标非有限数值']
        stroke=w*0.0015
        expanded={'x':s['x']-stroke,'y':s['y']-stroke,'width':s['width']+stroke*2,'height':s['height']+stroke*2}
        if not all(inside_shape(x,y,profile,w,h) for x,y in corners(expanded)):errors.append('完整章框含描边超出形状')
        if max(left,s['x'])<min(right,s['x']+s['width']) and max(bottom,s['y'])<min(top,s['y']+s['height']):errors.append('主文字与章框重叠')
    if profile in ('pwa-maskable','android-adaptive'):
        radius=w*(0.4 if profile=='pwa-maskable' else 33/108)
        if not all(math.hypot(x-w/2,y-h/2)<=radius+1e-6 for g in glyphs for x,y in corners(g)):errors.append('实际轮廓超出平台安全圆')
    if profile=='pwa-maskable' and not data.get('maskable_glyph_safe_zone_passed'):errors.append('PWA安全圆未通过')
    if profile=='android-adaptive' and not data.get('android_glyph_safe_zone_passed'):errors.append('Android安全圆未通过')
    return errors

def audit_kit(folder, expected_background=None, expected_font=None):
    folder=Path(folder);kit=json.loads((folder/'kit.json').read_text());errors=[];results=[]
    for profile in [*kit['profiles'],'favicon-simple-option']:
        local=[]
        try:
            directory=folder/profile;data=json.loads((directory/'render.json').read_text())
            local=inspect_geometry(data)
            if png_size(directory/'logo.png')!=DIMENSIONS[data['profile']]:local.append('真实PNG尺寸不符')
            if sha(directory/'logo.png')!=data['png_sha256']:local.append('PNG哈希与配方不符')
            if sha(directory/'foreground.svg')!=data['foreground_sha256']:local.append('字形层哈希与配方不符')
            if expected_background and data['background_sha256']!=expected_background:local.append('背景不是已确认来源')
            if expected_font and data['font_sha256']!=expected_font:local.append('固定字体漂移')
            if data['font_postscript']!='MaShanZheng-Regular':local.append('字体名称漂移')
        except (ValueError,OSError,KeyError,TypeError) as exc:local.append(str(exc))
        errors.extend(f'{profile}: {x}' for x in local);results.append({'profile':profile,'passed':not local,'errors':local})
    try:
        manifest=json.loads((folder/'site.webmanifest').read_text())
        for icon in manifest['icons']:
            size=png_size(folder/icon['src'])
            if icon['sizes']!=f'{size[0]}x{size[1]}':errors.append('manifest尺寸声明与PNG不符')
        raw=(folder/'favicon.ico').read_bytes()
        if struct.unpack('<HHH',raw[:6])!=(0,1,3):errors.append('ICO不是三帧')
        for i,size in enumerate((16,32,48)):
            w,h,_,_,_,_,length,offset=struct.unpack('<BBBBHHII',raw[6+i*16:22+i*16])
            if (w,h)!=(size,size) or raw[offset:offset+length]!=(folder/f'favicon/preview-{size}.png').read_bytes():errors.append('ICO帧/偏移不符')
        for density,size in [('mdpi',108),('hdpi',162),('xhdpi',216),('xxhdpi',324),('xxxhdpi',432)]:
            for layer in ('foreground','background'):
                if png_size(folder/f'android-res/drawable-{density}/ic_launcher_{layer}.png')!=(size,size):errors.append('Android密度尺寸错误')
        ET.parse(folder/'android-res/mipmap-anydpi-v26/ic_launcher.xml')
        ET.parse(folder/'favicon.svg')
        if (folder/'macos-legacy/AppIcon.icns').read_bytes()[:4]!=b'icns':errors.append('ICNS文件头错误')
        if len(list((folder/'macos-legacy/AppIcon.iconset').glob('*.png')))!=10:errors.append('iconset槽位不完整')
    except (ValueError,OSError,KeyError,TypeError,struct.error,ET.ParseError) as exc:errors.append(str(exc))
    return {'version':1,'passed':not errors,'errors':errors,'profiles':results,'scope':'确定性轮廓、配方、尺寸与封装校验；PNG只读header，不冒充完整解码或设备/光学验收','requires_visual_review':['参照是否正确','正文与印章整体关系','背景人物残影/裁切','真实小尺寸与深浅背景','目标设备及工程接入'],'limitations':['真实设备安装未由本脚本验证','OG域名仍须消费工程填入','固定字体与底图许可分别处理']}

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('folder',type=Path);args=p.parse_args()
    report=audit_kit(args.folder);print(json.dumps(report,ensure_ascii=False,indent=2))
    if not report['passed']:raise SystemExit(1)
if __name__=='__main__':main()
