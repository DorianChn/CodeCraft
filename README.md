# ⚡ CodeCraft

**AI 项目灵感雷达** — 给 Vibe Coding 新手精选的 90 个开源项目。

> 工具装好了，不知道做什么？CodeCraft 帮你找到最适合开工的项目。

🔗 **在线访问**: https://dorianchn.github.io/CodeCraft/

---

## 📥 下载安装

| 方式 | 链接 | 说明 |
|------|------|------|
| 💻 Windows 桌面版 | [下载 CodeCraft.exe](https://github.com/DorianChn/CodeCraft/releases/download/v1.0.1/CodeCraft.exe) | 双击即用，无需安装，36 MB |
| 🌐 网页版 | https://dorianchn.github.io/CodeCraft/ | 浏览器直接打开 |
| 📱 手机版 | 打开网页版 → 浏览器菜单 → 添加到主屏幕 | PWA 离线可用 |

---

## ✨ 功能一览

| 功能 | 说明 |
|------|------|
| 🎯 智能推荐 | 选时间/目标/形式/舒适度，推荐最适合你的 3 个项目 |
| ⭐ 明星项目 | 追踪本周 GitHub 增长最快的开源项目（自动更新） |
| 📋 全部项目 | 90 个项目，按好玩/好用/好搓分类 |
| 🔍 搜索高亮 | 搜索关键词自动高亮匹配内容 |
| 📊 排序筛选 | 按评分/MVP 时间/名称排序 |
| ⭐ 收藏功能 | 收藏感兴趣的项目，下次直接查看 |
| 📋 开工提示词 | 可编辑的提示词，一键复制到 AI 编程工具 |
| 🎨 粒子动画 | Hero 区动态粒子背景 |
| 📱 分享到抖音 | 一键复制分享文案 |
| 💻 桌面应用 | Windows .exe 桌面版 |
| 📲 PWA 支持 | 离线可用，可安装到手机主屏幕 |

---

## 🎯 什么是 Vibe Coding？

用自然语言告诉 AI 你想要什么，AI 帮你写代码。你负责创意和描述，AI 负责实现。

**CodeCraft 的 4 步开工流程：**

1. 💡 **想一个点子** — 从 90 个项目里挑一个感兴趣的
2. 📋 **复制开工提示词** — 一键复制，可自定义编辑
3. 🔨 **开始做** — 粘贴到 Cursor/Codex/Claude Code，跟着 AI 的节奏
4. 🎉 **完成分享** — 做出作品，发给朋友看

---

## 🏗️ 技术栈

- **前端**: 纯 HTML + CSS + JavaScript（单文件，零依赖）
- **托管**: GitHub Pages（免费）
- **存储**: localStorage（收藏数据，浏览器本地）
- **API**: GitHub API（明星项目抓取，免费 60 次/小时）
- **桌面版**: PyWebView + PyInstaller 打包
- **零费用，零维护**

---

## 📂 项目结构

```
CodeCraft/
├── index.html              # 主页面（所有功能在一个文件里）
├── manifest.json           # PWA 配置
├── sw.js                   # Service Worker（离线缓存）
├── icon-192.png            # 应用图标 192x192
├── icon-512.png            # 应用图标 512x512
├── main.py                 # 桌面应用入口（pywebview）
├── README.md               # 本文件
├── .gitignore              # Git 忽略规则
└── scripts/
    └── update_stars.py     # GitHub Trending 自动抓取脚本
```

---

## 🚀 本地运行

```bash
# 方式 1：直接用浏览器打开
start index.html

# 方式 2：起个本地服务器
python -m http.server 8080
# 然后打开 http://localhost:8080

# 方式 3：运行桌面版
pip install pywebview
python main.py
```

---

## 🔄 更新明星项目

明星项目数据通过 `scripts/update_stars.py` 自动从 GitHub 抓取：

```bash
python scripts/update_stars.py
```

脚本会：
1. 从 GitHub API 搜索本周增长最快的仓库
2. 生成 STARS 数组
3. 自动更新 `index.html`

---

## 🛠️ 自定义

### 添加新项目

编辑 `index.html` 中的 `PROJECTS` 数组：

```javascript
{
  id: 91,
  track: "play",        // play=好玩, use=好用, hw=好搓
  name: "项目名称",
  desc: "一句话描述",
  tags: ["标签1", "标签2"],
  score: 85,            // 1-100 评分
  mvp: "1-2天",         // 预估 MVP 时间
  source: "https://github.com/user/repo",
  demo: "https://demo.example.com"
}
```

### 修改推荐算法

编辑 `getRecommendations()` 函数中的评分逻辑。

---

## 📊 数据统计

| 指标 | 数值 |
|------|------|
| 总项目数 | 90 |
| 分类 | 好玩 / 好用 / 好搓 / 明星 |
| 真实 GitHub 链接 | 33+ |
| 文件大小 | ~52 KB |
| 依赖 | 0 |
| API 费用 | ¥0 |

---

## 📝 更新日志

### v2.0 (2026-08-05)
- ⭐ 收藏功能（localStorage 持久化）
- 📊 排序筛选（按评分/MVP 时间/名称）
- 🔍 搜索关键词高亮
- 📋 开工提示词可编辑
- 🎨 粒子动画背景
- 📈 计数动画
- ✨ 渐变光效卡片
- 👥 在线人数氛围
- 🔗 33 个真实 GitHub 源码链接
- 🔄 GitHub Trending 自动抓取脚本

### v1.0.1 (2026-08-04)
- 📱 PWA 支持（离线可用）
- 💻 Windows 桌面应用
- 🎯 智能推荐系统
- ⭐ 明星项目追踪
- 📋 90 个精选项目
- 📱 抖音分享按钮

---

## 📄 License

MIT

---

Made with ❤️ by [山川志](https://github.com/DorianChn)
