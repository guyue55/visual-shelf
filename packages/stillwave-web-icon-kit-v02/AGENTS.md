# AGENTS.md — 静澜 Stillwave 网站图标交付包（v02 书法体）

> 本文件是这个包的**自描述入口**：AI 或开发者进入本目录后先读这一份，即可准确理解用途、文件、接入步骤、前置条件与未验证项，无需向用户反复索要提示词。
> 机器可读清单见 `kit.json`；给人看的速览见 `README.md`。最后更新 2026-11-17。

## 1. 这是什么

为「静澜 Stillwave」助眠冥想网站（`https://guyue55.github.io/stillwave/`）制作的「静」字网站图标，以及浏览器/PWA/iOS 可直接使用的场景成品。

- **来源**：素材库正式收录的主图 `product-stillwave-jing-logo-circle-calligraphy-v02-png`（用户 2026-11-17 在对照实看后明确选择"用书法体的"，确认并收录）。
- **字体合规（本版核心）**：主字为项目**固定字体 MaShanZheng-Regular（马善政书法体）**真实轮廓，从固定 TTF 加载（SHA `6d2546bb…`，与 `resources/fonts/mashanzheng/provenance.json` 一致），PS 名硬校验、缺字报错；**非系统字体、非图像模型画字**。这修复了旧 v01 用系统苹方、未遵守 `docs/PERSONAL-STYLE.md` 固定字体规范的问题。
- **风格**：贴合站点深色青灰极简设计——书法体字 + 青灰同心涟漪环（呼应站名「澜」与站点 breath-ring）；配色严格取自站点 `tokens.css`。**刻意不带古月章**（产品标识，非个人古风作品；章规则不适用）。
- **小尺寸例外（已生效）**：`favicon-16.png` 与 `favicon.ico` 的 16px 帧改用**青灰涟漪符号**——实测书法体「静」与旧苹方「静」在 16px 均糊成不可辨墨点；32/48px 及以上仍为固定书法体。依据与边界见 §4。
- **版本关系**：本 v02 替代 `stillwave-web-icon-kit-v01`（其 source 为系统苹方 v01，字体不合规，已禁止接入）。旧的 v01 素材/包保留作历史追溯，勿再取用。
- **状态**：`approved-source-kit`（成品已备好）但 `NOT_INTEGRATED`（尚未接入站点）。**接入站点是产品侧改版决策，必须先获得用户/项目侧明确授权**，不要看到包就自行改动站点仓库。

## 2. 文件地图

默认主推 = 书法体字版；16px favicon 为已生效的清晰符号例外；`optional/` 仅余更大尺寸的候选方案。

| 文件 | 用途 | 关键事实 |
| --- | --- | --- |
| `favicon.ico` | 浏览器标签默认图标 | 多帧 16/32/48 PNG 封装；16 帧为涟漪符号，32/48 帧为书法体 |
| `favicon-16/32/48.png` | 分尺寸浏览器图标 | 圆形、透明外部；`favicon-16.png` = 涟漪符号（例外），32/48 = 书法体 |
| `apple-touch-icon.png` | iOS 主屏 | 180×180 满幅不透明，iOS 自动加圆角 |
| `icon-192.png` / `icon-512.png` | PWA `any` | 满幅不透明 |
| `maskable-192.png` / `maskable-512.png` | PWA `maskable` | 关键内容缩进中心安全区，满幅不透明 |
| `stillwave-jing-circle.svg` | 矢量原图 | 1024×1024，纯静态、无脚本/外部引用，字形为固定字体轮廓 |
| `head-snippet.html` | 接入片段 | 复制 `<link>` 声明到站点 `<head>` |
| `kit.json` | 机器清单 | 全部文件 SHA-256、字体来源、接入判断、未验证项 |
| `optional/*-ripple.png`、`optional/ripple-symbol.svg` | 更大尺寸的替代候选 | 仅 32/48 与矢量；`PROPOSED_NOT_ADOPTED`，默认不启用（原 16 版已转正为主文件） |

每个成品文件的 SHA-256 在 `kit.json` 的 `files` / `optional.files`。改动任何字节前先想清楚：哈希校验会失败，且"已确认"状态失效。

## 3. 接入站点（须先获授权）

站点本地仓库：`/Users/guyue/WorkBuddy/2026-11-09-23-43-37/stillwave`（本库不要擅自改动它）。

**前置判断（来自对站点 QA 源码的逐行复核，不是猜测）**：

