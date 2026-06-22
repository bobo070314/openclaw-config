#!/usr/bin/env node
/**
 * gbrain MCP Server
 * 
 * 通过 stdio JSON-RPC 2.0 暴露知识库能力给 OpenClaw 工具链
 * 
 * 使用方法 (在 openclaw.json 中配置):
 * "mcpClients": {
 *   "servers": {
 *     "gbrain": {
 *       "command": "node",
 *       "args": ["skills/gbrain/mcp-server.js"],
 *       "env": { "GBRAIN_ROOT": "D:\\bobo\\openclaw-foreign\\state\\gbrain" }
 *     }
 *   }
 * }
 */

const path = require('path');
const readline = require('readline');

// 🔐 独占锁定验证
const { guard } = require('./lib/lock');
guard(false);

const { Storage } = require('./lib/storage');

// MCP 工具定义
const TOOLS = [
  {
    name: 'gbrain_search',
    description: '搜索知识库，支持语义+全文混合搜索',
    inputSchema: {
      type: 'object',
      properties: {
        kbName: { type: 'string', description: '知识库名称' },
        query: { type: 'string', description: '搜索关键词' },
        limit: { type: 'number', description: '返回结果数量，默认 5' }
      },
      required: ['kbName', 'query']
    }
  },
  {
    name: 'gbrain_add',
    description: '添加文档到知识库',
    inputSchema: {
      type: 'object',
      properties: {
        kbName: { type: 'string', description: '知识库名称' },
        title: { type: 'string', description: '文档标题' },
        content: { type: 'string', description: '文档内容' },
        tags: { type: 'array', items: { type: 'string' }, description: '标签列表' }
      },
      required: ['kbName', 'title', 'content']
    }
  },
  {
    name: 'gbrain_stats',
    description: '获取知识库统计信息',
    inputSchema: {
      type: 'object',
      properties: {
        kbName: { type: 'string', description: '知识库名称' }
      },
      required: ['kbName']
    }
  },
  {
    name: 'gbrain_list',
    description: '列出所有知识库',
    inputSchema: {
      type: 'object',
      properties: {}
    }
  },
  {
    name: 'gbrain_delete',
    description: '删除知识库中的文档',
    inputSchema: {
      type: 'object',
      properties: {
        kbName: { type: 'string', description: '知识库名称' },
        docId: { type: 'string', description: '文档 ID' }
      },
      required: ['kbName', 'docId']
    }
  }
];

// 工具处理器
const HANDLERS = {
  gbrain_search: async (args) => {
    const { kbName, query, limit = 5 } = args;
    const store = new Storage(kbName);
    try {
      const results = store.hybridSearch(query, limit);
      return results.map(r => ({
        id: r.id,
        title: r.title || '(无标题)',
        content: (r.content || '').substring(0, 500),
        tags: r.tags || [],
        score: r.score || 0,
        type: r.type || 'text',
        createdAt: r.createdAt
      }));
    } finally {
      store.close();
    }
  },

  gbrain_add: async (args) => {
    const { kbName, title, content, tags = [] } = args;
    const store = new Storage(kbName);
    try {
      const result = store.addDocument({ title, content, type: 'text', tags });
      return { id: result.id || result, status: 'indexed', title };
    } finally {
      store.close();
    }
  },

  gbrain_stats: async (args) => {
    const { kbName } = args;
    const store = new Storage(kbName);
    try {
      return store.stats();
    } finally {
      store.close();
    }
  },

  gbrain_list: async () => {
    const fs = require('fs');
    const ROOT = process.env.GBRAIN_ROOT || path.join(__dirname, '..', '..', '..', 'state', 'gbrain');
    if (!fs.existsSync(ROOT)) return { kbs: [] };

    const dirs = fs.readdirSync(ROOT, { withFileTypes: true })
      .filter(d => d.isDirectory() && !d.name.startsWith('.'))
      .map(d => {
        try {
          const store = new Storage(d.name);
          const stats = store.stats();
          store.close();
          return { name: d.name, ...stats };
        } catch {
          return { name: d.name, error: '无法读取' };
        }
      });
    return { kbs: dirs };
  },

  gbrain_delete: async (args) => {
    const { kbName, docId } = args;
    const store = new Storage(kbName);
    try {
      // Storage 没有直接删除方法，用内部 _initJSON 方式处理
      const fs = require('fs');
      const dataPath = path.join(
        process.env.GBRAIN_ROOT || path.join(__dirname, '..', '..', '..', 'state', 'gbrain'),
        kbName, 'store.json'
      );
      if (fs.existsSync(dataPath)) {
        const data = JSON.parse(fs.readFileSync(dataPath, 'utf-8'));
        const { loadEncryptedJSON, saveEncryptedJSON } = require('./lib/lock');
        // 加载后过滤
        const raw = fs.readFileSync(dataPath, 'utf-8');
        const decrypted = loadEncryptedJSON(dataPath);
        if (decrypted && decrypted.documents) {
          decrypted.documents = decrypted.documents.filter(d => d.id !== docId);
        }
        saveEncryptedJSON(dataPath, decrypted);
        return { status: 'deleted', docId };
      }
      return { status: 'not_found', docId };
    } finally {
      store.close();
    }
  }
};

// 发送 JSON-RPC 响应
function sendResponse(id, result) {
  const msg = JSON.stringify({ jsonrpc: '2.0', id, result });
  process.stdout.write(msg + '\n');
}

function sendError(id, code, message) {
  const msg = JSON.stringify({ jsonrpc: '2.0', id, error: { code, message } });
  process.stdout.write(msg + '\n');
}

// 主循环
const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout,
  terminal: false
});

rl.on('line', async (line) => {
  try {
    const req = JSON.parse(line.trim());
    const { id, method, params = {} } = req;

    switch (method) {
      case 'tools/list':
        sendResponse(id, { tools: TOOLS });
        break;

      case 'tools/call': {
        const { name, arguments: args = {} } = params;
        const handler = HANDLERS[name];
        if (!handler) {
          sendError(id, -32601, `Tool not found: ${name}`);
          break;
        }
        try {
          const result = await handler(args);
          sendResponse(id, { content: [{ type: 'text', text: JSON.stringify(result, null, 2) }] });
        } catch (e) {
          sendError(id, -32000, `Tool error: ${e.message}`);
        }
        break;
      }

      case 'server/info':
        sendResponse(id, { name: 'gbrain', version: '1.0.0', description: 'gbrain 知识库 MCP Server' });
        break;

      default:
        sendError(id, -32601, `Method not found: ${method}`);
        break;
    }
  } catch (e) {
    // 非 JSON 行忽略
  }
});

// 启动日志
const s = require('process').stderr;
s.write('[gbrain-mcp] MCP Server ready (stdio)\n');
s.write('[gbrain-mcp] Tools: ' + TOOLS.map(t => t.name).join(', ') + '\n');
