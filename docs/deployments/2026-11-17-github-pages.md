> 历史记录：文中的旧阅字v04、早期章候选及套件v02已由v06/整套v03替代，原路径不再作为取用入口。当前确认、配色、复现与清理见 [正式交付](../creation-runs/2026-11-17-v06-final-delivery.md)。原MacRightClick来源与A/C底图不因此停用。

# GitHub建仓、推送与Pages首次发布验收

记录与线上核查日期：2026-11-17（Asia/Shanghai）。依据用户明确要求使用gh，在guyue55下创建仓库、管理推送并部署GitHub Pages；继续任务时重新读取云端状态，不以先前触发记录当作完成。

## 已执行

- gh登录账号guyue55；使用gh repo create创建公开仓库guyue55/visual-shelf，将已有本地Git历史推送main，配置origin和跟踪分支。
- 使用Pages REST API创建workflow类型站点，设置仓库Homepage与相关主题；保留现有手动Pages工作流和push/PR自动CI，不改触发策略。
- 仓库 https://github.com/guyue55/visual-shelf ，站点 https://guyue55.github.io/visual-shelf/ ，HTTPS enforced=true。

## 首次验收基线

代码提交：96f26663b7ede1358410b015fe9fdc53eeafc382。

- [CI运行43848596772](https://github.com/guyue55/visual-shelf/actions/runs/43848596772)：success；69项Python测试，9项macOS原生测试在Ubuntu按条件跳过，其余通过；包含Node筛选测试与语法、素材校验和构建。
- [Pages运行43848703310](https://github.com/guyue55/visual-shelf/actions/runs/43848703310)：build/deploy均success，已不是仅有配置或待执行计划。
- HTTP首页200；catalog与organization可读取，15素材/6系列/1产品/6组件。全部15份线上素材下载后SHA-256与目录一致；HTML引用的JS/CSS及相对资源请求全部200。
- IAB实际打开真实HTTPS站点，进入阅字系列、展开圆角月夜详情，修订v04，路径及下载链接保持/visual-shelf/子路径，SHA为fc2075…babfa；切换系列视图成功，已加载图片无损坏。
- 真实站点截图（历史截图已随v06替代清理，原图可在Git历史追溯）。未将本机截图当作线上验收；剪贴板原生桥接内容未作为本次验证依据。

本记录随后以文档提交推送，并对最新main再执行手动Pages发布；首次基线保留便于追溯，后续每次部署的确切headSha和run id以[Actions](https://github.com/guyue55/visual-shelf/actions)为准。网页产物仍只包括站点和正式素材，不包括packages/retired或本地草稿/ZIP。公开源仓库中的已提交工程资料可访问，与Pages产物范围不同。

## 边界

未改全库开源许可证，未知作者/素材许可继续标unknown；公开不是无限制商用授权。原MacRightClick工程未改动，设备安装与平台图标验收没有因静态网页部署而自动完成。后续命令和发布检查见docs/PUBLISHING.md。
