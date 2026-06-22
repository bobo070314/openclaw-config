const fs = require('fs');
const path = require('path');
const { Storage } = require('../lib/storage');
const { guard } = require('../lib/lock');

guard(false);

const KB_NAME = 'notes';
const NOTE_DIR = path.join(__dirname, '..', '..', 'state', 'gbrain', KB_NAME);

function ensureNoteDir() {
  if (!fs.existsSync(NOTE_DIR)) {
    fs.mkdirSync(NOTE_DIR, { recursive: true });
  }
}

function createNote(title, content) {
  const docId = `note:${Date.now()}`;
  const store = new Storage(KB_NAME);
  store.addDocument({
    id: docId,
    title,
    content,
    source: `file://${NOTE_DIR}/${docId}.md`,
    timestamp: new Date().toISOString(),
    embedding: []
  });
  console.log(`[✓] 笔记已创建: ${title}`);
}

function listNotes() {
  const store = new Storage(KB_NAME);
  store.getDocuments().then(docs => {
    docs.forEach(doc => {
      console.log(`${doc.id} | ${doc.title} | ${doc.timestamp}`);
    });
  });
}

// CLI
if (process.argv.includes('--create')) {
  const index = process.argv.indexOf('--create');
  const title = process.argv[index + 1];
  const content = process.argv.slice(index + 2).join(' ');
  if (!title || !content) {
    console.error('❌ 缺少标题或内容');
    process.exit(1);
  }
  createNote(title, content);
} else if (process.argv.includes('--list')) {
  listNotes();
}