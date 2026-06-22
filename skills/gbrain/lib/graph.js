#!/usr/bin/env node
/**
 * gbrain 知识图谱引擎
 * 
 * 实体关系图：将知识库中的实体及其关系以图结构存储。
 * 支持实体识别、关系抽取、图查询、可视化导出。
 * 
 * 完全不依赖外部图数据库，纯内存 + JSON 文件存储。
 * 
 * 核心数据结构:
 *   entities: { id: { name, type, aliases, metadata, createdAt, updatedAt } }
 *   relations: [{ id, source, target, type, weight, metadata, createdAt }]
 */

const fs = require('fs');
const path = require('path');

class KnowledgeGraph {
  /**
   * @param {string} kbPath - 知识库路径 (state/gbrain/<kb_name>/)
   * @param {object} [options]
   * @param {number} [options.maxEntities=10000] - 最大实体数
   * @param {number} [options.maxRelations=50000] - 最大关系数
   */
  constructor(kbPath, options = {}) {
    this.kbPath = kbPath;
    this.maxEntities = options.maxEntities || 10000;
    this.maxRelations = options.maxRelations || 50000;
    this.graphPath = path.join(kbPath, 'knowledge-graph.json');
    
    // 加载或初始化
    this.entities = new Map();
    this.relations = [];
    this.entityIndex = new Map(); // name -> id
    
    this._load();
  }

  // ============================
  // 实体操作
  // ============================

  /**
   * 添加实体
   */
  addEntity(name, type = 'concept', metadata = {}) {
    // 去重
    if (this.entityIndex.has(name)) {
      const id = this.entityIndex.get(name);
      const entity = this.entities.get(id);
      entity.updatedAt = Date.now();
      Object.assign(entity.metadata, metadata);
      this._save();
      return entity;
    }

    const id = `ent_${Date.now()}_${Math.random().toString(36).substring(2, 8)}`;
    const entity = {
      id,
      name,
      type,  // concept, person, technology, organization, tool, language, framework, topic
      aliases: [],
      metadata,
      createdAt: Date.now(),
      updatedAt: Date.now(),
    };
    this.entities.set(id, entity);
    this.entityIndex.set(name, id);
    this._save();
    return entity;
  }

  /**
   * 为实体添加别名
   */
  addAlias(entityName, alias) {
    const id = this.entityIndex.get(entityName);
    if (!id) throw new Error(`实体 "${entityName}" 不存在`);
    const entity = this.entities.get(id);
    if (!entity.aliases.includes(alias)) {
      entity.aliases.push(alias);
      this.entityIndex.set(alias, id);
      this._save();
    }
  }

  /**
   * 通过名称查找实体（含别名搜索）
   */
  findEntity(name) {
    // 直接匹配
    if (this.entityIndex.has(name)) {
      return this.entities.get(this.entityIndex.get(name));
    }
    // 部分匹配
    for (const [id, entity] of this.entities) {
      if (entity.name.toLowerCase().includes(name.toLowerCase())) return entity;
      if (entity.aliases.some(a => a.toLowerCase().includes(name.toLowerCase()))) return entity;
    }
    return null;
  }

  /**
   * 列出所有实体（过滤、分页）
   */
  listEntities(filter = {}) {
    let results = Array.from(this.entities.values());
    
    if (filter.type) {
      results = results.filter(e => e.type === filter.type);
    }
    if (filter.search) {
      const q = filter.search.toLowerCase();
      results = results.filter(e => 
        e.name.toLowerCase().includes(q) || 
        e.aliases.some(a => a.toLowerCase().includes(q))
      );
    }

    const total = results.length;
    const page = filter.page || 1;
    const pageSize = filter.pageSize || 50;
    const start = (page - 1) * pageSize;
    
    return {
      total,
      page,
      pageSize,
      results: results.slice(start, start + pageSize),
    };
  }

  /**
   * 删除实体（级联删除关联关系）
   */
  deleteEntity(name) {
    const id = this.entityIndex.get(name);
    if (!id) return false;
    
    this.entities.delete(id);
    this.entityIndex.delete(name);
    
    // 删除该实体相关的所有关系
    const entity = this.entities.get(id);
    if (entity) {
      entity.aliases.forEach(a => this.entityIndex.delete(a));
    }
    this.relations = this.relations.filter(r => r.source !== id && r.target !== id);
    
    this._save();
    return true;
  }

  // ============================
  // 关系操作
  // ============================

