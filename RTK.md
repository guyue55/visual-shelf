# 我的图标 · Repository Task Kit

## 项目定位

个人视觉素材库，管理 logos、icons、legends、covers。仓库文件是唯一事实来源，静态网站是生成的消费入口。

## 开发入口

- Python 3.11+ 标准库；前端原生 HTML/CSS/JS；没有必须安装的依赖。
- `python3 scripts/library.py validate`：元数据、哈希、路径、重复内容、SVG 静态子集校验。
- `python3 -m unittest discover -s tests -v`：导入与构建边界测试。
- `python3 scripts/library.py build`：输出到 `dist/`。
- `python3 -m http.server 4173 --bind 127.0.0.1 --directory dist`：本地预览。
- `node --check site/app.js` 和 `git diff --check`：提交前检查。

## 维护约定

- 先读 README、CONTRIBUTING、docs/RESEARCH.md；核对真实素材和元数据。
- 每个素材一个 `catalog/<id>.json`；文件路径稳定，使用英文小写短横线。
- 来源、许可、作者不确定时用 `unknown`；不把集合许可推断为品牌商标许可。
- 示例素材为初始化时生成的参数化 SVG，不冒充真实品牌 Logo。
- 原始设计工程和大文件不混入分发目录；单文件最大 5 MiB。
- 不盲目优化品牌路径；不内联导入的 SVG。SVG 使用明确的静态白名单，复杂内容需人工清理。
- 未获得明确授权，不创建远端仓库、不 push、不发布；Pages 工作流只允许手动触发。
- 只修改当前任务相关文件，保留他人改动。中文提交说明，例如 `feat(library): 初始化个人视觉素材库`。
- 不要将别的仓库的 RTK.md 当作本项目规则。上层磁盘迁移手册只在实际执行迁移时适用。
