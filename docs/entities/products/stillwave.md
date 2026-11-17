# 静澜 Stillwave · 产品登记卡

- 类型：product；稳定 slug：stillwave。
- 名称：静澜 Stillwave。
- 定位：浏览器端冥想 / 专注 / 助眠声景网站，本地合成声景、场景切换、呼吸节奏、声景叠加与睡眠定时；强调全免费、无需登录、不采集数据、零网络依赖。
- 站点：https://guyue55.github.io/stillwave/ （2026-11-17 访问核对）。
- 归属：用户提供的自有网站；此声明不用于推断逐图创作者。
- 本次依据：站点页面文本与 styles/tokens.css 配色令牌，2026-11-17 核对。
- 状态：已收录「静」字标识（极简青灰圆形为主推 v02 固定书法体、圆角月夜为个人作品方向；另有极简青灰苹方 v01 历史修订已废弃）；已备好网站图标场景包 `packages/stillwave-web-icon-kit-v02/`（含 AI 自描述入口 AGENTS.md）。**未改动网站仓库或接入图标**（产品侧决策，待授权）。
- 负责人：用户；图像作者 unknown。
- 品牌档案：[stillwave](../../brands/products/stillwave.md)。

## 素材家族与推荐项

家族 `stillwave-jing-logo`，主归属 `product:stillwave`，分类 logos。标识用字属于产品识别资产，不归入通用功能 icons。家族下有视觉体系：贴合站点极简语言的「极简青灰」（当前主推 v02 用固定书法体）与个人古风作品方向的「月夜深蓝」，用 variant 区分，不代表站点官方确认任一版为品牌规范。

| 变体 | 当前 asset id | 用途与状态 |
| --- | --- | --- |
| 圆形极简青灰 v02 | product-stillwave-jing-logo-circle-calligraphy-v02-png | **主推**：贴合站点青灰极简语言，**固定 MaShanZheng 书法体**真实字形＋青灰涟漪环、无印章；字体合规（用户 2026-11-17 在对照实看后明确要求"用书法体的"） |
| 圆形极简青灰 v01 | product-stillwave-jing-logo-circle-minimal-v01-png | **历史修订·已废弃**：用系统 PingFang SC，未遵守固定字体规范；v02 替代后不再主推、禁止新导出（见 `packages/advisories.json`），文件仅作追溯 |
| 圆角月夜 v01 | product-stillwave-jing-logo-rounded-moonlit-v01-png | 个人古风作品方向（用户 2026-11-17 明确满意收录） |

固定马善政字体＋右下古月章是「月夜」个人作品默认规则；「极简青灰」版刻意不带印章、按站点 tokens.css 取色，同样受"主文案固定真实字体"规范约束——这正是 v01 因用系统苹方被 v02 修复的原因。两版都是设计选择，非站点官方品牌规范。文件路径与 SHA-256 见 catalog。

## 与站点视觉的关系（设计选择，非已确认品牌规范）

- 站点本身为深色低刺激青灰主题（背景 `#0e1418`、主色 `#7fa8a0`），风格克制、以文字与符号为主，无独立图形 Logo。
- **极简青灰版**（主推 v02）：配色严格取自站点 tokens.css，**固定 MaShanZheng 书法体**真实字形＋青灰涟漪同心环（呼应站名「澜」与 breath-ring），刻意无印章，视觉上贴合站点。v01 曾用系统苹方被判定不合规，已由 v02 修复。即便如此，它仍是本库独立素材，**站点并未接入**。
- **圆角月夜版**：采用项目已确认的「月夜深蓝」古风方向（深蓝山水＋月亮＋人物＋米白书法字＋古月章），气质呼应静夜助眠，但不属于站点现有配色令牌，是个人作品方向。
- 两版均未据像素取色宣称官方品牌色；是否接入站点由用户另行决定。形状/尺寸为探索起点，非任何平台官方最终规格；接入 favicon / PWA / Apple Touch 需按各自安全区另行导出与验收（见场景包记录）。

## 场景包与使用记录

- 场景包：`packages/stillwave-web-icon-kit-v02/`（favicon ICO/PNG、Apple Touch 180、PWA any/maskable 192/512、完整 SVG；`kit.json` 登记哈希，包内 `AGENTS.md` 为 AI/开发者自描述入口）。源自主推 v02 固定书法体版。旧包 `stillwave-web-icon-kit-v01`（苹方）已标废弃、禁止取用。
- 小尺寸适配（2026-11-17 用户授权，已生效）：16px 下书法体「静」与旧苹方「静」实看均糊成不可辨墨点，故 v02 包的 `favicon-16.png` 与 ICO 的 16px 帧改用清晰的青灰涟漪符号；32/48px、Apple Touch、PWA、SVG 仍为固定书法体。这是**仅限 16px** 的可读性例外，不是换字体或系统回退，依据与边界见场景包 `AGENTS.md §4`。`optional/` 仅余 32/48 涟漪候选（`PROPOSED_NOT_ADOPTED`）。
- **已证实使用记录：无**。场景包已备好但站点未接入，不计作已使用。站点本地仓库 `/Users/guyue/WorkBuddy/2026-11-09-23-43-37/stillwave` 本轮未改动（git 干净）。

## 缺口与更新规则

- 图像生成工具、作者、逐图许可、精确品牌色与可编辑矢量均为 unknown，不从风格推断。
- 图形、文案或裁切变化则新建 id / revision；文件字节变动需重新展示并取得确认，不沿用本次 approval。
- 实际接入后再补使用记录（消费方、路径或 URL、用途、确认日期）；计划使用不计作已使用。接入步骤、QA 前置与 BR-29 口径判断见场景包 `AGENTS.md §3`；接入后把该包 `kit.json` 的 `site_integration.status` 改为 `INTEGRATED`。
- 不另建同名 project 卡：目前没有独立交付项目需求。
