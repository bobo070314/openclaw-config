#!/usr/bin/env node
/**
 * 🔐 gbrain 独占锁定模块 — 三重防护
 * 
 * 层 1: 环境指纹校验（运行时检测）
 * 层 2: AES-256-CBC 数据加密（存储层）
 * 层 3: 入口守卫（所有命令调用前检查）
 * 
 * 国际版独占，国内版无法加载/读取知识库数据。
 */

const crypto = require('crypto');
const fs = require('fs');
const path = require('path');

// ========== 常量 ==========

// 主钥匙 — gbrain 的硬编码签名密码（AES-256 密钥派生用）
const MASTER_PASSPHRASE = 'gbrain-international-exclusive-v1';
const HARDCODED_SALT = 'openclaw-global-2026';
const KEY_ITERATIONS = 16384;
const KEY_LENGTH = 32; // AES-256
const IV_LENGTH = 16;
const AUTH_TAG_LENGTH = 16;

// ===== 层 1: 环境指纹 =====

/**
 * 环境指纹检测
 * 验证当前运行的是国际版 OpenClaw 环境
 * 
 * 指纹要素:
 * 1. 运行时端口 18791（国际版特征）
 * 2. openclaw.json 中的 gbrain.root 路径
 * 3. openclaw.json 中的 international 特征值
 * 4. 文件系统中的 IDENTITY.md 存在
 */
function checkFingerprint(strict = false) {
  // 指纹 1: 端口 18791 在进程中
  const portOK = process.env.OPENCLAW_PORT === '18791' ||
    (process.env.PORT || '').includes('18791') ||
    (process.env.NODE_OPTIONS || '').includes('18791') ||
    process.execPath.toLowerCase().includes('openclaw');
  
  // 指纹 2: gbrain root 路径含 openclaw-foreign
  const gbrainRoot = process.env.GBRAIN_ROOT || '';
  const pathOK = gbrainRoot.includes('openclaw-foreign') ||
    __dirname.includes('openclaw-foreign');
  
  // 指纹 3: 配置文件国际版标识
  const configPath = path.join(__dirname, '..', '..', '..', 'openclaw.json');
  let configIDOK = false;
  try {
    if (fs.existsSync(configPath)) {
      const config = JSON.parse(fs.readFileSync(configPath, 'utf-8'));
      // 多个特征联合检验
      const hasExtractHint = JSON.stringify(config).includes('openclaw-foreign');
      const hasModel = JSON.stringify(config).includes('deepseek');
      const hasExtraDirs = JSON.stringify(config).includes('extraDirs');
      configIDOK = hasExtractHint && hasModel && hasExtraDirs;
    }
  } catch (e) { /* 文件可能不存在或不可解析 */ }
  
  // 指纹 4: IDENTITY.md 的存在
  const identityPath = path.join(__dirname, '..', '..', '..', '..', 'IDENTITY.md');
  const identityOK = fs.existsSync(identityPath);
  
  // 指纹 5: 节点版本和操作系统特征
  const runtimeOK = process.platform === 'win32' && 
    process.release?.name === 'node';
  
  if (strict) {
    // 严格模式：必需端口 + 路径 + 配置全部通过
    return portOK && pathOK && configIDOK;
  }
  
  // 宽松模式：至少满足 3 个指纹
  const score = [portOK, pathOK, configIDOK, identityOK, runtimeOK]
    .filter(Boolean).length;
  return score >= 3;
}

// ===== 层 2: 数据加密 =====

/**
 * 派生 AES-256 密钥
 */
function deriveKey(passphrase, salt) {
  return crypto.scryptSync(
    passphrase || MASTER_PASSPHRASE,
    salt || HARDCODED_SALT,
    KEY_LENGTH,
    { N: KEY_ITERATIONS, r: 8, p: 1 }
  );
}

/**
 * 加密数据（AES-256-CBC）
 * 输出格式: base64(iv):base64(ciphertext)
 */
function encrypt(plaintext, customPassphrase) {
  const key = deriveKey(customPassphrase);
  const iv = crypto.randomBytes(IV_LENGTH);
  const cipher = crypto.createCipheriv('aes-256-cbc', key, iv);
  
  let encrypted = cipher.update(plaintext, 'utf-8', 'base64');
  encrypted += cipher.final('base64');
  
  return iv.toString('base64') + ':' + encrypted;
}

/**
 * 解密数据
 * 输入格式: base64(iv):base64(ciphertext)
 */
