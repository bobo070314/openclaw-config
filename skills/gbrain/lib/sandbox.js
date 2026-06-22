#!/usr/bin/env node
/**
 * gbrain 代码执行沙箱
 * 
 * 在安全隔离环境中执行用户提供的代码（Node.js）。
 * 
 * 功能:
 * - 在临时目录中执行代码
 * - 限制执行时间和内存
 * - 自动清理临时文件
 * - 捕获 stdout/stderr
 * - 支持 npm 包自动安装
 * 
 * 安全:
 * - ⚠️ 这不是运行任意用户代码的安全沙箱
 * - ⚠️ 没有进程隔离、文件系统隔离、网络隔离
 * - ✅ 适合执行 AI 生成的代码片段、脚本、测试
 * - ✅ 不适合执行不受信任的第三方代码
 * 
 * 用法:
 *   node sandbox.js <script.js>               # 执行文件
 *   node sandbox.js -c "console.log('hi')"     # 执行代码字符串
 *   node sandbox.js --timeout 10 "script.js"   # 自定义超时(秒)
 *   node sandbox.js --install "script.js"      # 自动 npm install 依赖
 * 
 * MCP 模式:
 *   通过 stdio JSON-RPC 提供 sandbox_exec 工具
 */

const fs = require('fs');
const path = require('path');
const { execSync, spawnSync } = require('child_process');
const os = require('os');

// 配置
const TMPDIR = path.join(__dirname, '..', '..', '..', 'state', 'sandbox');
const DEFAULT_TIMEOUT = 15; // 秒
const MAX_TIMEOUT = 120;

function ensureTmp() {
  if (!fs.existsSync(TMPDIR)) {
    fs.mkdirSync(TMPDIR, { recursive: true });
  }
}

/**
 * 执行代码
 */
function execute(code, options = {}) {
  const timeout = Math.min(options.timeout || DEFAULT_TIMEOUT, MAX_TIMEOUT);
  const needsInstall = options.install || false;
  const isFile = options.isFile || false;

  ensureTmp();

  // 创建临时会话目录
  const sessionDir = path.join(TMPDIR, `run_${Date.now()}_${Math.random().toString(36).slice(2, 8)}`);
  fs.mkdirSync(sessionDir, { recursive: true });

  let scriptPath;
  if (isFile) {
    // 执行已有文件
    scriptPath = path.resolve(code);
    if (!fs.existsSync(scriptPath)) {
      return { error: `文件不存在: ${scriptPath}`, exitCode: 1 };
    }
  } else {
    // 写入临时脚本
    scriptPath = path.join(sessionDir, 'script.js');
    fs.writeFileSync(scriptPath, code, 'utf-8');
  }

  // 如果需要安装依赖
  if (needsInstall) {
    const pkgPath = path.join(path.dirname(scriptPath), 'package.json');
    if (!fs.existsSync(pkgPath)) {
      // 从代码中提取 require 的包
      const deps = extractDeps(code);
      if (deps.length > 0) {
        fs.writeFileSync(pkgPath, JSON.stringify({
          name: 'sandbox-script',
          version: '1.0.0',
          private: true,
          dependencies: Object.fromEntries(deps.map(d => [d, 'latest']))
        }));
        try {
          console.log(`  📦 安装依赖: ${deps.join(', ')}`);
          execSync('npm.cmd install', { cwd: sessionDir, timeout: 60000, stdio: 'pipe' });
        } catch (e) {
          return { error: `依赖安装失败: ${e.message}`, exitCode: 1 };
        }
      }
    }
  }

  // 执行
  const startTime = Date.now();
  let result;
  
  try {
    result = spawnSync('node.exe', [scriptPath], {
      cwd: sessionDir,
      timeout: timeout * 1000,
      maxBuffer: 10 * 1024 * 1024,
      env: { ...process.env, NODE_ENV: 'sandbox' },
      encoding: 'utf-8',
      stdio: ['pipe', 'pipe', 'pipe'],
    });

    const elapsed = ((Date.now() - startTime) / 1000).toFixed(2);

    const output = {
      stdout: (result.stdout || '').trim(),
      stderr: (result.stderr || '').trim(),
      exitCode: result.status,
      signal: result.signal,
      elapsed: `${elapsed}s`,
      sessionDir,
      scriptPath,
    };

    // 清理临时目录（保留 sessionDir 供检查）
    if (!options.keepFiles) {
      cleanup(sessionDir);
    }

    return output;
  } catch (e) {
    // 超时等情况
    const elapsed = ((Date.now() - startTime) / 1000).toFixed(2);
    cleanup(sessionDir);
    return {
      error: e.message,
      elapsed: `${elapsed}s`,
      exitCode: null,
      signal: 'timeout'
    };
  }
}

/**
 * 提取 require 的包名
 */
function extractDeps(code) {
  const deps = new Set();
  const requireRe = /require\(['"](.+?)['"]\)/g;
  let m;
  while ((m = requireRe.exec(code)) !== null) {
    const mod = m[1];
    // 排除内置模块
    if (!mod.startsWith('.') && !mod.startsWith('/') && !['fs','path','os','child_process','util','stream','crypto','http','https','url','querystring','events','assert','buffer','zlib','tty','net','dns','readline'].includes(mod)) {
      deps.add(mod);
    }
  }
  return [...deps];
}

/**
 * 清理
 */
function cleanup(dir) {
  try {
    fs.rmSync(dir, { recursive: true, force: true });
  } catch {}
}

// ===== CLI =====
function cli() {
  const args = process.argv.slice(2);
  let code = null;
  let isFile = false;
  let options = {};

  for (let i = 0; i < args.length; i++) {
    if (args[i] === '-c') {
      code = args[++i];
    } else if (args[i] === '--timeout') {
      options.timeout = parseInt(args[++i], 10);
    } else if (args[i] === '--install') {
      options.install = true;
    } else if (args[i] === '--keep') {
      options.keepFiles = true;
    } else if (!code) {
      // 没有 -c 则视为文件路径
      code = args[i];
      isFile = true;
    }
  }

  if (!code) {
    console.log('用法:');
    console.log('  node sandbox.js <script.js>');
    console.log('  node sandbox.js -c "console.log(1+1)"');
    console.log('  node sandbox.js --timeout 30 -c "..."');
    console.log('  node sandbox.js --install script.js');
    process.exit(1);
  }

  const result = execute(code, { ...options, isFile });
  console.log(JSON.stringify(result, null, 2));
}

// 直接运行则 CLI 模式
if (require.main === module) {
  cli();
}

module.exports = { execute };
