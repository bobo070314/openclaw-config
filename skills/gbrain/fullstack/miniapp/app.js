// gbrain 小程序入口
App({
  globalData: {
    // 修改为实际服务器地址（开发时用局域网 IP）
    baseUrl: 'http://localhost:3001',
    userInfo: null
  },
  onLaunch() {
    console.log('🧠 gbrain 小程序启动');
  }
});
