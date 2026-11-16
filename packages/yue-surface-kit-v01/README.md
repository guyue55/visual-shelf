# 古月 · 阅 · 多场景交付套件 v01

状态：approved。正文：阅；默认署名章：古月；固定字体：MaShanZheng-Regular。
本包是已确认效果的交付材料，未安装到任何项目，也不表示获得了未核实的第三方再分发许可。

先运行 `python3 VERIFY.py`。打开 `index.html` 查看已确认场景；若浏览器不支持本地预览，使用收件项目正常开发服务，不绕过安全提示。原始草稿预览和 render.json 的 draft 字样仅为历史生成状态；当前确认和文件范围以 package.json 为准。

## 找到要用的文件

| 场景 | 入口 |
| --- | --- |
| web | `payload/favicon.ico`、`payload/favicon.svg`、`payload/apple-touch-icon.png`、`payload/site.webmanifest`、`payload/head-snippet.html` |
| logo | `payload/circle-logo/logo.png`、`payload/rounded-logo/logo.png`、`payload/square-master/logo.png` |
| cover | `payload/cover/logo.png`、`payload/web/logo.png`、`payload/og-image.png` |
| macos | `payload/macos-legacy/AppIcon.icns`、`payload/macos-legacy/AppIcon.iconset`、`payload/macos-legacy/AppIcon.png` |
| android | `payload/android-res/mipmap-anydpi-v26/ic_launcher.xml`、`payload/android-res/drawable-mdpi` |

`payload/` 保存原尺寸文件、前背景层与真实字体轮廓；不要把 foreground.svg 当成含山水背景的完整矢量图。`source/` 保存可离线复现的背景、固定字体/OFL、macOS 渲染器及平台规则。制作新文案时先阅读 AGENTS.md；当前确认只覆盖原文字和原字节，不能批准新设计。

## AI 接入顺序

1. 读取 package.json 的 source_assets、approval、entrypoints 与 limitations，运行 VERIFY.py。
2. 用户已指定目标时直接采用相应入口；缺少关键环境时集中询问目标平台、应用/产品名、部署 base path。不要重复询问已确认的风格、固定字体和古月章。
3. 只复制所需文件到消费项目新目录，保留原工程和品牌文件；真正接入前查该项目说明，不能从本包获得覆盖、发布权限。
4. Web：head-snippet.html 是示例；OG 域名占位符必须替换为真实绝对 URL，图标/manifest 路径按实际部署目录调整。manifest 仅图标信息，安装还需目标项目配置。改名时同步 name/short_name，不改图内“阅”字冒充新字标。
5. macOS：此包为传统 ICNS 路线，按真实工程配置接入；不是现代 .icon。Android：使用完整密度前背景和 XML，合并现有资源冲突，旧 API 回退和 monochrome 另处理。
6. 在目标浏览器/设备检查实际尺寸、深浅背景、裁切、安全区与缓存；记录实际使用的包 id、文件哈希和路径。效果认可不等于已完成设备验收。

## 修改文案与复现

在 macOS（Swift/CoreText）运行，例如：

```sh
bash source/scripts/render-logo.sh --background source/background.png --text 知 \
  --profile rounded-logo --theme dark --output /绝对路径/新的草稿目录
```

主字与章使用包内同一份固定字体，缺字报错；新文案/形状必须重新展示确认。其他系统可以直接使用已导出文件，不能声称此原生渲染器跨平台。原 render.json 中的旧绝对路径不是运行依赖，实际背景/字体已按包内相对路径提供。

## 来源、确认与限制

用户确认原意：用户本轮明确：生成的一套 185 个文件的草稿包效果也可以；要求及时更新文档，完善包内信息便于 AI 直接使用。确认原有整套文件效果；无章款继续作为备选，未授权替换默认古月章。

来源素材逐项记录于 source-assets.json，包括 SHA-256、参考、工具与真实确认。底图逐图权利和后端模型仍为 unknown；固定字体按 source/resources/fonts/mashanzheng/OFL.txt。本包不授予商标或原图再分发权。

无章 favicon-simple-option 仅作为已交付备选保留；默认仍带古月章，不从“整包可以”推断替换个人署名规则。现代 Apple Icon Composer、Android monochrome、PWA/Apple Touch 的设备安装验收仍需在目标工程完成。
