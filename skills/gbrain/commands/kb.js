#!/usr/bin/env node
/**
 * gbrain - 知识库管理器
 * 
 * 命令: node commands/kb.js list|create|delete|stats [name]
 */

const fs = require('fs');
const path = require('path');
const { Storage } = require('../lib/storage');
const { guard } = require('../lib/lock');

// 🔐 gbrain 独占锁定验证
guard(true);

const ROOT = process.env.GBRAIN_ROOT || path.join(__dirname, '..', '..', '..', 'state', 'gbrain');

function listKBs() {
  try {
    if (!fs.existsSync(ROOT)) {
      return { kbs: [] };
    }
    const dirs = fs.readdirSync(ROOT, { withFileTypes: true })
      .filter(d => d.isDirectory() && !d.name.startsWith('.') && d.name !== 'embeddings')
      .map(d => {
        const store = new Storage(d.name);
        const s = store.stats();
        store.close();
        return { name: d.name, ...s };
      });
    return { kbs: dirs };
  } catch (e) {
    return { error: e.message };
  }
}

const args = process.argv.slice(2);
const cmd = args[0];

switch (cmd) {
  case 'list':
    console.log(JSON.stringify(listKBs(), null, 2));
    break;

  case 'create':
    if (!args[1]) {
      console.error('Usage: node kb.js create <kb_name>');
      process.exit(1);
    }
    const store = new Storage(args[1]);
    console.log(JSON.stringify({ kb: args[1], status: 'created', stats: store.stats() }));
    store.close();
    break;

  case 'delete':
    if (!args[1]) {
      console.error('Usage: node kb.js delete <kb_name>');
      process.exit(1);
    }
    try {
      fs.rmSync(path.join(ROOT, args[1]), { recursive: true, force: true });
      console.log(JSON.stringify({ kb: args[1], status: 'deleted' }));
    } catch (e) {
      console.error('Delete error:', e.message);
    }
    break;

  case 'stats':
    if (!args[1]) {
      console.error('Usage: node kb.js stats <kb_name>');
      process.exit(1);
    }
    {
      const s = new Storage(args[1]);
      console.log(JSON.stringify(s.stats(), null, 2));
      s.close();
    }
    break;

  default:
    console.log(`Usage: node kb.js list|create|delete|stats`);
    break;
}
