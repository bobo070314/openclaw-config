/** gbrain 首页逻辑 */
const api = require('../../utils/api');

Page({
  data: {
    kbList: [],
    kbNames: [],
    selectedKBIndex: 0,
    searchQuery: '',
    results: [],
    loading: false,
    searched: false
  },

  onLoad() {
    this.loadKBList();
  },

  onShow() {
    if (this.data.kbList.length > 0) return;
    this.loadKBList();
  },

  loadKBList() {
    api.getStatus().then(data => {
      const kbs = data.kbs || [];
      this.setData({
        kbList: kbs,
        kbNames: kbs.map(k => k.name),
        selectedKBIndex: 0
      });
    }).catch(err => {
      console.error('加载失败:', err);
      wx.showToast({ title: '无法连接服务器', icon: 'none' });
    });
  },

  onSearchInput(e) {
    this.setData({ searchQuery: e.detail.value });
  },

  onSearch() {
    const q = this.data.searchQuery;
    const kbName = this.data.kbNames[this.data.selectedKBIndex];
    if (!q || !kbName) {
      wx.showToast({ title: '请输入搜索词', icon: 'none' });
      return;
    }

    this.setData({ loading: true, searched: true });
    api.searchKB(kbName, q).then(data => {
      this.setData({ results: data.results || [], loading: false });
    }).catch(err => {
      this.setData({ loading: false });
      wx.showToast({ title: '搜索失败', icon: 'none' });
    });
  },

  onKBChange(e) {
    this.setData({ selectedKBIndex: e.detail.value, results: [], searched: false });
  },

  goDetail(e) {
    const id = e.currentTarget.dataset.id;
    const item = this.data.results.find(r => r.id === id);
    if (item) {
      wx.navigateTo({
        url: `/pages/detail/detail?id=${id}&kb=${this.data.kbNames[this.data.selectedKBIndex]}`,
        success: (res) => {
          res.eventChannel.emit('docData', item);
        }
      });
    }
  }
});
