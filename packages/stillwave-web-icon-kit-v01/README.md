# 静澜 Stillwave · 网站图标交付包

> 面向人的速览。AI / 开发者请优先读 [AGENTS.md](AGENTS.md)（完整入口：用途、文件、接入步骤、QA 前置、未验证项）；机器清单见 [kit.json](kit.json)。

## 这是什么

「静澜 Stillwave」助眠冥想网站的「静」字图标场景成品，贴合站点深色青灰极简风格：苹方真实字形 + 青灰涟漪环，不带古月章。主图方案已由用户确认满意并正式收录，本包是它的浏览器 / PWA / iOS 适配成品。

**状态：成品已备好，尚未接入站点**（接入是产品侧决策，需授权）。

## 交付内容

- **浏览器**：`favicon.ico`（16/32/48 多帧）、`favicon-16/32/48.png`
- **iOS**：`apple-touch-icon.png`（180×180）
- **PWA**：`icon-192/512.png`（any）、`maskable-192/512.png`（安全区）
- **矢量**：`stillwave-jing-circle.svg`
- **接入片段**：`head-snippet.html`

## 两个要先用起来的入口

1. [AGENTS.md](AGENTS.md) — AI 拿到本包先读它，即可准确使用，不必再问用户要提示词。
2. [head-snippet.html](head-snippet.html) — 接入时复制 `<link>` 声明到站点 `<head>`，注意保持 `./` 相对路径。

## 一条实测建议

16px 下「静」字会糊成墨点。若更看重浏览器标签里的辨识度，`optional/` 提供青灰涟漪符号版（16/32/48，实测清晰）。它是**可选、默认未启用**——用户已确认的正式方案是字版，换符号版需明确选择。

## 接入前必读

站点 favicon 目前是刻意留空的 `data:,`（为保住"零 404"验收）。接入真实图标属产品侧改版，需：获授权 → 复制文件 → 替换引用 → 装 playwright 后跑 `qa/run_all.py` 确认零 404/零 error。具体契约细节与"哪些 QA 契约不需要改"见 [AGENTS.md §3](AGENTS.md)。本环境未运行站点 browser QA（缺 playwright），不声称已验证。
