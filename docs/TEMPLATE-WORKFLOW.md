# 喜欢的视觉模板与确认后收录

更新：2026-11-16。用户已明确喜欢水墨浅色 A/B 与月夜深蓝这些视觉方向，希望用于不同产品的 web、封面、Logo、应用图标，并要求满意无误后才收录。此要求是后续制作默认流程。

## 模板是什么

- `templates/visual/styles.json`：三种视觉方向、真实参考 asset id 和本次偏好依据，作为 AI 可读取的模板索引。
- `.drafts/<job>/reference.png`：制作时复制的原图，避免覆盖原件。
- `.drafts/<job>/prompt.md` 和 `task.json`：本次需求、用途建议、参考信息与工作状态。
- 用户已确认的无字底图 A/C 已在 styles.json 登记 approved_background；prepare 会复制为 background.png 并记录哈希，避免每次重新去字去章。浅色 B 的瑕疵底图仍待修。底图 PNG 不冒称可编辑字形图层。
- PNG 的书法字与背景已经合成；局部修改应使用图像编辑工具，复杂字形可重建。准确标题适合单独排版，用户已明确“古月”为个人专属名称，个人作品默认带章；先做无字/无章底图仅为分层步骤，最终按 [个人规范](PERSONAL-STYLE.md) 合成固定字体署名。

原有 MacRightClick 主用款保持原样。本次认可的是视觉方向，不意味着所有新产品必须沿用“右”字、月亮或人物，也不意味着任何衍生稿都自动被接受。

## 日常说法

> 用月夜深蓝做一个应用图标，大字换成“知”，其他尽量保留，先给我看。

> 给产品 X 做一个水墨封面，标题“项目手记”，你先建议布局。

> 这版满意，按这个文件收录到产品 X，标签加“知识管理”。

AI 读取资料后，根据目标给出简短建议并推进草稿；不每次重新询问已知风格。精确文案或归属有歧义时集中补问；尺寸、留白等非关键空白可明示采用默认探索值。

## 用途处理规则

| 用途 | 默认建议 | 入库分类 |
| --- | --- | --- |
| web | 重做横幅布局、留出页面文案区；1600×600 仅是探索预设，确认实际位置后适配 | covers，标签 web |
| 封面 | 16:9、1600×900 探索，标题与标识单独排版，不拉伸圆角源图 | covers |
| Logo | 1:1 探索，复杂山水可建议简化；需要路径时另做矢量终稿 | logos |
| 应用图标 | 1024×1024、透明圆角探索，保留主体比例，额外检查小尺寸 | logos，标签 app-icon |

以上尺寸是项目预设，不是所有平台官方标准。不同用途分别建任务/变体，不把一张图盲目缩放交差。AI 可建议两种布局，但有明确要求时直接按要求推进，不反复要求选方案。

## 形状与字体

新任务默认古月印章，主文案采用固定 MaShanZheng-Regular 真字形；支持圆形、圆角方形、未裁方形、横幅/封面及 PWA 安全区配置。完整使用见 [个人规范](PERSONAL-STYLE.md) 和 [平台规范](PLATFORM-PROFILES.md)。古风是默认方向，不覆盖已有产品明确的品牌规则。

## 实际命令

```sh
python3 scripts/studio.py list
python3 scripts/studio.py prepare --job knowledge-app-v01 \
  --style moonlit-blue --purpose app-icon --text '知' \
  --owner product:knowledge --profile circle-logo --platform generic \
  --instructions '保留月夜氛围，默认带古月章，固定字体排版'
```

prepare 仅复制参考并生成制作建议，**不会自动调用模型或生成新图**。AI 应先查看 reference，使用当次可用图像工具实际编辑，输出放到该任务目录。图像编辑沿用宿主 imagegen 能力，不私自安装或收费接入其他工具。

完成候选后：

```sh
python3 scripts/studio.py review --job knowledge-app-v01 \
  --file /绝对路径/候选.png --tool '实际工具或模型标识' \
  --checks '记录逐字、残影、边缘、背景、尺寸检查结果及未验证项'
```

review 将待确认文件复制为 candidate，记录 SHA-256；AI 必须向用户显示**这份文件**并等待明确满意/准许收录。不能把工具成功、AI 自评“好看”或用户未回复当作批准。

确认后由 AI 使用实际信息运行 accept，参数见 `python3 scripts/studio.py accept --help`。它要求 job、已 review 的 SHA-256、用户原意的确认记录、正式 id/名称、真实 owner、family、variant、revision、描述，可补 tags/license/author。目录内没有默认确认文本可直接复用，AI 不得编造确认。

accept 会拒绝未 review、缺确认、未知归属、改动后的文件、未修改的参考重复入库及重复提交。确认绑定精确字节：改了一个字或重新导出也需重新 review 并确认。`catalog` 保存 approval 记录、源参考和工具信息，不能只把证据留在忽略提交的草稿区。

该机制防止常见误操作，不是带身份认证的审批服务：有本地写权限的人可以修改代码或 JSON。AI 的授权依据仍须来自用户真实消息。

## 原模板命令的新行为

- `library.py create` 改为生成 `.drafts/<id>/template.svg` 和任务记录，不直接写 catalog。之后可以通过 studio review/accept 完成确认后收录。
- `library.py add` 仍是直接收录已批准文件的底层入口，但现在必填 `--approval-note`，记录用户对该准确文件的真实确认；不能用于尚未展示的生成草稿。
- 默认使用 studio 逐步流程，避免从创作直接跳到正式库。已有 11 份历史素材不追溯伪造审批记录。
- 低层 Python 函数供工具与测试调用，不是 AI 绕过用户确认的许可。

## 检查与补信息

AI 先检查准确大字、原文字/印章残影、主体比例、背景拼接、裁切、透明区域、用途尺寸；展示结果时说明有意义的未验证项。用户不满意继续修改同一任务；已接受后再修改则新建任务或修订。

正式收录前补齐：真实产品/项目归属、名称、用途、family/variant/revision 和便于检索的中英文标签。作者、模型或许可未披露时记 unknown，不重复逼用户猜测；说明缺口即可。同步产品登记卡、品牌决策和制作记录，再运行 validate、restart、status 更新预览。

草稿区在 .gitignore 内，不随 build、Git 或 Pages 分发，也不代表有异地备份。正式候选必须在批准时保存入库记录；需要同步未完成任务时单独明确安排私有备份，不把草稿当成已收录资产。

## 当前模板与质量入口

最终已确认样例为阅字v06：主字居中、右下小章；styles.json只引用当前正式id和整套v03。prepare复制已确认无字底图，并带当前样例/章位/参照和包，不继续引用旧章v04/旧套件v02。新制作仍先review展示，用户确认后accept；已授权的本轮整套重导正常执行。

严格按 [视觉QA规范](VISUAL-QA.md) 及review-checklist检查，分别记录自动、实图和设备验证。正文移动后重新看印章关系；“章坐标未变”不能证明效果一致。历史疑问及最终收录见 [最终记录](creation-runs/2026-11-17-v06-final-delivery.md)。
