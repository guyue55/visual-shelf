# AGENTS.md — 静澜 Stillwave 网站图标交付包（v01，已废弃）

> ⚠️ **本包已废弃，禁止取用/接入**：其 source 主图 `product-stillwave-jing-logo-circle-minimal-v01-png` 用系统 PingFang SC，未遵守项目固定字体规范；用户 2026-11-17 选择书法体后，已由 `packages/stillwave-web-icon-kit-v02/`（固定 MaShanZheng-Regular）替代。本包仅保留历史追溯，请勿接入站点或导出。改用 → [v02 包](../stillwave-web-icon-kit-v02/AGENTS.md)。

> 本文件是这个包的**自描述入口**：AI 或开发者进入本目录后先读这一份，即可准确理解用途、文件、接入步骤、前置条件与未验证项，无需向用户反复索要提示词。
> 机器可读清单见 `kit.json`；给人看的速览见 `README.md`。最后更新 2026-11-17。

## 1. 这是什么

为「静澜 Stillwave」助眠冥想网站（`https://guyue55.github.io/stillwave/`）制作的「静」字网站图标，以及浏览器/PWA/iOS 可直接使用的场景成品。

- **来源**：素材库正式收录的主图 `product-stillwave-jing-logo-circle-minimal-v01-png`（方案已由用户明确确认满意并收录）。
- **风格**：贴合站点深色青灰极简设计——系统 PingFang SC 真实字形轮廓（CoreText 提取，非图像模型画字）+ 青灰同心涟漪环（呼应站名「澜」与站点 breath-ring 呼吸环）；配色严格取自站点 `tokens.css`。**刻意不带古月章**（产品标识，非个人古风作品）。
- **与主图的关系**：本包是主图的场景适配成品，不是新的设计提案，不改主图、不新增 catalog 素材计数。
- **状态**：`approved-source-kit`（成品已备好）但 `NOT_INTEGRATED`（尚未接入站点）。**接入站点是产品侧改版决策，必须先获得用户/项目侧明确授权**，不要看到包就自行改动站点仓库。

## 2. 文件地图

默认主推 = 字版（带「静」字）。极小尺寸可选 = 涟漪符号版（见 `optional/`）。

| 文件 | 用途 | 关键事实 |
| --- | --- | --- |
| `favicon.ico` | 浏览器标签默认图标 | 多帧 16/32/48 PNG 封装 |
| `favicon-16/32/48.png` | 分尺寸浏览器图标 | 圆形、透明外部；16px 字会糊 |
| `apple-touch-icon.png` | iOS 主屏 | 180×180 满幅不透明，iOS 自动加圆角 |
| `icon-192.png` / `icon-512.png` | PWA `any` | 满幅不透明 |
| `maskable-192.png` / `maskable-512.png` | PWA `maskable` | 关键内容缩进中心安全区，满幅不透明 |
| `stillwave-jing-circle.svg` | 矢量原图 | 1024×1024，纯静态、无脚本/外部引用 |
| `head-snippet.html` | 接入片段 | 复制 `<link>` 声明到站点 `<head>` |
| `kit.json` | 机器清单 | 全部文件 SHA-256、来源、接入判断、未验证项 |
| `optional/*-ripple.png`、`optional/ripple-symbol.svg` | 极小尺寸可选方案 | 见 §4；`PROPOSED_NOT_ADOPTED`，默认不启用 |

每个成品文件的 SHA-256 在 `kit.json` 的 `files` / `optional.files`。改动任何字节前先想清楚：哈希校验会失败，且"已确认"状态失效。

## 3. 接入站点（须先获授权）

站点本地仓库：`/Users/guyue/WorkBuddy/2026-11-09-23-43-37/stillwave`（本库不要擅自改动它）。

**前置判断（来自对站点 QA 源码的逐行复核，不是猜测）**：

