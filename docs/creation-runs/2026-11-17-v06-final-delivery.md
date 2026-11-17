# v06固定古月章正式收录与整套v03

日期：2026-11-17。用户明确确认章字/大小和建议的浅色暗朱红A63A30、月夜亮朱红CF6650，并授权正式收录、统一渲染器/模板/整套、两种交付模式重导和清理替代材料。本轮以此明确授权执行，不重复索要相同效果确认。

## 当前版本与范围

- 独立章：shared-guyue-seal-ink-b-v01-png，源PNG透明笔迹64×114，SHA 5f36bc94e402258a98de0fccf577fbf4fb3c464e784f5c926d3e6c39ceb30f9b；字体名/逐图许可unknown，非纯矢量。
- 浅色阅v06：shared-guyue-yue-circle-light-v06-png，SHA 84f20f1d4f8fd7403daf5c07b1dec5dd4241fb3592656b73fccde14cdb0c51d5。
- 月夜阅v06：shared-guyue-yue-rounded-moonlit-v06-png，SHA 0ed70ade05da6938ffa1facfbf890945ca19f14ea8218ce0ce3d6e942e24f58a，与此前认可月夜候选完全同字节。
- 当前归档yue-surface-kit-v03；独立章增加1份素材，替换旧两图后正式目录16素材/7系列。MacRightClick三张原图和A/C无字底图不属于本次替代清理对象。

## 工程与视觉检查

render-logo主字仍固定马善政真实轮廓；章独立读哈希固定的蒙版，不再用主文字体排古月。配置位于resources/seals/guyue-b/provenance.json。根据明确theme选A63A30/CF6650，不任意识别背景换色。章裁切alpha边界1,1至61,112，按60:111原比例放入对应profile容纳框；完整章框已在源蒙版中，不再另画边框。

布局版本3记录seal_kind/asset_id/sha/color、原尺寸/透明边界、实际章框与容纳框；正文中心独立检查。foreground.svg为正文轮廓+内嵌PNG章，另有seal-source.png、seal-layer.png；不冒称纯矢量。QA独立复算比例、章位/大小、完整形状边界、安全圆、主题色、源与颜色层哈希和SVG内嵌字节/坐标，并保留尺寸、ICO/iconset/ICNS/Android/manifest检查。

AI实际查看两款1024成品、整套圆形/圆角/PWA/Android128px、favicon32px及OG/封面/web大图。未把自动通过当作视觉验收；小章在极小favicon仍弱，默认带章、无章仅备选。两款正文/背景沿用已确认配方；月夜与认可候选字节一致。字体、底图和蒙版各有独立来源与哈希。

## 交付与替代

完整归档保留205个场景输出，比旧185多出每个带章profile的固定章源和颜色层；文件数增加是分层可复用资料，不重复登记为205条素材。只接入不携带这些设计源，默认按surface选最少必要资源；可编辑携带字体/OFL、蒙版及配置、背景、渲染器、QA与实际确认资料，可在macOS离线复现。

被替代v04两图/元数据、旧整套v02、深褐预览、旧studio草稿和所有旧版出口，按先验证新版本再移除的顺序处理；retired只留清单、指纹、来源提交与替代关系，不留旧图片/ZIP作为取用入口。advisories拒绝旧ID再导出；历史查询/记录不是当前素材入口。原始MacRightClick三图、无字底图A/C和新固定章不会误删。

核对每个导出目录、ZIP的清单与逐文件SHA；只接入保留macOS10槽、Android5密度前背景与Web引用尺寸/manifest。旧版导出已被替代，不能继续拿v04或v02包混用。

## 授权与验收边界

确认覆盖已认可章形/大小、明确主题色和本轮统一重导；不编造逐场景/逐设备均由用户目视确认。现代Apple.icon、Android monochrome/旧API回退、真实设备安装、PWA/OG域名与消费工程接入仍未由本轮完成。Git推送与Pages发布不从本轮本地收录推断授权，线上仍需另行发布。

最终统计、导出体积、清理明细和新鲜验证结果见本记录后续验收部分及docs/VERIFICATION.md。

## 最终验收

- 当前16素材/7系列，整套205场景输出、总233文件，包内VERIFY和工程QA通过；包内正文字体/固定章/背景/渲染器离线复现两款PNG均与确认SHA一致，独立于已清理草稿。
- 全量Python78项通过，包含macOS原生渲染；前端模型4项及两份JS语法通过；validate16、build、git diff --check通过。清理后另外运行当前引用/固定章QA回归通过。
- 浏览器实际进入两款v06详情，确认修订/路径/SHA和图片加载；点击下载浅色PNG，下载文件SHA与正式目录一致；进入独立章系列成功。当前页面截图见 [v06素材馆](../evidence/2026-11-17-v06-library.jpg)。
- 旧两图与套件v02实际导出请求被拒绝，.drafts已无候选图入口，.exports只含v03/v06。33个被替代入口共1075文件已清理；准确指纹、源提交及保留对象见retired/2026-11-17-v06-cleanup.json。仅本轮生成并被新包替代的临时重建副本另行清理，不混进历史统计。
- 受管预览本地地址http://127.0.0.1:4174/。曾有一次健康请求超时并记录BrokenPipe，随后status复核为RUNNING；不据此声称长期稳定性已验收。未push、未触发Pages。

| 当前ZIP | 文件数 | MiB |
| --- | ---: | ---: |
| yue-surface-kit-v03-all-install | 48 | 16.36 |
| yue-surface-kit-v03-all-editable | 233 | 51.87 |
| yue-surface-kit-v03-web-install | 20 | 2.24 |
| yue-surface-kit-v03-web-editable | 132 | 26.99 |
| yue-surface-kit-v03-macos-install | 19 | 5.92 |
| yue-surface-kit-v03-android-install | 18 | 0.69 |
| yue-circle-v06-original | 6 | 1.26 |
| yue-rounded-v06-original | 6 | 1.34 |

以上8个导出目录和ZIP都验证完整文件集合、逐项SHA与入口存在；独立JSON证据为docs/evidence/2026-11-17-v06-delivery.json。只接入是日常默认，完整可编辑包用于离线创作/归档，不因已生成而日常总发整包。