  /**
   * 在两个实体之间创建关系
   */
  addRelation(sourceName, targetName, type = 'related_to', metadata = {}, weight = 1) {
    const source = this.findEntity(sourceName);
    const target = this.findEntity(targetName);

    if (!source) throw new Error(`源实体 "${sourceName}" 不存在`);
    if (!target) throw new Error(`目标实体 "${target.name}" 不存在`);

    // 去重：相同三元组只更新权重
    const existing = this.relations.find(r => 
      r.source === source.id && r.target === target.id && r.type === type
    );
    if (existing) {
      existing.weight += weight;
      existing.metadata = { ...existing.metadata, ...metadata };
      this._save();
      return existing;
    }

    const relation = {
      id: `rel_${Date.now()}_${Math.random().toString(36).substring(2, 6)}`,
      source: source.id,
      target: target.id,
      type,   // related_to, depends_on, extends, implements, contains, part_of, used_in
      weight,
      metadata,
      createdAt: Date.now(),
    };
    this.relations.push(relation);
    this._save();
    return relation;
  }

  /**
   * 增/减关系权重
   */
  strengthenRelation(sourceName, targetName, amount = 1) {
    const source = this.findEntity(sourceName);
    const target = this.findEntity(targetName);
    if (!source || !target) return false;

    let found = false;
    for (const r of this.relations) {
      if (r.source === source.id && r.target === target.id) {
        r.weight += amount;
        found = true;
      }
    }
    if (found) this._save();
    return found;
  }

  /**
   * 查询实体的相关实体（含关系方向）
   */
  getNeighbors(entityName, options = {}) {
    const entity = this.findEntity(entityName);
    if (!entity) return { entity: null, neighbors: [] };

    const depth = options.depth || 1;
    const maxDepth = Math.min(depth, 5); // 最多5层
    
    const visited = new Set([entity.id]);
    const results = [];
    let queue = [{ id: entity.id, depth: 0 }];

    while (queue.length > 0) {
      const current = queue.shift();
      if (current.depth >= maxDepth) continue;

      for (const rel of this.relations) {
        let neighborId = null;
        let direction = '';
        
        if (rel.source === current.id) {
          neighborId = rel.target;
          direction = 'outgoing';
        } else if (rel.target === current.id) {
          neighborId = rel.source;
          direction = 'incoming';
        }
        
        if (neighborId && !visited.has(neighborId)) {
          visited.add(neighborId);
          const neighbor = this.entities.get(neighborId);
          if (neighbor) {
            results.push({
              entity: neighbor,
              relation: rel,
              direction,
              depth: current.depth + 1,
            });
            queue.push({ id: neighborId, depth: current.depth + 1 });
          }
        }
      }
    }

    return {
      center: entity,
      neighbors: results,
      total: results.length,
    };
  }

  /**
   * 查找两个实体间的路径
   */
  findPath(sourceName, targetName) {
    const source = this.findEntity(sourceName);
    const target = this.findEntity(targetName);
    if (!source || !target) return null;

    // BFS 找最短路径
    const visited = new Set([source.id]);
    const queue = [{ id: source.id, path: [source.id] }];

    while (queue.length > 0) {
      const { id, path } = queue.shift();
      
      for (const rel of this.relations) {
        let nextId = null;
        if (rel.source === id) nextId = rel.target;
        else if (rel.target === id) nextId = rel.source;
        if (!nextId || visited.has(nextId)) continue;

        visited.add(nextId);
        const newPath = [...path, nextId];

        if (nextId === target.id) {
          return {
            path: newPath.map(id => ({
              entity: this.entities.get(id),
              relation: id === nextId ? null : this.relations.find(r => 
                (r.source === id && r.target === newPath[newPath.length - 2]) ||
                (r.target === id && r.source === newPath[newPath.length - 2])
              ),
            })),
            length: newPath.length - 1,
          };
        }
        queue.push({ id: nextId, path: newPath });
      }
    }
    return null; // 无路径
  }

  // ============================
  // 导出 & 统计
  // ============================

  /**
   * 导出为 D3 可视化数据格式
   */
  toD3Graph() {
    return {
      nodes: Array.from(this.entities.values()).map(e => ({
        id: e.id,
        name: e.name,
        type: e.type,
        group: ENTITY_TYPE_GROUPS[e.type] || 0,
      })),
      links: this.relations.map(r => ({
        source: r.source,
        target: r.target,
        type: r.type,
        weight: r.weight,
      })),
    };
  }

  /**
   * 统计
   */
  stats() {
    const typeCounts = {};
    const relationCounts = {};
    
    for (const entity of this.entities.values()) {
      typeCounts[entity.type] = (typeCounts[entity.type] || 0) + 1;
    }
    for (const rel of this.relations) {
      relationCounts[rel.type] = (relationCounts[rel.type] || 0) + 1;
    }

    return {
      totalEntities: this.entities.size,
      totalRelations: this.relations.length,
      entityTypes: typeCounts,
      relationTypes: relationCounts,
      avgRelationsPerEntity: this.entities.size > 0 
        ? (this.relations.length / this.entities.size).toFixed(2) 
        : 0,
      stronglyConnected: this._countStronglyConnected(),
    };
  }

