# MacRightClick 收录与全库统计快照

核对日期：2026-11-16。依据：来源仓库提交 `552effdd3054abcd74dd6dc30e213cd33838da6c`；素材库基于 `3b61efd` 加本次收录变更。此快照为历史结果，后续重新读取实际文件。

## 来源盘点

| 来源文件 | 字节 | SHA-256 | 处理 |
| --- | ---: | --- | --- |
| img/app-icons-q96/img-1-appicon-q96.png | 1655496 | 412ac308bc31dd5ae4aae944f979ff6290c9160077a651640825512c270ac8ef | 原样收录至 logos |
| img/app-icons-q96/img-2-appicon-q96.png | 1362823 | b2c0a629af3dbad2dff081514f84c14207d7191d704f2ff8e663fca238497604 | 原样收录至 logos |
| img/app-icons-q96/img-3-appicon-q96.png | 1367009 | edd55002dca93b97c645e260191757c9a71b007d2458c7a23ff0bc2180562e57 | 原样收录至 logos |
| img/app-icons-q96/preview-q96.png | 453148 | 8efbfb1501718d7281b063214429abee8ffbf6d7c7587dca0ddfb7c2976cc9e9 | 仅记录来源，不重复导入 |
| img/img-1.png | 2677341 | 9abc69f50505457410aa6c959f26658c14bbbd11d28d73e72e0b2fb51efb8c49 | 仅记录来源，不重复导入 |
| img/img-2.png | 2351139 | e3c362b0fe7f3d52817db33bb88ef6e43ab199ee1c772a79865259365db4bb13 | 仅记录来源，不重复导入 |
| img/img-3.png | 2369923 | 5d096f709dc44524c08f20073955879e5386964db24b63e9fad847d40462c682 | 仅记录来源，不重复导入 |

来源共 7 张 PNG：3 张 1254×1254 RGB 原稿，3 张 1024×1024 RGBA 应用候选，1 张 1320×520 RGB 对比拼图。q96 标识与“96 色量化”来自来源 README；本轮未重新运行量化或验证颜色数量。

## 本次收录

- 新增 3 份 PNG，1 个素材家族，1 个产品登记卡；没有独立项目登记卡。
- 主用月夜深蓝与 Resources/AppIcon.png 的 SHA-256 一致；该资源是 README 中英文页及构建脚本输入。
- 新增 ready 1、draft 2；8 份初始化示例仍未标注 owner/family/status。
- 两张候选不会因为进入目录就成为主用，但当前站点不会按 draft 标签隐藏。

## 全库快照

- 文件总数：11；分类：{'icons': 3, 'logos': 3, 'covers': 3, 'legends': 2}。
- 格式：{'.svg': 8, '.png': 3}；原文件总字节：4,388,971。
- MacRightClick 新增原文件字节：4,385,328。
- 已登记产品 1、项目 0；已标注家族 1，未标注 family 文件 8。
- 来源 unknown 文件 0；许可 unknown 文件 3；作者 unknown 文件 11。上述字段不能证明逐图授权均已核验。
- 有源码位置证据的使用记录 3，涉及唯一资产 1、消费产品 1；这是源码使用，不是发行包运行验收。

## 验证范围

已检查 PNG 实际尺寸、透明通道、3 张应用候选视觉、哈希与引用链；来源仓库保持只读，原有未跟踪 .serena/ 保留。未运行原应用构建、ICNS 打包、量化工具、极小尺寸独立验收或公开发布。

## 入库验证结果

- `python3 scripts/library.py validate`：11 份通过；受管预览 restart 构建 11 份并健康运行。
- `python3 -m unittest discover -s tests -v`：16 项通过。服务测试的 HTTP 数量断言改为核对临时副本 catalog 的实际记录数，避免后续新增素材被固定的 8 项断言阻塞。
- 浏览器搜索 macrightclick 返回 3 项；三张图的 naturalWidth 均为 1024 且加载完成；主用详情显示来源、标签、许可和文件路径。
- [检索预览截图](2026-11-16-macrightclick-preview.jpg)。
- 本地文档链接和 git diff --check 已通过。原仓库 HEAD 与 origin/main 跟踪引用均为上述来源提交；未执行 fetch，因此不声称跟踪引用证明远端此刻完全无更新。
