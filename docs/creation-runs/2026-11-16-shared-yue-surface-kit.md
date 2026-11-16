# 阅 · 多场景模板套件草稿

> 后续状态更新：用户已在 2026-11-16 明确确认并准许收录。底图 A/C、阅字 Logo A/B 及原 185 文件套件已正式保存；详见 [确认收录记录](2026-11-16-approved-guyue-assets.md)。以下“未确认”等表述仅记录最初制作阶段，浅色 B 瑕疵底图仍待修。


日期：2026-11-16。用户要求各类模板提前准备，尤其浏览器标签。未收到对任何新成品的正式收录批准。

## 实际生成

执行 export-kit.py，文字“阅”，深色主题，背景为此前无字月夜 PNG，输出到 `.drafts/yue-surface-kit-v01/`。生成 10 类主配置加一个标签简化备选，共 185 个文件（不含 kit.json 自身），约 39 MiB。字体仍为固定 MaShanZheng-Regular，普通版本默认古月章。

包括实际 favicon SVG/16-32-48 PNG/三帧 ICO、Apple Touch 180 PNG、PWA any/maskable 的 192/512 PNG 与 manifest、1200×630 分享图、1600×900 封面、1600×600 横幅、圆形/圆角 Logo、未裁方形母版、Android 前背景及五档密度 XML 资源，以及传统 macOS ICNS 包。

favicon 为素色高对比背景和短标记，避免把山水直接缩到十几像素。另给 favicon-simple-option 无章备选，未自动启用。现代 Apple `.icon` 和 Android monochrome 不在实际生成能力内。

## 验证

- ICO：文件头 3 帧、尺寸 16/32/48、偏移/长度与实际 PNG 对应，系统 file 命令识别为 Windows icon resource。
- SVG：独立底色与真实文字轮廓，XML 可解析，不依赖用户安装字体。
- PWA：manifest 各相对图标存在，PNG 尺寸与 sizes 相符；maskable 字形和章在安全圆内。
- Android：108/162/216/324/432 px 前景/背景与 XML 已输出，1080px 母版的关键字形安全区通过。
- 固定字体、alpha、小尺寸/新平台及文件格式回归：本地全量 37 项测试通过。
- 目视检查 32px 带章/简化标签和分享图：正文可辨，带章小图章文很弱。分享图背景按 cover 裁切，不能保证原人物完整，正式用途仍需调整构图与实际验收。
- 预览 HTML 的浏览器加载未完成：浏览器工具拒绝 file:// 协议。本轮没有绕过协议限制、没有另启服务公开草稿，也没有把样例接入本库线上或本地正式站点。

## 交付边界

kit.json 记录每个文件的哈希；素材清单仍为 11 份，未调用 accept。原 MacRightClick 图标与应用未改动。site.webmanifest 只含图标信息，不是完整 PWA；head-snippet 的域名占位符需要真实项目接入时替换。Android/Apple Touch/PWA 安装效果、各浏览器 favicon 实际选择与缓存、现代 Icon Composer 尚未设备验收。
