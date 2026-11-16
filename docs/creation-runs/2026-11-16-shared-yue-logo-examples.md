# “阅” · 圆形与月夜圆角示例

> 后续状态更新：用户已在 2026-11-16 明确确认并准许收录。底图 A/C、阅字 Logo A/B 及原 185 文件套件已正式保存；详见 [确认收录记录](2026-11-16-approved-guyue-assets.md)。以下“未确认”等表述仅记录最初制作阶段，浅色 B 瑕疵底图仍待修。


日期：2026-11-16。用户要求：古风，个人专属“古月”印章，固定字体，按字数与形状适配，制作两份正文为“阅”的 Logo 示例。用户仅授权制作展示，尚未确认满意或准许正式收录。

## 实际制作

- A：`.drafts/yue-circle-v02/candidate.png`，圆形浅色水墨；1024×1024 RGBA。
- B：`.drafts/yue-rounded-v02/candidate.png`，圆角方形月夜深蓝；1024×1024 RGBA。
- 背景：前一轮 template-ink-light-a / template-moonlit-blue 的无字 PNG 候选，沿用已生成参考，不重新让模型写字。本轮未使用有外缘缺陷的浅色 B。
- 字体：MaShanZheng-Regular，取自固定 Google Fonts 提交 `406197b91ff39a93061c2c2eeaee67ddf2ae1f0d`，字体 SHA-256 `6d2546bb189c732a8ca29af9e22457b152387d158aa459e4ac2ce1e51788b7fb`。
- 渲染：本地 macOS CoreText/CoreGraphics，由真实字体生成“阅/古/月”轮廓，背景、主文案与竖排朱文边框分开组合。不是生成模型临摹字，也不冒称原图字体或纯矢量整图。
- 每份 render 目录输出 logo.png、foreground.svg、32/64/128/256 缩略图及 render.json。SVG 只含正文和印章的真实轮廓，背景仍为位图。
- 渲染入口拒绝覆盖输出目录；早先 render v01 为中间产物，v02 为本次待确认候选，按 task.json 的候选哈希验收。

## 记录与检查

| 项 | A：圆形浅色 | B：圆角深蓝 |
| --- | --- | --- |
| profile | circle-logo | rounded-logo |
| 正文 / 印章 | 阅 / 古月 | 阅 / 古月 |
| PNG SHA-256 | cfb2b0aabe4881ae0ac7589df7a2d3f56d4c0499ee81982f7a2f5c5b55740abe | fd59b0b65e6f03d9cca0ca9244948197cc743ef5bb8da26efb0d2db5439fb7d5 |
| 字形与章边界 | 自动检查在形状内 | 自动检查在形状内 |
| alpha | 两个对角透明、中心不透明 | 两个对角透明、中心不透明 |
| 目视 | 正文与章准确，人物保持在核心画面；圆形裁切背景边缘 | 正文与章准确，月亮和人物保留 |
| 收录 | awaiting-user，未 accept | awaiting-user，未 accept |

128px 已实际查看；主字可辨，章与复杂山水细节缩小后变弱。32px 文件已生成，但完整章文不应承诺可读：如需要 favicon/极小尺寸交付，应另做简化布局并取得取舍确认，不默认删章或让 AI 换字。

## 传统 macOS 试打包

B 额外通过 export-macos.sh 输出 `.drafts/yue-rounded-v02/macos-legacy/`：1024 PNG、完整 10 槽 AppIcon.iconset 和 AppIcon.icns；ICNS SHA-256 `43db53c04e2b6ba89ec382a47bc232842c867a4e012cc1761a25978089a6040a`。这是传统位图路线的实际文件验证，不是现代 Icon Composer 分层文件，未安装到 Dock/Launchpad，也未修改 MacRightClick 原项目。

## 验收与后续

两份均由 studio review 登记并绑定准确哈希，待向用户展示和确认。保持正式 catalog 11 份不变。若后续需要改字、章、形状或再次导出，重新生成新目录并 review，不沿用旧确认；收录时补充真正归属、用途、关键词及未知权利信息。
