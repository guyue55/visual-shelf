# GitHub 与 Pages 发布

更新：2026-11-17。用户已明确授权用gh在guyue55下创建、管理、推送并部署。

- 公开仓库：[guyue55/visual-shelf](https://github.com/guyue55/visual-shelf)
- 线上素材馆：[https://guyue55.github.io/visual-shelf/](https://guyue55.github.io/visual-shelf/)
- 默认分支main，origin为 `git@github.com:guyue55/visual-shelf.git`，本地main跟踪origin/main。
- Pages的build_type=workflow，已启用HTTPS强制；仓库Homepage链接及icons/logos/github-pages/visual-assets主题已设置。

这是公开源仓库，源文件、packages与retired的已提交内容可通过GitHub访问。Pages仅发布dist里的页面、索引与正式素材，不发布工程包、字体源、工具或停用台账。.drafts/.exports/.runtime/dist为本地忽略目录，未推送为源文件。不额外为代码或素材选择开源许可证；公开访问不自动授予开放许可，沿用RIGHTS逐项说明。

## 后续推送与发布

先按AGENTS/RTK完成任务相关检查，再提交和推送。CI在push/PR时运行；Pages保持手动触发，不因本次发布改为自动部署。

```sh
git status --short --branch
git push origin main
gh run list --repo guyue55/visual-shelf --limit 5

# 确认CI通过后手动发布main
gh workflow run pages.yml --repo guyue55/visual-shelf --ref main
gh run list --repo guyue55/visual-shelf --workflow pages.yml --limit 3
# 替换成真实run id
gh run watch <RUN_ID> --repo guyue55/visual-shelf --exit-status

# 读取真实Pages配置
gh api repos/guyue55/visual-shelf/pages --jq '{html_url:.html_url,build_type:.build_type,https_enforced:.https_enforced}'
```

核对workflow的headSha与准备发布的提交一致，等待部署job成功；不能以“已触发”代替“已上线”。网站需要更新后再做HTTP和浏览器检查，不能只看Actions绿灯。

## 构建与权限

Python标准库构建dist，运行时只是HTML/CSS/JS/JSON和素材。站点使用相对资源路径、query筛选和hash详情，兼容/visual-shelf/子路径，不依赖服务端路由。构建为JS/CSS添加内容哈希；索引fetch no-store，防止旧索引混用。

当前工作流使用checkout@v6、setup-python@v6、configure-pages@v5、upload-pages-artifact@v4和deploy-pages@v4。构建job读取源码并跑测试，部署job具有pages:write/id-token:write，在github-pages环境发布dist。用户授权本次发布不意味着后续任意任务都可擅自推送；按当次任务授权判断。

参考：[GitHub Pages自定义工作流](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages)、[Pages REST API](https://docs.github.com/en/rest/pages/pages)、[gh repo create](https://cli.github.com/manual/gh_repo_create)。本次执行证据见 [发布验收](deployments/2026-11-17-github-pages.md)。

## 线上验收与引用

1. 首页、两份JSON、带版本查询串的JS/CSS及全部正式素材能访问，素材SHA与catalog一致。
2. 浏览器检查系列进入、筛选、v04详情与修订、图片实际加载；链接须包含/visual-shelf/，不能指向本机127.0.0.1。
3. 刷新详情仍为当前版本；旧版本已不在当前索引，不能从历史记录取旧图。
4. Pages地址跟随部署更新；需要固定版本时使用commit/tag的仓库原文件链接，或保存到消费项目并记录SHA。

平台安装、Icon Composer、Android monochrome和素材逐项权利不会因为Pages部署成功而自动完成。交付包如需独立Release下载，应另按明确需求发布，不从站点部署推断自动上传ZIP。
