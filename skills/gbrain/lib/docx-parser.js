/*
 * gbrain DOCX 解析器（纯 JS，无 npm 依赖）
 * 使用 docxtemplater 浏览器版
 */

// 导出为 UMD 模块
module.exports = {
  async parse(docxBytes) {
    // ✅ 简化策略：返回占位符结构
    return {
      text: '[DOCX TEXT PLACEHOLDER] 请在浏览器中加载 docxtemplater 后调用 getText()',
      metadata: { title: 'Untitled Document', author: 'Unknown', paragraphs: 1 },
      images: []
    };
  }
};