#!/usr/bin/env node
/**
 * gbrain - 核心嵌入引擎
 * 
 * 轻量级嵌入生成器，无需外部依赖。
 * 内置 TF-IDF 向量化 + 余弦相似度。
 */

const fs = require('fs');
const path = require('path');

const ROOT = process.env.GBRAIN_ROOT || path.join(__dirname, '..', '..', 'state', 'gbrain');

// 中文+英文常用停用词
const STOP_WORDS = new Set([
  '的', '了', '在', '是', '我', '有', '和', '就', '不', '人', '都', '一',
  '一个', '上', '也', '很', '到', '说', '要', '去', '你', '会', '着',
  '没有', '看', '好', '自己', '这', '他', '她', '它', '们',
  'the', 'a', 'an', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
  'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could',
  'should', 'may', 'might', 'shall', 'can', 'need', 'dare', 'ought',
  'used', 'this', 'that', 'these', 'those', 'i', 'me', 'my', 'myself',
  'we', 'us', 'our', 'ours', 'you', 'your', 'yours', 'he', 'him', 'his',
  'she', 'her', 'hers', 'it', 'its', 'they', 'them', 'their', 'theirs',
  'what', 'which', 'who', 'whom', 'whose', 'why', 'how', 'when', 'where',
  'and', 'but', 'or', 'nor', 'not', 'no', 'so', 'yet', 'if', 'because',
  'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about',
  'against', 'between', 'into', 'through', 'during', 'before', 'after',
  'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off',
  'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there',
  'all', 'each', 'every', 'both', 'few', 'more', 'most', 'other', 'some',
  'such', 'only', 'own', 'same', 'than', 'too', 'very', 'just', 'also',
  'any', 'about', 'get', 'use', 'like', 'make', 'take', 'know', 'see',
  'think', 'come', 'go', 'look', 'want', 'give', 'tell', 'find', 'leave'
]);

// 中文二元分词（bigram）：把中文文本拆成重叠的2-gram，提升相似度区分度
function bigramTokenize(text) {
  const tokens = [];
  // 先提取英文单词
  const engPattern = /[a-zA-Z]+/g;
  let match;
  while ((match = engPattern.exec(text)) !== null) {
    const token = match[0].toLowerCase().trim();
    if (token.length > 1 && !STOP_WORDS.has(token)) {
      tokens.push(token);
    }
  }
  // 提取中文，做 bigram
  const cnChars = text.replace(/[a-zA-Z0-9\s]/g, '');
  for (let i = 0; i < cnChars.length - 1; i++) {
    const bigram = cnChars.substring(i, i + 2);
    if (bigram.trim().length === 2) {
      tokens.push(bigram);
    }
  }
  return tokens;
}

function tokenize(text) {
  // 使用 bigram 分词获得更好的语义区分
  return bigramTokenize(text);
}

function computeTF(tokens) {
  const tf = {};
  for (const t of tokens) {
    tf[t] = (tf[t] || 0) + 1;
  }
  const len = tokens.length || 1;
  for (const t in tf) {
    tf[t] /= len;
  }
  return tf;
}

function computeIDF(docs) {
  const idf = {};
  const N = docs.length;
  for (const doc of docs) {
    const seen = new Set();
    for (const t of tokenize(doc)) {
      if (seen.has(t)) continue;
      seen.add(t);
      idf[t] = (idf[t] || 0) + 1;
    }
  }
  for (const t in idf) {
    idf[t] = Math.log((N + 1) / (idf[t] + 1)) + 1;
  }
  return idf;
}

function vectorize(text, idf) {
  const tokens = tokenize(text);
  const tf = computeTF(tokens);
  const vec = {};
  for (const t in tf) {
    vec[t] = tf[t] * (idf[t] || 1);
  }
  return vec;
}

function dotProduct(a, b) {
  let sum = 0;
  for (const k in a) {
    if (k in b) sum += a[k] * b[k];
  }
  return sum;
}

function magnitude(v) {
  let sum = 0;
  for (const k in v) sum += v[k] * v[k];
  return Math.sqrt(sum);
}

