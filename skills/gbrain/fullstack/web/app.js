// gbrain Web 管理后台 — 前端逻辑
const API = '/api';

let state = {
  kbs: [],
  selectedKB: null,
  results: [],
  stats: null
};

// ==== API 封装 ====
async function api(method, path, body) {
  const opts = {
    method,
    headers: { 'Content-Type': 'application/json' }
  };
  if (body) opts.body = JSON.stringify(body);
  const res = await fetch(`${API}${path}`, opts);
  return res.json();
}

// ==== 渲染 ====
function render() {
  renderHeader();
  renderKBList();
  renderSearch();
  renderAddForm();
  renderStats();
}

function renderHeader() {
  const el = document.getElementById('header-status');
  if (!el) return;
  api('GET', '/status').then(data => {
    el.innerHTML = `
      <span class="status-dot ${data.status === 'ok' ? 'ok' : 'error'}"></span>
      ${data.kbs.length} 知识库 · v${data.version}
    `;
    state.kbs = data.kbs || [];
    renderKBList();
  }).catch(() => {
    el.innerHTML = '<span class="status-dot error"></span> 无法连接';
  });
}

function renderKBList() {
  const el = document.getElementById('kb-list');
  if (!el) return;
  if (state.kbs.length === 0) {
    el.innerHTML = '<div class="empty-state">暂无知识库，请先在命令行创建</div>';
    return;
  }
  el.innerHTML = state.kbs.map(kb => `
    <div class="kb-card ${state.selectedKB === kb.name ? 'active' : ''}"
         onclick="selectKB('${kb.name}')">
      <h3>📚 ${kb.name}</h3>
      <div class="kb-stats">📄 ${kb.documents || 0} 文档 · 📝 ${kb.notes || 0} 笔记</div>
    </div>
  `).join('');
}

function selectKB(name) {
  state.selectedKB = name;
  state.results = [];
  state.stats = null;
  render();
  loadStats(name);
}

async function loadStats(name) {
  try {
    const data = await api('GET', `/kb/${name}/stats`);
    state.stats = data;
    renderStats();
  } catch (e) {
    console.error('加载统计失败:', e);
  }
}

function renderSearch() {
  const el = document.getElementById('search-panel');
  if (!el) return;
  const kbOptions = state.kbs.map(k =>
    `<option value="${k.name}" ${state.selectedKB === k.name ? 'selected' : ''}>${k.name}</option>`
  ).join('');

  el.innerHTML = `
    <h2>🔍 搜索</h2>
    <div class="search-row">
      <select id="search-kb" style="background:var(--bg);border:1px solid var(--border);border-radius:8px;padding:10px;color:var(--text);font-size:14px;">
        ${kbOptions}
      </select>
      <input type="text" id="search-query" placeholder="输入搜索关键词..." onkeydown="if(event.key==='Enter') doSearch()" />
      <button onclick="doSearch()">搜索</button>
    </div>
    <div id="search-results"></div>
  `;
}

async function doSearch() {
  const kb = document.getElementById('search-kb').value;
  const q = document.getElementById('search-query').value;
  if (!kb || !q) return showToast('请选择知识库并输入搜索词');

  try {
    const data = await api('GET', `/kb/${kb}/search?q=${encodeURIComponent(q)}&limit=10`);
    state.results = data.results || [];
    renderResults();
  } catch (e) {
    showToast('搜索失败: ' + e.message);
  }
}

function renderResults() {
  const el = document.getElementById('search-results');
  if (!el) return;
  if (state.results.length === 0) {
    el.innerHTML = '<div class="empty-state">没有找到结果</div>';
    return;
  }
  el.innerHTML = state.results.map(r => `
    <div class="result-item">
      <h4>${r.title || '(无标题)'}</h4>
      <p>${(r.content || '').substring(0, 200)}...</p>
      <span class="score">匹配度: ${(r.score || 0).toFixed(2)}</span>
    </div>
  `).join('');
}

