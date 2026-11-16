# 个人视觉素材库：调研与项目方案

调研日期：2026-11-16。范围：个人常用 Logo、通用图标、文档/架构图图例、封面；来源优先官方网站和维护者仓库。下列事实与项目决定分开陈述。网页内容和许可会变化，导入时应再次检查具体文件。

## 1. 完善后的需求

核心任务不是收集尽可能多的图，而是让下一次使用更快：**找得到 → 看得清 → 知道能怎么用 → 拿得到 → 下次还能更新。**

- 收藏：保存小而常用的成品，不把搜索结果全部搬入。
- 创建：可编辑 SVG、参数化模板和创作说明；保留源头与生成过程。
- 取用：文件路径、完整 URL、Markdown、原文件下载和 SVG 源码。
- 整理：按用途分类，中文名、英文 id、标签联合搜索，内容哈希去重。
- 积累：来源、许可、作者、日期随文件保存，不依赖某个网站账号才能找回。

第一版面向库主人本地维护、公开或私有 GitHub 版本管理。静态浏览页不承担在线上传、多人审批和权限管理。封面、图例是独立分类，不强制套入 24×24 的图标体系。

## 2. 标杆与来源对比

| 来源 | 一手证据与实际定位 | 适用场景 | 对本项目的决定 |
| --- | --- | --- | --- |
| [Simple Icons](https://github.com/simple-icons/simple-icons) | 品牌 SVG 集合；README 提供文件/CDN/包入口；[免责声明](https://github.com/simple-icons/simple-icons/blob/develop/DISCLAIMER.md) 明确集合 CC0 不代表全部品牌图标都是 CC0 | 技术产品、服务品牌单色图标 | 作为按需查找入口；逐项带来源和品牌规范，不整库搬运 |
| [Lucide](https://github.com/lucide-icons/lucide) | 通用矢量图标，统一设计体系；[许可页](https://lucide.dev/license) 为 ISC，部分源于 Feather 的图标还列出 MIT 声明 | UI、文档、功能图标 | 通用图标首选候选；导入时保留完整归属与许可声明 |
| [Lobe Icons](https://github.com/lobehub/lobe-icons) | 面向 AI/LLM 品牌，提供静态 SVG/PNG/WebP 与组件；仓库标示 MIT | AI Agent、模型服务、AI 架构图 | AI 品牌的重点来源；仍需核对品牌规范和具体内容 |
| [Dashboard Icons](https://github.com/homarr-labs/dashboard-icons) | Dashboard 服务图标与 Logo，SVG/PNG/WebP、CDN；仓库标示 Apache-2.0 | 自托管、服务拓扑、仪表盘 | 学习一致命名与格式分发，不依赖在线 CDN 运行 |
| [selfh.st/icons](https://github.com/selfhst/icons) | 软件服务标识、索引、标签和多格式，仓库标示 CC-BY-4.0 | 自托管服务、文档插图 | 借鉴标签检索与 SVG 优先、多格式按需衍生 |
| [Iconify 源码](https://github.com/iconify/iconify) | 跨图标集的工具体系；本轮其文档站页面访问失败，源码许可文件可访问 | 未来统一前端图标调用 | 现阶段不依赖在线 API；未以本轮未读取的文档为许可或 API 实现依据 |

上述候选库主要覆盖图标和品牌，不直接解决个人封面和私有项目设计归档；因此本项目保留自己的 assets 和 metadata，而非只做某一个图标库的前端。

## 3. 存储与分发决策

[GitHub 大文件文档](https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-large-files-on-github) 说明：常规 Git 超过 50 MiB 提示，超过 100 MiB 阻止；通过网页上传上限 25 MiB；建议仓库尽量低于 1 GB。项目自行采用更保守的 **5 MiB/文件** 上限。这是项目策略，不是 GitHub 限额。

[GitHub Pages 限额](https://docs.github.com/en/pages/getting-started-with-github-pages/github-pages-limits) 包括发布站点最大 1 GB、每月 100 GB 软带宽额度及适用用途限制。个人小型素材预览适合静态发布；它不是无成本无限容量图床。大 PSD/Figma 导出包、视频与素材备份应另放设计源文件存储、Release 或对象存储，本期不自动配置 LFS。

[jsDelivr 官方文档](https://www.jsdelivr.com/documentation) 本轮页面正文动态加载，缓存细节未完整抓取；因此不据此声称缓存时效或可用性保证。项目初期以本地文件和 Pages 同源路径为主，未来外部引用使用固定 commit/tag，避免把可变 main 当作可复现版本。

## 4. 模型与命名

- `assets/<kind>/<slug>.<ext>`：小写英文、短横线；已使用的路径保持稳定。
- `catalog/<id>.json`：一份文件对应一条记录，避免单个大 JSON 的合并冲突。
- 必填：id、name、kind、path、tags、source、license、author、created、description、sha256。
- 未知信息写 `unknown`；没有 license 数据不代表无约束。
- 变体暂用独立 id + 公共标签；将来素材规模上来后再增加 family、variants、dimensions 和衍生链。
- 内容哈希去重避免同一个文件被换名重复导入。它不能识别不同压缩/重新导出的视觉近似重复。

格式策略：SVG 为可编辑矢量优先格式；PNG 用于透明位图，WebP/JPG 适合封面。只存实际使用的格式，当前没有自动 PNG 导出管线。SVG 的 viewBox 与根元素规范可参考 [W3C SVG 结构规范](https://www.w3.org/TR/SVG2/struct.html)。

## 5. 技术选择与取舍

| 方案 | 适用性 | 本轮结论 |
| --- | --- | --- |
| 仅文件夹 + README | 容易开始，检索和批量预览弱 | 保留文件优先理念，补静态目录与工具 |
| React/Vite + 资源后台 | 可扩展强，但引入安装、构建和状态维护 | 第一版不需要这一复杂度 |
| Python 标准库 + 原生前端 + JSON | 零第三方运行依赖，可离线校验，静态部署直接 | 本轮采用；前端为现代浏览器 |
| 数据库/对象存储/鉴权服务 | 适合大规模与多人在线编辑 | 等出现实际需求再引入 |

脚本的 SVG 策略是限制导入子集，不是通用安全清洗器。页面用 img 加载文件，不把收藏 SVG 注入 DOM。项目不处理任意上传和多租户不可信内容。

## 6. 当前交付与后续节奏

本轮：本地 Git、规范与研究、8 份原创几何 SVG 示例、静态搜索与详情、导入与模板创建、基础校验与测试、CI、手动 Pages 工作流。示例未套用第三方品牌；作者与开放许可尚待库主人决定。

建议后续顺序：

1. 确认 GitHub 账户/仓库名与公开范围、代码许可与原创署名；建立远端。
2. 按实际使用清单精选首批 20～50 份素材（数量为建议目标，不是已经导入）；优先常用 AI/云服务、方案图例和项目封面。
3. 有重复需求时再加入矢量到位图导出、深浅变体分组、主题包/批量打包。
4. 多端频繁维护后再考虑网页拖拽导入、认证和 GitHub PR 写入；不能把静态页提示当成写入成功。
5. 真实模型创建、MCP 搜索服务、外部 CDN 均为候选方向，本轮未接入。

## 7. 证据覆盖

- found：Simple Icons、Lucide、Lobe Icons、Dashboard Icons、selfh.st 官方仓库；GitHub 大文件、Pages 限额与[工作流文档](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages)；W3C SVG 规范。
- found：Context7 的 GitHub Actions 官方文档索引，用于核对 workflow_dispatch 和 token 权限；Pages 配置以官方工作流页面为直接依据。
- partial：jsDelivr 文档页面可访问但主体未完整加载，不用于缓存细节结论。
- unreachable：Iconify 文档站本轮两个页面无法通过浏览工具读取；源码仓库许可可访问。不将访问失败解释为不存在。
- 未进行第三方素材批量下载、CDN 各地区实测、GitHub 远端发布和商标逐项授权核验；这些都不作为已完成交付。
