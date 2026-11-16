> 原仓库规范快照：文中仓库相对命令不等于本包目录。包内真实运行入口以 README.md、AGENTS.md 和 package.json 为准；原仓库历史链接已标明。

# 形状、安全区与平台导出规范

调研与更新：2026-11-16。机器可读索引为 templates/visual/profiles.json；个人风格、字体和古月章见 [PERSONAL-STYLE.md](PERSONAL-STYLE.md)。规范覆盖不等于自动导出均已实现，具体见各行能力。

## 环境先于格式

制作前确认：用途 → 平台及工具链 → 外形/掩膜 → 内容安全区 → 颜色/透明度 → 字体与印章 → 输出格式/尺寸 → 实际验收。用户未指定目标时可先做通用 Logo 探索，但不能把预览图当作某平台正式交付。

| profile | 用途和要求 | 当前能力 |
| --- | --- | --- |
| circle-logo | 1024 方形画布，真正圆形 alpha；文字、印章和核心主体在圆内，风景可裁切 | 原生渲染，轮廓边界检查 |
| rounded-logo | 1024 圆角方形通用 Logo；适配画面、留白、文字与印章，不叠加旧蒙版碎片 | 原生渲染；不是 Apple 官方系统 mask |
| square-master | 1024 未预裁切方形，满幅不透明背景；适合现代 Apple 路线的位图起点 | 原生渲染；不是已完成的分层 Icon Composer |
| cover / web | 1600×900 / 1600×600 为项目探索值，重新安排背景/标题与署名，具体平台尺寸另核对 | 原生文字重排与背景等比 cover；复杂构图仍需图像或设计工具调整 |
| pwa-maskable | 满幅、尽量不透明，关键字与章在中心半径 40% 的安全圆内 | 原生母版渲染并检查字形安全区；192/512 等实际清单按接入项目生成，不冒称 W3C 强制尺寸 |
| macos-legacy-icns | 已适配的 1024 PNG → 完整 10 槽 iconset → ICNS | export-macos.sh 可打包；须核对目标应用兼容路线 |
| android-adaptive | 独立 foreground/background，按需 monochrome；108×108 dp 图层、关键标记 66×66 dp 安全区 | 已提供前背景 PNG、五密度和 XML；monochrome 未生成，设备未验收 |
| favicon | 16/32/48 PNG、多帧 ICO 与 SVG，固定短标记 | 已实现；带章默认与简化备选分开，需用户选择，不自动删章 |

圆形只是形状之一。PWA/Android 所谓“圆形显示”常由系统施加 mask，和导出一个圆形透明 PNG 不是一回事。用户希望带章时应把章放在安全区内，不把它留在四角被系统裁掉。

浏览器标签、触屏/PWA、分享图及全套导出见 [场景模板清单](SCENE-TEMPLATES.md)。

## Apple：现代路线与传统路线分开

[Apple HIG 当前文档](https://developer.apple.com/design/human-interface-guidelines/app-icons.md) 说明：现代 iOS/iPadOS/macOS 的布局为 1024×1024 方形，由系统施加圆角；推荐 Icon Composer，提供未预裁切图层，背景满幅不透明、文字转轮廓，并按实际系统外观预览。它也允许非分层位图，但位图不等于手工完成的层分离。

所以本项目的 square-master 不预裁圆角，不能直接拿圆形/圆角预览 PNG 当作现代分层素材。需要 `.icon` 时仍要使用 Icon Composer/Xcode 实际制作与验证，本工具不会伪造该格式。

MacRightClick 当前源码则走传统 `Resources/AppIcon.png → sips 多尺寸 → iconutil → AppIcon.icns`。这是本地已读构建代码支持的兼容路线，不能因现代 HIG 改动就擅自替换其工程配置。

```sh
./scripts/export-macos.sh .drafts/<任务>/render/logo.png .drafts/<任务>/macos-legacy
```

脚本只接受真正的 1024×1024 PNG、拒绝覆盖目录，生成 10 个命名槽及 AppIcon.icns，并记录源/包哈希。16/32 等预览要独立检查。打包成功不证明 Dock/Launchpad、签名/发行包或所有 macOS 版本都已验收；不能把一枚 ICNS 改名成 PNG，反之亦然。

## Web/PWA 与 Android

[Web Application Manifest 安全区](https://www.w3.org/TR/appmanifest/#icon-masks) 定义 maskable 核心安全区为以中心为圆心、半径最短边 40% 的圆，建议避免透明像素。正文和古月署名都算关键元素；背景可延伸到边界。本轮引用的是 2026-11-11 工作草案，不声称它是永久不变的最终标准。

[Android 官方自适应图标文档](https://developer.android.com/develop/ui/compose/system/icon_design_adaptive) 要求独立前景与背景图层、108 dp 画布、中央 66 dp 安全区，并说明系统可采用不同 mask。不要把带圆角/阴影的单张 macOS 图标直接当作 adaptive icon；Play 商店图标与设备 launcher 也要分别按用途核对。

## 字体、格式与验收记录

记录 profile、目标 OS/工具链、画布/尺寸、颜色空间、alpha、固定字体版本/哈希、正文、印章开关、安全区、背景来源与成品哈希。缺少目标环境时标 unspecified，不填猜测的“已适配”。

固定字体轮廓层是 SVG；含位图背景的完整成品是 PNG；复杂背景没有被转换成纯矢量。JPEG 不用于要求透明角的标识；WebP 可按网站接入需求衍生，ICNS/ICO 等打包产物留在交付工作区，当前 catalog 分发格式并未因此自动扩展。

- 自动检查：真实解码尺寸、字体缺字、形状内文字/印章边界、PWA 安全区、alpha 及导出包槽数。
- 人工检查：文字逐字、小尺寸、浅深背景、人物/主体是否裁切、章是否抢主体、目标环境实际显示。
- 用户确认：只针对展示的准确版本；通过自动检查不等于用户满意，不自动 accept。
- 本轮渲染与 ICNS 在 macOS 实测；Android 分层/ICO 已能实际生成但仍需目标环境验收；现代 `.icon` 仍不是本脚本已实现的输出。

## 正文居中检查

通用 Logo/方形母版/Apple Touch 采用 layout_version=2 的正文轮廓联合边界居中；印章独立定位。favicon、maskable/adaptive 与横向构图采用各自标题区，必须记录预期中心和通过结果，并与安全区检查同时执行。几何中心不自动代表书法光学满意，最终仍展示实际尺寸。旧阅字 v02 的偏移及修正规则见 复核记录（原仓库参考：creation-runs/2026-11-16-yue-centering-correction.md）。
