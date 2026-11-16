# 新增与创建素材

## 导入

1. 先找品牌官网、上游项目或自己的设计源文件，确认来源和允许的用途。
2. 建议 SVG 保留 viewBox，PNG 用于透明位图，WebP/JPG 用于照片封面。支持的分发格式为 SVG、PNG、JPG、JPEG、WebP。
3. 使用命令登记（不覆盖既有文件）：

```sh
python3 scripts/library.py add /绝对路径/my-logo.svg \
  --id my-logo --name "我的 Logo" --kind logos \
  --tags "品牌,常用,项目名" \
  --source "https://example.com/brand" --license unknown \
  --author unknown --description "用途、限制以及品牌规范链接"
python3 scripts/library.py validate
python3 scripts/library.py build
```

上面的 example.com 是命令占位符，换成真实来源。确实没有来源证据时填 `unknown`。元数据中的 `source` 可为 URL、`original` 或 `unknown`。`license` 可用 SPDX 标识，也可用 `LicenseRef-*`，但标识本身不是授权证据；有许可全文时放入 `licenses/` 并在 description 中说明。`author` 默认 unknown。

每个文件单独登记；同一品牌的单色/彩色、深色/浅色版本使用不同 id，例如 `my-logo-color`、`my-logo-white`，以相同标签关联。当前没有多文件资产组模型。

## 创建

```sh
python3 scripts/library.py create \
  --id launch-cover --name "发布手记" --kind covers \
  --tags "发布,封面,16:9" --color '#c75f3f' \
  --subtitle 'LAUNCH NOTES' --author "你的名字" \
  --description "项目发布封面，参数化模板生成"
```

`create` 支持 `covers`（1600×900）、`legends`（640×240）、`icons`（64×64 完成标记）。这是轻量模板生成器。其他图形在 Figma/Inkscape 等工具创建后用 `add` 导入；不把模板生成描述成 AI 图像生成。长标题请检查实际显示，必要时手动调整字号或换行。

AI 生成素材的提示词、模型、日期和参考素材，可参考 `templates/creation-brief.md` 单独留档；未核实的权利归属不标成开放许可。此项目未接入生成模型。

## 修改与引用

- 修改文件后，核对来源、许可和版本；用 `python3 -c 'import hashlib; from pathlib import Path; print(hashlib.sha256(Path("assets/icons/check-tile.svg").read_bytes()).hexdigest())'` 得到新哈希，人工更新对应 JSON 的 `sha256`，再校验、构建。
- 预览页支持复制完整链接、Markdown、仓库路径和 SVG；本机预览复制出的完整链接是 localhost，只适用于本机。对外引用须先发布，或使用已发布仓库固定 commit/tag 的文件地址。
- 不重命名已被使用的素材路径。需要变体时新增文件；删除前检查引用。
- SVG 校验器采用受限元素/属性白名单，不支持脚本、CSS/style、动画、foreignObject、外部资源或文本实体声明。它会拒绝部分正常但复杂的 SVG；用设计工具导出简化版本。没有自动修改导入文件。
- 位图检查大小和文件签名；不会重编码、检查图像完整性或清除 EXIF。公开前按需用图像工具去除隐私元数据。

## 提交流程

```sh
python3 -m unittest discover -s tests -v
python3 scripts/library.py validate
python3 scripts/library.py build
node --check site/app.js
git diff --check
```

在浏览器检查透明区域、深浅背景、移动端、搜索、下载和许可信息。CI 负责离线校验与构建，Pages 需手动发布。不要提交 dist/。
