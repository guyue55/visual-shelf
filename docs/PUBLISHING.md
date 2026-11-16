# GitHub 与 Pages 发布

本地仓库默认分支为 main，建议远端命名 `visual-shelf`。当前没有远端地址，不提供虚构的线上链接。

## 建立远端

先确定仓库归属、公开/私有、原创素材署名与代码许可。在 GitHub 创建空仓库（不添加 README/License），再使用真实地址：

```sh
git remote add origin https://github.com/YOUR_ACCOUNT/visual-shelf.git
git push -u origin main
```

`YOUR_ACCOUNT` 是占位符。若尚未提交，先按 RTK.md 完成本地检查后提交。不要把凭据写入仓库。项目自身尚未选择统一开源许可。

## 发布预览

1. 在 GitHub 仓库 Settings → Pages 将 Source 设置为 GitHub Actions。
2. 打开 Actions → Publish Pages (manual) → Run workflow，选择 main。
3. 从部署结果获取真实网站地址，验证 `/仓库名/` 子路径、所有素材、搜索与下载。
4. 将已验证的在线地址补到 README；在正式页面中复制的素材链接才可供其他人访问。

本项目配好 `configure-pages@v5`、`upload-pages-artifact@v4`、`deploy-pages@v4`。参见 [GitHub 官方自定义 Pages 工作流](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages)。站点不使用根绝对路径，可部署到任意子目录。GitHub 免费方案公共仓库支持 Pages，私有仓库可用性取决于方案，见 [Pages 文档](https://docs.github.com/en/pages/getting-started-with-github-pages/github-pages-limits)。不要假设私有源码意味着站点本身有访问控制。

CI 不会发布，Pages 也不在 push 时自动发布。首次线上部署仍需实际验证，工作流文件存在不代表云端已执行成功。

## 稳定引用

- 仓库内文档使用相对路径，例如 `![完成](assets/icons/check-tile.svg)`。
- 外部项目可下载到自身项目，或引用固定 commit/tag 的远端素材。
- Pages 地址随部署更新，适合希望跟随更新的使用场景；不要当成固定版本归档。
- 发布前根据 RIGHTS.md 核对逐项许可；unknown 素材可用于自己评估，不自动表示具备公开再分发权。

## 构建产物与子路径

这是纯静态站点；Python 只在本地或 CI 构建时运行。必须发布 dist/（包含 index.html、app.js、catalog-model.js、style.css、catalog.json、organization.json、assets/、.nojekyll），不能把 site/ 直接作为完整站点。目录关系和统计来自源文件构建，不依赖在线数据库。query 筛选和 hash 详情分享不要求服务端路由重写。草稿、源字体及工具脚本不进入站点。详见 [调研和实现边界](HIERARCHY-AND-PAGES.md)。
