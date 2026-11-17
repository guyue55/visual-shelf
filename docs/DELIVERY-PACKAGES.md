# 确认素材与 AI 交付包

更新：2026-11-17。当前已确认范本为阅字v04，当前可用整套为 **yue-surface-kit-v02**。旧包v01与旧错误图片/草稿/ZIP已清理；不能从历史文档取旧路径继续使用。

## 日常协作与确认范围

用户确认合用后正常收录，不重复询问同一准确文件是否满意。未提及交付时，可简短问需要原文件包还是Web/macOS/Android等场景；已明确目标和授权则直接导出。原样打包或挑选已确认场景不重复审批；新文案、形状、图形、字体、印章等可见变化仍要新草稿和展示。

本轮用户明确确认v04，并要求重新导出修正整套，故衍生按已确认规则和各平台profile执行。approval.scope如实说明“准确v04确认+整套修正重导授权”，不编造逐文件/逐设备都经用户目视验收。

## 源与副本

| 位置 | 含义 |
| --- | --- |
| assets/ + catalog/ | 当前正式单素材，15份；每份确认绑定准确SHA |
| packages/yue-surface-kit-v02/ | 当前正式交付源，随本地Git保存 |
| .exports/ | 当前导出目录/ZIP，忽略提交，可从正式包重建 |
| .drafts/ | 新创作过程；本轮已完成/错误工作副本已清理 |
| retired/ | 仅停用元数据、指纹和替代关系，不留旧图/ZIP作为取用入口 |

185个场景输出作为1套包，不制造185条catalog。新包附加QA报告/规范/清单、两款背景与确认原图、固定字体/OFL、原生渲染器及AI接入资料，总计 **211文件**（210内容文件+package.json），以实际清单为准。单catalog文件仍受5MiB约束；交付工程包单独管理。

packages、.exports、retired都不进入dist/Pages。本地归档和导出不表示已上传、发布、安装或获得未核实的版权许可。

## AI 从哪里开始

README.md → AGENTS.md → package.json → source-assets.json → quality-review.json。

```sh
python3 VERIFY.py
python3 source/scripts/visual_qa.py payload
```

第一条适用于所有包，验证完整文件集合、字节大小、SHA与清单校验值；第二条仅适用于包含完整payload/kit.json的可编辑整套，重算工程几何、配方、尺寸与封装。只接入包和场景子包不执行缺少源工程的整套审核。质量报告还记录实际AI看过的图和未验证项；机器检查不能替代光学、背景细节或设备验收。哈希不是身份认证签名，真实授权仍来自用户消息。

payload保持场景输出与生成状态快照；render.json旧绝对工作路径不作为运行依赖。source/background.png为月夜默认背景，source/backgrounds包含A/C；source/approved-examples保存两份已确认v04。可用包内固定字体及渲染器离线修改文案，缺字失败，新设计另行确认。

## 场景选择

- web：favicon SVG/PNG/ICO、触屏、PWA any/maskable、分享图与接入片段。
- logo：圆形/圆角/方形母版；整套默认月夜主题，浅色原图另见source/approved-examples。
- cover：封面、横幅与分享图。
- macos：传统ICNS、10槽iconset和PNG，不是现代.icon。
- android：前背景、5档密度及v26 XML；monochrome/旧API回退另处理。
- all：全部185场景输出和完整接入、复现资料。

默认古月章，无章favicon仅为备选，不因整包认可擅自改默认。manifest只有图标信息；OG域名占位符、base path、产品名与缓存策略须消费工程核对。

## 可执行命令

```sh
python3 scripts/packages.py list
python3 scripts/packages.py verify packages/yue-surface-kit-v02
python3 scripts/packages.py export --id yue-surface-kit-v02 --surface all --mode editable --output .exports/yue-all-next
python3 scripts/packages.py export --id yue-surface-kit-v02 --surface web --surface macos --output .exports/yue-web-macos-next
python3 scripts/packages.py asset --id shared-guyue-yue-circle-light-v04-png --output .exports/yue-circle-next
```

输出目录和同名ZIP必须不存在；next用于避免覆盖。当前已生成yue-surface-kit-v02-all、yue-surface-kit-v02-web及yue-circle-v04-original的目录和ZIP。

