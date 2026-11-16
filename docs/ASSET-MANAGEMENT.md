# 多项目与产品素材管理规范

更新：2026-11-16。本文件管理命名、版本、归属与统计；具体实现及研究来源见 [分层管理与静态页面](HIERARCHY-AND-PAGES.md)。

## 事实来源与层次

| 对象 | 事实来源 | 规则 |
| --- | --- | --- |
| 项目 / 产品 / 共享归属 | organization.json owners | product:<slug>、project:<slug>、shared；不明归属为 unknown，不自动变为 shared |
| 系列 / 合集 | organization.json series | 每系列一个主归属，可容纳不同类型素材 |
| 组件 | organization.json components | 应用标识、导航、播放器等职责；当前每图一个主组件 |
| 功能 / 平台 | 素材 organization.functions / platforms | 多值，用于横向筛选，不再增加目录层级 |
| 文件 | catalog/**/*.json 与 assets/ | 全局唯一 id，一份文件一个记录，SHA-256 去重与校验 |
| 品牌 / 实际使用 | docs/brands、docs/entities | 字体、风格、推荐项、使用方与实际路径；不重复维护逐图哈希 |

主归属、主系列、主组件各一个；跨项目复用通过标签、描述及使用记录关联，不能为统计重复复制同一文件。第三方品牌可登记为产品，但必须注明第三方身份；登记不产生版权授权。不同系列可使用相同组件，组件用于统一检索，不是产品专属实体模型。

## 本地路径

新增由 add 根据结构化字段生成 assets/<kind>/<归属目录>/<series-or-general>/<component>/<id>.<ext> 与 catalog/<归属目录>/<series-or-general>/<component>/<id>.json。产品归属目录为 products/<slug>，项目为 projects/<slug>，公共为 shared。省略空组件；也可用 --folder 指定至多五层英文短横线目录。

保留既有素材路径，避免破坏消费方引用。本次只将原 11 份元数据分入 products/macrightclick/app-icon、shared/editorial-covers、shared/document-symbols、shared/workflow-status；旧素材文件本身不搬动。查找 catalog 必须递归。id 不因路径不同而允许重复。SVG/PNG 等不同格式各有独立 id，不复制相同哈希内容。

## 命名、版本与生命周期

新 id 使用英文小写短横线，可采用 `<owner-type>-<owner-slug>-<family>-<variant>-<revision>-<format>`，例如 product-demo-primary-logo-color-v01-svg。仅示意，不据此虚构真实产品；共享素材可省略 owner-slug。文件路径稳定，中文显示名称与自由标签便于日常查找。

- family:<slug>：设计家族，可跨形状和导出格式；与主系列概念不同。
- variant:<slug>：浅色、深色、圆形等变体；revision:v01：本库设计修订。
- status:draft：已经登记的历史候选；不是 .drafts 私有创作工作区。
- status:ready：满足已记录使用范围；不表示发布或无限制商用。
- status:deprecated / archived：已有替代 / 不再维护，保留文件和引用。

状态标签目前由维护者核对单值，未标注不推测 ready。结构化引用由校验器执行；family、variant、revision 等语义和实际使用关系仍需人工或 AI 核对。organization 为分组权威，不再依赖 owner 标签推导；为兼容旧记录可保留既有 owner 标签，但不能互相冲突。

已使用素材发生图形、文案、裁切变化时新建 id 和 revision。不同格式衍生记录源 asset id。纯元数据纠错不增加设计修订。“当前推荐版本”写入实体/品牌卡，指向明确 id，不以 latest.svg 覆盖。任何已绑定确认哈希的文件变化都需重新展示确认。

## 新增与维护

1. 查已有归属、系列、组件和哈希，优先复用。必要时先登记 organization.json，并按 [实体卡](../templates/entity-record.md) / [品牌档案](../templates/brand-profile.md) 补充视觉约束。
2. 按 [AI 创作协议](AI-CREATION.md)、[个人规范](PERSONAL-STYLE.md) 和平台模板制作；探索阶段不凭文件名猜测归属、许可或作者，未知写 unknown。
3. 草稿在 .drafts；review 后展示准确文件、平台尺寸与必要信息，用户明确满意才 accept / add。不能用测试通过代替确认。
4. 正式收录传入 --owner、--series、--component、重复 --function / --platform，保留真实来源和许可。参数见 CONTRIBUTING.md 与 --help。
5. validate / build，实际查看素材；同步品牌卡推荐项、制作记录及真实 usage。用受管服务 restart 更新页面。
6. 实际接入后记录消费方、asset id、路径或 URL、用途、确认日期；计划使用标“计划”，不计作已使用。

## 统计与公开边界

页面及 dist/organization.json 在构建时自动统计正式文件数、原文件字节数、非空系列、非空产品/项目和非空组件；仅登记但没有素材的实体不计入页面数量。初始化共享示例不算用户新项目。缺少结构化信息的旧素材可读取并显示未分组，不猜测真实关联。

家族、格式分布、权利缺口、复用次数与真实使用覆盖仍使用 [统计快照](../templates/inventory-report.md) 按事实核对；当前没有这些维度的专用自动报表。快照注明日期与口径，不能替代当前文件。历史初始化 8 份 SVG 的数字不代表现有全库；MacRightClick 原始盘点见 [收录快照](inventories/2026-11-16-macrightclick.md)。

所有正式 assets/catalog 都进入构建，状态与筛选不控制公开范围。草稿完全排除。发布前按 RIGHTS.md 核对逐图权利；源仓库开源许可不自动授予图像、品牌商标的再分发权。GitHub 私有源码也不应被视为站点访问控制保证。
