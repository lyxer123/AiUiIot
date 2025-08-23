// app.js
App({
  globalData: {
    userInfo: null,
    // 服务器配置 - 需要根据实际网络环境修改
    serverConfig: {
      baseUrl: 'http://10.1.95.252:5000/api', // 修改为你的服务器IP
      timeout: 10000
    }
  },

  onLaunch() {
    // 小程序启动时执行
    console.log('ESP32控制小程序启动');
    
    // 检查微信版本
    this.checkWechatVersion();
    
    // 获取用户信息
    this.getUserProfile();
  },

  // 检查微信版本
  checkWechatVersion() {
    const systemInfo = wx.getSystemInfoSync();
    console.log('系统信息:', systemInfo);
    
    // 检查是否支持新版获取用户信息接口
    if (wx.getUserProfile) {
      console.log('支持新版getUserProfile接口');
    } else {
      console.log('使用旧版getUserInfo接口');
    }
  },

  // 获取用户信息
  getUserProfile() {
    // 这里先不主动获取，等用户点击授权按钮时再获取
    console.log('等待用户授权获取信息');
  },

  // 用户登录
  login() {
    return new Promise((resolve, reject) => {
      wx.login({
        success: (res) => {
          if (res.code) {
            console.log('微信登录成功，code:', res.code);
            resolve(res.code);
          } else {
            console.error('微信登录失败:', res.errMsg);
            reject(new Error(res.errMsg));
          }
        },
        fail: (err) => {
          console.error('微信登录异常:', err);
          reject(err);
        }
      });
    });
  },

  // 获取用户信息
  getUserProfile() {
    return new Promise((resolve, reject) => {
      if (wx.getUserProfile) {
        wx.getUserProfile({
          desc: '用于完善用户资料',
          success: (res) => {
            console.log('获取用户信息成功:', res.userInfo);
            this.globalData.userInfo = res.userInfo;
            resolve(res.userInfo);
          },
          fail: (err) => {
            console.error('获取用户信息失败:', err);
            reject(err);
          }
        });
      } else {
        // 兼容旧版本
        wx.getUserInfo({
          success: (res) => {
            console.log('获取用户信息成功(旧版):', res.userInfo);
            this.globalData.userInfo = res.userInfo;
            resolve(res.userInfo);
          },
          fail: (err) => {
            console.error('获取用户信息失败(旧版):', err);
            reject(err);
          }
        });
      }
    });
  },

  // 网络请求封装
  request(options) {
    return new Promise((resolve, reject) => {
      const { url, method = 'GET', data = {}, header = {} } = options;
      
      wx.request({
        url: this.globalData.serverConfig.baseUrl + url,
        method: method,
        data: data,
        header: {
          'Content-Type': 'application/json',
          ...header
        },
        timeout: this.globalData.serverConfig.timeout,
        success: (res) => {
          console.log('请求成功:', url, res);
          if (res.statusCode === 200) {
            resolve(res.data);
          } else {
            reject(new Error(`HTTP ${res.statusCode}: ${res.data}`));
          }
        },
        fail: (err) => {
          console.error('请求失败:', url, err);
          reject(err);
        }
      });
    });
  }
});