1. 站点 `index.html` 第 9 行现在是 `<link rel="icon" href="data:,">`，是为了消除 favicon 404、保住 A6「零 404」验收而**刻意留空**的工程决策，有 BR-29 用例背书。
2. ST-01 只校验 `EXPECTED_FILES` 齐全 + 无构建产物，**不检查多余文件**；把图标放在站点根目录不会触发违规。
3. ST-30 的 `published` 集合只有 `index.html` + `js/ styles/ data/ tools/ .github/`，**不含根目录文件**；所以根目录新增图标**不需要**改 `len(EXPECTED_FILES)==15`（上一版文档说"必须先改清单"是过度保守，已更正）。
4. ST-02 要求 `index.html` 本地资源用 `./` 相对路径——图标引用必须写 `./favicon.ico` 这类形式，不能写 `/favicon.ico`。
5. BR-29 在关闭 favicon 中性化的原始服务上断言零 404/零 console error/零 pageerror，并把 URL 含 `favicon` 的请求计入 `favicon_reqs`。**真实 favicon 是否触发该断言必须实跑 browser QA 才知道**，本环境无 playwright，不能预判通过。

**授权后的步骤**：

1. 复制所需成品到站点根目录（默认字版；极小尺寸若要换涟漪版见 §4）。
2. 用 `head-snippet.html` 的 `<link>` 声明替换 `index.html` 第 9 行，保持 `./` 相对路径。
3. `apple-touch-icon` 单独引用；PWA 需另建 `webmanifest` 并按尺寸用途引用（站点当前**无** manifest）。
4. 跑 `PYTHONPATH= python3 qa/run_all.py`（先安装 playwright），确认零 404 / 零 error / 契约全绿。
5. 若 BR-29 因真实图标请求而变红：这是产品侧 QA 口径决策（图标已存在时"零 favicon 请求"未必仍是正确目标，可评估改为"零 404"），不要由本库擅自改用例；与用户确认后再定。
6. 接入成功后，更新本库实体卡 `docs/entities/products/stillwave.md` 的「已证实使用记录」，并把 `kit.json` 的 `site_integration.status` 改为 `INTEGRATED` 并记录日期。

## 4. 极小尺寸建议（基于实测，须选择后才生效）

**实测发现**（16/32px PNG 实际看图）：字版在 16px 下「静」字糊成墨点、不可辨；32px 起可辨。这是笔画繁多汉字做 favicon 的固有问题，不是渲染缺陷。

**建议**：浏览器标签常见 16px，若项目侧把"小尺寸辨识度"排在"保留汉字"之前，可在本包 `optional/` 用青灰同心涟漪符号版替换 favicon 的 16/32（48 可保留字版）。涟漪符号在 16/32px 均清晰，且更贴合站点 breath-ring 意象。

**默认不选它**，因为用户已明确确认的正式方案是字版；换成涟漪版属于视觉选择，需用户/项目侧明确点头。选用后把 `kit.json` 的 `optional.status` 更新为 `ADOPTED`，并在站点接入时引用可选文件。

## 5. 来源、确认与边界

- 字形：系统 PingFang SC（苹方），CoreText 取真实轮廓；作者/许可未核实，按 unknown 处理，不推断开放许可。
- 配色：站点 `tokens.css` 的 `#0e1418` / `#7fa8a0` / `#e6edea`。
- 用户确认：2026-11-17 对极简「静」字圆形候选明确回复「满意」，允许正式收录；主图 SHA `874c9c46…dfebf27c`。
- 不要做的事：不要声称图标已上线；不要用图像生成模型重画字或章；不要改 `kit.json` 里的哈希来掩盖字节变化；不要在未获授权时改站点仓库或 QA 用例。

## 6. 未验证项（如实保留）

- 真实 iOS / Android 设备上的图标渲染效果。
- 站点 browser QA 全套（本环境无 playwright）；接入后必须由项目侧自行跑。
- SVG 在浏览器 favicon 场景的实际渲染；极小尺寸建议基于 PNG 实看。
- PWA 完整安装配置（本包只提供图标，站点当前无 manifest）。
