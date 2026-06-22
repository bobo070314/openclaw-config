#!/usr/bin/env node
/**
 * gbrain Ollama 集成桥
 * 
 * 连接本地 Ollama 实例，支持嵌入生成、对话、模型管理。
 * 所有请求使用原生 fetch（Node 18+），无需额外依赖。
 * 
 * 用法:
 *   node ollama.js check        — 检查 Ollama 状态
 *   node ollama.js list         — 列出已下载模型
 *   node ollama.js chat <model> — 对话（交互式）
 *   node ollama.js embed <text> — 获取嵌入
 */

const OLLAMA_HOST = process.env.OLLAMA_HOST || 'http://localhost:11434';

// ============================
// API 封装
// ============================

async function request(method, path, body) {
  const url = `${OLLAMA_HOST}${path}`;
  const opts = {
    method,
    headers: body ? { 'Content-Type': 'application/json' } : {},
  };
  if (body) opts.body = JSON.stringify(body);

  const res = await fetch(url, opts);
  if (!res.ok) {
    const text = await res.text();
    throw new Error(`Ollama API ${res.status}: ${text.substring(0, 200)}`);
  }
  return res;
}

// ============================
// 公开函数
// ============================

/**
 * 检查 Ollama 运行状态
 */
async function checkOllama() {
  try {
    const res = await request('GET', '/api/tags');
    const data = await res.json();
    const models = (data.models || []).map(m => m.name);
    // 尝试获取版本
    let version = 'unknown';
    try {
      const vRes = await fetch(`${OLLAMA_HOST}/api/version`);
      if (vRes.ok) {
        const vData = await vRes.json();
        version = vData.version || 'unknown';
      }
    } catch {}
    return { running: true, version, models, count: models.length };
  } catch (e) {
    return { running: false, version: null, models: [], error: `Ollama 未运行 (${OLLAMA_HOST})。请先启动: ollama serve`, detail: e.message };
  }
}

/**
 * 列出已下载的模型
 */
async function listModels() {
  try {
    const res = await request('GET', '/api/tags');
    const data = await res.json();
    return (data.models || []).map(m => ({
      name: m.name,
      size: formatBytes(m.size),
      sizeBytes: m.size,
      modified: m.modified_at,
      digest: m.digest ? m.digest.substring(0, 12) : null,
    }));
  } catch (e) {
    throw new Error(`无法列出模型: ${e.message}`);
  }
}

/**
 * 拉取（下载）模型
 */
async function pullModel(name) {
  const res = await request('POST', '/api/pull', { name, stream: true });
  const reader = res.body.getReader();
  const decoder = new TextDecoder();
  let buffer = '';
  let lastProgress = 0;

  while (true) {
    const { done, value } = await reader.read();
    if (done) break;

    buffer += decoder.decode(value, { stream: true });
    const lines = buffer.split('\n');
    buffer = lines.pop() || '';

    for (const line of lines) {
      if (!line.trim()) continue;
      try {
        const data = JSON.parse(line);
        if (data.status) {
          // 进度消息
          if (data.total) {
            const pct = Math.round((data.completed || 0) / data.total * 100);
            if (pct !== lastProgress) {
              lastProgress = pct;
              process.stderr.write(`\r  📥 ${data.status}: ${pct}% (${formatBytes(data.completed)}/${formatBytes(data.total)})`);
            }
          } else {
            process.stderr.write(`\r  📥 ${data.status}    \n`);
          }
        }
      } catch {}
    }
  }
  process.stderr.write('\n');
  return { status: 'downloaded', model: name };
}

/**
 * 对话
 */
async function chat(model, messages, options = {}) {
  const body = {
    model,
    messages,
    stream: options.stream || false,
    options: {
      temperature: options.temperature ?? 0.7,
      ...(options.num_predict ? { num_predict: options.num_predict } : {}),
      ...(options.top_p ? { top_p: options.top_p } : {}),
    }
  };

  if (options.stream) {
    // 流式返回
    const res = await request('POST', '/api/chat', body);
    const reader = res.body.getReader();
    const decoder = new TextDecoder();
    let fullContent = '';
    let buffer = '';

    while (true) {
      const { done, value } = await reader.read();
      if (done) break;
      buffer += decoder.decode(value, { stream: true });
      const lines = buffer.split('\n');
      buffer = lines.pop() || '';

      for (const line of lines) {
        if (!line.trim()) continue;
        try {
          const data = JSON.parse(line);
          if (data.message?.content) {
            fullContent += data.message.content;
            if (options.onToken) options.onToken(data.message.content);
          }
          if (data.done) {
            return {
              content: fullContent,
              totalDuration: data.total_duration,
              promptEvalCount: data.prompt_eval_count,
              evalCount: data.eval_count,
            };
          }
        } catch {}
      }
    }
    return { content: fullContent };
  }

  // 非流式
  const res = await request('POST', '/api/chat', body);
  const data = await res.json();
  return {
    content: data.message?.content || '',
    totalDuration: data.total_duration,
    promptEvalCount: data.prompt_eval_count,
    evalCount: data.eval_count,
  };
}

/**
 * 生成文本（简单模式）
 */
async function generate(model, prompt, options = {}) {
  const body = {
    model,
    prompt,
    stream: false,
    options: {
      temperature: options.temperature ?? 0.7,
    }
  };

  const res = await request('POST', '/api/generate', body);
  const data = await res.json();
  return {
    response: data.response,
    totalDuration: data.total_duration,
    promptEvalCount: data.prompt_eval_count,
    evalCount: data.eval_count,
  };
}

/**
 * 获取嵌入向量
 */
