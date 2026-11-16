# 分层素材管理与静态页面

更新：2026-11-16。本文描述已实现行为；云端 Pages 尚未部署。

## 调研与决策

| 一手来源 | 查阅结论 | 本库采用的设计 |
| --- | --- | --- |
| [GitHub Pages 官方说明](https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages) | 托管静态 HTML/CSS/JS，可先构建；项目站点通常带仓库子路径 | 仅发布 dist，所有加载采用相对路径；筛选用 query、详情用 hash，避免刷新嵌套路由 404 |
| [Lucide 的图标元数据](https://raw.githubusercontent.com/lucide-icons/lucide/main/icons/book-open.json) | 标签与类别为不同字段；当前文件存在继承引用 | 目录表达归属与系列，标签表达可交叉检索的语义；不把文件夹当成唯一分类 |
| [Iconify 官方集合登记](https://raw.githubusercontent.com/iconify/icon-sets/master/collections.json) | 集合记录名称、作者、许可、样例及类别等信息 | 系列独立登记；素材自己的来源、作者、许可仍逐项保存，不继承猜测 |
| [Carbon v10 官方筛选模式](https://v10.carbondesignsystem.com/patterns/filtering/) | 多类别筛选、显示已选条件、清除和结果反馈 | 即时组合筛选、条件标签、计数与空态；这是旧版设计参考，不引入 Carbon 依赖 |

以上网页/源码于 2026-11-16 查阅。Lucide/ Iconify 部分说明页访问未成功，使用其官方仓库实际元数据作为证据；不声称覆盖所有图标库或完成用户研究。具体字段、配色与布局是本项目取舍。

## 数据与目录

事实源为根目录 organization.json（归属、系列、组件登记）和递归 catalog/**/*.json（逐图资料）。展示用 dist/organization.json 的计数和样例由构建生成，不手改。

每份素材的 organization 包含：owner（product:<slug> / project:<slug> / shared）、series（单一主系列，可空）、component（单一主组件，可空）、functions 与 platforms（多值）。自由 tags 可交叉描述古风、用途、风格；原 family/variant/revision/status 标签继续兼容。新旧字段重复时结构化 organization 为分组依据；不要写入互相矛盾的归属。

新增归属、系列或组件先编辑 organization.json，系列必须绑定已有归属。校验器拒绝未知引用、系列归属不一致、重复标识和重复功能/平台。旧记录可无 organization，页面落入待整理，不凭名称推测产品。

默认新文件结构：

```text
assets/<kind>/products/<owner-slug>/<series-or-general>/<component>/<id>.<ext>
catalog/products/<owner-slug>/<series-or-general>/<component>/<id>.json
```

项目使用 projects，公共素材使用 shared；无组件时省略该层。id 全库唯一。add --folder 可指定最多 5 层英文短横线目录，不允许越界。物理目录用于维护，不产生额外独立素材；一份文件多处引用不复制。跨产品复用以标签、描述和实体使用记录关联；当前每图仅一个主归属/系列/组件。

本次把 11 份元数据分入 products/macrightclick 与 shared 下 4 个系列，现有 assets 路径及内容均不变，避免破坏引用。新文件才默认使用嵌套路径。8 个初始化 SVG 为共享示例，不虚构成用户新项目。

## 页面

古月藏图采用松墨侧栏、纸白背景和朱砂点缀。左侧按项目/产品→系列进入；主区可切换素材/系列视图，再按类型、组件、功能、平台、状态、自由标签和关键词组合。不同维度是 AND，搜索多个词也为 AND。菜单计数随其他条件更新，当前条件可以逐项移除或全部清空。筛选和详情可复制分享网址；本机地址仅本机可用。

素材卡使用真实正式文件；详情显示来源、权利、哈希和分组，可下载、复制链接/Markdown/仓库路径，SVG 可复制源码。底色有纸白、墨色、透明棋盘。手机有折叠目录。统计只计当前正式文件、非空系列、非空项目/产品与非空组件；候选状态的历史正式文件也计入，.drafts 永不计入。

新增 / AI 制作按钮提供本地操作说明，不是网页上传或远端写入接口。固定字体、古月印章及按准确哈希确认再收录的规则不变。

## Pages 边界

页面是静态的，Python 不需要部署到 Pages。先运行 library.py build，再用已有手动 Pages 工作流上传 dist。不能直接发布 site（缺少生成索引与素材）。没有在线上传、账号、数据库、AI API、浏览器直接写仓库或离线 PWA 安装能力。GitHub 工作流成功和真实网址仍需部署后单独验证。
