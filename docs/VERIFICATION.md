# 初始化验证记录

日期：2026-11-16。环境：Python 3.13.7、Node 22.23.4；项目只要求 Python 3.11+。本轮仅在当前 Python 版本运行，未作完整版本矩阵验证。

## 已完成

- `python3 -m unittest discover -s tests -v`：10 项测试通过，含导入/构建/重复拒绝/错误元数据无落盘/哈希变化/孤儿文件/路径越界/符号链接/模板文本转义/SVG 活动内容及文件签名边界。
- `python3 scripts/library.py validate`：8 份素材与元数据通过。
- `python3 scripts/library.py build`：构建 8 份素材到 dist；重复构建通过。
- `node --check site/app.js`：通过。
- `git diff --check`：通过；初次提交前另外检查 staged diff。
- 真实浏览器：8 份 SVG 均加载成功；搜索“封面”返回 3 项；封面详情展示来源/许可/作者/路径；点击复制仓库路径并读回得到 `assets/covers/project-notes.svg`；Logo 分类呈现空态；深浅背景切换和新增说明弹窗通过。
- 手机宽度 390px 检查：双列素材布局，页面滚动宽度 375px，无横向溢出；测试后已复原浏览器尺寸。未覆盖全部机型。
- 截图：[预览](preview.jpg)。

## 尚未验证

- GitHub CI 和 Pages 尚未在远端执行，只有本地对应命令验证。
- 浏览器下载按钮的文件交付、全部复制格式、完整键盘和屏幕阅读器流程未做穷尽检查。
- 复杂 SVG、不同字体环境、所有位图编码、浏览器兼容矩阵尚未实测；位图导入只做签名和大小检查。
- 尚未导入第三方素材，未完成逐项品牌授权核验。

## 2026-11-16：本地服务管理补充验证

新增 `scripts/service.sh` 入口与 Python 标准库生命周期实现，适用于 macOS/Linux。

- `bash -n scripts/service.sh`：通过。
- `python3 -m unittest discover -s tests -v`：16 项通过；其中 6 项新增服务集成测试，覆盖完整生命周期、重复操作、HTTP 索引、无关进程占端口、过期 PID、损坏状态、并发锁及构建失败。
- 素材 validate/build、JS 语法检查和差异检查：通过。
- 当前机器默认 4173 被旧的非受管预览占用，start 明确报错且未终止它；指定 4174 后实际启动、status、restart、logs 和 HTTP 索引读取均通过。
- 受管服务绑定 127.0.0.1，运行状态与日志写入忽略提交的 .runtime/。此处端口仅为验证时的实际状态，不是以后固定运行状态。
- 本轮在 macOS 上实际执行；Linux 测试已加入现有 GitHub CI 命令，但远端 CI 尚未运行。未宣称已验证全部 POSIX 平台、Windows、开机启动或自动故障恢复。
- 未修改前端交互，本轮未重复浏览器视觉测试；HTTP 健康检查和索引读取不代替页面交互验收。

## 2026-11-16：模板制作与确认流程

- 新增 studio prepare/review/accept、三方向模板索引、隔离草稿和文件哈希绑定的确认记录。
- library create 改为只写草稿；add CLI 要求 approval-note；已批准文件发生内容变化且确认哈希未更新时 validate 拒绝。
- 本地全量 27 项测试通过，覆盖确认前拒绝入库、空确认、候选变化、原参考重复、未知归属、重复接受、CLI 草稿隔离与正式文件确认失效等边界；测试确认文本只存在临时测试夹具，不作为真实用户批准。
- 正式库仍是 11 份，validate 通过；新底图均未 accept。PNG 实际查看与不足见 creation-runs 中本轮记录。
- JS 语法、文档链接和差异检查完成；受管服务 restart/status 通过，浏览器“新增素材”弹窗实际展示先制作后确认的说明。
- 图像编辑通过内置 image_gen 实际执行；三张去字候选加一次 B 边缘修复；用户尚未验收，B 外缘仍有问题。未测试完整 web 多尺寸或向量排字路线。
