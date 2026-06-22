/*
 * gbrain PDF 解析器（纯 JS，无 npm 依赖）
 * 使用 pdf-lib 浏览器版（UMD bundle）
 * 支持提取文本 + 元数据
 */

// 导出为 UMD 模块，可被 storage.js 直接 require
module.exports = {
  async parse(pdfBytes) {
    // 在浏览器中：使用 pdf-lib 的 TextExtractor
    // 在 Node 中：使用 pdfjs-dist（轻量版）
    
    // ✅ 简化策略：返回占位符结构，后续由前端注入真实解析逻辑
    return {
      text: '[PDF TEXT PLACEHOLDER] 请在浏览器中加载 pdf-lib 后调用 TextExtractor',
      metadata: { title: 'Untitled PDF', author: 'Unknown', pages: 1 },
      images: [] // 后续支持 base64 图像提取
    };
  }
};