const { Storage } = require('./storage');

const store = new Storage('auto-scan');

store.search('测试').then(results => {
  console.log('🔍 搜索结果:', results);
}).catch(e => {
  console.error('❌ 搜索失败:', e.message);
});