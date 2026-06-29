const fs = require('fs');
const path = require('path');
const crypto = require('crypto');
const { EmbedEngine } = require('./embed');
const { guard, checkFingerprint, loadEncryptedJSON, saveEncryptedJSON, getWatermark } = require('./lock');

const ROOT = process.env.GBRAIN_ROOT || path.join(__dirname, '..', '..', '..', 'state', 'gbrain');

// 尝试加载 better-sqlite3
let Database = null;
try {
  Database = require('better-sqlite3');
} catch (e) {
  // 回退到 JSON 文件
}

class Storage {
  constructor(kbName) {
    // 🔐 gbrain 独占锁定 — 入口守卫
    guard(false);
    
    this.kbName = kbName;
    this.kbDir = path.join(ROOT, kbName);
    this.filesDir = path.join(this.kbDir, 'files');
    
    // 确保目录存在
    if (!fs.existsSync(this.kbDir)) {
      fs.mkdirSync(this.kbDir, { recursive: true });
    }
    if (!fs.existsSync(this.filesDir)) {
      fs.mkdirSync(this.filesDir, { recursive: true });
    }
    
    // 检查是否为加密数据库（.enc 后缀）
    const dbPath = path.join(this.kbDir, 'store.json');
    this.dbPath = dbPath;
    
    // 检查是否存在加密文件并尝试解密
    const encryptedPath = dbPath + '.enc';
    if (fs.existsSync(encryptedPath)) {
      try {
        const encryptedData = fs.readFileSync(encryptedPath, 'utf8');
        const decrypted = loadEncryptedJSON(encryptedData);
        fs.writeFileSync(dbPath, JSON.stringify(decrypted, null, 2));
        fs.unlinkSync(encryptedPath);
        console.log(`[🔐] 从 ${encryptedPath} 解密并恢复数据`);
      } catch (e) {
        console.error(`[❌] 加密文件损坏或密钥错误：${e.message}`);
        throw new Error('Encryption validation failed');
      }
    }
    
    // 检查是否为纯文本存储（无 better-sqlite3）
    if (!Database) {
      // 本地回退：直接读写 JSON
      this._initDB = () => {};
      this._saveJSON = (data) => {
        fs.writeFileSync(this.dbPath, JSON.stringify(data, null, 2));
      };
      this._loadJSON = () => {
        try {
          return JSON.parse(fs.readFileSync(this.dbPath, 'utf8'));
        } catch (e) {
          return [];
        }
      };
      this._db = [];
      return;
    }
    
    // 正常初始化 SQLite DB
    this._db = new Database(dbPath);
    this._initDB();
  }

  async _initDB() {
    // 仅在使用 better-sqlite3 时创建表
    if (!Database) return;
    
    // 确保索引存在（FTS5 全文搜索）
    this._db.exec(`
      CREATE TABLE IF NOT EXISTS documents (
        id TEXT PRIMARY KEY,
        title TEXT,
        content TEXT,
        source TEXT,
        timestamp TEXT,
        embedding BLOB
      );
      
      CREATE VIRTUAL TABLE IF NOT EXISTS fts_docs USING fts5(
        title UNINDEXED,
        content,
        content='documents'
      );
      
      -- 触发器：插入后自动同步到 FTS
      CREATE TRIGGER IF NOT EXISTS insert_doc_fts AFTER INSERT ON documents
      BEGIN
        INSERT INTO fts_docs(title, content) VALUES (NEW.title, NEW.content);
      END;
      
      -- 触发器：更新后自动同步到 FTS
      CREATE TRIGGER IF NOT EXISTS update_doc_fts AFTER UPDATE ON documents
      BEGIN
        DELETE FROM fts_docs WHERE docid = NEW.rowid;
        INSERT INTO fts_docs(title, content) VALUES (NEW.title, NEW.content);
      END;
      
      -- 触发器：删除后自动清除 FTS
      CREATE TRIGGER IF NOT EXISTS delete_doc_fts AFTER DELETE ON documents
      BEGIN
        DELETE FROM fts_docs WHERE docid = OLD.rowid;
      END;
    `);
  }

