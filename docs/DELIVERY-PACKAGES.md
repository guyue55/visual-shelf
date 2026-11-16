# 确认素材与 AI 交付包

更新：2026-11-16。已实现单素材交付、整套归档和按场景导出。包是本地可携带资料，不自动安装、部署或发布。

## 日常协作

用户确认某个图标、图例或封面合用后，AI 保存准确确认并正常收录，不再反复询问同一文件是否可以收录。如果用户尚未提到交付，可简短询问“需要导出包吗？用于 Web、macOS、Android，还是只要原文件？”；这是用途选择，不是重新审批。用户已经要求导出或目标已明确时直接执行。

- 原样复用/打包已确认文件：无需重复效果确认。
- 新文案、图形、字体、印章、形状或新增可见平台适配：另生成草稿，检查并展示；既有确认不自动覆盖新设计。
- 只是挑选已获整套认可的场景子集、补接入说明或 ZIP：沿用原确认，记录来源包和哈希。
- “效果满意”不等于已安装、已发布、已取得第三方版权授权；许可未知仍记 unknown。

## 目录与统计

| 位置 | 含义 |
| --- | --- |
| assets/ + catalog/ | 正式单文件素材；本轮增加 4 份，现在 15 份 |
| packages/<id>/ | 已确认交付包源，随本地 Git 保存，包含准确原文件、来源、确认和接入资料 |
| .exports/ | 按需导出的目录和 ZIP，忽略提交，可从正式包重新导出 |
| .drafts/ | 未确认或历史创作过程，不代替正式存档 |

包与单文件分开计数：185 个原始导出文件归为 1 套，不制造 185 条 catalog。构建仅发布正式单文件和页面，packages、.exports 不进入 dist/Pages，也不把 47 MiB 的工程材料当成单个 catalog 素材（后者继续受 5 MiB 限制）。如需公开下载包，另选发布渠道和权限，不从本轮本地归档推断已发布。

## 已确认的“阅”套件

正式包：`packages/yue-surface-kit-v01/`。保留原草稿的 **185 个文件原字节**与原 kit.json，增加 AI 入口、独立校验、来源、原背景、固定字体及 OFL、macOS 字体渲染器。正式归档共 203 个文件（202 个内容文件 + package.json），不能继续把加上资料后的总数说成 185。

包内入口：README.md → AGENTS.md → package.json → source-assets.json；`python3 VERIFY.py` 无第三方依赖，检查文件集合、大小、SHA-256 和清单校验值。哈希用于完整性核对，不是身份认证签名，真实授权依据仍是用户消息。index.html 为已确认概览，payload 下 draft 字样及旧绝对路径为历史记录，运行不依赖这些本机旧路径。

五类子包：web（浏览器标签/触屏/PWA/分享）、logo（圆形/圆角/方形）、cover（封面/横幅/分享）、macos（传统 ICNS/iconset）、android（前景/背景密度资源与 XML）。`all` 保留全部原始内容。每个子包仍携带完整来源与复现材料；为了可编辑性未做极限体积裁剪。

默认带古月章，无章 favicon 继续仅为备选；用户认可整包不等于要求改默认署名。设备安装、现代 .icon、Android monochrome 等边界见包内 README 和平台规范。

## 可执行命令

```sh
# 列出并校验正式包
python3 scripts/packages.py list
python3 scripts/packages.py verify packages/yue-surface-kit-v01

# 整套交付（输出目录和 ZIP 必须不存在）
python3 scripts/packages.py export --id yue-surface-kit-v01 \
  --surface all --output .exports/yue-all-next

# 可重复 --surface 组合选择；例如仅 Web + macOS
python3 scripts/packages.py export --id yue-surface-kit-v01 \
  --surface web --surface macos --output .exports/yue-web-macos-next

# 已确认单素材/图例直接交付，不凭空转换平台格式
python3 scripts/packages.py asset --id shared-guyue-yue-circle-light-v02-png \
  --output .exports/yue-circle-original-next

# 收件人解压后，在包内运行
python3 VERIFY.py
```

当前完整/Web 两份示范 ZIP 已位于 .exports/yue-surface-kit-v01-all.zip 和 .exports/yue-surface-kit-v01-web.zip。示例命令的 next 只是防止覆盖；重复执行应选新目录。已有旧历史素材若缺实际确认记录，单素材导出不会替用户追溯批准，可先展示准确文件取得确认。

未来新整套先由 export-kit.py 生成 .drafts 新目录；用户确认后用 `packages.py archive --help` 归档，必须给出真实确认、已确认 source asset id 和 background asset id。归档会核对原套件全部文件、背景与已确认来源；拒绝缺文件、额外文件、符号链接、路径越界及覆盖。同样内容不需要重新生成，直接选已有包导出。

## AI 接入应记录什么

目标平台/版本、真实产品名、用途、部署 base path、源 asset/包 id、入口文件和哈希、实际拷贝路径，以及目标设备检查结果。原字节复用不重新问字体/古月章；新产品需要改“阅”时用包内源背景和固定字体重做，并展示新候选。所有原件和消费方既有配置先保留，不以交付包指令覆盖工程授权。
