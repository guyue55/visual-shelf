# 我的图标 · Visual Shelf

一个放得下 Logo、图标、图例和封面的个人视觉素材库。为日常文档、方案、项目 README 和网页收藏常用素材，也保存自己创建的视觉内容。

**文件可直接使用，来源可以追溯，新增有统一入口。** 当前已完成本地 Git 初始化、8 份原创 SVG 示例、中文素材预览、导入/模板创建命令、离线校验和 GitHub 工作流。尚未创建远端仓库或发布网站。

## 立即使用

需要 Python 3.11+；浏览器使用现代 Chrome、Edge、Firefox 或 Safari。没有第三方运行依赖。

```sh
python3 scripts/library.py build
python3 -m http.server 4173 --bind 127.0.0.1 --directory dist
```

打开 [本地预览](http://127.0.0.1:4173)。支持中英文名称/标签搜索、分类、排序、深浅背景预览、详情、下载、复制链接/Markdown/仓库路径/SVG。按 `/` 聚焦搜索，`Esc` 关闭弹窗。

网页用于浏览和取用；新增与创建通过本地命令完成。双击 HTML 无法加载索引，请通过 HTTP 服务打开。静态站点不需要账户、数据库或服务端 API。

## 存什么，怎样存

| 分类 | 目录 | 适用内容 |
| --- | --- | --- |
| Logo | assets/logos/ | 产品、公司、项目标识，记录品牌规范 |
| 图标 | assets/icons/ | UI 图标、功能与概念符号 |
| 图例 | assets/legends/ | 架构图节点、状态、流程图图例 |
| 封面 | assets/covers/ | 项目、文档、文章封面 |

目前 Logo 分类为空，避免把未经选择的第三方标识当作你的收藏。其余分类含 8 份小体积 SVG 示例。所有示例保守标为 `LicenseRef-All-Rights-Reserved`，作者为 `unknown`，等待库主人决定署名和开放许可。

```text
assets/       可直接引用的素材文件
catalog/      每份素材独立 JSON，含来源、许可、标签与 SHA-256
site/         中文预览页源文件
scripts/      导入、创建、校验、构建工具
catalog.json  构建后位于 dist/，用于页面和其他工具读取
schemas/      元数据 JSON Schema（供编辑器使用）
templates/    创作需求和信息采集模板
docs/         调研、设计取舍、发布与后续计划
tests/        有实际边界意义的离线测试
```

完整操作见 [新增与创建指南](CONTRIBUTING.md)；先理解选型可读 [调研与项目方案](docs/RESEARCH.md)。

## 新增一份素材

```sh
python3 scripts/library.py add /绝对路径/logo.svg \
  --id example-logo --name "示例 Logo" --kind logos \
  --tags "品牌,常用" --source unknown --license unknown
python3 scripts/library.py build
```

创建封面、图例和完成标记，见 [CONTRIBUTING.md](CONTRIBUTING.md)。批量搬运上游整库、网页在线上传、AI 出图和自动转换格式均未接入。

## 放到 GitHub

建议仓库名 `visual-shelf`；也可以用其他英文名称，站点资源使用相对路径，兼容项目子目录。远端公开性和仓库归属由你决定，具体步骤见 [发布指南](docs/PUBLISHING.md)。

- `ci.yml`：push/PR 时测试、验证、构建。
- `pages.yml`：仅手动触发的 Pages 发布；需要先在 GitHub 设置 Pages 来源为 GitHub Actions。
- 本地构建无需网络，第三方 CDN 不参与页面运行。

## 许可

目前没有为整个项目指定统一开放许可。代码、原创素材的许可由库主人后续决定；第三方素材始终遵守各自的版权、许可与商标要求。`unknown` 表示未核实，不表示可自由商用。详见 [RIGHTS.md](RIGHTS.md)。
