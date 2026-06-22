const fs = require('fs');
const path = require('path');
const { Storage } = require('../lib/storage');
const { guard } = require('../lib/lock');

guard(false);

const KB_NAME = 'graph';
const GRAPH_DIR = path.join(__dirname, '..', '..', 'state', 'gbrain', KB_NAME);

function ensureGraphDir() {
  if (!fs.existsSync(GRAPH_DIR)) {
    fs.mkdirSync(GRAPH_DIR, { recursive: true });
  }
}

function addRelation(from, to, label) {
  const docId = `rel:${Date.now()}`;
  const store = new Storage(KB_NAME);
  store.addDocument({
    id: docId,
    title: `${from} → ${to}`,
    content: label,
    source: `file://${GRAPH_DIR}/${docId}.json`,
    timestamp: new Date().toISOString(),
    embedding: []
  });
  console.log(`[✓] 关系已添加: ${from} → ${to} (${label})`);
}

function listRelations() {
  const store = new Storage(KB_NAME);
  store.getDocuments().then(docs => {
    docs.forEach(doc => {
      console.log(`${doc.id} | ${doc.title} | ${doc.content}`);
    });
  });
}

// CLI
if (process.argv.includes('--add')) {
  const index = process.argv.indexOf('--add');
  const from = process.argv[index + 1];
  const to = process.argv[index + 2];
  const label = process.argv.slice(index + 3).join(' ');
  if (!from || !to || !label) {
    console.error('❌ 缺少参数');
    process.exit(1);
  }
  addRelation(from, to, label);
} else if (process.argv.includes('--list')) {
  listRelations();
}