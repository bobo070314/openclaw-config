#!/usr/bin/env node
/**
 * gbrain - 搜索命令
 * 
 * 命令: node commands/search.js --kb <name> --query <text> [--mode semantic|text|hybrid] [--limit N]
 */

const path = require('path');
const { Storage } = require('../lib/storage');
const { guard } = require('../lib/lock');

// 🔐 gbrain 独占锁定验证
guard(true);

function parseArgs() {
  const args = process.argv.slice(2);
  const opts = { mode: 'hybrid', limit: 10, all: false };
  for (let i = 0; i < args.length; i++) {
    if (args[i] === '--kb') opts.kb = args[++i];
    else if (args[i] === '--query') opts.query = args[++i];
    else if (args[i] === '--mode') opts.mode = args[++i];
    else if (args[i] === '--limit') opts.limit = parseInt(args[++i]) || 10;
    else if (args[i] === '--all') opts.all = true;
  }
  return opts;
}

const opts = parseArgs();

if (!opts.query) {
  console.error('Usage: node commands/search.js --kb <kb_name> --query <text> [--mode hybrid|semantic|text] [--limit N]');
  process.exit(1);
}

if (opts.all) {
  // 搜索所有知识库
  const fs = require('fs');
  const { Storage: Store } = require('../lib/storage');
  const ROOT = process.env.GBRAIN_ROOT || path.join(__dirname, '..', '..', '..', 'state', 'gbrain');
  
  const allResults = [];
  if (fs.existsSync(ROOT)) {
    const dirs = fs.readdirSync(ROOT, { withFileTypes: true })
      .filter(d => d.isDirectory() && !d.name.startsWith('.') && d.name !== 'embeddings');
    
    for (const dir of dirs) {
      try {
        const store = new Store(dir.name);
        const results = store.hybridSearch(opts.query, opts.limit);
        allResults.push(...results.map(r => ({ ...r, kb: dir.name })));
        store.close();
      } catch {}
    }
  }
  
  allResults.sort((a, b) => (b.score || 0) - (a.score || 0));
  console.log(JSON.stringify(allResults.slice(0, opts.limit), null, 2));
} else if (opts.kb) {
  const store = new Storage(opts.kb);
  let results;
  
  switch (opts.mode) {
    case 'semantic':
      results = store.semanticSearch(opts.query, opts.limit);
      break;
    case 'text':
      results = store.ftsSearch(opts.query, opts.limit);
      break;
    default:
      results = store.hybridSearch(opts.query, opts.limit);
  }
  
  console.log(JSON.stringify(results.map(r => ({
    id: r.id,
    title: r.title,
    type: r.type,
    source: r.source,
    tags: r.tags,
    snippet: (r.content || '').substring(0, 200),
    score: r.score || r.semanticScore || -r.fts_score || 0
  })), null, 2));
  
  store.close();
} else {
  console.error('Specify --kb or --all');
}
