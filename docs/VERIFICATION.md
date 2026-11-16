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
