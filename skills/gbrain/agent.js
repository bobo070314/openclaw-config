#!/usr/bin/env node
/**
 * gbrain Super Agent — 统一入口
 * 
 * 聚合所有 gbrain 子系统的统一 CLI，提供一站式的知识管理、
 * 代码索引、沙箱执行、模型对话等功能。
 * 
 * 用法:
 *   node agent.js kb create <name>     — 创建知识库
 *   node agent.js kb list              — 列出知识库
 *   node agent.js search <kb> <query>  — 搜索
 *   node agent.js add <kb> <file>      — 添加文件
 *   node agent.js code scan [path]     — 扫描项目
 *   node agent.js code index [path]    — 索引代码
 *   node agent.js sandbox <code>       — 执行代码
 *   node agent.js chat <msg>           — 对话(用配置的LLM)
 *   node agent.js learn <topic>        — 自主学习
 *   node agent.js ollama <cmd> [args]  — Ollama 命令
 *   node agent.js ide detect           — 检测编辑器
 *   node agent.js status               — 系统状态
 */

const path = require('path');
const fs = require('fs');

const GBRAIN_LIB = path.join(__dirname, 'lib');
const GBRAIN_CMDS = path.join(__dirname, 'commands');
const GBRAIN_STATE = process.env.GBRAIN_ROOT || path.join(require('os').homedir(), '.openclaw', 'state', 'gbrain');

// 延迟加载模块
function load(mod) {
  return require(path.join(GBRAIN_LIB, mod));
}

async function status() {
  const storage = load('storage');
  const lock = load('lock');
  let ollamaStatus = { running: false };
  let ideInfo = null;

  try {
    const ollama = load('ollama');
    ollamaStatus = await ollama.checkOllama();
  } catch {}

  try {
    const ide = load('ide');
    ideInfo = ide.detectEditor();
  } catch {}

  console.log(JSON.stringify({
    version: '1.0.0',
    guard: lock.guard ? 'passed' : 'unknown',
    stateDir: GBRAIN_STATE,
    knowledgeBases: fs.existsSync(GBRAIN_STATE) ? fs.readdirSync(GBRAIN_STATE).filter(d => {
      const p = path.join(GBRAIN_STATE, d);
      return fs.statSync(p).isDirectory() && fs.existsSync(path.join(p, 'data.db'));
    }) : [],
    ollama: ollamaStatus,
    ide: ideInfo,
    modules: ['kb', 'search', 'add', 'code', 'sandbox', 'chat', 'learn', 'ollama', 'ide'],
    mcpServers: ['gbrain', 'sandbox'],
  }, null, 2));
}

async function main() {
  const args = process.argv.slice(2);
  if (args.length === 0) {
    console.log('用法见文件顶部注释或运行: node agent.js --help');
    return;
  }

  const cmd = args[0];
  const sub = args[1];
  const rest = args.slice(2);

  switch (cmd) {
    case '--help':
    case '-h':
      fs.readFile(__filename, 'utf-8', (err, content) => {
        if (err) return console.log('Agent — gbrain 超级智能体');
        const lines = content.split('\n').slice(2, 16);
        console.log(lines.join('\n'));
      });
      break;

    case 'status':
      await status();
      break;

    case 'kb':
      await require(path.join(GBRAIN_CMDS, 'kb')).main([sub, ...rest]);
      break;

    case 'search':
      if (!sub || !rest.length) {
        console.log('用法: node agent.js search <知识库名> <查询词>');
        process.exit(1);
      }
      await require(path.join(GBRAIN_CMDS, 'search')).main([sub, ...rest]);
      break;

    case 'add': {
      const kbName = sub;
      const filePath = rest[0];
      if (!kbName || !filePath) {
        console.log('用法: node agent.js add <知识库名> <文件路径> [标题]');
        process.exit(1);
      }
      const storage = load('storage');
      const { Storage } = storage;
      const store = new Storage(kbName);
      const content = fs.readFileSync(filePath, 'utf-8');
      const title = rest[1] || path.basename(filePath);
      store.addDocument({ title, content, source: filePath, type: path.extname(filePath).replace('.', '') });
      store.close();
      console.log(JSON.stringify({ status: 'ok', kb: kbName, added: title }, null, 2));
      break;
    }

    case 'code': {
      const ide = load('ide');
      if (sub === 'scan') {
        const scanPath = rest[0] || ide.getActiveProjectPath() || process.cwd();
        const depth = parseInt(rest[1] || '3', 10);
        console.log(JSON.stringify(ide.scanProject(scanPath, depth), null, 2));
      } else if (sub === 'index') {
        const kbName = rest[0] || 'code';
        const targetPath = rest[1] || ide.getActiveProjectPath() || process.cwd();
        const files = [];
        function walk(dir) {
          try {
            for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
              const full = path.join(dir, entry.name);
              if (entry.isDirectory() && !entry.name.startsWith('.') && entry.name !== 'node_modules') walk(full);
              else if (entry.isFile() && !entry.name.startsWith('.')) files.push(full);
            }
          } catch {}
        }
        walk(targetPath);
        const result = ide.indexOpenFiles(kbName, files);
        console.log(JSON.stringify(result, null, 2));
      } else {
        console.log('用法: node agent.js code scan|index [路径]');
      }
      break;
    }

    case 'sandbox': {
      const sandbox = load('sandbox');
      const code = sub ? [sub, ...rest].join(' ') : '';
      if (!code) {
        console.log('用法: node agent.js sandbox <代码>');
        process.exit(1);
      }
      const result = await sandbox.execute(code);
      console.log(JSON.stringify(result, null, 2));
      break;
    }

    case 'learn': {
      const learn = load('learn');
      const query = sub ? [sub, ...rest].join(' ') : '';
      const result = await learn.learnOne(query);
      console.log(JSON.stringify(result, null, 2));
      break;
    }

    case 'ollama': {
      try {
        const ollama = load('ollama');
        if (sub === 'check' || !sub) {
          console.log(JSON.stringify(await ollama.checkOllama(), null, 2));
        } else if (sub === 'list') {
          console.log(JSON.stringify(await ollama.listModels(), null, 2));
        } else if (sub === 'chat') {
          const model = rest[0] || 'qwen2.5:7b';
          const msg = rest.slice(1).join(' ') || '你好';
          const result = await ollama.chat(model, [
            { role: 'system', content: '你是一个有用的助手。' },
            { role: 'user', content: msg },
          ]);
          console.log(result.content);
        } else if (sub === 'embed') {
          const text = rest.join(' ');
          const result = await ollama.embed('nomic-embed-text', text);
          console.log(JSON.stringify(result, null, 2));
        } else if (sub === 'pull') {
          await ollama.pullModel(rest[0]);
        } else if (sub === 'recommend') {
          const recs = ollama.recommendModel(rest[0] || 'all');
          console.log(JSON.stringify(recs, null, 2));
        }
      } catch (e) {
        console.error('Ollama 错误:', e.message);
      }
      break;
    }

    case 'ide': {
      const ide = load('ide');
      if (sub === 'detect') {
        console.log(JSON.stringify({ editor: ide.detectEditor(), project: ide.getActiveProjectPath() }, null, 2));
      } else {
        console.log('用法: node agent.js ide detect');
      }
      break;
    }

    default:
      console.log(`未知命令: ${cmd}`);
      console.log('试试: node agent.js status');
      break;
  }
}

if (require.main === module) {
  main().catch(e => {
    console.error('Agent 错误:', e.message);
    process.exit(1);
  });
}

module.exports = { main, status };
