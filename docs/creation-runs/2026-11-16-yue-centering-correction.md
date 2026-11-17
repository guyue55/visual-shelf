> 历史记录：文中的旧阅字v04、早期章候选及套件v02已由v06/整套v03替代，原路径不再作为取用入口。当前确认、配色、复现与清理见 [正式交付](2026-11-17-v06-final-delivery.md)。原MacRightClick来源与A/C底图不因此停用。

# 阅字居中问题复核与修正候选

> 历史过程记录。2026-11-16用户已最终确认v04并要求清理错误版本；本页旧路径/待核查状态仅供追溯，不能作为当前操作入口。请读 [最终收录与清理](2026-11-16-v04-final-delivery.md) 和 [视觉QA](../VISUAL-QA.md)。

日期：2026-11-16。用户发现阅字似乎未居中，要求对照 MacRightClick 原右字图标，若确有问题则修正、展示核查并沉淀规则。本轮仅修改模板与生成新候选，尚未获得修正版效果确认。

## 结论与原因

旧圆形水墨和圆角月夜两款阅字 v02 的主字轮廓联合边界中心为 (527.36,568.32)，画布中心 (512,512)。CoreGraphics 坐标 y 向上，所以图片里是偏右 15.36 px（1.5%）、偏上 56.32 px（5.5%）。这不是字体基线或页面卡片造成的错觉。

根因是旧单字排版框 x=28.5%、y=32%、width=46%、height=47%，中心本来就是 (51.5%,55.5%)；旧规则“居中偏上”没有明确量化中心并验收。drawGlyph 在框内居中是正确的，但框偏离画布，所以单字最终偏移。此前仅测试轮廓在形状内，没有测试它是否居中。

已实际查看原右字 PNG 和阅字：右字笔画更舒展、占画面更大。原右字没有独立矢量/字体层，不能把目视判断冒充精确字体中心测量；这次问题证据来自阅字可测的真实轮廓。不擅自仿造右字字体，也不在定位修正中改变阅字字号。

## 本轮修正

- 通用圆形、圆角方形、方形母版及 Apple Touch 正文框以画布中心为目标。
- 先计算所有正文真实轮廓联合边界，再整体平移对齐目标；避免不同宽度字形、尾行居中后整个组仍偏移。
- 古月章独立定位，不纳入正文中心计算；背景、字体文件、主字大小和章字形位置均与旧版一致，已逐项核对。
- favicon、PWA、Android、横向标题区仍按各自 profile 的既定目标，明确标为 profile-title-area，不能宣称全部都在画布中心；安全区继续独立检查。
- render.json 新增 layout_version=2、main_bounds、main_center_expected/actual、main_canvas_offset、main_center_policy、main_center_check_passed 及坐标说明。误差必须≤0.5px，否则渲染失败；review 将这些字段带入确认记录。

完整机器测量见 [复核数据](../evidence/2026-11-16-yue-centering.json)。这是几何居中，仍需用户核查书法的光学观感；如再微调，记录明确偏移和适用场景，不静默更改默认规则。

## 待核查的两份准确候选

| 候选 | 新中心 | PNG SHA-256 |
| --- | --- | --- |
| .drafts/yue-circle-v03-centered/candidate.png | (512,512) | 9eb85c670d98e2a50b0df9888f259ccacfc9ca1332d2c4a92c309542531c8d74 |
| .drafts/yue-rounded-v03-centered/candidate.png | (512,512) | c02f964fbacac4c9bc40a3e68a56834402f66134cfa4d045980593f6f40e87cd |

两份均已实际查看 1024 PNG，并由 studio review 登记为 awaiting-user。没有 accept，没有把新图塞入 dist；用户核查满意后再用新 id/revision 收录，并按新渲染器重做受影响场景包，不能沿用本轮前的整包确认。

可重复生成（使用新输出目录，渲染器拒绝覆盖）：

```sh
bash scripts/render-logo.sh \
  --background assets/icons/shared/guyue-ink-backgrounds/template-background/shared-guyue-background-moonlit-blue-v01-png.png \
  --text 阅 --profile rounded-logo --theme dark \
  --output .drafts/yue-centered-next-render
```

## 已有版本与交付

旧两份阅字保留原路径、PNG 和真实历史批准，将状态改为 deprecated，并注明排版待修。无字底图 A/C 不受影响。旧 yue-surface-kit-v01 与全部 185 原文件、字体和渲染器仍原样保存，独立 VERIFY.py 继续能证明其历史完整性；它不是本轮修正版。

packages/advisories.json 记录两个旧 asset id 和旧包问题，list 显示，export/asset 暂停新导出。新整套 archive 要求每个场景均为 layout_version≥2 且通过中心检查，不能换 id 重收旧布局。已生成的 .exports 旧 ZIP 为历史文件，不能当作修正版交付；本轮没有重打包冒充已确认。

本库模板索引附排版复核提示，prepare 将该提示写入 task 和 prompt，避免 AI 继续把旧阅字样例当成居中基线。旧包离线校验只证明字节未损坏，使用推荐和已知问题要同时查原库 advisories。

## 回归要求

原生测试覆盖单字、多字、两种主要形状、方形母版和无章场景的正文联合边界中心（误差≤0.5px）、形状内边界；原平台安全区测试继续执行。交付测试覆盖已知问题阻止包/单素材导出、旧文件仍可校验以及旧布局不能新归档。完整结果追加到 docs/VERIFICATION.md。

## 后续反馈

用户已认可 v03 主字居中并授权收录/处理旧错误，随后要求对照原“右”字图标核查印章。主字无需再次确认，当前以 v04 单独比较右下落款，见 [印章复核](2026-11-16-yue-seal-reference.md)；最终印章关系确定后统一执行收录和旧版处理。
