# 水墨与月夜底图模板 · 草稿制作记录

> 后续状态更新：用户已在 2026-11-16 明确确认并准许收录。底图 A/C、阅字 Logo A/B 及原 185 文件套件已正式保存；详见 [确认收录记录](2026-11-16-approved-guyue-assets.md)。以下“未确认”等表述仅记录最初制作阶段，浅色 B 瑕疵底图仍待修。


日期：2026-11-16。依据用户明确喜欢三款风格并希望复制为不同用途模板的指令。本轮没有更换 MacRightClick 正式图标，也未将新生成图加入 catalog。

## 制作范围

- 原参考：templates/visual/styles.json 引用的 3 份 MacRightClick 图标；制作前已检查其原图。
- 工作目录：`.drafts/template-ink-light-a/`、`.drafts/template-ink-light-b/`、`.drafts/template-moonlit-blue/`。
- 每个目录保存 reference.png、prompt.md、task.json 和候选。此目录被 Git 忽略，不随网站构建发布；是本机实际工作文件，不是虚构的线上入口。
- 工具：内置 image_gen；后端具体模型标识未披露，记 unknown。
- 目的：去除主体“右”字和“古月”印章，补绘山水/纸纹/云雾，留出后续文案区；尽量保留人物、山水与月亮及圆角透明区域。
- 生成式编辑会改变原图细节，并非无损图层分离；底图仍是 PNG，不是可编辑书法或矢量。

## 实际处理与检查

| 方向 | 输出与检查 | 用户确认 |
| --- | --- | --- |
| 水墨浅色 A | background.png，1254×1254 RGBA；大字和印章已移除，人物山水保留；候选副本为 candidate.png，细节和透明边缘待用户审看 | 未确认，不入库 |
| 水墨浅色 B | 初版外侧有透明碎片，追加一次边缘清理为 background-clean-v02.png；仍有顶部/底部碎片，暂不建议接受；candidate.png 指向第二版 | 未确认，保留待修 |
| 月夜深蓝 | background.png，1254×1254 RGBA；大字和印章已移除，月亮与人物保留，中央云雾为重绘；候选副本为 candidate.png | 未确认，不入库 |

三个候选均已运行 studio review，实际 SHA-256、工具和检查结果保存在对应 task.json；当前状态 awaiting-user 不等于通过验收。review 没有调用 accept。

第一轮实际编辑指令（英文，按每张原图独立调用）：

```text
Edit this supplied square illustrated macOS icon NONDESTRUCTIVELY into a reusable text-free background template. Remove the entire large central calligraphy character 右 and remove the small 古月 seal and its border completely. Inpaint their former areas with a natural continuation of the existing subtle landscape, mist and paper/night texture, keeping the central area visually calm for later typography. Preserve the exact original visual direction, mountain positions, figure, tree, moon if present, colors, frame shape and proportions. Preserve transparent pixels outside the rounded icon silhouette. Do not add any lettering, symbols, seal, new person, new logo or watermarks. This is a background template draft, not a redesign of the original logo. Return one clean high-resolution square image.
```

B 第二轮要求只修复 alpha 外缘、清除主体之外的碎片、不修改内部图形。工具返回后仍未满足干净边缘目标，不能把“编辑调用完成”写成“效果通过”。

## 后续

用户确认某份具体文件满意并允许后，才可收录为 shared 模板家族（或用户指定归属），保存来源、模型/工具、未知许可与确认哈希。不把对风格的认可当作对本次衍生图的批准。web 与封面需按实际用途重构构图；本轮仅制作方形背景探索，不声称已有完整横幅/封面终稿。
