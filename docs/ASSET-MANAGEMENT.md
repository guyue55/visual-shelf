# 多项目与产品素材管理规范

更新日期：2026-11-16。本文是项目/产品归属、命名、版本与统计口径的规范入口。当前可使用现有标签和 Markdown 登记卡执行人工管理；结构化实体模型、自动报表和管理界面属于后续实现。

## 1. 管理层次与归属

| 对象 | 含义 | 标识约定 |
| --- | --- | --- |
| 项目 project | 有范围和交付目标的工作，可使用多个产品的素材 | 稳定英文 slug，例如 `demo-launch` |
| 产品 product | 有独立名称或品牌的产品/服务，可被多个项目使用 | 稳定英文 slug，例如 `demo-suite` |
| 素材家族 family | 同一设计意图的一组素材，例如一个产品的主 Logo | `demo-suite-primary-logo` |
| 文件 asset | 一个具体版本、变体与格式的可引用文件 | 全局唯一 id，对应一份 catalog JSON |
| 使用记录 usage | 某项目、产品或文档在某位置使用某素材 | 消费方 + 素材 id + 位置 + 确认日期 |

以上 demo 名称均为示意，不代表已经登记了真实项目或产品。项目与产品关系允许多对多，不把某一方固定塞到另一方目录下面。

每个家族只有一个主要归属：`project:<slug>`、`product:<slug>` 或 `shared`。归属不等于版权拥有者，也不等于使用方。例如：产品 Logo 归属产品家族，在另一个项目的 README 使用时只增加使用记录，不复制素材、不改变归属。跨项目通用的图例可归入 shared。

归属不确定填 `unknown` 并进入待整理清单；不能把没有归属的数据自动算成 shared。第三方品牌也可以登记为 product，注明第三方身份；登记不代表拥有其版权。真实业务名称未知时不由 AI 猜测。

## 2. 文件结构与登记卡

沿用当前校验器支持的三段路径，不新增项目/产品子目录：

```text
assets/logos/<asset-id>.svg
assets/covers/<asset-id>.webp
assets/icons/<asset-id>.svg
assets/legends/<asset-id>.svg
catalog/<asset-id>.json
```

新增实体时再按模板创建以下 Markdown 登记卡，无需提前创建空目录或虚构项目：

```text
docs/entities/projects/<slug>.md
docs/entities/products/<slug>.md
```

登记卡使用 [实体模板](../templates/entity-record.md)。它保存实体名称/别名、项目与产品关系、家族归属、默认推荐素材、引用位置和管理状态；素材文件的名称、分类、来源、许可、日期、哈希仍以 catalog 为准，不在卡中重复维护。

同一个产品和项目不得仅因中文名相同而合并；二者可以拥有相同 slug，但通过 `project:` / `product:` 类型区分。文件 id 前缀必须包含归属类型，避免冲突。中文改名只更新显示名称与别名，不改稳定 slug；确需迁移时保留旧新对应关系并核对引用。

共享家族可在实际产生时建立 `docs/entities/shared.md` 登记。主归属卡维护家族信息，消费方卡只维护使用记录，避免多处修改同一事实。

## 3. 命名、家族与变体

新素材 id 推荐格式：

```text
<owner-type>-<owner-slug>-<purpose>-<variant>-v<revision>-<format>
product-demo-suite-primary-logo-color-v01-svg
product-demo-suite-primary-logo-white-v01-svg
product-demo-suite-primary-logo-color-v01-png
project-demo-launch-readme-cover-16x9-v01-webp
shared-status-ready-green-v01-svg
```

shared 没有 owner-slug。扩展名仍正常保留，例如 `assets/logos/product-demo-suite-primary-logo-color-v01-svg.svg`。末尾格式名用于确保同一设计的 SVG 与 PNG 拥有不同全局 id；这是命名约定，不是当前程序自动生成的规则。

