/** gbrain 文档详情页逻辑 */
const api = require('../../utils/api');

Page({
  data: {
    doc: {},
    kbName: ''
  },

  onLoad(options) {
    const { id, kb } = options;
    this.setData({ kbName: kb });

    const eventChannel = this.getOpenerEventChannel();
    eventChannel.on('docData', (data) => {
      this.setData({ doc: data });
    });
  }
});