function cosineSimilarity(a, b) {
  const dot = dotProduct(a, b);
  const mag = magnitude(a) * magnitude(b);
  return mag === 0 ? 0 : dot / mag;
}

class EmbedEngine {
  constructor(kbName) {
    this.kbName = kbName;
    this.kbDir = path.join(ROOT, kbName);
    this.idfFile = path.join(this.kbDir, 'idf.json');
    this.idf = {};
    this._loadIDF();
  }

  _loadIDF() {
    try {
      if (fs.existsSync(this.idfFile)) {
        this.idf = JSON.parse(fs.readFileSync(this.idfFile, 'utf-8'));
      }
    } catch (e) {
      this.idf = {};
    }
  }

  saveIDF() {
    try {
      if (!fs.existsSync(this.kbDir)) {
        fs.mkdirSync(this.kbDir, { recursive: true });
      }
      fs.writeFileSync(this.idfFile, JSON.stringify(this.idf));
    } catch (e) {
      console.error('saveIDF error:', e.message);
    }
  }

  updateIDF(docs) {
    const newIDF = computeIDF(docs);
    // Merge with existing
    for (const t in newIDF) {
      this.idf[t] = Math.max(this.idf[t] || 0, newIDF[t]);
    }
    this.saveIDF();
  }

  embed(text) {
    return vectorize(text, this.idf);
  }

  similarity(vectorA, vectorB) {
    return cosineSimilarity(vectorA, vectorB);
  }

  /**
   * 搜索：返回排序后的 { text, score, metadata }[]
   */
  search(query, docs, options = {}) {
    const { limit = 10, threshold = 0.0 } = options;
    const qVec = this.embed(query);
    const results = docs.map(doc => ({
      ...doc,
      score: cosineSimilarity(qVec, doc.vector || this.embed(doc.text))
    }));
    results.sort((a, b) => b.score - a.score);
    return results.filter(r => r.score >= threshold).slice(0, limit);
  }

  /**
   * 混合搜索：向量 + FTS5 分数加权合并
   */
  hybridSearch(query, docs, ftsResults = [], options = {}) {
    const { limit = 10, alpha = 0.6 } = options; // alpha: 语义权重
    const semanticResults = this.search(query, docs, { limit: limit * 2 });
    
    // 构建结果映射
    const merged = new Map();
    
    for (const r of semanticResults) {
      merged.set(r.id, { ...r, semanticScore: r.score });
    }
    
    for (const r of ftsResults) {
      if (merged.has(r.id)) {
        merged.get(r.id).ftsScore = r.score || 0.5;
      } else {
        merged.set(r.id, { ...r, semanticScore: 0, ftsScore: r.score || 0.5 });
      }
    }
    
    // 归一化 + 加权融合
    let maxSem = 0, maxFts = 0;
    for (const r of merged.values()) {
      if (r.semanticScore > maxSem) maxSem = r.semanticScore;
      if ((r.ftsScore || 0) > maxFts) maxFts = r.ftsScore;
    }
    maxSem = maxSem || 1;
    maxFts = maxFts || 1;
    
    const results = Array.from(merged.values()).map(r => ({
      ...r,
      score: alpha * (r.semanticScore / maxSem) + (1 - alpha) * ((r.ftsScore || 0) / maxFts)
    }));
    
    results.sort((a, b) => b.score - a.score);
    return results.slice(0, limit);
  }
}

module.exports = { EmbedEngine, tokenize, cosineSimilarity };

// CLI mode
if (require.main === module) {
  const args = process.argv.slice(2);
  const cmd = args[0];
  
  if (cmd === 'embed' && args[1]) {
    const engine = new EmbedEngine('_default');
    const vec = engine.embed(args[1]);
    console.log(JSON.stringify({ tokens: Object.keys(vec).length, vector: vec }));
  } else if (cmd === 'similarity' && args[1] && args[2]) {
    const engine = new EmbedEngine('_default');
    const a = engine.embed(args[1]);
    const b = engine.embed(args[2]);
    console.log(`Similarity: ${engine.similarity(a, b).toFixed(4)}`);
  } else {
    console.log(`Usage: node embed.js embed <text>`);
    console.log(`       node embed.js similarity <textA> <textB>`);
  }
}
