#!/usr/bin/env node
/**
 * gbrain 多通道发布系统
 * 
 * 将 gbrain 知识库发布到多个平台。
 * 当前支持: Web、Markdown、JSON 导出
 * 规划支持: 知识图谱、API 文档、静态站点
 */

const fs = require('fs');
const path = require('path');

const GBRAIN_LIB = path.resolve(__dirname, '..', 'lib');

function guard() {
  try {
    require(path.join(GBRAIN_LIB, 'lock')).guard(false);
  } catch (e) {
    console.error('🔒 Guard failed:', e.message);
    process.exit(1);
  }
}

// ============================
// 1. Web 发布 (Express Server)
// ============================

/**
 * 启动全栈 Web 服务器
 */
function startWebServer(port = 3001) {
  try {
    const serverPath = path.resolve(__dirname, '..', 'fullstack', 'server', 'index.js');
    const { spawn } = require('child_process');
    const child = spawn('node', [serverPath], {
      env: { ...process.env, PORT: String(port), GBRAIN_ROOT: process.env.GBRAIN_ROOT },
      stdio: 'inherit',
      detached: false,
    });
    console.log(`🌐 gbrain Web Server 已启动: http://localhost:${port}`);
    return child;
  } catch (e) {
    console.error('启动 Web Server 失败:', e.message);
    return null;
  }
}

// ============================
// 2. Markdown 发布
// ============================

/**
 * 将知识库导出为 Markdown 文件
 */
