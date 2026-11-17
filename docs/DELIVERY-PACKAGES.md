# 确认素材与AI交付包

更新：2026-11-17。当前阅字v06、固定浅色B古月章、整套 **yue-surface-kit-v03**。旧v04和整套v02退出取用；retired只留指纹、确认及替代关系。完整记录见 [本轮正式交付](creation-runs/2026-11-17-v06-final-delivery.md)。

## 默认按用途选择

| 模式 | 参数 | 内容 |
| --- | --- | --- |
| 只接入 | `--mode install`，省略时默认 | 所选场景成品、必要尺寸/槽位/密度、README/AGENTS、来源与准确确认、父QA、所需许可文本、独立VERIFY；无字体/底图/渲染器/设计分层 |
| 可编辑 | `--mode editable` | 所选场景输出、分层/预览/配方及完整source：固定正文字体/OFL、独立章蒙版/配置、背景、确认原图、渲染器与QA规范 |

surface必须指定。用户已给平台直接按需导出，不默认all；缺关键环境只补问平台/工程。只要原图时用asset，不假装具备可编辑工程或自动平台转换。只有明确全平台需求才选all；all+install仍是全平台接入，all+editable才含全部复现资料。

```sh
python3 scripts/packages.py list
python3 scripts/packages.py verify packages/yue-surface-kit-v03
python3 scripts/packages.py export --id yue-surface-kit-v03 --surface web --output .exports/yue-web-install-next
python3 scripts/packages.py export --id yue-surface-kit-v03 --surface web --mode editable --output .exports/yue-web-editable-next
python3 scripts/packages.py export --id yue-surface-kit-v03 --surface macos --surface android --output .exports/yue-native-install-next
python3 scripts/packages.py export --id yue-surface-kit-v03 --surface all --mode editable --output .exports/yue-all-editable-next
python3 scripts/packages.py asset --id shared-guyue-yue-circle-light-v06-png --output .exports/yue-circle-original-next
```

输出必须是.exports下新目录和同名ZIP，拒绝覆盖。package.json记录mode、surfaces、parent_package和准确文件清单；单素材包type=single-asset、mode=install。来源未核实、许可unknown不能补造成自由商用。已确认文件原样打包不重复审批，新图形/章形/配色/文案仍另做草稿确认，用户已明确本轮配色和重导授权正常执行。

## 场景与依赖

- web：favicon SVG/PNG/ICO、Apple Touch、PWA any/maskable、OG和接入片段；保持manifest引用尺寸齐全。
- logo：圆形/圆角/方形成品；整套主主题月夜，浅色确认原图另在可编辑source/approved-examples，不把月夜circle误当浅色原图。
- cover：封面、横幅、OG。
- macos：传统ICNS、PNG及完整10槽iconset，不是现代.icon。
- android：5密度前背景与v26 XML，monochrome/旧API回退由消费项目处理。
- all：上述所有场景，按mode决定是否携带设计源。

install去除重复设计预览和源工程，但不删平台必需槽位/密度来凑小体积。若所选场景缺少清单入口，导出直接拒绝。OG真实域名、base path、manifest产品名和缓存策略须消费工程核对；提供资源不等于安装成功。

## 接手、验证与复现

README→AGENTS→package.json→source-assets.json→quality-review.json，先运行：

```sh
python3 VERIFY.py
# 仅可编辑完整整套、实际含payload/kit.json时再运行：
python3 source/scripts/visual_qa.py payload
```

VERIFY校验文件集合、大小、SHA及清单校验值，不是认证签名。子包父QA只说明来源整套检查范围，不能对缺少全套结构的子包运行整套审核，更不能声称设备验收。

可编辑包中source/background.png为月夜背景，source/backgrounds为A/C，source/approved-examples为两份准确v06。resources/seals/guyue-b/provenance.json给出包内固定章路径和SHA，正文与章分开，章绝非正文书法字体。按包内README在macOS使用source/scripts/render-logo.sh；缺字、字体或章哈希漂移会失败。两款已从包内材料实际复现为同字节，不依赖清理前草稿的绝对路径。

foreground.svg包含正文真实轮廓和内嵌PNG章，不是纯矢量；source章64×114，不能声称无限放大无损。新文案和可见修改须另行展示确认。

## 归档与版本管理

当前整套205场景输出，比旧185多出10个带章profile各自的seal-source.png和seal-layer.png；仍只作为1套包，不重复登记205条catalog。加上原清单、源工程及AI/QA资料，当前233文件，以实际package.json为准。

assets/catalog是当前18份单素材；packages是正式归档；.exports为可重建分发目录/ZIP；.drafts为过程稿；retired只留元数据。后三者和packages均不进入dist/Pages。

新整套先export-kit到.drafts，实际看图，再archive；必须真实--approval和--visual-review-note，layout_version≥3，固定章SHA/主题色/比例/完整边界、安全区、主字几何、尺寸/封装与配方通过visual_qa。不能换id把旧章重新归档。完整确认新版本后，才清理被替代文件和出口；advisories拒绝旧id导出，避免旧包混用。

未验证项如实保留：实际设备安装、现代Apple Icon Composer、Android monochrome/旧API回退、PWA完整安装、OG真实域名接入不由本库自动完成。所有许可分别说明，不从字体OFL推断底图或商标权利。
