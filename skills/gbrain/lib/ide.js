#!/usr/bin/env node
/**
 * gbrain IDE 集成桥
 * 
 * 将 gbrain 连接到 VS Code / Cursor / Windsurf 等编辑器。
 * 
 * 功能:
 * - 读取当前打开的项目路径（通过 VS Code CLI 或端口）
 * - 将编辑器中的代码语义化索引到 gbrain
 * - 在编辑器中搜索 gbrain 知识库
 * - 将 AI 建议写入编辑器文件
 * 
 * 工作方式:
 * 
 * VS Code 集成:
 *   code --folder-uri file:///path  → 打开项目
 *   code-insiders --locate-extension  → 获取扩展信息
 *   VS Code 的 Remote - SSH / Tunnel 自动处理远程场景
 * 
 * Cursor 集成:
 *   cursor --reuse-window  → 复用窗口打开
 * 
 * Windsurf 集成:
 *   windsurf 命令同 VS Code
 * 
 * 端口 API (VS Code 1.86+):
 *   localhost:<port>/  → VS Code 内嵌服务（需开启 settings.json 中的 remote.autoForwardPorts）
 * 
 * 核心能力: 将编辑器活动文件内容提取并存入 gbrain
 */

const fs = require('fs');
const path = require('path');
const { execSync, spawn } = require('child_process');
const os = require('os');

// 配置
const GBRAIN_SKILLS = path.resolve(__dirname, '..');
const GBRAIN_LIB = path.join(GBRAIN_SKILLS, 'lib');

// 缓存
let _storage = null;

function getStorage() {
  if (!_storage) {
    _storage = require(path.join(GBRAIN_LIB, 'storage'));
  }
  return _storage;
}

function guard() {
  try {
    require(path.join(GBRAIN_LIB, 'lock')).guard(false);
  } catch (e) {
    console.error('🔒 Guard failed:', e.message);
    process.exit(1);
  }
}

// ========================================
// 编辑器检测
// ========================================

const EDITORS = {
  'code': { name: 'VS Code', cmd: 'code', settingsPath: '.vscode' },
  'code-insiders': { name: 'VS Code Insiders', cmd: 'code-insiders', settingsPath: '.vscode' },
  'cursor': { name: 'Cursor', cmd: 'cursor', settingsPath: '.cursor' },
  'windsurf': { name: 'Windsurf', cmd: 'windsurf', settingsPath: '.windsurf' },
};

function detectEditor() {
  for (const [key, editor] of Object.entries(EDITORS)) {
    try {
      const result = execSync(`where ${editor.cmd} 2>nul || which ${editor.cmd} 2>/dev/null`, { encoding: 'utf-8', timeout: 3000 });
      if (result.trim()) {
        return { ...editor, key };
      }
    } catch {}
  }
  return null;
}

/**
 * 获取当前编辑器打开的项目路径
 * 通过检查常用编辑器窗口标题或进程信息
 */
