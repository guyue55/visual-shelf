# 2026-11-17 静澜 Stillwave 极简青灰「静」字标识制作记录

> ⚠️ 本记录为 v01 历史。该版主字用系统 PingFang SC，后经核实未遵守固定字体规范，已废弃、不再主推；当前主推为固定书法体 v02，见 [书法体 v02 记录](2026-11-17-stillwave-calligraphy-logo.md)。本文件保留当时的制作与调研轨迹，不作当前取用入口。

- 任务：为 https://guyue55.github.io/stillwave/ 做一版真正贴合站点极简设计语言的「静」字图标（区别于古风月夜版）。
- 触发：用户「由你充分调研和思考后，站在全局和更高的层次决定要做什么，我只要结果」→「按你建议执行」→ 对展示候选「满意」。
- 实体：product:stillwave；家族 stillwave-jing-logo；variant `circle-minimal`；系列 stillwave-jing-logo；组件 app-identity（复用现有登记，不新增系列）。
- 产出：`product-stillwave-jing-logo-circle-minimal-v01-png`（主推）。

## 调研与决定依据（先查证，非臆断）

- 线上站点实读 HTML + styles/tokens.css，并浏览器截图核对：深色低刺激青灰界面，全站无图片、无 manifest、无 apple-touch-icon；`<link rel="icon" href="data:,">` 是刻意留空。
- 站点本地仓库 `/Users/guyue/WorkBuddy/2026-11-09-23-43-37/stillwave`（git 干净），文档确认空 favicon 是为 A6「控制台零 404」验收的工程决策（03-implementation.md、04-qa-report.md，BR-29 实测背书），QA 静态契约 ST-30 限定发布文件数为 15。
- 结论：做一版贴合站点的极简标识作为独立可复用素材；不擅自改站点仓库、不接入（接入属产品侧改版，需用户明确授权并重跑 QA）。

## 制作输入与工具

- 配色严格取自站点 tokens.css：底 `#0e1418`、柔光 `#1c272e`、青灰主色 `#7fa8a0`、字 `#e6edea`。
- 主字「静」：系统 PingFang SC（PingFangSC-Regular，站点 sans-serif 首选），CoreText 提取**真实字形轮廓**，glyphsOK=true；非模型画字、非马善政体。
- 涟漪：Quartz 绘制三层青灰同心环，呼应站名「澜」与站点 breath-ring 呼吸环；中心柔光点。
- 刻意**不带古月章**——产品标识非个人古风作品。
- 渲染器：`.drafts/stillwave-minimal-v01/render.swift`（Swift 6.3.3，CoreText＋CoreGraphics），非 `render-logo.sh`，非图像生成模型。

## 候选与验证

- 圆形为主推、圆角为备选，均实看 1024 大图与 48px 小图：圆形涟漪完整落在圆内、无贴边、更集中，贴合 breath-ring 意象，定为主推；48px「静」字仍清晰、涟漪不成噪点。
- 几何：真实字形轮廓中心 (512.00, 527.36) 与目标涟漪中心零误差；x 精确居中，y 为 breath-ring 视觉重心刻意略下移。曾发现用 SVG 贝塞尔控制点反推中心会误判偏移，已改用 `boundingBoxOfPath` 真实轮廓核对（正确方法）。
- 多尺寸：16/32/48/128/180/256/1024 PNG 齐全，尺寸与 PNG 签名核对通过。
- 审核：候选 `candidate.png` SHA `874c9c462371d3adf94c22e48db1b19926549f432c81ee8f05c62816dfebf27c`，review 登记后用户确认满意，accept 收录，approval 绑定该 SHA 与用户原意。
- 未验证：真实设备渲染、浏览器深浅底叠加、站点接入（未接入，见上）。

## 收录与同步

- `studio.py review` → `studio.py accept` 走完整审计链收录（保留 checks/tool/approval）。
- 同步：实体卡、品牌档案（v02）、README 统计（19→20 份，系列仍 8）、SEAL-VARIANTS 统计。
- 场景包：见 `2026-11-17-stillwave-web-icon-kit.md`（favicon / PWA / Apple Touch 多尺寸，供将来接入取用）。
