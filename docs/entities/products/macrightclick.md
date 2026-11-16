# MacRightClick · 产品登记卡

- 类型：product；稳定 slug：macrightclick。
- 名称：MacRightClick；应用名称/别名：RightClickAssistant、右键助手。
- 定位：macOS Finder 右键菜单辅助工具，支持新建文件、文件管理、路径复制、终端/编辑器及实用工具。
- 归属：用户明确称为自己的项目；此声明不用于推断逐图创作者。
- 仓库：https://github.com/guyue55/MacRightClick
- 本次依据：本地提交 `552effdd3054abcd74dd6dc30e213cd33838da6c`，2026-11-16 核对。
- 状态：有维护中的源码及当前图标引用；未在本轮构建或运行原应用。
- 负责人：用户；图像作者 unknown。
- 品牌档案：[macrightclick](../../brands/products/macrightclick.md)。

## 素材家族与推荐项

家族 `macrightclick-app-icon`，主归属 `product:macrightclick`，分类 logos。应用图标是产品识别资产，不归入通用功能 icons。

| 变体 | 当前 asset id | 用途与状态 |
| --- | --- | --- |
| 月夜深蓝 q96 | product-macrightclick-app-icon-moonlit-blue-q96-v01-png | 当前主用，ready（已接入证据，不代表逐图授权已核验） |
| 水墨浅色 A q96 | product-macrightclick-app-icon-ink-light-a-q96-v01-png | draft 候选，不推荐自动替换主用款 |
| 水墨浅色 B q96 | product-macrightclick-app-icon-ink-light-b-q96-v01-png | draft 候选，不推荐自动替换主用款 |

本库 v01 是首次收录修订，不推断为原项目图标版本，也不等于应用版本。三个文件未重新编码或裁切，SHA-256 见 catalog 和 [收录快照](../../inventories/2026-11-16-macrightclick.md)。

## 已证实的使用记录

以下均引用月夜深蓝 asset，确认日期 2026-11-16：

| 消费方 | 使用位置 | 用途 | 状态 |
| --- | --- | --- | --- |
| MacRightClick | Resources/AppIcon.png | 应用图标构建输入，与入库文件哈希一致 | 已接入源码 |
| MacRightClick | README.md 顶部 img | 中文文档 128×128 产品标识，引用 Resources/AppIcon.png | 已接入源码 |
| MacRightClick | README_EN.md 顶部 img | 英文文档 128×128 产品标识，引用 Resources/AppIcon.png | 已接入源码 |

`Scripts/build.sh:180` 起将该 PNG 缩放为 iconset，再通过 iconutil 打包 AppIcon.icns。该构建链路已阅读，未在本轮执行；不能据此证明最新发行包已使用同一字节内容。不额外把生成的每个尺寸重复计为源素材。

本产品不另建同名 project 卡：目前没有独立项目交付实体需求。未来具体发布/活动项目需要时再创建并关联本产品。

## 更新规则与缺口

- 本轮只写本素材库，不改 MacRightClick 源仓库或 Resources/AppIcon.png。
- 原仓库为应用运行与打包的事实源，本库为带来源快照的复用副本；不自动双向同步。
- 原图更新时比较哈希、核对变体，新增本库修订并更新推荐项及使用记录；不覆盖旧快照。
- 封面、字标、单色矢量标记、favicon 尚未登记；需要时按品牌档案创作，不把现有 PNG 冒充矢量。
- 图像生成工具、提示词、生成时间、字体来源及逐图许可待补充，不能从水墨风格或印章推断。
