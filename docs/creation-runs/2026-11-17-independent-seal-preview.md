> 历史记录：文中的旧阅字v04、早期章候选及套件v02已由v06/整套v03替代，原路径不再作为取用入口。当前确认、配色、复现与清理见 [正式交付](2026-11-17-v06-final-delivery.md)。原MacRightClick来源与A/C底图不因此停用。

# 浅色B独立古月章候选与交付模式

日期：2026-11-17。用户授权：按浅色B原章制作固定独立章，先在两款阅字上对比，满意后才更新模板和正式导出包；同时实现只接入/可编辑、默认按需导出。

## 当前状态

已制作独立章和两款对照，三个studio任务均为 **awaiting-user**，没有accept。正式15素材、模板styles/profiles、render-logo默认章及packages/yue-surface-kit-v02的内容均保持原版。导出模式代码已经实现，模式验证包复用原已确认v04，不能误认为新章已归档。

## 参照、方法与失败经验

准确参照：`product-macrightclick-app-icon-ink-light-b-q96-v01-png`，SHA `b2c0a629af3dbad2dff081514f84c14207d7191d704f2ff8e663fca238497604`。与原MacRightClick `img/app-icons-q96/img-2-appicon-q96.png`一致，前轮已复核。本次再次实际查看原图。

先用imagegen两次尝试透明提取，提示要求保留原笔迹、边框和古/月字形：第一次出现晕边，第二次仍改了笔形，均未采用。失败图和生成结果不能作为印章母版。后改为原像素亮度蒙版提取：原图左上坐标裁切x776,y721,w64,h114；alpha=clamp((145-meanRGB)/55)，墨色#463A33。没有生成新笔画，没有猜字体。已把具体来源SHA校验、固定区域和算法固化到scripts/extract_seal_b.swift，同源重复执行哈希一致。

这是一份 **64×114透明位图印章**，保留原小图笔迹和框线纹理，字体名及逐图许可为unknown。纸纹/山水通过蒙版分离，边缘有阈值取舍，不能宣称与原图笔迹每个像素无损相同；也不冒称纯矢量、原字体工程或无限放大母版。大尺寸印刷/放大仍需更高清原章或另外展示确认的矢量重建。

## 准确候选

| 对象 | studio任务与候选 | SHA-256 |
| --- | --- | --- |
| 独立章 | `.drafts/guyue-seal-b-master-v01/candidate.png` | `5f36bc94e402258a98de0fccf577fbf4fb3c464e784f5c926d3e6c39ceb30f9b` |
| 圆形水墨阅 | `.drafts/yue-seal-b-light-v05/candidate.png` | `6e60f3ea3664804207beb85d82ca56a0ea80a15dbcc6f1a245635eed36e873ec` |
| 圆角月夜阅 | `.drafts/yue-seal-b-dark-v05/candidate.png` | `0ed70ade05da6938ffa1facfbf890945ca19f14ea8218ce0ce3d6e942e24f58a` |

合成工作目录：`.drafts/guyue-seal-b-v01/`。`comparison.png`左列为当前v04，右列为候选；`seal.json`记录源、算法、章SHA及两图SHA；light/dark的preview.json记录章范围、比例、颜色与章区外像素比对。候选图仅保存在.drafts，不加入正式catalog或Pages。

正文和背景先使用原固定字体/背景配方生成无章中间层（--no-seal仅用于分层，不改变个人默认带章偏好）；scripts/preview_seal.swift再合成固定章蒙版。圆形沿用x82.5%、圆角x85%，容纳框y27.5%、宽6.5%、高14.5%（CoreGraphics y向上），章按原比例居于该框内，不拉成长条。浅色用原章深褐#463A33，月夜沿用当前朱红#CF6650，保证与深背景对比。因原章长宽比不同，实际章高度比当前章短，这是等比适配而非字体变形。

两款主字中心仍为(512,512)。逐像素核对：旧/新章容纳框外差异为0，证明主字和背景未被误改；两款使用同一章SHA。实际查看独立章、两份1024成品、128px缩略图及对照；小章在极小显示尺寸下仍弱，不冒充各设备已验收。精确记录见 [候选证据](../evidence/2026-11-17-independent-seal-review.json)。

## 复现入口

```sh
swift scripts/extract_seal_b.swift assets/logos/product-macrightclick-app-icon-ink-light-b-q96-v01-png.png .drafts/<新任务>/seal.png
# base为原render-logo配方--no-seal输出；approved为对应当前v04原文件
swift scripts/preview_seal.swift --base .drafts/<新任务>/base/logo.png \
  --approved assets/logos/shared/guyue-yue-logos/personal-identity/shared-guyue-yue-circle-light-v04-png.png \
  --seal .drafts/<新任务>/seal.png --x 0.825 --y 0.275 --width 0.065 --height 0.145 \
  --color 463A33 --output .drafts/<新任务>/preview
```

仅macOS/Swift；输出必须为.drafts新文件/目录，拒绝覆盖；源图SHA不符、非透明章、非法坐标或章区之外发生变化会拒绝。它是独立预览工具，不绕过正式渲染/工程QA的归档门槛。

## 用户确认后的执行清单

1. 绑定上述准确章及两款候选的实际确认；若有修改则新候选、新SHA重新review。
2. 将独立章作为单独有来源/版本/确认的资源正式收录，正文与章分开管理；把原像素章及复现算法一起保存，不能改成每次调用模型重画。
3. 扩展正式渲染器与visual_qa处理固定透明章、章SHA、含框边界、平台安全区和foreground分层；不能把蒙版冒充马善政字形或直接绕过旧glyph校验。
4. 更新模板引用后，按场景实际看图、生成新的整套版本并验证；只接入和可编辑按目标分别导出，保留真实确认范围。不把“两款满意”编成逐设备验收。
5. 完成新版本验证后，再按用户明确范围处理被替代文件和出口，避免混用；当前不提前清理仍有效的v04。

## 已实现的交付模式

export新增--mode install/editable，默认install；surface仍须明确。install只带平台成品和必要资源/说明/来源/确认/父QA/许可/VERIFY；editable保留源工程、分层、多尺寸预览和复现资料。asset原文件包标记mode=install，仍不假装可编辑。

实测Web只接入20文件、ZIP2,351,736字节（约2.24MiB）；可编辑120文件、28,286,564字节（约26.98MiB）。macOS只接入19文件、约5.91MiB；Android只接入18文件、约0.68MiB。目录VERIFY、ZIP逐文件SHA、清单入口均实际核对通过；macOS保留10槽iconset，Android保留5密度前背景，Web保留manifest和引用图标，未做设备安装。完整数据见 [交付模式实测](../evidence/2026-11-17-delivery-modes.json)，命令见 [交付规范](../DELIVERY-PACKAGES.md)。

这四个模式验证包位于.exports/yue-v04-{web-install,web-editable,macos-install,android-install}，不含待确认章，不修改父归档。仅清理本轮被替代的临时模式验证出口；历史确认包和其他导出未误删。
