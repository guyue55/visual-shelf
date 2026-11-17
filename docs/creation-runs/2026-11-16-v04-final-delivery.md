> 历史记录：文中的旧阅字v04、早期章候选及套件v02已由v06/整套v03替代，原路径不再作为取用入口。当前确认、配色、复现与清理见 [正式交付](2026-11-17-v06-final-delivery.md)。原MacRightClick来源与A/C底图不因此停用。

# 阅字v04正式收录、错误清理与修正整套交付

日期：2026-11-16。用户明确：“更合适，确认无误正式收录，错误的素材、草稿和导出包都处理好，别再混用旧版；同步更新模板引用和文档，重新导出修正后的整套包”，并要求沉淀多维检查经验。

## 最终版本

| 当前正式id | 准确PNG SHA-256 |
| --- | --- |
| shared-guyue-yue-circle-light-v04-png | ae52f8e3773261fd1e4ec3bf56d6471f3ca705170d43f9331b3cf38528f16b56 |
| shared-guyue-yue-rounded-moonlit-v04-png | fc207509de42b75ac6c4005366b1ebcedb14c3c549ad71579e7376cce02babfa |

两份通过studio accept收录，确认原话与准确哈希保存在catalog。正文中心(512,512)，固定马善政字体，古月小章右下，圆形额外内收。原MacRightClick右字为章位比较基准，不是旧阅字。用户已确认v04，不再重复索要收录许可。

styles.json只引用v04样例及yue-surface-kit-v02；通用Logo默认right-lower，其他平台保留各自profile。prepare按目标场景解析章位，不把通用右下章机械套到PWA/Android/favicon等。

## 实际清理

旧两份阅字v02已从assets/catalog移除；v01/v02/v03工作稿、碎片B底图、旧整套及额外副本、旧ZIP与单图导出已删除。第一阶段21个入口共1000文件；完成后又清理7个入口246文件，包含已正式存档的工作副本、旧复现图与旧截图。业务草稿目录已无旧稿，剩余.DS_Store为系统目录信息，不是素材。

retired仅保存旧元数据/任务记录/文件指纹和替代关系，不保留可拿去用的旧图或ZIP；历史已提交字节可从Git恢复。详细逐入口记录见 retired/2026-11-16-v04-cleanup.json。advisories保留旧id禁用与新id指向；原MacRightClick三份来源、8份初始化SVG、无字底图A/C未误删，当前共15份单素材。

## 修正套件

当前正式包 packages/yue-surface-kit-v02。185个场景输出+原清单、AI入口、来源、固定字体/OFL、两款背景/确认样例、离线渲染器、QA规范/清单/报告，共211文件（210内容+package.json）。其中主用rounded-logo与准确确认v04 PNG哈希一致，传统ICNS由该PNG生成。

用户授权重导整套，approval.scope如实记录“准确v04确认+按规则重导的衍生范围”，不冒称用户逐文件或逐设备验收。几何/配方/封装通过，真实设备安装、Icon Composer、Android monochrome、OG真实URL仍按目标工程另验证。

导出副本：.exports/yue-surface-kit-v02-all.zip、yue-surface-kit-v02-web.zip、yue-circle-v04-original.zip。整包和Web子包均带quality-review.json；Web报告来自已校验父套件，子包只要求VERIFY，不错误要求运行依赖全套结构的审核命令。单图包仅交付原文件和元数据，不伪造平台转换。

已用正式包source里的背景/字体/渲染器离线复现圆角月夜，输出哈希与fc2075…babfa完全一致。生成状态快照中的旧工作绝对路径不作为运行依赖。原包v01和旧ZIP已经实际移除，不作为当前下载入口。

## 检查与经验沉淀

见 [视觉QA规范](../VISUAL-QA.md) 与 templates/visual/review-checklist.json，覆盖参照、主字几何/光学、印章、形状/描边、字体、背景、透明/底色、小尺寸、平台、来源、确认与版本。自动检查独立复算实际glyph坐标和完整章框，不只相信passed；拒绝NaN坐标、重叠、旧章位、错误封装或来源漂移。archive强制QA及真实visual-review-note，报告区分机器检查、实际看图与未验证项。

另发现浏览器曾缓存旧索引：服务端新文件不等于页面已取新资源。已加本地Cache-Control:no-store、索引fetch no-store、构建JS/CSS内容哈希；卡片/详情显示修订号。浏览器再次刷新确认详情为v04、图片实际加载成功，下载后核对准确SHA。不能以“刷新过”代替实际URL/哈希验证。

最终素材库截图（历史截图已随v06替代清理，原图可在Git历史追溯）。完整验证结果追加在 docs/VERIFICATION.md。未执行push、Pages发布或目标工程安装。
