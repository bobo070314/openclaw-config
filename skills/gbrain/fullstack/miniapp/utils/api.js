// gbrain 小程序 API 封装
const app = getApp();

/**
 * 请求封装
 */
function request(url, method = 'GET', data = {}) {
  return new Promise((resolve, reject) => {
    wx.request({
      url: app.globalData.baseUrl + url,
      method,
      data,
      header: { 'Content-Type': 'application/json' },
      success: res => resolve(res.data),
      fail: err => reject(err)
    });
  });
}

/**
 * 获取系统状态 + 知识库列表
 */
function getStatus() {
  return request('/api/status');
}

/**
 * 搜索知识库
 */
function searchKB(kbName, query, limit = 10) {
  return request(`/api/kb/${kbName}/search?q=${encodeURIComponent(query)}&limit=${limit}`);
}

/**
 * 添加文档
 */
function addDocument(kbName, title, content, tags = []) {
  return request(`/api/kb/${kbName}/add`, 'POST', { title, content, tags });
}

/**
 * 获取知识库统计
 */
function getStats(kbName) {
  return request(`/api/kb/${kbName}/stats`);
}

module.exports = {
  getStatus,
  searchKB,
  addDocument,
  getStats
};
