# 我的图标 · 运行手册

通用 AI 协作规则见 [AGENTS.md](AGENTS.md)。本文件只维护运行命令和实现边界。

## 环境与验证

在仓库根目录运行。需要 Python 3.11+；JS 语法检查需要 Node.js。运行与构建无需安装第三方依赖。

```sh
# 查看命令帮助
python3 scripts/library.py --help
python3 scripts/library.py add --help
python3 scripts/library.py create --help

# 素材、元数据、哈希、重复内容及 SVG 静态子集
python3 scripts/library.py validate

# 工具行为与边界测试
python3 -m unittest discover -s tests -v

# 生成网站和目录；只替换 dist/
python3 scripts/library.py build

# 前端语法和差异格式
node --check site/app.js
node --check site/catalog-model.js
node --test tests/catalog-model.test.cjs
git diff --check
```

## 本地预览：统一管理入口

macOS / Linux、Bash、Python 3.11+。从任意目录都可用脚本绝对路径运行；在仓库根目录使用：

```sh
./scripts/service.sh start          # 构建并后台启动；重复执行不会多开
./scripts/service.sh status         # 检查进程归属与 HTTP 健康状态
./scripts/service.sh logs           # 最近 80 行服务日志
./scripts/service.sh restart        # 停止后重新构建并启动，沿用受管端口
./scripts/service.sh stop           # 只停止本脚本管理的进程；重复停止安全
./scripts/service.sh --help
```

默认地址 http://127.0.0.1:4173/ ，以脚本实际输出为准。默认仅监听本机；后台进程可在终端退出后继续运行，不是开机自启或自动故障恢复服务。

```sh
./scripts/service.sh start --port 4174
./scripts/service.sh restart --port 4175
```

- 可选 `VISUAL_SHELF_PYTHON=/绝对路径/python3` 指定解释器；不要用环境变量拼接附加命令参数。
- 启动成功必须同时通过进程归属与 HTTP 检查，不以 PID 文件存在作为成功证据。
- 已运行时再次 start 不重建；修改代码/素材后使用 restart，再刷新浏览器。原有 library.py build 仍可独立使用。
- `.runtime/service.json` 保存受管 PID、端口和每次启动标识；`.runtime/service.log` 追加日志；`.runtime/service.lock` 为内核锁。运行文件均忽略提交，不要手动复制状态到其他仓库。
- 管理命令通过内核锁串行互斥；遇到并发会立即报错，完成后再重试。锁文件存在不代表仍被锁定，不需要删除锁文件。
- 退出码：0 为操作成功或服务健康；status 返回 1 为未运行/不健康；管理错误返回 2。stop 在已停止时返回 0；logs 无日志时返回 0。
- 状态中的进程已退出或 PID 被复用时，stop 只清理过期记录，不向其他进程发信号。损坏的 JSON 状态会报错，先人工核对进程和日志，不能据此直接 kill。
- 端口占用时明确报错，不自动抢占或偷偷换端口；指定空闲端口再启动。status 仅报告受管服务，不负责列出全部端口服务。
- stop 使用 TERM 并等待；超时会保留状态并报错，不自动强杀。restart 会先停旧服务，构建/新启动失败时服务可能保持停止；检查日志和构建错误后重新 start，不承诺无停机更新。
- 日志当前不自动轮转，需要时在服务停止后归档；不要把大量日志提交仓库。

浏览器按改动检查搜索、分类、空态、详情、复制、下载、深浅背景和窄屏布局；新增素材需实际查看。

### AI 操作顺序

先运行 status。需要启动用 start；需要更新已有预览用 restart；用户要求停止用 stop。根据退出码和日志诊断，完成后再次 status 并报告实际 URL。不要使用 `pkill -f`、按端口强杀或绕过脚本创建第二个常驻预览；旧的手动 http.server 不会自动纳入脚本管理。

## 服务脚本验证

```sh
bash -n scripts/service.sh
python3 -m unittest discover -s tests -v
```

服务测试在临时副本、空闲端口运行，覆盖启动/重复启动/HTTP/重启/停止、其他进程占端口、过期 PID、损坏状态、并发互斥和构建失败；测试不会接管日常预览服务。

## 新增与创建

完整参数和示例见 [CONTRIBUTING.md](CONTRIBUTING.md)，创作需求见 [templates/creation-brief.md](templates/creation-brief.md)。

