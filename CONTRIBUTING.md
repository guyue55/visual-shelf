# 新增与创建素材

## 满意后再收录

新创作遵循 [模板与确认流程](docs/TEMPLATE-WORKFLOW.md)：草稿 → review → 向用户展示准确版本 → 明确满意并准许 → accept。以下 add 示例只适用于用户已确认的文件；不得填假确认。create 现在只写 .drafts 草稿，不直接入库。

## 先确定归属与版本

涉及不同项目/产品时，先读 [素材管理规范](docs/ASSET-MANAGEMENT.md)，确认主要归属、素材家族、变体、修订和真实使用方。首次实体使用 [登记卡模板](templates/entity-record.md)；优先复用已有文件。归属未知如实记录，不自动算作 shared。

新素材采用该规范的 id 与标签约定；下文简短命令仅演示工具参数，不代表已完成项目登记。当前工具没有 `--project`、`--product` 或自动统计参数，关联由现有 `--tags` 和登记卡维护。校验器尚不会检查管理标签和实体关系。

## 导入

1. 先找品牌官网、上游项目或自己的设计源文件，确认来源和允许的用途。
2. 建议 SVG 保留 viewBox，PNG 用于透明位图，WebP/JPG 用于照片封面。支持的分发格式为 SVG、PNG、JPG、JPEG、WebP。
3. 使用命令登记（不覆盖既有文件）：

```sh
python3 scripts/library.py add --approval-note "填入用户对该文件的实际确认" /绝对路径/my-logo.svg \
  --id my-logo --name "我的 Logo" --kind logos \
  --tags "品牌,常用,项目名" \
  --source "https://example.com/brand" --license unknown \
  --author unknown --description "用途、限制以及品牌规范链接"
python3 scripts/library.py validate
python3 scripts/library.py build
```

上面的 example.com 是命令占位符，换成真实来源。确实没有来源证据时填 `unknown`。元数据中的 `source` 可为 URL、`original` 或 `unknown`。`license` 可用 SPDX 标识，也可用 `LicenseRef-*`，但标识本身不是授权证据；有许可全文时放入 `licenses/` 并在 description 中说明。`author` 默认 unknown。

每个文件单独登记；同一品牌的单色/彩色、深色/浅色版本使用不同 id，例如 `my-logo-color`、`my-logo-white`，以相同标签关联。当前没有程序支持的多文件资产组模型；家族、变体和跨项目使用的人工管理方式见 [素材管理规范](docs/ASSET-MANAGEMENT.md)。

## 创建

个人作品默认带古月章，字体与字数排版见 [个人规范](docs/PERSONAL-STYLE.md)；形状与不同平台格式见 [平台规范](docs/PLATFORM-PROFILES.md)。使用固定字体渲染时先制作无字底图，再运行 render-logo.sh；背景无需让模型重新画文字。

重复制作同一项目/产品的素材时，按 [AI 辅助创作协议](docs/AI-CREATION.md) 先复用品牌档案与场景流程，再记录本次变化；不要每次重新索要配色、字体和参考。下方命令只是仓库内置的模板路线，其他创作工具按实际能力调用并留存制作记录。

```sh
python3 scripts/library.py create \
  --id launch-cover --name "发布手记" --kind covers \
  --tags "发布,封面,16:9" --color '#c75f3f' \
  --subtitle 'LAUNCH NOTES' --author "你的名字" \
  --description "项目发布封面，参数化模板生成"
```

`create` 生成的 template.svg 可用 studio review 登记，用户确认后 accept。仅 build 不会把草稿加入预览。

`create` 支持 `covers`（1600×900）、`legends`（640×240）、`icons`（64×64 完成标记）。这是轻量模板生成器。其他图形在 Figma/Inkscape 等工具创建后用 `add` 导入；不把模板生成描述成 AI 图像生成。长标题请检查实际显示，必要时手动调整字号或换行。

AI 生成素材的提示词、模型、日期和参考素材，可参考 `templates/creation-brief.md` 单独留档；未核实的权利归属不标成开放许可。此项目未接入生成模型。

## 修改与引用

- 已被使用的素材发生可见变化时，按管理规范新增修订与文件，保留旧引用；原路径修改限未被使用的草稿或明确无需新修订的维护。修改文件后，核对来源、许可和版本；用 `python3 -c 'import hashlib; from pathlib import Path; print(hashlib.sha256(Path("assets/icons/check-tile.svg").read_bytes()).hexdigest())'` 得到新哈希，人工更新对应 JSON 的 `sha256`，再校验、构建。
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

涉及项目/产品或版本关系时，同时核对管理标签、登记卡、推荐 asset id 和使用位置；集中整理或交付前按 [统计模板](templates/inventory-report.md) 生成快照。状态标签不会隐藏网页素材，不能作为保密控制。

使用 `./scripts/service.sh start` 启动，`restart` 更新预览，`stop` 停止；状态和排查见 [RTK.md](RTK.md)。

在浏览器检查透明区域、深浅背景、移动端、搜索、下载和许可信息。CI 负责离线校验与构建，Pages 需手动发布。不要提交 dist/。

## 按归属与系列收录

先在 organization.json 登记 owner、series、component。查看 [分层管理规范](docs/HIERARCHY-AND-PAGES.md)。在原 add 命令增加：

```sh
  --owner product:macrightclick --series macrightclick-app-icon \
  --component app-identity --function 产品识别 --function 应用启动 --platform macOS
```

该片段须接在完整 add 命令后。只有实际确认的文件才能 add（必填 --approval-note）；studio accept 同样支持这些分组参数。未知归属不能凭文件名猜测；尚未明确时留在草稿并提示补充。新增默认建立分组目录，旧文件不搬动。检索元数据用递归查找，不再假定 catalog 根目录有全部 JSON。create 的 --folder 不适用（尚未正式入库）；其结构化参数仅作为草稿建议保存。