单素材包只交付原文件、元数据、AI入口和独立校验，不凭空生成或声称平台转换。缺实际确认的历史素材不能冒充已确认导出。

## 新整套的归档门槛

先export-kit.py在.drafts新目录生成，实际看图并取得相应确认/重导授权，再packages.py archive。必须提供已确认asset/background id、真实--approval与--visual-review-note。每场景布局版本≥2、正文目标中心、字体/背景、章位/完整章框、实际尺寸与封装检查均须通过；不能换id重收旧布局。

依据 [视觉QA规范](VISUAL-QA.md) 覆盖十二个维度，使用passed/failed/not-verified/not-applicable记录；未知来源、许可、模型不能补造。确认完整交付后再清理旧稿，清理指纹与替代记录见retired。旧id仍由advisories阻止导出并指向新版本。

## 体积与按需交付（2026-11-17）

完整包是可复现归档，当前211文件约54.80MiB，ZIP约51.84MiB。按SHA识别完全同字节的多余副本约10.82MiB，其中既有可优化的背景副本，也有平台固定入口/槽名；不直接删文件破坏校验和接入。详见 [实测和取舍](creation-runs/2026-11-17-seal-reference-and-package-size.md)。

日常优先单素材asset包（现有圆形ZIP约1.26MiB）或指定surface子包；明确全平台/离线修改需求再发all。Web子包约26.98MiB，当前仍包含完整source，是可复现开发包，并非最轻运行包。本轮已实现两种模式，见下节；历史Web子包相当于可编辑模式。字体/底图/渲染器不应成为每次仅安装图标的必带项；平台必要槽位、密度、来源、确认和校验不可随意去除。

## 两种模式：默认按需导出（已实现）

| 模式 | 参数 | 内容与用途 |
| --- | --- | --- |
| 只接入 | `--mode install`（省略时默认） | 所选场景的成品入口、必要图标尺寸/资源、README/AGENTS、来源/准确确认、父质量报告、许可文本及独立VERIFY；无字体、底图、渲染器、分层及冗余设计预览 |
| 可编辑 | `--mode editable` | 所选场景原输出/分层/预览/配方，以及完整source字体/OFL、背景、确认例图、渲染器、QA规范；适合离线改字和复现，原生渲染器仍需macOS |

```sh
# 日常Web接入，默认install；目标已明确不再问要不要整套
python3 scripts/packages.py export --id yue-surface-kit-v02 --surface web --output .exports/yue-web-install-next
# 本地继续制作时明确要可编辑
python3 scripts/packages.py export --id yue-surface-kit-v02 --surface web --mode editable --output .exports/yue-web-editable-next
# 可组合平台；不默认all
python3 scripts/packages.py export --id yue-surface-kit-v02 --surface macos --surface android --output .exports/yue-native-install-next
```

必须指定surface。未给目标且影响接入时只补问平台；只需单图仍优先asset原文件包。all是明确请求全平台才用；all + install仍只交付全平台接入资源，all + editable才是完整可复现导出。

install保留Web所有根入口及manifest引用尺寸；logo只带圆形/圆角/方形logo.png，cover只带cover/web/OG成品；macOS保留ICNS、PNG与完整10槽iconset；Android保留五密度前背景和v26 XML。不能为了去重删必要槽位。入口缺失将拒绝导出，输出目录/ZIP仍拒绝覆盖。package.json记录mode、surfaces、parent_package及实际清单；quality-review是父套件工程检查，不冒充本包目标设备验收。

实测当前确认v04：Web install 20文件/ZIP约2.24MiB；Web editable 120文件/约26.98MiB；macOS install 19文件/约5.91MiB；Android install 18文件/约0.68MiB。均核对目录、ZIP逐文件SHA和入口存在；[精确体积记录](evidence/2026-11-17-delivery-modes.json)。这些是已有v04的模式验证包，不包含待确认的浅色B独立章，正式归档字节未改写。

待独立章及两款阅字候选获用户确认后，再更新渲染/QA支持、模板引用和正式新包；不能因为导出模式已实现就提前把候选加入正式包。候选与后续清单见 [本轮制作记录](creation-runs/2026-11-17-independent-seal-preview.md)。