async function embed(model, text) {
  const res = await request('POST', '/api/embeddings', {
    model: model || 'nomic-embed-text',
    prompt: text,
  });
  const data = await res.json();
  return {
    embedding: data.embedding,
    dimension: data.embedding ? data.embedding.length : 0,
    model: model || 'nomic-embed-text',
  };
}

/**
 * 推荐模型
 */
function recommendModel(task) {
  const recommendations = {
    'embed': [
      { name: 'nomic-embed-text', size: '~274MB', desc: '轻量嵌入模型，适合文档向量化' },
      { name: 'all-minilm', size: '~133MB', desc: '更轻量的嵌入模型' },
      { name: 'bge-m3', size: '~2.2GB', desc: '高质量多语言嵌入模型' },
    ],
    'code': [
      { name: 'deepseek-coder:6.7b', size: '~3.8GB', desc: '代码补全和生成' },
      { name: 'codellama:7b', size: '~3.8GB', desc: 'Meta 代码 LLM' },
      { name: 'qwen2.5-coder:7b', size: '~4.7GB', desc: '通义代码模型' },
    ],
    'chat': [
      { name: 'qwen2.5:7b', size: '~4.7GB', desc: '通义千问 2.5，综合能力强' },
      { name: 'llama3.2:3b', size: '~2.0GB', desc: 'Meta Llama 3.2，轻量' },
      { name: 'gemma2:9b', size: '~5.5GB', desc: 'Google Gemma 2' },
    ],
    'reasoning': [
      { name: 'deepseek-r1:7b', size: '~4.7GB', desc: 'DeepSeek R1 推理模型' },
      { name: 'qwq:7b', size: '~4.7GB', desc: 'QwQ 推理模型' },
    ],
    'vision': [
      { name: 'llava:7b', size: '~4.5GB', desc: '多模态视觉模型' },
      { name: 'minicpm-v:8b', size: '~5.5GB', desc: 'MiniCPM-V 视觉模型' },
    ],
  };
  return recommendations[task] || recommendations.chat;
}

// ============================
// 工具函数
// ============================

function formatBytes(bytes) {
  if (!bytes) return '0B';
  const sizes = ['B', 'KB', 'MB', 'GB', 'TB'];
  const i = Math.floor(Math.log(bytes) / Math.log(1024));
  return (bytes / Math.pow(1024, i)).toFixed(1) + sizes[i];
}

// ============================
// CLI
// ============================

async function cli() {
  const args = process.argv.slice(2);
  const cmd = args[0];

  switch (cmd) {
    case 'check': {
      const status = await checkOllama();
      console.log(JSON.stringify(status, null, 2));
      break;
    }
    case 'list': {
      const models = await listModels();
      console.log(JSON.stringify(models, null, 2));
      break;
    }
    case 'pull': {
      const name = args[1];
      if (!name) { console.log('用法: node ollama.js pull <模型名>'); process.exit(1); }
      const result = await pullModel(name);
      console.log(JSON.stringify(result));
      break;
    }
    case 'chat': {
      const model = args[1];
      if (!model) { console.log('用法: node ollama.js chat <模型名>'); process.exit(1); }
      const messages = [
        { role: 'system', content: '你是一个有用的 AI 助手。请简洁回答。' },
        { role: 'user', content: args.slice(2).join(' ') || '你好' },
      ];
      console.log(`🧠 对话 (${model})...`);
      const result = await chat(model, messages, { stream: true, onToken: (t) => process.stdout.write(t) });
      process.stdout.write('\n\n');
      console.log(JSON.stringify({ duration: result.totalDuration, tokens: result.evalCount }, null, 2));
      break;
    }
    case 'embed': {
      const text = args.slice(1).join(' ');
      if (!text) { console.log('用法: node ollama.js embed <文本>'); process.exit(1); }
      const result = await embed('nomic-embed-text', text);
      console.log(JSON.stringify({
        dimension: result.dimension,
        vector: `[${result.embedding.slice(0, 5).map(v => v.toFixed(4)).join(', ')}...]`,
        fullLength: result.embedding.length,
      }, null, 2));
      break;
    }
    case 'recommend': {
      const task = args[1] || 'all';
      if (task === 'all') {
        for (const [t, recs] of Object.entries({
          'embed': recommendModel('embed'),
          'code': recommendModel('code'),
          'chat': recommendModel('chat'),
          'reasoning': recommendModel('reasoning'),
          'vision': recommendModel('vision'),
        })) {
          console.log(`\n## ${t}`);
          recs.forEach(r => console.log(`  ${r.name} (${r.size}) — ${r.desc}`));
        }
      } else {
        const recs = recommendModel(task);
        console.log(`推荐 ${task} 模型:`);
        recs.forEach(r => console.log(`  ${r.name} (${r.size}) — ${r.desc}`));
      }
      break;
    }
    default:
      console.log('用法:');
      console.log('  node ollama.js check                    — 检查 Ollama');
      console.log('  node ollama.js list                     — 列出模型');
      console.log('  node ollama.js pull <模型名>             — 下载模型');
      console.log('  node ollama.js chat <模型名> [消息]      — 对话');
      console.log('  node ollama.js embed <文本>              — 获取嵌入');
      console.log('  node ollama.js recommend [任务类型]      — 推荐模型');
      console.log('');
      console.log('任务类型: embed, code, chat, reasoning, vision');
      break;
  }
}

if (require.main === module) {
  cli().catch(e => {
    console.error('Error:', e.message);
    process.exit(1);
  });
}

module.exports = {
  checkOllama,
  listModels,
  pullModel,
  chat,
  generate,
  embed,
  recommendModel,
};
