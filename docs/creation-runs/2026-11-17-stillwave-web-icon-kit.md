# 2026-11-17 静澜 Stillwave 网站图标场景包导出记录

- 任务：把已收录的极简青灰「静」字主图（circle-minimal）导出为网站各场景可直接使用的图标。
- 来源主图：`product-stillwave-jing-logo-circle-minimal-v01-png`，SHA `874c9c462371d3adf94c22e48db1b19926549f432c81ee8f05c62816dfebf27c`。
- 场景包：`packages/stillwave-web-icon-kit-v01/`，`kit.json` 记录 10 个交付文件的 SHA-256。
- 关联：[极简版制作记录](2026-11-17-stillwave-minimal-logo.md)、[品牌档案](../brands/products/stillwave.md)。

## 为何不用现成 export-kit.py

`scripts/export-kit.py` 依赖月夜底图＋MaShanZheng 字体＋古月章，完全不适用于极简青灰版（无底图、PingFang 字、无章）。故用极简版专用渲染器 `render.swift` 导出。

## 渲染器增强与向后兼容（关键）

- 给 `render.swift` 增加 `--shape square`（满幅不透明方形，供 apple-touch / PWA）与 `--safe on`（关键内容 ×0.72 缩放到中心 40% 安全圆，供 maskable），并新增完整矢量 `full.svg`。
- **向后兼容硬验证**：增强后重渲 circle 主图，SHA 与入库版 `874c9c46…` 完全一致；glyph.svg 字节一致。默认参数行为未变。

## 交付尺寸与验证

| 文件 | 规格 | 验证 |
| --- | --- | --- |
| favicon.ico | 16/32/48 多帧 PNG 封装 | 帧尺寸 16/32/48，PNG 签名有效 |
| favicon-16/32/48.png | 圆形、透明外部（alpha 四角=0） | sips 尺寸确认，CoreGraphics 逐像素核对 |
| apple-touch-icon.png | 180×180 满幅不透明（四角 alpha=255） | 实看：字清晰、涟漪完整 |
| icon-192/512.png | 192/512 满幅不透明（PWA any） | sips 尺寸 + alpha 核对 |
| maskable-192/512.png | 192/512 满幅不透明，内容缩到中心安全区 | 实看 512：字清晰、在安全区、无裁切 |
| stillwave-jing-circle.svg | 1024 完整矢量（形状+背景+涟漪+字形） | 文本导出，未在浏览器 favicon 实测 |

## 接入现状与边界

- **未接入站点**。站点 favicon `<link rel="icon" href="data:,">` 是刻意留空，为 A6「控制台零 404」验收的工程决策（有 BR-29 实测背书），且其 QA 静态契约 ST-30 限定发布文件数为 15。
- 仅对图标「满意」不等于授权改站点仓库。接入需用户明确授权，并：复制交付文件→替换 index.html 的 icon 链接→更新 EXPECTED_FILES 与 QA 基线→重跑站点全套 QA 确认零 404/零 error→更新实体卡使用记录。
- `head-snippet.html` 提供候选接入片段（含上述前置条件注释），按实际部署根调整路径。
- 未验证：真实 iOS/Android 设备渲染、浏览器 SVG favicon 实测、完整 PWA 安装配置。
- 本场景包不计入 catalog 单素材计数（当前 20 份不含本包）。

## 2026-11-17 后续更新（同日二次复核）

- **更正上文一处过度保守判断**：逐行复核站点 `qa/test_static_contracts.py` 后确认——ST-01 只校验清单齐全、不查多余文件；ST-30 的 `published` 集合仅含 index.html + js/styles/data/tools/.github，**不含站点根目录**。因此根目录新增图标通常**无需**改 `EXPECTED_FILES` 或 `len==15`（上文"需更新 EXPECTED_FILES"作废，以包内 `AGENTS.md §3` 为准）。约束是 ST-02 的 `./` 相对路径，以及 BR-29 对真实图标请求的实测结果。
- **BR-29 未预判**：该用例断言零 favicon 请求，本环境无 playwright，无法实跑确认真实图标是否触发；接入后由项目侧自行验证，若变红属产品侧 QA 口径决策，不擅自改用例。
- **补 AI 自描述入口**：包内新增 `AGENTS.md`（用途/文件地图/接入步骤/QA 前置/未验证项）与 `README.md`，更新 `kit.json`（`agent_entry`、`readme`、`code_reviewed_facts`），并把 `head-snippet.html` 注释同步为更正后的判断。目标：AI 接手本包无需用户复制提示词。
- **补极小尺寸实测候选**：实看 16px 字版「静」糊成墨点、32px 可辨；给 `render.swift` 加 `--no-text` 开关（默认字节不变，主图 SHA 仍 874c9c46…），生成 `optional/` 涟漪符号版 16/32/48 + SVG（实测清晰）。状态 `PROPOSED_NOT_ADOPTED`，未替换默认字版，用不用需明确选择。
- 复核：kit.json 主 10 项 + optional 4 项哈希全通过，ICO 3 帧、SVG 无活动/外部内容、git diff 干净；站点仓库仍 git 干净未改动。

## 2026-11-17 再更新（同日字体合规修正，本包 v01 已废弃）

- **本包 v01 已废弃、禁止取用**：其 source 主图 `product-stillwave-jing-logo-circle-minimal-v01-png` 用系统 PingFang SC，未遵守项目固定真实字体规范。用户指出后二次核实确认违规，用固定 MaShanZheng-Regular 书法体重做主图 v02，用户明确要求"用书法体的"。
- **新版场景包**：`packages/stillwave-web-icon-kit-v02/`，所有尺寸用固定书法体重导，含 AI 自描述 AGENTS.md/README.md/kit.json/head-snippet.html；本 v01 包的 AGENTS.md 与 kit.json 已标注废弃（`state: superseded-do-not-use`），`packages/advisories.json` 同步登记替代关系。
- 上述关于 ST-01/ST-30/BR-29、AI 自描述入口的复核结论**仍适用于 v02 包**（其 AGENTS.md 已继承并更新字体事实）。16px 书法体同样糊成墨点；用户 2026-11-17 同日授权小尺寸例外后，v02 的 16px favicon 已改用涟漪符号版（正文仍为固定书法体），详见 [书法体 v02 记录](2026-11-17-stillwave-calligraphy-logo.md) 末尾「小尺寸可读性例外」。本文件保留为 v01 历史记录，不作为当前取用入口。
