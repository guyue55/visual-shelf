# 制作记录：静澜 Stillwave「静」字极简青灰书法体 v02（字体合规修正）

- 日期：2026-11-17
- 实体：product:stillwave；家族 stillwave-jing-logo；新变体 circle-calligraphy，revision v02。
- 主图 asset id：`product-stillwave-jing-logo-circle-calligraphy-v02-png`；SHA-256 `7b69ae5cc3a47c0853f2b285ad1c814cd4993a0fd532e3cb4c178377937b1456`。
- 草稿与源码：`.drafts/stillwave-mashanzheng-v02/`（render.swift、task.json、候选）。

## 起因：一次字体规范违背及其修正

- 用户质疑："图标文案应该有字体要求吧？为什么没遵守？还是觉得用你这种字体更好看？"
- 二次核实一手规范：`docs/PERSONAL-STYLE.md` 第 10/17/22 行、`AGENTS.md` 明确要求主文案用固定真实字体（默认 MaShanZheng-Regular，固定 TTF + SHA `6d2546bb…`），**禁止静默切换字体、禁止系统 fallback、禁止随机生成笔画**，换字体须改为"另一份固定字体并重新验收"。
- 确认事实：古风月夜版遵守（`render-logo.sh` 用固定 TTF + SHA 校验）；**极简青灰 v01 违规**——`render.swift` 第 118–120 行用 `CTFontCreateWithName("PingFang SC")`（系统字体，无固定文件/SHA/跨机复现）。
- 归因：我当时把"站点 tokens.css 无外部字体、sans-serif，苹方更贴合极简视觉"当成自洽理由自行决定，未作为取舍提出、未走字体验收——属疏漏，非审美偏好。已向用户如实承认。

## 修正做法

- 新渲染器 `.drafts/stillwave-mashanzheng-v02/render.swift`：把字体加载改为 `CGFont(CGDataProvider)` 从固定 TTF 读取，硬校验 PostScript 名 = `MaShanZheng-Regular`，缺字直接报错；错误字体（实测 ArialMT）被拒且不产文件。配色/涟漪/形状/safe/no-text/印章逻辑与 v01 逐字一致，仅换字体，便于 A/B 对照。
- 书法体字宽高与无衬线不同：按目标高度 0.40×S 等比缩放后几何居中，真实轮廓中心 (512.00, 527.36) 与目标零误差。
- 三联对照图二次核验字形：新候选为书法体（笔锋/粗细变化/连带牵丝），旧 v01 为规整黑体（系统苹方）；用户实看后明确要求"用书法体的"。
- 48px 放大实看：书法体字在 16px 糊成墨点（复杂汉字固有问题，换字体解决不了），涟漪符号版清晰 → 当时场景包继续提供 `optional/` 涟漪版建议（`PROPOSED_NOT_ADOPTED`，不默认替换）。**同日稍后用户授权小尺寸例外，16px 已转正采用涟漪符号，以文末更新为准。**

## 审计链与版本处理

- 走 `studio.py review → accept` 正规链：草稿 task.json 补齐 `state/reference_sha256/checks/tool/style/reference/purpose` 等字段后才通过 review（手写草稿字段不全是已知坑，本次复现并修正）。
- approval 绑定候选 SHA `7b69ae5c…`，记录用户"用书法体的"原话与核对事实。
- **v01 不物理删除**（用户未授权清理）：在 `packages/advisories.json` 登记 `block_export:true`、`state:superseded-not-removed`、`replacement=v02`；v01 元数据 tags 改 `status:superseded` 并在 description 标注废弃；文件保留仅作追溯。这和项目"先收录替代、保存 retired 元数据与替代关系"的规范一致。

## 连带更新

- 场景包：新建 `packages/stillwave-web-icon-kit-v02/`（全部尺寸用固定书法体重导，含 AI 自描述 AGENTS.md/README.md/kit.json/head-snippet.html）；旧包 v01 标废弃禁止取用。见 [场景包记录](2026-11-17-stillwave-web-icon-kit.md)。
- 文档：项目根 AGENTS.md 重构（加硬约束速查卡，固化"固定字体"红线）、实体卡、品牌档案 v03、README/SEAL-VARIANTS 统计 20→21 份。
- 验证：validate/build、kit 哈希、ICO/SVG 结构、主图回归、git diff --check 见本轮最终核对。

## 2026-11-17 后续更新（同日 23:20，用户授权小尺寸可读性例外）

- 用户明确："如果一些特殊情况，比如 16px 下书法体更容易糊，那可以用更清晰的方案或字体，不必僵硬遵守要求而制造垃圾。"
- **二次核实（不是凭印象）**：把 16px 书法体、旧 v01 苹方字、涟漪符号三张 PNG 各自放大到 512 实看——前两者都糊成不可辨墨点，涟漪符号清晰；32px 书法体可辨、48px 清晰。结论：此尺寸问题来自复杂汉字的信息量，换字体无法解决，应换更简符号。
- **决定**：仅把 v02 场景包的 `favicon-16.png` 和 `favicon.ico` 的 16px 帧换成涟漪符号（原 `optional/favicon-16-ripple.png` 转正并移除重复文件）；32/48px、Apple Touch、PWA、SVG 仍为固定书法体，主图字节与确认状态不变。这不是全局换字体，也不是系统字体回退。
- **验证**：ICO 从三张独立 PNG 干净重建，3 帧尺寸 16/32/48、PNG 签名有效、逐帧字节与主文件一致；包内主 10 项 + optional 3 项哈希重算一致。
- **规范固化**：项目根 `AGENTS.md` §2 增「小尺寸可读性例外」一行；`docs/PERSONAL-STYLE.md` 新增同名小节（判定/边界/记录/当前实例）；`docs/VISUAL-QA.md` §实际尺寸补例外条件。包内 `AGENTS.md`/`README.md`/`kit.json`/`head-snippet.html` 与实体卡、品牌档案同步。

## 经验（已固化到 AGENTS.md）

即使为了贴合品牌视觉，也不能静默换系统字体绕过固定字体规范；产品标识可不带古月章，但"主文案固定真实字体"同样适用。换字体必须：作为取舍先提出 → 用另一份固定字体 → 重新验收 → 更新规范记录。

红线不是教条：明确尺寸下实测不可辨时，允许在**该尺寸**改用更清晰方案，但必须实图对照、限定范围、显式记录并重算哈希；禁止借例外静默换系统字体或扩散到主图。
