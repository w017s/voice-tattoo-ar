Page({
  data: {
    tattooImages: {},
  },

  // 上传音频文件
  uploadAudio() {
    wx.chooseMessageFile({
      count: 1,
      type: 'file',
      extension: ['mp3', 'wav', 'm4a'],
      success: (res) => {
        const file = res.tempFiles[0];

        // 上传文件到后端
        wx.uploadFile({
          url: 'http://192.168.1.50:5000/upload',  // 替换成你的后端服务器 IP 地址
          filePath: file.path,
          name: 'file',
          success: (res) => {
            const data = JSON.parse(res.data);
            if (data.success) {
              this.setData({ tattooImages: data.images });
            } else {
              wx.showToast({ title: '上传失败', icon: 'none' });
            }
          },
          fail: () => {
            wx.showToast({ title: '上传失败', icon: 'none' });
          }
        });
      }
    });
  },

  // 跳转到 AR 页面
  tryOnAR(e) {
    const style = e.currentTarget.dataset.style;
    const tattooImageUrl = this.data.tattooImages[style];
    if (!tattooImageUrl) {
      wx.showToast({ title: '请先上传音频生成纹身图案', icon: 'none' });
      return;
    }

    wx.navigateTo({
      url: `/pages/ar/ar?tattoo=${encodeURIComponent(tattooImageUrl)}`
    });
  }
});