  /**
   * 自动从文本中抽取实体和关系
   */
  extractFromText(text, sourceId) {
    const entityRegex = /([A-Z][a-zA-Z0-9]+(?:\s+[A-Z][a-zA-Z0-9]+)*)/g;
    const potentialEntities = new Set();
    let match;
    while ((match = entityRegex.exec(text)) !== null) {
      const word = match[1].trim();
      if (word.length >= 2 && !STOP_WORDS.has(word.toLowerCase())) {
        potentialEntities.add(word);
      }
    }

    const added = [];
    for (const name of potentialEntities) {
      try {
        const entity = this.addEntity(name, this._inferType(name), { source: sourceId });
        added.push(entity);
      } catch {}
    }

    // 实体出现在同一文本中的 → 创建关系
    if (added.length >= 2) {
      for (let i = 0; i < added.length; i++) {
        for (let j = i + 1; j < added.length; j++) {
          this.addRelation(added[i].name, added[j].name, 'co_occurrence', {}, 0.5);
        }
      }
    }

    return { extracted: added.length };
  }

  // ============================
  // 内部
  // ============================

  _inferType(name) {
    const patterns = [
      { types: ['person'], patterns: [/^[A-Z][a-z]+ [A-Z][a-z]+$/, /^[A-Z]\. [A-Z][a-z]+$/] },
      { types: ['technology'], patterns: [/JavaScript|TypeScript|Python|Rust|Go|React|Node|Docker|Kubernet/i] },
      { types: ['framework'], patterns: [/^[A-Z][a-z]+(?:JS|\.js|\.ts)$/, /Express|Next|Nest|Spring|Django|Flask|Laravel|Vue|Angular/i] },
      { types: ['tool'], patterns: [/^[A-Z]{2,}$/, /Git|NPM|Yarn|Webpack|Vite|ESLint|Prettier/i] },
      { types: ['organization'], patterns: [/Inc\.|Corp\.|LLC|Ltd\.|Google|Microsoft|Meta|Amazon|Apple/i] },
      { types: ['language'], patterns: [/^[A-Z][a-z]+(?:Script|Lang)$/i, /C\+\+|C#|Java|Swift|Kotlin|Ruby|PHP|Perl/i] },
    ];

    for (const { types, patterns: pats } of patterns) {
      for (const pat of pats) {
        if (pat.test(name)) return types[0];
      }
    }
    return 'concept';
  }

  _countStronglyConnected() {
    // 简化的连通分量计数
    const visited = new Set();
    let count = 0;

    const dfs = (id) => {
      visited.add(id);
      for (const r of this.relations) {
        if (r.source === id && !visited.has(r.target)) dfs(r.target);
        if (r.target === id && !visited.has(r.source)) dfs(r.source);
      }
    };

    for (const id of this.entities.keys()) {
      if (!visited.has(id)) {
        count++;
        dfs(id);
      }
    }
    return count;
  }

  _load() {
    try {
      if (fs.existsSync(this.graphPath)) {
        const data = JSON.parse(fs.readFileSync(this.graphPath, 'utf-8'));
        this.entities = new Map(Object.entries(data.entities || {}));
        this.relations = data.relations || [];
        
        // 重建名称索引
        for (const [id, entity] of this.entities) {
          this.entityIndex.set(entity.name, id);
          entity.aliases?.forEach(a => this.entityIndex.set(a, id));
        }
      }
    } catch (e) {
      console.warn(`知识图谱加载失败: ${e.message}，将创建新图`);
    }
  }

  _save() {
    try {
      const dir = path.dirname(this.graphPath);
      if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
      
      fs.writeFileSync(this.graphPath, JSON.stringify({
        entities: Object.fromEntries(this.entities),
        relations: this.relations,
        updatedAt: Date.now(),
      }, null, 2), 'utf-8');
    } catch (e) {
      console.error(`知识图谱保存失败: ${e.message}`);
    }
  }

  clear() {
    this.entities.clear();
    this.relations = [];
    this.entityIndex.clear();
    this._save();
  }
}

// ============================
// 常量
// ============================

const ENTITY_TYPE_GROUPS = {
  person: 1,
  technology: 2,
  framework: 3,
  tool: 4,
  organization: 5,
  language: 6,
  concept: 7,
  topic: 8,
};

const STOP_WORDS = new Set([
  'the', 'this', 'that', 'with', 'from', 'what', 'when', 'where', 'which',
  'how', 'why', 'who', 'whom', 'whose', 'and', 'but', 'for', 'nor', 'or',
  'yet', 'so', 'a', 'an', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
  'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'can', 'could',
  'shall', 'should', 'may', 'might', 'must', 'not', 'no', 'none', 'nothing',
  'hello', 'world', 'example', 'test', 'foo', 'bar', 'baz',
]);

// ============================
// CLI
// ============================

function cli() {
  const args = process.argv.slice(2);
  const cmd = args[0];
  const kbPath = args[1] || path.join(process.env.GBRAIN_ROOT || path.join(__dirname, '..', '..', 'state', 'gbrain'), 'default');

  const graph = new KnowledgeGraph(kbPath);

  switch (cmd) {
    case 'stats':
      console.log(JSON.stringify(graph.stats(), null, 2));
      break;

    case 'entity': {
      const action = args[2];
      const name = args[3];
      if (action === 'add' && name) {
        const type = args[4] || 'concept';
        const entity = graph.addEntity(name, type);
        console.log(`✅ 添加实体: ${entity.name} (${entity.type})`);
      } else if (action === 'list') {
        const filter = { page: parseInt(args[3]) || 1, type: args[4] };
        const result = graph.listEntities(filter);
        console.log(`共 ${result.total} 个实体:`);
        result.results.forEach(e => console.log(`  ${e.name} (${e.type})`));
      } else if (action === 'find' && name) {
        const entity = graph.findEntity(name);
        console.log(entity ? JSON.stringify(entity, null, 2) : '未找到');
      } else if (action === 'neighbors' && name) {
        const neighbors = graph.getNeighbors(name, { depth: parseInt(args[4]) || 1 });
        console.log(`"${name}" 的相邻实体 (${neighbors.total}):`);
        neighbors.neighbors.forEach(n => 
          console.log(`  ${n.direction === 'outgoing' ? '→' : '←'} ${n.entity.name} (${n.relation.type})`)
        );
      } else if (action === 'delete' && name) {
        const ok = graph.deleteEntity(name);
        console.log(ok ? `✅ 已删除"${name}"` : '未找到');
      } else if (action === 'extract') {
        const text = args.slice(4).join(' ');
        const result = graph.extractFromText(text);
        console.log(`提取了 ${result.extracted} 个实体`);
      } else {
        console.log('用法: node graph.js <kbPath> entity <add|list|find|neighbors|delete|extract> ...');
      }
      break;
    }

    case 'relation': {
      const source = args[2];
      const target = args[3];
      const type = args[4] || 'related_to';
      if (source && target) {
        const rel = graph.addRelation(source, target, type);
        console.log(`✅ 创建关系: ${source} —${type}→ ${target}`);
      }
      break;
    }

    case 'path': {
      const source = args[2];
      const target = args[3];
      if (source && target) {
        const p = graph.findPath(source, target);
        if (p) {
          console.log(`路径 (${p.length} 步):`);
          p.path.forEach((n, i) => console.log(`  ${n.entity?.name || '?'}${n.relation ? ` —${n.relation.type}→ ` : ''}`));
        } else {
          console.log('无连接路径');
        }
      }
      break;
    }

    case 'export':
      const format = args[2] || 'd3';
      if (format === 'd3') {
        const d3 = graph.toD3Graph();
        const outPath = path.join(kbPath, 'graph-d3.json');
        fs.writeFileSync(outPath, JSON.stringify(d3, null, 2));
        console.log(`✅ 导出到 ${outPath} (${d3.nodes.length}节点 / ${d3.links.length}关系)`);
      }
      break;

    case 'clear':
      graph.clear();
      console.log('✅ 知识图谱已清空');
      break;

    default:
      console.log('图形数据库引擎');
      console.log('用法:');
      console.log('  node graph.js <知识库路径> stats                    — 统计');
      console.log('  node graph.js <知识库路径> entity add <名称> [类型] — 添加实体');
      console.log('  node graph.js <知识库路径> entity list             — 列出实体');
      console.log('  node graph.js <知识库路径> entity find <名称>       — 查找实体');
      console.log('  node graph.js <知识库路径> entity neighbors <名称>  — 相邻实体');
      console.log('  node graph.js <知识库路径> entity extract <文本>    — 文本提取');
      console.log('  node graph.js <知识库路径> relation <源> <目标> [类型] — 创建关系');
      console.log('  node graph.js <知识库路径> path <源> <目标>         — 路径查找');
      console.log('  node graph.js <知识库路径> export [d3]             — 导出可视化');
      console.log('  node graph.js <知识库路径> clear                   — 清空');
      break;
  }
}

if (require.main === module) {
  cli();
}

module.exports = { KnowledgeGraph };
