# 我的图标 · Visual Shelf

一个放得下 Logo、图标、图例和封面的个人视觉素材库。为日常文档、方案、项目 README 和网页收藏常用素材，也保存自己创建的视觉内容。

**文件可直接使用，来源可以追溯，新增有统一入口。** 当前已完成本地 Git 初始化、8 份原创 SVG 示例与 MacRightClick 产品图标、中文素材预览、导入/模板创建命令、离线校验和 GitHub 工作流。尚未创建远端仓库或发布网站。

## 立即使用

需要 Python 3.11+；浏览器使用现代 Chrome、Edge、Firefox 或 Safari。没有第三方运行依赖。

```sh
./scripts/service.sh start
./scripts/service.sh status
```

打开 [本地预览](http://127.0.0.1:4173)，以启动输出的实际端口为准。

```sh
./scripts/service.sh stop       # 停止
./scripts/service.sh restart    # 重新构建并重启
./scripts/service.sh logs       # 查看日志
```

脚本适用于 macOS/Linux，支持 `start --port 4174` 指定端口；端口冲突会报错，不会停止其他服务。状态和日志存于忽略提交的 `.runtime/`。完整行为、退出码与排查步骤见 [RTK.md](RTK.md)。

预览现为「古月藏图」：项目/产品→系列目录、素材/系列双视图，支持组件、功能、平台、状态、标签和关键词组合筛选，以及排序、三种底色、详情、下载、复制链接/Markdown/仓库路径/SVG与分享筛选。按 `/` 聚焦搜索，`Esc` 关闭弹窗。

网页用于浏览和取用；新增与创建通过本地命令完成。双击 HTML 无法加载索引，请通过 HTTP 服务打开。静态站点不需要账户、数据库或服务端 API。

## 存什么，怎样存

| 分类 | 目录 | 适用内容 |
| --- | --- | --- |
| Logo | assets/logos/ | 产品、公司、项目标识，记录品牌规范 |
| 图标 | assets/icons/ | UI 图标、功能与概念符号 |
| 图例 | assets/legends/ | 架构图节点、状态、流程图图例 |
| 封面 | assets/covers/ | 项目、文档、文章封面 |

已收录 15 份正式素材：MacRightClick 的 3 张原图、8 份初始化 SVG，以及用户本轮确认的 2 份古风无字底图和 2 份“阅”Logo。另有 1 套已确认多场景交付包，包内文件不重复计作单素材。所有示例保守标为 `LicenseRef-All-Rights-Reserved`，作者为 `unknown`，等待库主人决定署名和开放许可。

```text
assets/       可直接引用的素材文件
catalog/      按归属/系列分层，每份素材独立 JSON，含来源、许可、标签与 SHA-256
organization.json  归属、系列和组件登记（构建时计算统计）
site/         中文预览页源文件
scripts/      导入、创建、校验、构建与预览服务管理工具
catalog.json  构建后位于 dist/，用于页面和其他工具读取
schemas/      元数据 JSON Schema（供编辑器使用）
templates/    创作需求、AI 交付入口和信息采集模板
packages/     已确认的完整交付包（不自动构建到 Pages）
docs/         调研、设计取舍、发布与后续计划
tests/        有实际边界意义的离线测试
```

完整操作见 [新增与创建指南](CONTRIBUTING.md)；先理解选型可读 [调研与项目方案](docs/RESEARCH.md)。

## 按项目与产品管理

已实现结构化归属、系列和组件登记，以及功能/平台多值分类。详见 [分层管理与静态页面](docs/HIERARCHY-AND-PAGES.md)。

- `organization.json` 维护项目、产品、系列和组件；逐图 `organization` 字段引用登记标识。
- 元数据已分入 `catalog/products/`、`catalog/shared/`。新增素材自动建立对应目录；原素材链接保持稳定。
- 页面按目录浏览，也可交叉筛选；统计从正式目录构建，不计未确认草稿。
- 新系列先登记，新增用 `add --owner ... --series ... --component ... --function ... --platform ...`；收录仍需真实确认。

**可以部署到 GitHub Pages。** 构建后的 `dist/` 是纯静态站点，Python 只用于本地操作和构建；现有发布工作流保持手动触发，尚未创建远端或执行部署。参见 [发布步骤](docs/PUBLISHING.md)。

## 喜欢的风格，直接交给 AI 制作

已保存水墨浅色 A/B、月夜深蓝三种参考。可以直接说“用月夜款，大字改成知，做应用图标，先给我看”，或“给产品 X 做水墨封面，先建议布局”。AI 使用 [模板制作与确认流程](docs/TEMPLATE-WORKFLOW.md)，读取参考、准备草稿、检查并展示；你明确满意后才收录。

`python3 scripts/studio.py list` 查看风格；prepare 复制参考并生成建议，review 记录准确候选，accept 保存确认与成品。图像生成仍由 AI 使用当次可用工具完成，脚本不假装自动出图。原 `library.py create` 现在只出草稿；直接 add 必填 `--approval-note`。

## 形状、字体与平台导出

个人作品默认古风并带“古月”署名章，正文与章使用固定真实字体，不由图像模型编造文字。支持圆形、圆角方形、方形母版、封面/web 排版及 PWA 安全区配置；macOS 传统 ICNS 与现代 Icon Composer 路线分开处理。见 [个人风格与字数排版](docs/PERSONAL-STYLE.md)、[形状与平台规范](docs/PLATFORM-PROFILES.md)。

原生渲染命令 `./scripts/render-logo.sh --help`，当前需 macOS/Swift；传统图标打包命令 `./scripts/export-macos.sh 输入.png 新目录`。新示例仍走草稿确认；已确认的“阅”圆形浅色和圆角月夜 v02 已正式入库。字体文件及 OFL 许可位于 resources/fonts/mashanzheng。

## 常用场景模板套件

浏览器标签（SVG/PNG/多帧 ICO）、Apple Touch Icon、PWA any/maskable、分享图、web/封面、圆形/圆角 Logo、传统 macOS 图标包及 Android 分层资源均有模板入口。用 `python3 scripts/export-kit.py --help` 生成本地草稿套件；包括实际尺寸预览、接入片段和哈希清单，未批准不会替换站点或自动入库。完整能力与限制见 [场景模板清单](docs/SCENE-TEMPLATES.md)。

## 已登记产品

- [MacRightClick · 右键助手](docs/entities/products/macrightclick.md)：主用月夜深蓝图标、两张浅色候选及真实引用位置。后续创作先读 [品牌与使用档案](docs/brands/products/macrightclick.md)；盘点与哈希见 [收录快照](docs/inventories/2026-11-16-macrightclick.md)。

## 新增一份素材

```sh
python3 scripts/library.py add --approval-note "填入用户对该文件的实际确认" /绝对路径/logo.svg \
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

## 已确认作品与按需交付

底图 A/C、阅字 Logo A/B 和原 185 文件套件已依据用户明确确认收录。详情见 [确认与交付记录](docs/creation-runs/2026-11-16-approved-guyue-assets.md)。浅色 B 瑕疵底图仍待修。

需要使用时可以说：“把这份图例打个 AI 接入包”，或“导出阅的 Web / macOS 包”。AI 先复用已确认文件，不重复问是否满意；目标缺失时只补问必要的用途。每包包含来源、确认、入口、哈希、README/AGENTS 与独立校验；整套还包含原背景、固定字体/OFL 和原生渲染器。命令和文件位置见 [交付包规范](docs/DELIVERY-PACKAGES.md)。
