> 原仓库规范快照：文中仓库相对命令不等于本包目录。包内真实运行入口以 README.md、AGENTS.md 和 package.json 为准；原仓库历史链接已标明。

# 常用场景模板与一键导出套件

更新：2026-11-16。用户要求各类场景提前准备，包括浏览器标签。以下是可执行模板与导出约定，不是把一个 PNG 改名发到所有环境。

## 场景清单

| 场景 | 实际模板/产物 | 适配要点 |
| --- | --- | --- |
| 浏览器标签 favicon | 固定字体短标记，SVG、16/32/48 PNG 与含三帧 PNG 的 ICO | 最多两字，素色高对比底；默认带章，另给无章简化备选，只有用户选择后才替换 |
| 网站触屏图标 | apple-touch-icon.png，180×180 | 满幅不透明、真实目标设备验收；不能把标签小图直接放大 |
| PWA 通用安装图标 | any 192/512 PNG | 完整标识用途，与 maskable 分开引用 |
| PWA maskable | maskable 192/512 PNG | 主字和章在中心 40% 半径安全圆内，背景满幅 |
| 网站导航/个人头像 | 1024 圆形或圆角方形、透明外缘、SVG 字形层 | 不同形状重新校验内容安全区 |
| 文章/文档封面 | cover 1600×900 | 项目预设，准确文案、字体与章；背景构图按题材继续调整 |
| web 横幅 | web 1600×600 | 项目预设，横向标题区；背景裁切后不保证人物完整，需实际检查 |
| 社交分享图 | og-image 1200×630、OG 标签片段 | 项目预设而非所有平台强制值；发布时改为真实绝对 URL并验证平台裁切 |
| macOS 传统 App | 1024 PNG、10 槽 iconset、ICNS | 仅传统兼容路线；Dock/实际工程另验证 |
| 现代 Apple 图标母版 | square-master、正文/章前景层、背景层 | 提供未预裁方形起点，不是已完成 `.icon`；仍需 Icon Composer/Xcode |
| Android adaptive | 前背景 PNG、5 档密度资源及 v26 adaptive-icon XML | 108dp 图层、66dp 核心安全区；未生成 monochrome，未在设备安装验证 |

默认古风、古月章及固定字体规则见 [个人规范](PERSONAL-STYLE.md)，平台一手来源和边界见 [平台规范](PLATFORM-PROFILES.md)。新的小尺寸例外不改变带章母版：简化版本只作为明确标识的备选草稿，不自动启用。

## 一键生成（当前 macOS）

```sh
python3 scripts/export-kit.py \
  --background /绝对路径/无字底图.png \
  --text 阅 --name '古月 · 阅' --theme dark \
  --output .drafts/my-new-kit
```

需要 macOS、Swift、Python 3.11+、sips/iconutil；使用仓库固定字体。只输出到 .drafts 下的新目录，不覆盖、不写 assets/catalog/site、不部署。后台图像不由该脚本重新生成：它负责已备背景的排版与场景导出；复杂构图仍须 AI/设计工具调整。

输出包含：

- `preview.html`：全套概览，带章与简化标签的真实 16/32/48 像素对比。
- `favicon.ico/svg`、`favicon-16/32/48.png`，默认仍引用带章款。
- `favicon-simple-option/`：无章小尺寸备选，未替用户作满意确认。
- `apple-touch-icon.png`、`icon-192/512.png`、`maskable-192/512.png`。
- `site.webmanifest`：只提供名称和图标信息，不是完整 PWA 安装方案，没有 Service Worker。
- `head-snippet.html`：相对路径接入示例，OG URL 是明显占位符，接入时换成真实域名。不能原样当成已上线配置。
- `android-res/`：mdpi/hdpi/xhdpi/xxhdpi/xxxhdpi 的 108/162/216/324/432 px 图层与 XML，单色主题图尚需制作。
- `macos-legacy/`：实际 ICNS 和 iconset，不自动安装到原项目。
- 每个场景的 PNG、真实字体轮廓 foreground.svg、前景/背景 PNG 层、render.json 及 `kit.json` 文件清单和哈希。

PNG 内嵌 ICO 面向现代浏览器/系统，不承诺古老的仅 BMP ICO 消费程序兼容。SVG favicon 独立包含底色，避免浅色字形在浅色标签栏上消失。

## 单场景任务与收录

studio prepare 的 purpose 现支持 `favicon`、`apple-touch`、`pwa`、`android-icon`、`share-card`，以及已有 logo/app-icon/cover/web。读取模板索引选择对应 profile；平台没明确时先做草稿，不冒充已集成。

```sh
python3 scripts/studio.py prepare --job reader-tab-v01 \
  --style moonlit-blue --purpose favicon --text 阅 --platform browser
```

一整套生成只是候选集合，不代表全部满意。逐用途检查，按准确文件 review，再由用户明确批准后才 accept；素材包不会自动批量入库。ICO、ICNS、XML 与清单留在交付工作区，现有 catalog 仍仅接收支持的单个分发格式。

AI 接入真实项目时还需确认 base path、manifest 的部署位置、名称/品牌归属、缓存更新策略和实际平台显示。当前本库站点未把这些未批准示例替换为自己的 favicon。

## 调研依据（2026-11-16）

- [MDN：link 的图标 sizes](https://developer.mozilla.org/en-US/docs/Web/API/HTMLLinkElement/sizes)：图标资源与尺寸声明。
- [web.dev：manifest 图标](https://web.dev/articles/add-manifest)：Chromium 的 192/512 图标与 maskable 指定；不把图标文件本身称为完整 PWA。
- [Apple Safari Web Content 归档文档](https://developer.apple.com/library/archive/documentation/AppleApplications/Reference/SafariWebContent/ConfiguringWebApplications/ConfiguringWebApplications.html)：apple-touch-icon 与 180 尺寸示例；该文档是历史归档，实际 Safari 版本需验证。
- Android、Apple 现代路线及 W3C maskable 依据沿用平台规范中已核对的一手链接。

## 当前正式交付（2026-11-16）

用户确认阅字最终v04并授权重导整套，当前包为 packages/yue-surface-kit-v02；源输出仍含185个场景文件，附加资料不混入此原始数量。采用正文居中、通用Logo右下小章，其他平台维持各自安全区规则。整套归档强制通过 scripts/visual_qa.py，交付含quality-review.json与视觉检查清单。

旧v01和错误草稿/导出已清理，旧id有阻止导出的替代提示，不要使用历史文档里的旧路径。详见 交付规范（原仓库参考：DELIVERY-PACKAGES.md） 和 [视觉QA](VISUAL-QA.md)。
