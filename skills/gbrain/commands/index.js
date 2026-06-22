#!/usr/bin/env node
/**
 * gbrain - 文件索引器
 * 
 * 命令: node commands/index.js --kb <name> --file|--dir|--url <source>
 */

const fs = require('fs');
const path = require('path');
const { Storage } = require('../lib/storage');
const { guard } = require('../lib/lock');

// 🔐 gbrain 独占锁定验证
guard(true);

// 简单文件解析（复杂文档交给已有技能处理）
function extractText(filePath) {
  const ext = path.extname(filePath).toLowerCase();
  const content = fs.readFileSync(filePath);
  
  switch (ext) {
    case '.txt':
    case '.md':
    case '.js':
    case '.ts':
    case '.py':
    case '.json':
    case '.yaml':
    case '.yml':
    case '.toml':
    case '.html':
    case '.css':
    case '.xml':
    case '.sh':
    case '.bat':
    case '.ps1':
    case '.env':
    case '.gitignore':
    case '.dockerfile':
    case '.sql':
      return content.toString('utf-8');
    default:
      return content.toString('utf-8');
  }
}

function parseArgs() {
  const args = process.argv.slice(2);
  const opts = {};
  for (let i = 0; i < args.length; i++) {
    if (args[i] === '--kb') opts.kb = args[++i];
    else if (args[i] === '--file') opts.file = args[++i];
    else if (args[i] === '--dir') opts.dir = args[++i];
    else if (args[i] === '--url') opts.url = args[++i];
    else if (args[i] === '--recursive') opts.recursive = true;
    else if (args[i] === '--title') opts.title = args[++i];
    else if (args[i] === '--tags') opts.tags = args[++i].split(',');
  }
  return opts;
}

async function indexFile(kbName, filePath, tags) {
  const store = new Storage(kbName);
  const fullPath = path.resolve(filePath);
  
  if (!fs.existsSync(fullPath)) {
    console.error(`File not found: ${fullPath}`);
    store.close();
    return;
  }
  
  try {
    const content = extractText(fullPath);
    const title = path.basename(fullPath);
    const ext = path.extname(fullPath).toLowerCase();
    
    const typeMap = {
      '.js': 'code', '.ts': 'code', '.py': 'code', '.go': 'code',
      '.rs': 'code', '.java': 'code', '.c': 'code', '.cpp': 'code',
      '.md': 'markdown', '.txt': 'text', '.json': 'data',
      '.yaml': 'config', '.yml': 'config', '.toml': 'config',
      '.html': 'markup', '.css': 'markup', '.xml': 'markup',
      '.sh': 'script', '.bat': 'script', '.ps1': 'script',
      '.sql': 'data', '.env': 'config'
    };
    
    const docType = typeMap[ext] || 'file';
    const allTags = [...(tags || []), ext.replace('.', '')];
    
    const id = store.addDocument({
      title,
      content,
      type: docType,
      source: fullPath,
      filePath: fullPath,
      tags: allTags
    });
    
    console.log(JSON.stringify({ id, title, type: docType, size: content.length }));
  } catch (e) {
    console.error(`Index error for ${fullPath}:`, e.message);
  }
  
  store.close();
}

async function indexDir(kbName, dirPath, recursive) {
  const fullPath = path.resolve(dirPath);
  if (!fs.existsSync(fullPath)) {
    console.error(`Directory not found: ${fullPath}`);
    return;
  }
  
  const ignoreDirs = new Set(['node_modules', '.git', 'dist', 'build', '.next', 'target', '__pycache__', '.venv', 'venv']);
  const ignoreFiles = new Set(['package-lock.json', 'yarn.lock', 'pnpm-lock.yaml']);
  
  const files = [];
  function walk(dir) {
    const entries = fs.readdirSync(dir, { withFileTypes: true });
    for (const entry of entries) {
      if (entry.isDirectory()) {
        if (!ignoreDirs.has(entry.name) && recursive) {
          walk(path.join(dir, entry.name));
        }
      } else if (entry.isFile() && !ignoreFiles.has(entry.name)) {
        files.push(path.join(dir, entry.name));
      }
    }
  }
  walk(fullPath);
  
  console.log(JSON.stringify({ total: files.length, directory: fullPath }));
  
  let indexed = 0;
  for (const file of files) {
    try {
      const content = extractText(file);
      if (content.length > 0) {
        const store = new Storage(kbName);
        const relPath = path.relative(fullPath, file);
        store.addDocument({
          title: relPath,
          content: content.substring(0, 50000), // 限制单文件大小
          type: 'code',
          source: file,
          filePath: file,
          tags: [path.extname(file).replace('.', '')]
        });
        store.close();
        indexed++;
        process.stdout.write('.');
      }
    } catch {
      process.stdout.write('x');
    }
  }
  console.log(`\nIndexed: ${indexed}/${files.length} files`);
}

const opts = parseArgs();

if (!opts.kb) {
  console.error('Usage: node commands/index.js --kb <kb_name> --file <path> | --dir <path> [--recursive] | --url <url>');
  process.exit(1);
}

if (opts.file) {
  indexFile(opts.kb, opts.file, opts.tags);
} else if (opts.dir) {
  indexDir(opts.kb, opts.dir, opts.recursive !== false);
} else if (opts.url) {
  console.log('URL indexing requires web_fetch. Use the SKILL workflow instead.');
} else {
  console.error('Specify --file, --dir, or --url');
}

module.exports = {
  search: require('./search'),
  kb: require('./kb'),
  note: require('./note'),
  graph: require('./graph'),
  query: require('./query')
};