// gbrain 全栈 — Express 服务器入口
// 提供 REST API + Web 管理后台静态文件服务

const express = require('express');
const cors = require('cors');
const path = require('path');
const fs = require('fs');
const config = require('./config');

// 确保数据目录存在
if (!fs.existsSync(config.dataDir)) {
  fs.mkdirSync(config.dataDir, { recursive: true });
  console.log(`[gbrain] 创建数据目录: ${config.dataDir}`);
}

// 确保 GBRAIN_ROOT 指向 gbrain state（让 storage.js 能找到）
process.env.GBRAIN_ROOT = config.gbrainRoot;

const app = express();

// 中间件
app.use(cors());
app.use(express.json({ limit: '10mb' }));
app.use(express.urlencoded({ extended: true }));

// API 路由
app.use('/api', require('./routes/api'));

// Web 管理后台静态文件
app.use(express.static(config.staticDir));

// 根路径重定向到 Web 后台
app.get('/', (req, res) => {
  res.sendFile(path.join(config.staticDir, 'index.html'));
});

// 健康检查
app.get('/health', (req, res) => {
  res.json({ status: 'ok', uptime: process.uptime() });
});

// 启动
app.listen(config.port, () => {
  console.log('');
  console.log('  🧠 gbrain 全栈服务器已启动');
  console.log('  ─────────────────────────────');
  console.log(`  REST API:    http://localhost:${config.port}/api/status`);
  console.log(`  Web 后台:    http://localhost:${config.port}/`);
  console.log(`  知识库目录:  ${config.gbrainRoot}`);
  console.log('');
  console.log('  API 端点:');
  console.log('  GET  /api/status              — 系统状态');
  console.log('  GET  /api/kb/:name/search?q=  — 搜索知识库');
  console.log('  POST /api/kb/:name/add        — 添加文档');
  console.log('  GET  /api/kb/:name/stats      — 知识库统计');
  console.log('');
});
