# 2026-11-17 静澜 Stillwave「静」字标识制作记录

- 任务：为 https://guyue55.github.io/stillwave/ 生成图标，主字「静」。
- 实体：product:stillwave（本轮首次登记）；家族 stillwave-jing-logo；系列 stillwave-jing-logo；组件 app-identity。
- 需求来源：用户「为这个网站生成图标，这次用 静」，随后对展示候选确认「满意」。
- 风格决定：沿用已确认「月夜深蓝」古风方向与固定马善政字体＋古月章体系（设计选择，非站点官方品牌规范）。站点为深色低刺激青灰声景站，月夜方向气质契合。

## 制作输入

- 无字底图：shared-guyue-background-moonlit-blue-v01-png，SHA `dc959806d8d7ce003d3d121f88f169c668018b434bb7c42d5306d99bffa0736b`。
- 固定字体：MaShanZheng-Regular（provenance SHA 校验通过）。
- 固定章：shared-guyue-seal-ink-b-v01-png，SHA `5f36bc94e402258a98de0fccf577fbf4fb3c464e784f5c926d3e6c39ceb30f9b`；深色亮朱红 `#CF6650`。
- 参考图：product-macrightclick-app-icon-moonlit-blue-q96-v01-png（风格参照，不沿用「右」字或归属）。

## 执行与工具

- `studio.py prepare --job stillwave-jing-v01 --style moonlit-blue --purpose app-icon --text 静 --owner product:stillwave --profile rounded-logo --platform generic`。
- 渲染：`scripts/render-logo.sh --background <草稿>/background.png --text 静 --profile rounded-logo --theme dark --output <草稿>/candidate-a`（Swift 6.3.3 / CoreText / CoreGraphics）。
- 工具结合固定字体真实轮廓与固定章蒙版，主字非模型生成；未调用图像生成模型。

## 候选与验证

- 唯一候选 `.drafts/stillwave-jing-v01/candidate-a/logo.png`，review 后待确认文件 `candidate.png`，SHA `9516b1e2b3eab107eb2f05048f3f6b349ade26ceb8e78e63f3576e2dfb76f18c`。
- 几何：layout_version=3；主字实际轮廓中心 (512,512) = 画布中心，零误差；main_canvas_offset=(0,0)；章框完整落在圆角形状内且未与主字重叠。
- 哈希：PNG / foreground.svg / 字体 / 底图 / 章源与配方和已确认来源一致；字体名 MaShanZheng-Regular；章为 fixed-alpha-mask、未伪装成字体字形。
- 实图：已查看 1024 大图——「静」字清晰、米白字＋月夜山水、右下亮朱红古月章清楚且不压主体、圆角外透明完整；已查看 48px 预览——主字仍可辨，印章变弱属小尺寸预期。
- 未验证：真实设备图标渲染、浏览器深浅底实际叠加、站点是否接入及目标平台正式规格。

## 确认与收录

- 用户 2026-11-17 回复「满意」，明确允许收录。
- `studio.py accept` 收录为 `product-stillwave-jing-logo-rounded-moonlit-v01-png`；approval 绑定上述 SHA 与用户原意。
- 同轮补齐 organization.json 归属/系列登记、产品登记卡、品牌档案；validate / build / 预览重启结果见本轮任务交付说明。
- 交付包尚未导出；用户需要时按场景（Web / PWA / Apple Touch / Android / favicon）单独生成，不默认整套。