function decrypt(ciphertext, customPassphrase) {
  try {
    const [ivB64, dataB64] = ciphertext.split(':');
    if (!ivB64 || !dataB64) return null;
    
    const key = deriveKey(customPassphrase);
    const iv = Buffer.from(ivB64, 'base64');
    const decipher = crypto.createDecipheriv('aes-256-cbc', key, iv);
    
    let decrypted = decipher.update(dataB64, 'base64', 'utf-8');
    decrypted += decipher.final('utf-8');
    
    return decrypted;
  } catch (e) {
    return null; // 解密失败 = 钥匙不对/数据被篡改
  }
}

/**
 * 验证并解密 JSON 文件
 * 自动识别文件格式（明文/加密）
 */
function loadEncryptedJSON(filePath) {
  try {
    const raw = fs.readFileSync(filePath, 'utf-8').trim();
    
    // 格式 1: 加密数据（iv:encrypted 格式）
    if (raw.includes(':') && raw.length > 50) {
      const decrypted = decrypt(raw);
      if (decrypted) return JSON.parse(decrypted);
      throw new Error('DECRYPT_FAILED');
    }
    
    // 格式 2: 明文 JSON（迁移兼容）
    return JSON.parse(raw);
  } catch (e) {
    if (e.message === 'DECRYPT_FAILED') throw e;
    throw e;
  }
}

/**
 * 加密并写入 JSON 文件
 */
function saveEncryptedJSON(filePath, data) {
  const json = JSON.stringify(data);
  const encrypted = encrypt(json);
  fs.writeFileSync(filePath, encrypted, 'utf-8');
}

// ===== 层 3: 入口守卫 =====

/**
 * 环境校验守卫（在 CLI 命令入口调用）
 * 
 * 失败时:
 * - CLIMode: 打印警告但允许继续（不打断命令行体验）
 * - StrictMode: 直接退出进程
 */
function guard(strict = false) {
  const ok = checkFingerprint(strict);
  
  if (!ok) {
    if (strict) {
      console.error('🚫 ERROR: gbrain 仅限 OpenClaw 国际版使用');
      console.error('🚫 当前环境未通过国际版身份验证');
      console.error('🚫 端口:', process.env.OPENCLAW_PORT || 'unknown');
      console.error('🚫 路径:', __dirname);
      process.exit(1);
    }
    // 非严格模式下打印警告
    console.warn('⚠️  gbrain: 环境指纹校验未完全通过（非阻塞模式）');
    console.warn('⚠️  当前进程:', process.pid, '端口:', process.env.OPENCLAW_PORT || '(未设置)');
    return false;
  }
  return true;
}

/**
 * 获取文件系统指纹令牌（用于文件级水印）
 */
function getWatermark() {
  const key = deriveKey();
  // 取密钥的前8字节转为hex作为文件标识
  return 'GBRAIN' + key.toString('hex').substring(0, 8).toUpperCase();
}

// ===== 导出 =====

module.exports = {
  checkFingerprint,
  guard,
  encrypt,
  decrypt,
  loadEncryptedJSON,
  saveEncryptedJSON,
  deriveKey,
  getWatermark
};

// CLI 测试
if (require.main === module) {
  const cmd = process.argv[2];
  
  if (cmd === 'check') {
    const strict = process.argv.includes('--strict');
    const ok = checkFingerprint(strict);
    console.log(JSON.stringify({
      passed: ok,
      mode: strict ? 'strict' : 'normal',
      port: process.env.OPENCLAW_PORT || '(none)',
      pid: process.pid,
      cwd: process.cwd(),
      watermark: getWatermark()
    }));
  } else if (cmd === 'encrypt-text' && process.argv[3]) {
    console.log(encrypt(process.argv[3]));
  } else if (cmd === 'decrypt-text' && process.argv[3]) {
    console.log(decrypt(process.argv[3]));
  } else if (cmd === 'convert' && process.argv[3]) {
    const filePath = path.resolve(process.argv[3]);
    if (!fs.existsSync(filePath)) {
      console.error('File not found:', filePath);
      process.exit(1);
    }
    try {
      const data = JSON.parse(fs.readFileSync(filePath, 'utf-8'));
      const encrypted = encrypt(JSON.stringify(data));
      fs.writeFileSync(filePath, encrypted);
      console.log('✅ Converted and encrypted:', filePath);
    } catch (e) {
      console.error('Failed to convert:', e.message);
    }
  } else if (cmd === 'watermark') {
    console.log(getWatermark());
  } else if (cmd === 'guard') {
    guard(process.argv.includes('--strict'));
  } else {
    console.log('Usage: node lock.js check [--strict]');
    console.log('       node lock.js encrypt-text <text>');
    console.log('       node lock.js decrypt-text <encrypted>');
    console.log('       node lock.js convert <json_file_path>');
    console.log('       node lock.js watermark');
    console.log('       node lock.js guard [--strict]');
  }
}