- `purpose`：`primary-logo`、`wordmark`、`readme-cover`、`article-cover`、`status-ready` 等真实用途。
- `variant`：颜色、深浅适配、横竖版、比例、语言或尺寸；多个维度按固定顺序“版式 → 配色 → 比例 → 语言 → 尺寸”串接，省略无关维度。例如 `horizontal-white-zh-cn`。
- `white` 表示白色图形，不把它命名成语义不清的 `dark`；适用背景在登记卡中说明。
- `revision`：设计修订从 v01 开始，新增修订递增；格式转换不自动增加设计修订。
- 一个家族可含多个变体；一个变体可含多种格式，每个文件独立登记。同内容不因使用方不同而重复导入。
- 初始 8 份示例保持原 id 与路径，不为符合新格式批量重命名；先登记实际归属再补管理标签。

## 4. 当前可执行的标签规则

目前 `add/create` 无实体、家族、版本或状态专属参数。使用现有 `--tags` 记录以下约定，不新增未经实现的 JSON 字段或虚构 CLI 参数：

| 标签 | 数量 | 用途 |
| --- | --- | --- |
| `owner:product:<slug>` / `owner:project:<slug>` / `owner:shared` / `owner:unknown` | 恰好一个 | 主要归属 |
| `family:<family-id>` | 一个 | 家族聚合 |
| `variant:<variant-id>` | 一个 | 变体聚合 |
| `revision:v01` | 一个 | 设计修订 |
| `status:draft` / `status:ready` / `status:deprecated` / `status:archived` | 恰好一个 | 工作状态 |
| `project:<slug>`、`product:<slug>` | 可多个 | 已确认的关联或使用方，不能代替主要归属 |
| 中文用途标签 | 按需 | 日常搜索，如“官网、封面、发布” |

现有验证器只检查 tags 是非空字符串数组，不检查上述数量、引用存在性或值域；当前由人或 AI 在任务中核对。网页可搜索完整标签，也能用空格组合条件，但没有独立项目筛选器、精确标签查询或状态隐藏逻辑。

使用现有参数的示例（demo 为占位符，需替换成真实登记信息）：

```sh
python3 scripts/library.py add /绝对路径/logo.svg \
  --id product-demo-suite-primary-logo-color-v01-svg \
  --name "演示产品 · 主 Logo · 彩色" --kind logos \
  --tags "owner:product:demo-suite,family:demo-suite-primary-logo,variant:color,revision:v01,status:draft,product:demo-suite,品牌" \
  --source unknown --license unknown --author unknown \
  --description "来源、适用背景、品牌规范与具体限制待核实"
```

不要仅为凑齐信息填入示例产品。既有无管理标签的素材保留原样，统计为“未标注”，不推断状态、家族和归属。

## 5. 生命周期与版本

- draft：正在创作、核对或整理。预览通过不自动等于 ready。
- ready：经过视觉检查、用途与来源核对，满足已记录的使用范围；不表示对外发布或无限制商用。权利待确认时仍明确记录，不能擅自标成可公开再分发。
- deprecated：已有替代版本，不推荐新用途；记录替代 asset id，保留旧引用。
- archived：不再维护，仍保留历史文件与引用证据。

当前所有进入 assets/catalog 的素材都会出现在构建站点，状态标签不会控制公开范围。需要保密或不能随站点分发的草稿不得导入本库分发目录，应在用户指定的私有工作位置创作；公开前按 RIGHTS.md 核对。

已对外使用的素材发生可见图形、文字或裁切变化时新增 revision 和 id，保留旧文件；格式衍生增加文件记录并标明源 asset id。纯元数据纠错不增加设计修订。未被使用的草稿可原路径修改，但仍更新哈希并校验。

“当前推荐版本”由归属登记卡按用途/变体指向明确 asset id，不通过重命名文件成 latest 或 latest.svg 实现。修订、新增文件和真实使用关系变化时同步更新卡片；项目归档不应把被其他项目使用的产品素材一起归档。

## 6. 新增与维护流程

