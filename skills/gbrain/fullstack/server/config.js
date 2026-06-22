// gbrain 全栈 — 服务器配置
const path = require('path');

module.exports = {
  port: parseInt(process.env.PORT || '3001', 10),
  // gbrain 知识库根目录
  gbrainRoot: process.env.GBRAIN_ROOT || path.resolve(__dirname, '..', '..', '..', '..', 'state', 'gbrain'),
  // gbrain skills 路径（用于 require storage）
  gbrainSkills: path.resolve(__dirname, '..', '..'),
  // 前端静态文件
  staticDir: path.resolve(__dirname, '..', 'web'),
  dataDir: path.resolve(__dirname, '..', 'data'),
};
