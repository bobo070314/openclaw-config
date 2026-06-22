# 🧠 gbrain Full-Stack Scaffold

> gbrain 全栈脚手架 — 知识库驱动的微信小程序 + Web 管理后台 + REST API

## 项目结构

```
fullstack/
├── server/          # Express 后端 (port 3001)
│   ├── index.js     # 入口文件
│   ├── config.js    # 配置
│   ├── routes/
│   │   └── api.js   # REST API 路由
│   └── models/
│       └── index.js # 数据模型
├── miniapp/         # 微信小程序
│   ├── app.js       # 小程序入口
│   ├── app.json     # 全局配置
│   ├── pages/
│   │   ├── index/   # 首页：知识库列表 + 搜索
│   │   └── detail/  # 文档详情页
│   └── utils/
│       └── api.js   # API 封装
├── web/             # Web 管理后台
│   ├── index.html   # HTML 页面
│   ├── app.js       # 前端逻辑
│   └── style.css    # 样式
├── package.json     # 依赖
├── .env.example     # 环境变量模板
└── deploy.md        # 部署指南
```

## 快速开始

```bash
# 1. 安装依赖
cd skills/gbrain/fullstack
npm install

# 2. 启动服务器
node server/index.js
# 服务运行在 http://localhost:3001

# 3. 打开 Web 管理后台
# 浏览器访问 http://localhost:3001

# 4. 连接小程序
# 微信开发者工具导入 miniapp/ 目录
# 修改 miniapp/utils/api.js 中的 baseUrl 为你的服务器地址
```

## API 端点

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | /api/status | 系统状态和知识库列表 |
| GET | /api/kb/:name/search?q=&limit= | 搜索知识库 |
| POST | /api/kb/:name/add | 添加文档 |
| GET | /api/kb/:name/stats | 知识库统计 |
| GET | / | Web 管理后台 |

## 技术栈

- **后端**: Node.js + Express
- **知识库**: gbrain (本地加密存储)
- **小程序**: 原生微信小程序
- **前端**: 纯 HTML/CSS/JS (零依赖)
- **部署**: 支持 Vercel / 腾讯云 / 自托管

## 注意事项

- 所有数据通过 gbrain 本地存储，无需外部数据库
- 微信小程序开发需要注册小程序 AppID
- 生产部署建议配置 HTTPS