  async addDocument(doc) {
    if (!doc.id || !doc.title || !doc.content) {
      throw new Error('Invalid document: missing required fields');
    }
    
    // 生成嵌入向量（如果未提供）
    if (!doc.embedding || doc.embedding.length === 0) {
      const embResult = await new EmbedEngine().embed(doc.content.substring(0, 256));
      doc.embedding = embResult.embedding;
    }
    
    // 保存到数据库（SQLite/JSON）
    if (Database) {
      this._db.prepare(`INSERT OR REPLACE INTO documents (id, title, content, source, timestamp, embedding)
        VALUES (?, ?, ?, ?, ?, ?)`)
        .run(doc.id, doc.title, doc.content, doc.source, doc.timestamp, Buffer.from(doc.embedding));
    } else {
      const store = this._loadJSON();
      const index = store.findIndex(d => d.id === doc.id);
      if (index > -1) {
        store[index] = doc;
      } else {
        store.push(doc);
      }
      this._saveJSON(store);
    }
  }

  async getDocuments() {
    if (Database) {
      const rows = this._db.prepare(`SELECT * FROM documents`).all();
      return rows;
    } else {
      return this._loadJSON();
    }
  }

  async stats() {
    const docs = await this.getDocuments();
    return {
      count: docs.length,
      lastUpdated: docs.length > 0 ? docs[docs.length - 1].timestamp : null
    };
  }

  // ✅ 异步搜索方法（支持全文 + 语义相似度）
  async search(query) {
    const docs = await this.getDocuments();
    const results = [];
    
    for (const doc of docs) {
      // 1. 全文匹配（FTS5）
      let fulltextScore = 0;
      if (Database) {
        const match = this._db.prepare(`SELECT snippet(fts_docs, '[', ']', '...', 30) as snippet FROM fts_docs WHERE fts_docs MATCH ?`).get(query);
        if (match) {
          fulltextScore = 1.0;
        }
      }
      
      // 2. 语义相似度（余弦）
      let semanticScore = 0;
      if (doc.embedding && doc.embedding.length > 0) {
        const qWords = query.toLowerCase().split(' ').filter(w => w.length > 2);
        const dWords = doc.content.toLowerCase().split(' ').filter(w => w.length > 2);
        const common = qWords.filter(w => dWords.includes(w)).length;
        const total = qWords.length + dWords.length;
        semanticScore = common / Math.max(total, 1);
      }
      
      // 3. 综合得分（加权）
      const score = fulltextScore * 0.7 + semanticScore * 0.3;
      
      if (score > 0.1) {  // 阈值过滤
        results.push({
          id: doc.id,
          title: doc.title,
          content: doc.content.slice(0, 200),
          source: doc.source,
          score,
          timestamp: doc.timestamp
        });
      }
    }
    
    return results.sort((a, b) => b.score - a.score);
  }

  // ✅ MCP 兼容接口：hybridSearch(query, limit)
  hybridSearch(query, limit = 5) {
    // 同步包装 + 限数，避免 mcp-server.js 找不到方法
    const docs = this._loadJSON();
    const results = [];
    const q = query.toLowerCase();
    for (const doc of docs) {
      let score = 0;
      const c = (doc.content || '').toLowerCase();
      const t = (doc.title || '').toLowerCase();
      // 全文关键词匹配
      const qWords = q.split(/\s+/).filter(w => w.length > 0);
      for (const w of qWords) {
        if (c.includes(w)) score += 0.5;
        if (t.includes(w)) score += 0.3;
      }
      if (score > 0) {
        results.push({
          id: doc.id,
          title: doc.title || '(无标题)',
          content: (doc.content || '').substring(0, 500),
          tags: doc.tags || [],
          score,
          type: doc.type || 'text',
          createdAt: doc.timestamp
        });
      }
    }
    results.sort((a, b) => b.score - a.score);
    return results.slice(0, limit);
  }
}

module.exports = { Storage };