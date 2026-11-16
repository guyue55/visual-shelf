# 古月素材与整套交付 · 明确确认收录

日期：2026-11-16。本记录基于用户本轮真实指令，替代前三轮“尚未确认”的当前状态，保留其历史制作和检查事实。

用户原意：“之前几轮需要我确认才能收录到都满意，你正常收录（A、C 满意、A、B 的效果满意）”；同时明确“185 个文件的草稿包效果也可以”，要求完善包内资料方便 AI 使用。根据之前展示与制作记录，A/C 对应两张底图，A/B 对应两张阅字 Logo v02；没有把两组 B 混淆。

| 展示选择 | 正式 id | 准确候选 SHA-256 |
| --- | --- | --- |
| 底图 A · 水墨浅色 | shared-guyue-background-ink-light-a-v01-png | defcd773dbbfa4043f2fafd0f12d9ebc715e58c98f6675dd69d55b372bb46a03 |
| 底图 C · 月夜深蓝 | shared-guyue-background-moonlit-blue-v01-png | dc959806d8d7ce003d3d121f88f169c668018b434bb7c42d5306d99bffa0736b |
| Logo A · 阅字圆形浅色 v02 | shared-guyue-yue-circle-light-v02-png | cfb2b0aabe4881ae0ac7589df7a2d3f56d4c0499ee81982f7a2f5c5b55740abe |
| Logo B · 阅字圆角月夜 v02 | shared-guyue-yue-rounded-moonlit-v02-png | fd59b0b65e6f03d9cca0ca9244948197cc743ef5bb8da26efb0d2db5439fb7d5 |

实际通过 studio accept 完成：归属 shared（个人可复用，不归为 MacRightClick 官方新素材），系列 guyue-ink-backgrounds / guyue-yue-logos，组件 template-background / personal-identity。逐图 catalog 保存实际确认、原参考、工具、检查和字体配方；文件与 hash 未重新导出。底图按 icons/模板底图分类，字标按 logos 分类。正式单文件从 11 增为 15；原 MacRightClick 工程、图标和路径不变。

浅色 B 无字底图仍有外缘碎片，保留 .drafts/template-ink-light-b awaiting-user，不将 Logo B 的确认套用于它。

## 正式套件

原 .drafts/yue-surface-kit-v01 的 kit.json 清单中 185 个文件逐一核对；原 kit.json 也完整保存。packages/yue-surface-kit-v01 为 1 套正式包，package.json 保存本轮整套确认、原始文件数和全部 185 个原哈希；新增资料后总计 203 个文件，不声称总数仍为 185。

新增 README/AGENTS、独立 VERIFY.py、index.html、来源素材完整 JSON、原背景、固定字体/OFL 及原生渲染器。包内路径可携带，原 render.json 的绝对路径只作为历史证据；复现从 source/ 相对路径读取，不依赖原 .drafts 或已安装字体。包内仍明确底图权利 unknown、具体后端模型 unknown、字体 OFL，以及设备/现代平台未验收范围。

已按原确认导出完整与 Web 子包到 .exports/，目录和 ZIP 可从正式包重建。单素材 asset 命令也可为已确认图例提供原文件交付；不伪造格式适配。未来确认合用后可询问是否要包和用途，明确需要则直接输出，不重复问是否准许收录。新文案/新设计仍需展示确认。

完整入口和命令见 [交付包规范](../DELIVERY-PACKAGES.md)。无章标签依旧只作备选，不由整包确认推断取消古月默认署名。
