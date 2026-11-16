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
git diff --check
```

## 本地预览

```sh
python3 scripts/library.py build
python3 -m http.server 4173 --bind 127.0.0.1 --directory dist
```

打开 http://127.0.0.1:4173/ 。该命令会持续运行，结束预览时用 Ctrl+C 停止自己启动的服务；不终止不属于当前任务的进程。若端口被占用可换空闲端口。修改源文件后重新 build 并刷新页面。

浏览器按改动检查搜索、分类、空态、详情、复制、下载、深浅背景和窄屏布局；新增素材需实际查看。

## 新增与创建

完整参数和示例见 [CONTRIBUTING.md](CONTRIBUTING.md)，创作需求见 [templates/creation-brief.md](templates/creation-brief.md)。

- `add` 导入文件，`create` 创建 SVG 模板；两者登记后均需 build 才更新预览。
- `create` 当前支持 covers、legends、icons；不提供品牌 Logo 或 AI 模型生成。
- 文件与 `catalog/` 为可维护源，`dist/catalog.json` 为生成索引。
- Schema 供编辑器参考；运行时实际准入规则以 `scripts/library.py` 为准。
- 位图仅检查签名和大小；SVG 是受限白名单，不能宣称通用清洗或完整图像解码验证。

## 发布与历史记录

- 发布方式见 [docs/PUBLISHING.md](docs/PUBLISHING.md)，以实际远端配置和工作流执行结果为准。
- [docs/RESEARCH.md](docs/RESEARCH.md) 是选型背景；[docs/VERIFICATION.md](docs/VERIFICATION.md) 是初始化时的历史验证，不代表此后改动已通过。
- 本手册仅适用于本仓库，不引入其他项目的运行、磁盘迁移或部署约定。