function renderAddForm() {
  const el = document.getElementById('add-panel');
  if (!el) return;
  const kbOptions = state.kbs.map(k =>
    `<option value="${k.name}" ${state.selectedKB === k.name ? 'selected' : ''}>${k.name}</option>`
  ).join('');

  el.innerHTML = `
    <h2>📝 添加文档</h2>
    <div class="form-row">
      <label>目标知识库</label>
      <select id="add-kb" style="width:100%;background:var(--bg);border:1px solid var(--border);border-radius:8px;padding:10px;color:var(--text);font-size:14px;">
        ${kbOptions}
      </select>
    </div>
    <div class="form-row">
      <label>标题</label>
      <input type="text" id="add-title" placeholder="文档标题" />
    </div>
    <div class="form-row">
      <label>内容</label>
      <textarea id="add-content" placeholder="文档内容..."></textarea>
    </div>
    <div class="form-row">
      <label>标签（逗号分隔）</label>
      <input type="text" id="add-tags" placeholder="标签1, 标签2" />
    </div>
    <div class="form-actions">
      <button class="btn-primary" onclick="doAdd()">添加</button>
      <button class="btn-secondary" onclick="clearAddForm()">清空</button>
    </div>
  `;
}

async function doAdd() {
  const kb = document.getElementById('add-kb').value;
  const title = document.getElementById('add-title').value;
  const content = document.getElementById('add-content').value;
  const tagsStr = document.getElementById('add-tags').value;

  if (!title || !content) return showToast('请填写标题和内容');

  const tags = tagsStr ? tagsStr.split(/[,，]/).map(t => t.trim()).filter(Boolean) : [];

  try {
    const data = await api('POST', `/kb/${kb}/add`, { title, content, tags });
    showToast(`✅ 已添加: ${data.title}`);
    clearAddForm();
    loadStats(kb);
  } catch (e) {
    showToast('添加失败: ' + e.message);
  }
}

function clearAddForm() {
  ['add-title', 'add-content', 'add-tags'].forEach(id => {
    const el = document.getElementById(id);
    if (el) el.value = '';
  });
}

function renderStats() {
  const el = document.getElementById('stats-panel');
  if (!el) return;
  if (!state.stats) {
    el.innerHTML = '<div class="empty-state">选择一个知识库查看统计</div>';
    return;
  }
  el.innerHTML = `
    <h2>📊 知识库统计</h2>
    <div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(120px,1fr));gap:12px;">
      <div style="background:var(--bg);border:1px solid var(--border);border-radius:8px;padding:16px;text-align:center;">
        <div style="font-size:28px;font-weight:700;color:var(--accent);">${state.stats.documents || 0}</div>
        <div style="font-size:12px;color:var(--text-dim);margin-top:4px;">文档</div>
      </div>
      <div style="background:var(--bg);border:1px solid var(--border);border-radius:8px;padding:16px;text-align:center;">
        <div style="font-size:28px;font-weight:700;color:var(--success);">${state.stats.notes || 0}</div>
        <div style="font-size:12px;color:var(--text-dim);margin-top:4px;">笔记</div>
      </div>
      <div style="background:var(--bg);border:1px solid var(--border);border-radius:8px;padding:16px;text-align:center;">
        <div style="font-size:28px;font-weight:700;color:var(--warn);">${state.stats.entities || 0}</div>
        <div style="font-size:12px;color:var(--text-dim);margin-top:4px;">实体</div>
      </div>
      <div style="background:var(--bg);border:1px solid var(--border);border-radius:8px;padding:16px;text-align:center;">
        <div style="font-size:28px;font-weight:700;color:#9c27b0;">${state.stats.relations || 0}</div>
        <div style="font-size:12px;color:var(--text-dim);margin-top:4px;">关系</div>
      </div>
    </div>
  `;
}

let toastTimer = null;
function showToast(msg) {
  const existing = document.querySelector('.toast');
  if (existing) existing.remove();
  clearTimeout(toastTimer);

  const el = document.createElement('div');
  el.className = 'toast';
  el.textContent = msg;
  document.body.appendChild(el);

  toastTimer = setTimeout(() => el.remove(), 3000);
}

// 自动刷新
document.addEventListener('DOMContentLoaded', () => {
  render();
  setInterval(() => {
    renderHeader();
    if (state.selectedKB) loadStats(state.selectedKB);
  }, 30000);
});