function getActiveProjectPath() {
  const editors = ['code.exe', 'cursor.exe', 'windsurf.exe', 'idea64.exe'];
  
  for (const exe of editors) {
    try {
      // 通过进程的命令行获取打开文件夹路径
      const result = execSync(
        `wmic process where "name='${exe}'" get commandline /format:textvaluelist 2>nul`,
        { encoding: 'utf-8', timeout: 5000 }
      );
      if (result) {
        const lines = result.split('\n');
        for (const line of lines) {
          // 找 --folder-uri 或打开路径
          const match = line.match(/--folder-uri[= ]file:\/\/([^\s"]+)/);
          if (match) {
            return decodeURIComponent(match[1]);
          }
          // 或直接路径
          const pathMatch = line.match(/([A-Z]:\\[^"\\]+\\(?:[^"\\]+\\)*[^"\\]+)/i);
          if (pathMatch) {
            const p = pathMatch[1];
            if (fs.existsSync(p) && fs.statSync(p).isDirectory()) {
              return p;
            }
          }
        }
      }
    } catch {}
  }

  // 最后手段：检查当前目录
  const cwd = process.cwd();
  if (fs.existsSync(path.join(cwd, '.git'))) {
    return cwd;
  }
  return null;
}

// ========================================
// 代码索引
// ========================================

/**
 * 索引编辑器中的文件到 gbrain 知识库
 */
function indexOpenFiles(kbName, filePaths) {
  guard();
  const { Storage } = getStorage();
  const store = new Storage(kbName || 'code');

  let count = 0;
  const results = [];

  for (const filePath of filePaths) {
    try {
      // 跳过忽略文件
      if (shouldIgnore(filePath)) continue;

      const content = fs.readFileSync(filePath, 'utf-8');
      const ext = path.extname(filePath);
      const relativePath = filePath;

      // 分块：大文件按 200 行分块
      const lines = content.split('\n');
      if (lines.length <= 200) {
        store.addDocument({
          title: path.basename(filePath),
          content,
          type: 'code',
          tags: [ext.replace('.', ''), 'code', path.basename(path.dirname(filePath))],
          source: relativePath,
        });
        count++;
        results.push({ file: filePath, status: 'indexed', lines: lines.length });
      } else {
        // 大文件按函数/类分块
        const chunks = chunkCode(content, ext);
        for (const chunk of chunks) {
          store.addDocument({
            title: `${path.basename(filePath)} — ${chunk.name}`,
            content: chunk.content,
            type: 'code',
            tags: [ext.replace('.', ''), 'code', chunk.type],
            source: `${relativePath}:${chunk.lineStart}`,
          });
          count++;
          results.push({ file: filePath, func: chunk.name, status: 'indexed' });
        }
      }
    } catch (e) {
      results.push({ file: filePath, status: 'error', message: e.message });
    }
  }

  store.close();
  return { kb: kbName, total: count, results };
}

/**
 * 忽略的文件/目录
 */
function shouldIgnore(filePath) {
  const base = path.basename(filePath);
  const dir = path.basename(path.dirname(filePath));
  const ignoredDirs = ['node_modules', '.git', 'dist', 'build', '.next', '.nuxt', '__pycache__', 'venv', '.venv', 'target', 'bin', 'obj'];
  const ignoredExts = ['.jpg', '.png', '.gif', '.ico', '.woff', '.woff2', '.ttf', '.eot', '.map', '.min.js', '.min.css'];
  const ignoredFiles = ['package-lock.json', 'yarn.lock', 'pnpm-lock.yaml', '.DS_Store'];

  if (ignoredDirs.includes(dir)) return true;
  if (ignoredFiles.includes(base)) return true;
  if (ignoredExts.some(ext => base.endsWith(ext))) return true;
  return false;
}

/**
 * 代码分块：按函数/类/接口拆分
 */
function chunkCode(content, ext) {
  const lang = ext.replace('.', '');
  const chunks = [];
  const lines = content.split('\n');

  // 检测代码结构
  const patterns = {
    function: [
      /^(?:export\s+)?(?:async\s+)?function\s+(\w+)/,
      /^(?:export\s+)?(?:const|let|var)\s+(\w+)\s*=\s*(?:async\s+)?(?:function|\(|\w+\s*=>)/,
      /^(?:public|private|protected|static)?\s*(?:async\s+)?(\w+)\s*\([^)]*\)\s*{/,
      /^def\s+(\w+)\s*\(/,
      /^func\s+(\w+)/,
    ],
    class: [
      /^(?:export\s+)?(?:abstract\s+)?class\s+(\w+)/,
      /^(?:export\s+)?interface\s+(\w+)/,
      /^type\s+(\w+)\s*=/,
      /^struct\s+(\w+)/,
    ],
    module: [
      /^(?:export\s+)?(?:default\s+)?(?:module|namespace)\s+(\w+)/,
    ]
  };

  let currentName = `${path.basename(process.argv[1] || 'file')} (全文)`;
  let currentType = 'module';
  let currentLineStart = 1;
  let currentLines = [];
  let depth = 0;

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    const trimmed = line.trim();

    // 检测新块开始
    let foundName = null;
    let foundType = null;

    for (const [type, pats] of Object.entries(patterns)) {
      for (const pat of pats) {
        const m = trimmed.match(pat);
        if (m) {
          foundName = m[1];
          foundType = type;
          break;
        }
      }
      if (foundName) break;
    }

    // 如果有前一块且新块开始了 → 保存前一块
    if (foundName && currentLines.length > 30) {
      if (currentLines.length > 5) {
        chunks.push({
          name: currentName,
          type: currentType,
          content: currentLines.join('\n'),
          lineStart: currentLineStart,
        });
      }
      currentName = foundName;
      currentType = foundType;
      currentLineStart = i + 1;
      currentLines = [];
    }

    currentLines.push(line);
  }

  // 最后一块
  if (currentLines.length > 5) {
    chunks.push({
      name: currentName,
      type: currentType,
      content: currentLines.join('\n'),
      lineStart: currentLineStart,
    });
  }

  return chunks;
}

// ========================================
// 知识库搜索 (从编辑器)
// ========================================

function searchCode(kbName, query, limit = 5) {
  guard();
  const { Storage } = getStorage();
  const store = new Storage(kbName || 'code');
  const results = store.hybridSearch(query, limit);
  store.close();
  return results;
}

// ========================================
// 文件操作 (AI 写入文件)
// ========================================

function writeFile(filePath, content) {
  const dir = path.dirname(filePath);
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
  }
  fs.writeFileSync(filePath, content, 'utf-8');
  return { file: filePath, size: content.length };
}

function readFile(filePath) {
  if (!fs.existsSync(filePath)) return null;
  return fs.readFileSync(filePath, 'utf-8');
}

// ========================================
// 项目结构扫描
// ========================================

function scanProject(projectPath, depth = 3) {
  const result = { path: projectPath, name: path.basename(projectPath), files: [], dirs: [] };
  if (!fs.existsSync(projectPath)) return result;

  try {
    const entries = fs.readdirSync(projectPath, { withFileTypes: true });

    for (const entry of entries) {
      if (entry.name.startsWith('.') || shouldIgnore(path.join(projectPath, entry.name))) continue;

      const fullPath = path.join(projectPath, entry.name);
      if (entry.isDirectory()) {
        if (depth > 1) {
          const sub = scanProject(fullPath, depth - 1);
          result.dirs.push(sub);
        } else {
          result.dirs.push({ path: fullPath, name: entry.name, truncated: true });
        }
      } else {
        result.files.push({ path: fullPath, name: entry.name, size: fs.statSync(fullPath).size });
      }
    }
  } catch {}

  return result;
}

// ========================================
// CLI
// ========================================

function cli() {
  const args = process.argv.slice(2);
  const command = args[0];

  switch (command) {
    case 'detect':
      const editor = detectEditor();
      const project = getActiveProjectPath();
      console.log(JSON.stringify({ editor, project }, null, 2));
      break;

    case 'scan':
      const scanPath = args[1] || getActiveProjectPath() || process.cwd();
      const tree = scanProject(scanPath, parseInt(args[2] || '3', 10));
      console.log(JSON.stringify(tree, null, 2));
      break;

    case 'index': {
      const kbName = args[1] || 'code';
      const targetPath = args[2] || getActiveProjectPath() || process.cwd();
      const files = walkFiles(targetPath);
      const result = indexOpenFiles(kbName, files);
      console.log(JSON.stringify(result, null, 2));
      break;
    }

    case 'search': {
      const skb = args[1] || 'code';
      const query = args.slice(2).join(' ');
      if (!query) { console.log('用法: node ide.js search [知识库] 搜索词'); process.exit(1); }
      const results = searchCode(skb, query);
      console.log(JSON.stringify(results, null, 2));
      break;
    }

    case 'write':
      const wf = args[1];
      const wc = args.slice(2).join(' ');
      if (wf && wc) {
        const r = writeFile(wf, wc);
        console.log(JSON.stringify(r));
      }
      break;

    case 'guard':
      guard();
      console.log(JSON.stringify({ guard: 'passed' }));
      break;

    default:
      console.log('用法:');
      console.log('  node ide.js detect                    — 检测编辑器');
      console.log('  node ide.js scan [路径] [深度]        — 扫描项目结构');
      console.log('  node ide.js index [知识库] [路径]     — 索引项目代码');
      console.log('  node ide.js search [知识库] 搜索词    — 搜索知识库');
      console.log('  node ide.js write <文件> <内容>       — 写入文件');
      console.log('  node ide.js guard                     — 测试锁');
      break;
  }
}

function walkFiles(dir) {
  const results = [];
  try {
    const entries = fs.readdirSync(dir, { withFileTypes: true });
    for (const entry of entries) {
      const fullPath = path.join(dir, entry.name);
      if (shouldIgnore(fullPath)) continue;
      if (entry.isDirectory()) {
        results.push(...walkFiles(fullPath));
      } else if (entry.isFile()) {
        results.push(fullPath);
      }
    }
  } catch {}
  return results;
}

if (require.main === module) {
  cli();
}

module.exports = {
  detectEditor,
  getActiveProjectPath,
  indexOpenFiles,
  searchCode,
  writeFile,
  readFile,
  scanProject,
  guard,
};