1. 查找是否已有实体、家族或相同素材；先复用，不因新项目复制品牌标识。
2. 确认主要归属、用途和适用背景；首次实体使用模板建卡。记录真实项目/产品关联。
3. 决定新家族、变体、修订或格式衍生，按规范命名，并记录创作过程。
4. 用现有 add/create 登记文件，补标签与卡片中的家族/推荐项；AI 不根据文件名猜测来源和权利。
5. 执行 validate/build，实际查看素材；工具只验证文件部分，人工核对关系、标签和引用。
6. 在真实接入后记录 usage：消费方、asset id、路径或 URL、用途、确认日期。计划使用须标“计划”，不计入已使用统计。
7. 生成或更新统计快照，注明时间、范围和缺口；只对当前任务相关资料更新，不顺手改造历史素材。

## 7. 统计口径

当前没有自动报表命令，先用 [统计快照模板](../templates/inventory-report.md) 根据 catalog、文件和登记卡人工核对。快照是历史结果，不能作为新的权威台账，也不要手工维护一个永远不更新的 README 总数。

| 指标 | 口径与注意事项 |
| --- | --- |
| 文件数 | 一条有效 catalog 记录算一份；SVG 与 PNG 分开计数，须与文件对应 |
| 家族数 | 去重 family 标签；没有标签单列“未标注”，不按名称猜测 |
| 项目数 / 产品数 | 按有效实体登记卡分别去重；没有登记卡不算已登记实体，标签无对应卡列为缺口 |
| 分类 / 格式分布 | 按 kind / 文件扩展名统计，分组总和应等于文件总数 |
| 主归属分布 | 每文件仅归入一个 owner；缺失或多值分别列出，不自动归到 shared |
| 状态分布 | 每文件仅一个 status；缺失或冲突单列，不默认 ready |
| 存储占用 | 求和 catalog 指向原文件的字节数；不含 dist 副本、Git 历史、设计工程与文档 |
| 来源 / 权利完整度 | 分别统计 source unknown、license unknown、author unknown；三项可能重叠，不相加当文件总数。非 unknown 只表示填了信息，不表示授权已核验 |
| 复用 | usage 中“已接入”且有位置证据的关系；同一消费方 + asset id + 同一位置去重。多个位置可多次使用，不能与唯一文件数混淆 |
| 归档与替代 | 状态数量、失效推荐 id、缺失替代 id、待核实引用分别列出 |

快照记录生成日期、统计所依据的提交与未提交变更、样本范围及未知项。每次涉及实体/版本/使用关系的变更重新核对相关登记卡；集中整理或交付前做全库快照。普通文案修改无需生成统计。

### 当前基线（2026-11-16 核对）

- catalog 文件记录 8 份：logos 0、icons 3、legends 2、covers 3；格式全部 SVG。
- catalog 对应原文件共 3,643 bytes；不含构建产物等其他文件。
- 8 份均是初始化示例，source 为 original；author 均为 unknown；许可均标为 LicenseRef-All-Rights-Reserved。
- 8 份均未标注本规范的 owner/family/status 标签，不自动归到 shared 或 ready。
- 尚无实体登记卡和使用记录。已登记项目/产品数为 0；真实使用数量未知，不能用“没有记录”断言从未使用。

该段仅为本次文档规划时的快照。后续统计应重新读取真实文件，不在多份文档重复维护数字。

## 8. 后续实现顺序与验收

| 阶段 | 工作与验收 |
| --- | --- |
| 当前文档约定 | 标签、登记卡、命名和手动统计流程可执行；不迁移旧路径 |
| 结构化登记 | 实现实体/家族/使用关系 schema 与 CLI，校验归属唯一、关联存在、变体修订与替代引用；从标签/卡片一次性迁移并停止维护重复事实源 |
| 自动统计 | 输出分组文件数、家族数、实体数、原文件字节、来源/权利缺口及关系异常；与人工样本对照，确定排序、时间和去重规则 |
| 管理页面 | 实现项目/产品筛选、家族/版本详情、推荐素材与统计页；浏览器验证空态、未知项和查询组合 |
| 按需扩展 | 实际需要时再接入格式转换、批量导入、AI 创建和外部设计源文件存储 |

本次仅更新文档与模板，不修改脚本、Schema、素材元数据或网站，不声称上述后续能力已经实现。