- `create` 只生成 .drafts 下的 SVG 草稿；add 直接收录已确认文件，必填 --approval-note。新创作优先按 studio prepare/review/accept 执行，正式收录后 restart 更新预览。
- `create` 当前支持 covers、legends、icons；不提供品牌 Logo 或 AI 模型生成。
- 文件与 `catalog/` 为可维护源，`dist/catalog.json` 为生成索引。
- Schema 供编辑器参考；运行时实际准入规则以 `scripts/library.py` 为准。
- 位图仅检查签名和大小；SVG 是受限白名单，不能宣称通用清洗或完整图像解码验证。

## 模板与确认收录

运行 `python3 scripts/studio.py list`、`prepare --help`、`review --help`、`accept --help`。完整流程见 [docs/TEMPLATE-WORKFLOW.md](docs/TEMPLATE-WORKFLOW.md)。模板索引位于 templates/visual/styles.json，未批准文件位于忽略提交的 .drafts/；不得以自动校验通过代替用户满意确认。

## 固定字体渲染与平台导出

```sh
./scripts/render-logo.sh --help
./scripts/render-logo.sh --background /绝对路径/无字底图.png \
  --text 阅 --profile circle-logo --theme light --output .drafts/<任务>/render
./scripts/export-macos.sh .drafts/<任务>/render/logo.png .drafts/<任务>/macos-legacy
```

渲染仅适用于 macOS/Swift，使用固定字体轮廓，默认古月章；`--no-seal` 仅在用户明确要求时使用。每次输出到新目录，不覆盖已展示候选。支持配置见 [平台规范](docs/PLATFORM-PROFILES.md)，个人偏好与字数规则见 [个人规范](docs/PERSONAL-STYLE.md)。原生字体/alpha/布局测试在 macOS 运行，Linux 自动跳过；ICNS 输出不能代替目标环境视觉验收。

## 常用场景整套导出

`python3 scripts/export-kit.py --help` 提供浏览器标签、触屏/PWA、分享图、Android 前背景和传统 macOS 等草稿导出。当前依赖 macOS/Swift/sips/iconutil。详情见 [docs/SCENE-TEMPLATES.md](docs/SCENE-TEMPLATES.md)。输出只允许 .drafts 下的新目录；不得把草稿接入当前站点冒充已批准。

## AI 辅助创作

读取 [docs/AI-CREATION.md](docs/AI-CREATION.md) 与 [docs/CREATION-RECIPES.md](docs/CREATION-RECIPES.md)，再定位实体品牌档案。当前是 AI 可遵循的文件协议，没有自动上下文导出或生成 API 命令；不要虚构 CLI 参数。

## 项目与产品管理

归属、命名、版本和统计口径见 [docs/ASSET-MANAGEMENT.md](docs/ASSET-MANAGEMENT.md)。已实现 organization.json 登记、递归 catalog、owner/series/component 关系校验和构建统计。add 与 studio accept 支持 --owner、--series、--component、重复 --function / --platform；create 可保存建议分组到草稿，accept 时验证后使用。详情见 [分层管理](docs/HIERARCHY-AND-PAGES.md)。

## 发布与历史记录

- 发布方式见 [docs/PUBLISHING.md](docs/PUBLISHING.md)，以实际远端配置和工作流执行结果为准。
- [docs/RESEARCH.md](docs/RESEARCH.md) 是选型背景；[docs/VERIFICATION.md](docs/VERIFICATION.md) 是初始化时的历史验证，不代表此后改动已通过。
- 本手册仅适用于本仓库，不引入其他项目的运行、磁盘迁移或部署约定。

## 当前确认、检查与交付

已确认范本为阅字v04，当前包yue-surface-kit-v02。旧版图像、草稿、包与ZIP已清理，旧id由advisories提示替代。通用Logo默认右下小章；favicon/PWA/Android/横幅等按各自安全区。

```sh
python3 scripts/packages.py list
python3 scripts/packages.py verify packages/yue-surface-kit-v02
python3 scripts/packages.py export --id yue-surface-kit-v02 --surface all --output .exports/yue-all-new
python3 scripts/packages.py asset --id shared-guyue-yue-circle-light-v04-png --output .exports/yue-circle-new
python3 scripts/visual_qa.py .drafts/<新套件目录>
```

正式整套包带quality-review.json；收件人先python3 VERIFY.py，再python3 source/scripts/visual_qa.py payload。新archive还必须--visual-review-note记录实际看过的图和未验证项，不允许自动编造视觉检查。

渲染检查layout_version=2、main_center_expected/actual、main_canvas_offset及seal_bounds/placement/frame_inside_shape；通用主字误差≤0.5px。完整规则见 [视觉QA](docs/VISUAL-QA.md)，包命令与限制见 [交付规范](docs/DELIVERY-PACKAGES.md)。