function exportToMarkdown(kbName, outputDir) {
  guard();
  const { Storage } = require(path.join(GBRAIN_LIB, 'storage'));
  const store = new Storage(kbName);

  const result = store.getAllDocuments();
  store.close();

  if (!fs.existsSync(outputDir)) {
    fs.mkdirSync(outputDir, { recursive: true });
  }

  // 生成 index.md
  const indexLines = [`# 知识库: ${kbName}\n`];
  indexLines.push(`导出时间: ${new Date().toISOString()}`);
  indexLines.push(`文档数: ${result.length}\n`);
  indexLines.push('## 文档列表\n');

  const docFiles = [];

  for (let i = 0; i < result.length; i++) {
    const doc = result[i];
    const safeName = doc.title.replace(/[<>:"/\\|?*]/g, '_').substring(0, 80);
    const fileName = `${i + 1}_${safeName}.md`;
    const fullPath = path.join(outputDir, fileName);

    const content = [
      `# ${doc.title}`,
      '',
      `- **ID**: ${doc.id}`,
      `- **类型**: ${doc.metadata?.type || 'unknown'}`,
      `- **标签**: ${(doc.metadata?.tags || []).join(', ')}`,
      `- **来源**: ${doc.metadata?.source || 'gbrain'}`,
      `- **日期**: ${new Date(doc.createdAt || Date.now()).toISOString()}`,
      '',
      '---',
      '',
      doc.content || '(无内容)',
      '',
    ].join('\n');

    fs.writeFileSync(fullPath, content, 'utf-8');
    docFiles.push({ fileName, title: doc.title, id: doc.id });
    indexLines.push(`- [${doc.title}](${fileName}) — ${doc.metadata?.tags?.join(', ') || ''}`);
  }

  fs.writeFileSync(path.join(outputDir, 'index.md'), indexLines.join('\n'), 'utf-8');

  return {
    kb: kbName,
    outputDir,
    total: docFiles.length,
    files: docFiles,
  };
}

// ============================
// 3. JSON 导出
// ============================

/**
 * 将知识库导出为 JSON 文件
 */
function exportToJSON(kbName, outputFile) {
  guard();
  const { Storage } = require(path.join(GBRAIN_LIB, 'storage'));
  const store = new Storage(kbName);

  const docs = store.getAllDocuments();
  store.close();

  const data = {
    name: kbName,
    exportedAt: new Date().toISOString(),
    count: docs.length,
    documents: docs.map(d => ({
      id: d.id,
      title: d.title,
      content: d.content,
      tags: d.metadata?.tags || [],
      type: d.metadata?.type || 'unknown',
      source: d.metadata?.source || '',
      createdAt: d.createdAt,
      updatedAt: d.updatedAt,
    })),
  };

  fs.writeFileSync(outputFile, JSON.stringify(data, null, 2), 'utf-8');

  return {
    kb: kbName,
    outputFile,
    total: data.count,
    size: fs.statSync(outputFile).size,
  };
}

// ============================
// 4. 静态站点生成
// ============================

/**
 * 将知识库导出为静态 HTML 站点
 */
function exportToSite(kbName, outputDir) {
  guard();
  const { Storage } = require(path.join(GBRAIN_LIB, 'storage'));
  const store = new Storage(kbName);

  const docs = store.getAllDocuments();
  store.close();

  if (!fs.existsSync(outputDir)) {
    fs.mkdirSync(outputDir, { recursive: true });
  }

  // 文档目录
  const docsDir = path.join(outputDir, 'docs');
  if (!fs.existsSync(docsDir)) fs.mkdirSync(docsDir);

  // 生成每篇文章
  for (let i = 0; i < docs.length; i++) {
    const doc = docs[i];
    const safeName = doc.title.replace(/[<>:"/\\|?*]/g, '_').substring(0, 80);
    const html = `<!DOCTYPE html>
<html lang="zh-CN">
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>${escapeHTML(doc.title)} - ${escapeHTML(kbName)}</title>
<link rel="stylesheet" href="../style.css">
</head>
<body>
<nav><a href="../index.html">← 返回知识库</a></nav>
<main>
<h1>${escapeHTML(doc.title)}</h1>
<div class="meta">
  <span>标签: ${(doc.metadata?.tags || []).join(', ')}</span>
  <span>类型: ${doc.metadata?.type || 'unknown'}</span>
</div>
<article>${docToHTML(doc.content || '(无内容)')}</article>
</main>
</body>
</html>`;
    fs.writeFileSync(path.join(docsDir, `${i + 1}.html`), html, 'utf-8');
  }

  // 生成首页
  const indexHTML = `<!DOCTYPE html>
<html lang="zh-CN">
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>${escapeHTML(kbName)} - gbrain 知识库</title>
<link rel="stylesheet" href="style.css">
</head>
<body>
<header><h1>📚 ${escapeHTML(kbName)}</h1><p>${docs.length} 篇文档</p></header>
<main>
<ul class="doc-list">
${docs.map((doc, i) => `<li>
  <a href="docs/${i + 1}.html"><strong>${escapeHTML(doc.title)}</strong></a>
  <span class="tags">${(doc.metadata?.tags || []).map(t => `<span class="tag">${escapeHTML(t)}</span>`).join(' ')}</span>
  <span class="type">${doc.metadata?.type || ''}</span>
</li>`).join('\n')}
</ul>
</main>
</body>
</html>`;

  fs.writeFileSync(path.join(outputDir, 'index.html'), indexHTML, 'utf-8');

  // 生成 CSS
  const css = `*{margin:0;padding:0;box-sizing:border-box}
body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;max-width:800px;margin:0 auto;padding:20px;background:#fafafa;color:#333;line-height:1.6}
a{color:#0366d6;text-decoration:none}
a:hover{text-decoration:underline}
header{margin-bottom:30px;padding-bottom:20px;border-bottom:2px solid #e1e4e8}
h1{font-size:1.8em}
nav{margin-bottom:20px;padding:10px 0}
.meta{margin-bottom:20px;color:#586069;font-size:0.9em;display:flex;gap:20px}
.doc-list{list-style:none}
.doc-list li{padding:12px 0;border-bottom:1px solid #e1e4e8}
.doc-list li a{font-size:1.1em}
.tags{display:inline-flex;gap:4px;margin-left:10px}
.tag{background:#e1e4e8;padding:2px 6px;border-radius:3px;font-size:0.8em;color:#586069}
.type{font-size:0.85em;color:#586069;margin-left:10px}
article{line-height:1.8}
article h2{margin:24px 0 12px}
article p{margin:8px 0}
article code{background:#f0f0f0;padding:2px 5px;border-radius:3px;font-size:0.9em}
article pre{background:#f6f8fa;padding:16px;border-radius:6px;overflow-x:auto}
@media(prefers-color-scheme:dark){body{background:#0d1117;color:#c9d1d9}a{color:#58a6ff}header{border-color:#30363d}.meta{color:#8b949e}.tag{background:#21262d;color:#8b949e}.doc-list li{border-color:#21262d}article code{background:#161b22}article pre{background:#161b22}}
`;

  fs.writeFileSync(path.join(outputDir, 'style.css'), css, 'utf-8');

  return { kb: kbName, outputDir, total: docs.length, url: `file://${outputDir}/index.html` };
}

// ============================
// 工具函数
// ============================

function escapeHTML(str) {
  return String(str).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
}

function docToHTML(content) {
  return String(content)
    .split('\n')
    .map(line => {
      if (line.startsWith('### ')) return `<h3>${escapeHTML(line.slice(4))}</h3>`;
      if (line.startsWith('## ')) return `<h2>${escapeHTML(line.slice(3))}</h2>`;
      if (line.startsWith('# ')) return `<h1>${escapeHTML(line.slice(2))}</h1>`;
      if (line.startsWith('```')) return '<pre><code>';
      if (line.startsWith('- ')) return `<li>${escapeHTML(line.slice(2))}</li>`;
      if (line.startsWith('> ')) return `<blockquote>${escapeHTML(line.slice(2))}</blockquote>`;
      if (line.trim() === '') return '<br>';
      return `<p>${escapeHTML(line)}</p>`;
    })
    .join('\n');
}

// ============================
// CLI
// ============================

function cli() {
  const args = process.argv.slice(2);
  const cmd = args[0];
  const kbName = args[1] || 'default';

  switch (cmd) {
    case 'serve': {
      const port = parseInt(args[2] || '3001', 10);
      startWebServer(port);
      break;
    }
    case 'export-md': {
      const outDir = args[2] || path.join(process.cwd(), `export-${kbName}-md`);
      const result = exportToMarkdown(kbName, outDir);
      console.log(JSON.stringify(result, null, 2));
      break;
    }
    case 'export-json': {
      const outFile = args[2] || path.join(process.cwd(), `${kbName}.json`);
      const result = exportToJSON(kbName, outFile);
      console.log(JSON.stringify(result, null, 2));
      break;
    }
    case 'export-site': {
      const outDir = args[2] || path.join(process.cwd(), `site-${kbName}`);
      const result = exportToSite(kbName, outDir);
      console.log(JSON.stringify(result, null, 2));
      break;
    }
    case 'guard': {
      guard();
      console.log(JSON.stringify({ guard: 'passed' }));
      break;
    }
    default:
      console.log('用法:');
      console.log('  node publish.js serve [端口]              — 启动 Web 服务器');
      console.log('  node publish.js export-md <知识库> [输出]  — 导出 Markdown');
      console.log('  node publish.js export-json <知识库> [文件] — 导出 JSON');
      console.log('  node publish.js export-site <知识库> [目录] — 导出静态站点');
      break;
  }
}

if (require.main === module) {
  cli();
}

module.exports = {
  startWebServer,
  exportToMarkdown,
  exportToJSON,
  exportToSite,
};