1. 站点 `index.html` 第 9 行现在是 `<link rel="icon" href="data:,">`，是为了消除 favicon 404、保住 A6「零 404」验收而**刻意留空**的工程决策，有 BR-29 用例背书。
2. ST-01 只校验 `EXPECTED_FILES` 齐全 + 无构建产物，**不检查多余文件**；把图标放在站点根目录不会触发违规。
3. ST-30 的 `published` 集合只有 `index.html` + `js/ styles/ data/ tools/ .github/`，**不含根目录文件**；所以根目录新增图标**不需要**改 `len(EXPECTED_FILES)==15`。
4. ST-02 要求 `index.html` 本地资源用 `./` 相对路径——图标引用必须写 `./favicon.ico` 这类形式，不能写 `/favicon.ico`。
5. BR-29 在关闭 favicon 中性化的原始服务上断言零 404/零 console error/零 pageerror，并把 URL 含 `favicon` 的请求计入 `favicon_reqs`。**真实 favicon 是否触发该断言必须实跑 browser QA 才知道**，本环境无 playwright，不能预判通过。

**授权后的步骤**：

1. 复制所需成品到站点根目录（16px 已按 §4 的例外用涟漪符号版，其余默认书法体字版）。
2. 用 `head-snippet.html` 的 `<link>` 声明替换 `index.html` 第 9 行，保持 `./` 相对路径。
3. `apple-touch-icon` 单独引用；PWA 需另建 `webmanifest` 并按尺寸用途引用（站点当前**无** manifest）。
4. 跑 `PYTHONPATH= python3 qa/run_all.py`（先安装 playwright），确认零 404 / 零 error / 契约全绿。
5. 若 BR-29 因真实图标请求而变红：这是产品侧 QA 口径决策（图标已存在时"零 favicon 请求"未必仍是正确目标，可评估改为"零 404"），不要由本库擅自改用例；与用户确认后再定。
6. 接入成功后，更新本库实体卡 `docs/entities/products/stillwave.md` 的「已证实使用记录」，并把 `kit.json` 的 `site_integration.status` 改为 `INTEGRATED` 并记录日期。

## 4. 16px 可读性例外（已生效，别回退）

**实图依据（2026-11-17 二次复核）**：16px 书法体「静」放大后糊成不可辨墨点；旧 v01 的系统苹方「静」在 16px 同样糊——说明**换字体解决不了**，问题是复杂汉字在极小尺寸的信息量。32px 书法体可辨、48px 清晰；16px 涟漪符号版清晰且贴合站点 breath-ring。

**决定范围**：用户明确授权"特殊情况可用更清晰方案，不必僵硬遵守而制造垃圾"。因此仅把 `favicon-16.png` 与 `favicon.ico` 的 16px 帧换成涟漪符号（原 `optional/favicon-16-ripple.png` 转正，旧文件不重复保留）；32/48px、Apple Touch、PWA、SVG **仍是固定 MaShanZheng 书法体**。这不是全局换字体，也不是系统字体回退。

**接入时**：直接用主文件即可，不需要再选 optional。`optional/` 仅保留 32/48 涟漪版与矢量候选，状态仍为 `PROPOSED_NOT_ADOPTED`；若项目侧想让 32px 也用符号，需另行明确选择并更新 `kit.json`。

**例外规则出处**：项目根 `AGENTS.md` §2「小尺寸可读性例外」、`docs/PERSONAL-STYLE.md` §小尺寸可读性例外、`docs/VISUAL-QA.md` §实际尺寸。

## 5. 来源、确认与边界

- 字形：**固定 MaShanZheng-Regular（马善政书法体）**，从固定 TTF 加载、SHA 与 provenance 一致，CoreText 取真实轮廓；作者/许可按 unknown 处理，不推断开放许可。
- 配色：站点 `tokens.css` 的 `#0e1418` / `#7fa8a0` / `#e6edea`。
- 用户确认：2026-11-17 在书法体/苹方对照三联图实看后明确要求"用书法体的"，主图 SHA `7b69ae5c…b1456`。
- 不要做的事：不要声称图标已上线；不要回退到系统字体或用图像生成模型重画字；不要把 16px 涟漪版误判为系统字体回退或全局换字体，也不要把它扩散到 32/48/PWA；不要改 `kit.json` 里的哈希来掩盖字节变化；不要在未获授权时改站点仓库或 QA 用例；不要取用已禁止的 v01 旧包/旧素材。

## 6. 未验证项（如实保留）

- 真实 iOS / Android 设备上的图标渲染效果。
- 站点 browser QA 全套（本环境无 playwright）；接入后必须由项目侧自行跑。
- SVG 在浏览器 favicon 场景的实际渲染；极小尺寸建议基于 PNG 实看。
- PWA 完整安装配置（本包只提供图标，站点当前无 manifest）。
