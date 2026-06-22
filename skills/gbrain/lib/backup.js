/*
 * gbrain 数据备份脚本
 * 备份 state/gbrain/ 目录到 backup/ 时间戳子目录
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const BACKUP_ROOT = path.join(__dirname, '..', '..', '..', 'backup');
const GBRAIN_STATE = path.join(__dirname, '..', '..', '..', 'state', 'gbrain');

if (!fs.existsSync(GBRAIN_STATE)) {
  console.log('[⚠️] gbrain state 目录不存在，跳过备份');
  process.exit(0);
}

// 创建备份目录
const timestamp = new Date().toISOString().replace(/[:.]/g, '-').slice(0, 19);
const backupDir = path.join(BACKUP_ROOT, `gbrain-${timestamp}`);
fs.mkdirSync(backupDir, { recursive: true });

try {
  // 使用 robocopy（Windows）或 cp（Linux/macOS）
  if (process.platform === 'win32') {
    execSync(`robocopy "${GBRAIN_STATE}" "${backupDir}" /E /Z /R:3 /W:5`, { stdio: 'inherit' });
  } else {
    execSync(`cp -r "${GBRAIN_STATE}" "${backupDir}"`, { stdio: 'inherit' });
  }
  
  console.log(`[✅] 备份完成：${backupDir}`);
} catch (e) {
  console.error('[❌] 备份失败:', e.message);
  process.exit(1);
}