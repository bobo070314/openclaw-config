// gbrain 全栈 — 数据模型定义
// 定义知识库文档、笔记、关系的数据结构

/**
 * 文档结构
 * @typedef {Object} Document
 * @property {string} id - 唯一 ID
 * @property {string} title - 标题
 * @property {string} content - 内容
 * @property {string} type - 类型 (text/code/url/file)
 * @property {string[]} tags - 标签
 * @property {string} [filePath] - 文件路径（如果是文件）
 * @property {number} [page] - 页码（如果是 PDF）
 * @property {string} source - 来源
 * @property {string} createdAt - 创建时间
 */

/**
 * 笔记结构
 * @typedef {Object} Note
 * @property {string} id - 唯一 ID
 * @property {string} title - 笔记标题
 * @property {string} content - 笔记内容（Markdown）
 * @property {string[]} tags - 标签
 * @property {string} createdAt - 创建时间
 * @property {string} updatedAt - 更新时间
 */

/**
 * 实体（知识图谱节点）
 * @typedef {Object} Entity
 * @property {string} id - 唯一 ID
 * @property {string} name - 实体名称
 * @property {string} type - 类型 (concept/tool/person/project)
 * @property {string} [description] - 描述
 */

/**
 * 关系（知识图谱边）
 * @typedef {Object} Relation
 * @property {string} id - 唯一 ID
 * @property {string} from - 源实体 ID
 * @property {string} to - 目标实体 ID
 * @property {string} type - 关系类型 (depends/contains/related/extends)
 */

module.exports = {
  Document: class Document {
    constructor({ title, content, type = 'text', tags = [], source = '', filePath = null, page = null }) {
      this.title = title;
      this.content = content;
      this.type = type;
      this.tags = tags;
      this.source = source;
      this.filePath = filePath;
      this.page = page;
    }
  },
  Note: class Note {
    constructor({ title, content, tags = [] }) {
      this.title = title;
      this.content = content;
      this.tags = tags;
    }
  },
  Entity: class Entity {
    constructor({ name, type = 'concept', description = '' }) {
      this.name = name;
      this.type = type;
      this.description = description;
    }
  },
  Relation: class Relation {
    constructor({ from, to, type = 'related' }) {
      this.from = from;
      this.to = to;
      this.type = type;
    }
  }
};
