# 🚀 gbrain 全栈部署指南

## 方式 1：本地生产部署（Windows 服务）

```bash
# 1. 安装 pm2（进程管理）
npm install -g pm2

# 2. 进入项目目录
cd skills/gbrain/fullstack

# 3. 安装依赖
npm install

# 4. 启动
pm2 start server/index.js --name gbrain-api -i 1

# 5. 设置开机自启
pm2 startup
pm2 save

# 6. 查看状态
pm2 status
pm2 logs gbrain-api
```

## 方式 2：部署到 Vercel

> 注意：Vercel 需要 Serverless 化改造，只适合 API 层

1. 在 `server/` 下创建 `vercel.json`：

```json
{
  "builds": [{ "src": "server/index.js", "use": "@vercel/node" }],
  "routes": [{ "src": "/api/(.*)", "dest": "server/index.js" }]
}
```

2. Vercel 不支持本地文件写入，gbrain 知识库需要改为外部存储（如 Supabase）

## 方式 3：腾讯云 / 轻量服务器

```bash
# 1. 安装 Node.js
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo bash -
sudo apt install -y nodejs

# 2. 复制项目到服务器
scp -r skills/gbrain/fullstack user@server:/opt/gbrain/

# 3. 安装依赖并启动
cd /opt/gbrain
npm install
PORT=3001 node server/index.js &
```

## 方式 4：Docker（推荐）

```dockerfile
FROM node:20-alpine
WORKDIR /app
COPY . .
RUN npm install
EXPOSE 3001
ENV PORT=3001
CMD ["node", "server/index.js"]
```

```bash
docker build -t gbrain-api .
docker run -d -p 3001:3001 -v /path/to/state/gbrain:/app/state/gbrain gbrain-api
```

## 生产注意事项

1. **HTTPS**：使用 Nginx/Caddy 反向代理 + Let's Encrypt 证书
2. **数据安全**：gbrain 数据本身已 AES 加密，建议再加文件系统加密
3. **备份**：定期备份 `state/gbrain/` 目录
4. **监控**：pm2 自带监控，或接入 Grafana

## 小程序发布

1. 微信小程序后台 → 开发 → 开发设置 → 添加服务器域名（需 HTTPS）
2. 修改 `miniapp/utils/api.js` 中的 `baseUrl` 为生产域名
3. 微信开发者工具 → 上传 → 提交审核
