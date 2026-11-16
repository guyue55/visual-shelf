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

## 按项目与产品管理

后续不同项目和产品的 Logo、封面等，统一遵循 [多项目与产品素材管理规范](docs/ASSET-MANAGEMENT.md)：

- 分类目录保持稳定，使用实体登记卡与标签关联项目、产品、素材家族、变体和修订。
- 同一产品素材可被多个项目复用，记录实际使用位置，不因使用方不同重复存文件。
- 新素材按“归属类型、归属标识、用途、变体、修订、格式”命名，旧路径保持不变。
- 统一文件数、家族数、项目/产品数、存储、权利缺口和复用的统计口径。

目前可通过标签、[实体登记卡](templates/entity-record.md) 和 [统计快照](templates/inventory-report.md) 人工管理；结构化关系校验、自动统计和专用管理页面尚未实现。规范中附有当前文件基线及后续实现顺序。

## 新增一份素材

```sh
python3 scripts/library.py add /绝对路径/logo.svg \
  --id example-logo --name "示例 Logo" --kind logos \
  --tags "品牌,常用" --source unknown --license unknown
python3 scripts/library.py build
```

创建封面、图例和完成标记，见 [CONTRIBUTING.md](CONTRIBUTING.md)。批量搬运上游整库、网页在线上传、AI 出图和自动转换格式均未接入。

## 让 AI 持续辅助制作

除了保存成品，也保存可复用的制作上下文。按 [AI 辅助创作协议](docs/AI-CREATION.md)，首次为实体建立 [品牌档案](templates/brand-profile.md)，记录已确认的配色、字体、参考、固定元素和否决项；后续只提供本次主题与变化。AI 先读已有档案，再按 [Logo、封面、图例制作流程](docs/CREATION-RECIPES.md) 执行，减少重复沟通。

例如：

> 给产品 X 做一张“新版本发布”封面，沿用已确认品牌和系列版式，标题为“……”。

档案、场景流程和 [制作记录模板](templates/creation-run.md) 已就绪，可供能读仓库的 AI 使用；自动上下文导出、模型调用与创作界面尚未实现。内置 `create` 仍是有限 SVG 模板生成，不等同于 AI 图像生成。

## 放到 GitHub

建议仓库名 `visual-shelf`；也可以用其他英文名称，站点资源使用相对路径，兼容项目子目录。远端公开性和仓库归属由你决定，具体步骤见 [发布指南](docs/PUBLISHING.md)。

- `ci.yml`：push/PR 时测试、验证、构建。
- `pages.yml`：仅手动触发的 Pages 发布；需要先在 GitHub 设置 Pages 来源为 GitHub Actions。
- 本地构建无需网络，第三方 CDN 不参与页面运行。

## 使用 AI 维护

将仓库交给 AI 助手时，让它先读取 [AGENTS.md](AGENTS.md)。这里集中维护项目结构、工作流程、素材规范、验证与交接要求；[RTK.md](RTK.md) 提供实际命令。[CLAUDE.md](CLAUDE.md) 是轻量入口，引用同一份规则。

不同工具自动加载项目说明的方式可能不同，本项目不保证所有工具自动识别；手动指定读取 `AGENTS.md` 即可，无需安装专属插件。可直接使用以下开场指令：

> 请先读取 AGENTS.md 和 RTK.md，检查当前工作区，再完成以下任务：……。按改动范围验证，并说明完成内容与未验证项。

跨会话继续时可使用 [任务交接模板](templates/task-handoff.md)。添加其他工具入口时只引用 `AGENTS.md`，避免复制出多套规则。

## 许可

目前没有为整个项目指定统一开放许可。代码、原创素材的许可由库主人后续决定；第三方素材始终遵守各自的版权、许可与商标要求。`unknown` 表示未核实，不表示可自由商用。详见 [RIGHTS.md](RIGHTS.md)。
