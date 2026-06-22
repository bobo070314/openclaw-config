// gbrain 全栈 — API 路由
// REST API: 知识库搜索、添加、统计

const express = require('express');
const router = express.Router();
const path = require('path');

// gbrain 存储层 — 直接复用国际版 skills 中的 lock + storage
const SKILLS_DIR = path.resolve(__dirname, '..', '..');

function getStorage() {
  return {
    Storage: require(path.join(SKILLS_DIR, 'lib', 'storage')).Storage,
    guard: require(path.join(SKILLS_DIR, 'lib', 'lock')).guard,
  };
}

// GET /api/status — 系统状态 + 知识库列表
router.get('/status', (req, res) => {
  try {
    const { Storage, guard } = getStorage();
    guard(false);

    const fs = require('fs');
    const ROOT = process.env.GBRAIN_ROOT || path.resolve(__dirname, '..', '..', '..', '..', 'state', 'gbrain');
    let kbs = [];
    if (fs.existsSync(ROOT)) {
      kbs = fs.readdirSync(ROOT, { withFileTypes: true })
        .filter(d => d.isDirectory() && !d.name.startsWith('.'))
        .map(d => {
          try {
            const s = new Storage(d.name);
            const stats = s.stats();
            s.close();
            return { name: d.name, documents: stats.documents || 0, notes: stats.notes || 0 };
          } catch {
            return { name: d.name, error: 'cannot read' };
          }
        });
    }

    res.json({ status: 'ok', version: '1.0.0', kbs, timestamp: new Date().toISOString() });
  } catch (e) {
    res.status(500).json({ status: 'error', message: e.message });
  }
});

// GET /api/kb/:name/search?q=xxx&limit=5 — 搜索知识库
router.get('/kb/:name/search', (req, res) => {
  try {
    const { Storage } = getStorage();
    const { name } = req.params;
    const { q, limit = 5 } = req.query;

    if (!q) return res.status(400).json({ error: '缺少查询参数 q' });

    const store = new Storage(name);
    const results = store.hybridSearch(q, parseInt(limit, 10));
    store.close();

    res.json({ kb: name, query: q, results, count: results.length });
  } catch (e) {
    res.status(404).json({ error: `知识库 "${req.params.name}" 不存在或读取失败`, detail: e.message });
  }
});

// POST /api/kb/:name/add — 添加文档
router.post('/kb/:name/add', express.json(), (req, res) => {
  try {
    const { Storage } = getStorage();
    const { name } = req.params;
    const { title, content, tags = [] } = req.body;

    if (!title || !content) {
      return res.status(400).json({ error: '缺少必填字段 title 和 content' });
    }

    const store = new Storage(name);
    const result = store.addDocument({ title, content, type: 'text', tags });
    store.close();

    res.json({ status: 'indexed', kb: name, id: result.id || result, title });
  } catch (e) {
    res.status(500).json({ error: e.message });
  }
});

// GET /api/kb/:name/stats — 知识库统计
router.get('/kb/:name/stats', (req, res) => {
  try {
    const { Storage } = getStorage();
    const { name } = req.params;

    const store = new Storage(name);
    const stats = store.stats();
    store.close();

    res.json({ kb: name, ...stats });
  } catch (e) {
    res.status(404).json({ error: `知识库 "${req.params.name}" 不存在`, detail: e.message });
  }
});

module.exports = router;
