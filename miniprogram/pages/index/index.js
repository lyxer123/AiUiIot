// index.js
const app = getApp();

Page({
  data: {
    loading: true,
    error: null,
    systemStatus: {
      mqtt: false,
      device: '未知'
    },
    ad1Data: {
      value: null,
      timestamp: null,
      count: 0
    },
    io1Status: {
      state: false,
      timestamp: null
    },
    refreshTimer: null
  },

  onLoad() {
    console.log('首页加载');
    this.initPage();
  },

  onShow() {
    // 页面显示时刷新数据
    this.refreshAllData();
  },

  onHide() {
    // 页面隐藏时清除定时器
    this.clearRefreshTimer();
  },

  onUnload() {
    // 页面卸载时清理资源
    this.clearRefreshTimer();
  },

  // 初始化页面
  async initPage() {
    try {
      this.setData({ loading: true, error: null });
      
      // 获取系统状态
      await this.getSystemStatus();
      
      // 获取AD1数据
      await this.getAD1Data();
      
      // 获取IO1状态
      await this.getIO1Status();
      
      // 启动自动刷新
      this.startAutoRefresh();
      
      this.setData({ loading: false });
    } catch (error) {
      console.error('页面初始化失败:', error);
      this.setData({ 
        loading: false, 
        error: '页面初始化失败，请检查网络连接' 
      });
    }
  },

  // 获取系统状态
  async getSystemStatus() {
    try {
      const result = await app.request({
        url: '/status'
      });
      
      if (result.success) {
        this.setData({
          'systemStatus.mqtt': result.data.mqtt_connected,
          'systemStatus.device': result.data.system_status
        });
      }
    } catch (error) {
      console.error('获取系统状态失败:', error);
    }
  },

  // 获取AD1数据
  async getAD1Data() {
    try {
      const result = await app.request({
        url: '/ad1/data?limit=1'
      });
      
      if (result.success && result.data.length > 0) {
        const latestData = result.data[0];
        this.setData({
          'ad1Data.value': latestData.value,
          'ad1Data.timestamp': this.formatTime(latestData.timestamp),
          'ad1Data.count': result.data.length
        });
      }
    } catch (error) {
      console.error('获取AD1数据失败:', error);
    }
  },

  // 获取IO1状态
  async getIO1Status() {
    try {
      const result = await app.request({
        url: '/io1/current'
      });
      
      if (result.success) {
        this.setData({
          'io1Status.state': result.data.state,
          'io1Status.timestamp': this.formatTime(new Date())
        });
      }
    } catch (error) {
      console.error('获取IO1状态失败:', error);
    }
  },

  // 开启IO1
  async turnOnIO1() {
    try {
      wx.showLoading({ title: '正在开启...' });
      
      const result = await app.request({
        url: '/io1/control',
        method: 'POST',
        data: { state: true }
      });
      
      if (result.success) {
        wx.showToast({ 
          title: 'IO1已开启', 
          icon: 'success' 
        });
        
        // 延迟刷新状态
        setTimeout(() => {
          this.getIO1Status();
        }, 1000);
      } else {
        wx.showToast({ 
          title: result.error || '开启失败', 
          icon: 'error' 
        });
      }
    } catch (error) {
      console.error('开启IO1失败:', error);
      wx.showToast({ 
        title: '网络错误', 
        icon: 'error' 
      });
    } finally {
      wx.hideLoading();
    }
  },

  // 关闭IO1
  async turnOffIO1() {
    try {
      wx.showLoading({ title: '正在关闭...' });
      
      const result = await app.request({
        url: '/io1/control',
        method: 'POST',
        data: { state: false }
      });
      
      if (result.success) {
        wx.showToast({ 
          title: 'IO1已关闭', 
          icon: 'success' 
        });
        
        // 延迟刷新状态
        setTimeout(() => {
          this.getIO1Status();
        }, 1000);
      } else {
        wx.showToast({ 
          title: result.error || '关闭失败', 
          icon: 'error' 
        });
      }
    } catch (error) {
      console.error('关闭IO1失败:', error);
      wx.showToast({ 
        title: '网络错误', 
        icon: 'error' 
      });
    } finally {
      wx.hideLoading();
    }
  },

  // 刷新状态
  async refreshStatus() {
    try {
      wx.showLoading({ title: '刷新中...' });
      await this.getSystemStatus();
      wx.showToast({ title: '刷新成功', icon: 'success' });
    } catch (error) {
      wx.showToast({ title: '刷新失败', icon: 'error' });
    } finally {
      wx.hideLoading();
    }
  },

  // 刷新IO1状态
  async refreshIO1Status() {
    try {
      wx.showLoading({ title: '刷新中...' });
      await this.getIO1Status();
      wx.showToast({ title: '刷新成功', icon: 'success' });
    } catch (error) {
      wx.showToast({ title: '刷新失败', icon: 'error' });
    } finally {
      wx.hideLoading();
    }
  },

  // 测试连接
  async testConnection() {
    try {
      wx.showLoading({ title: '测试中...' });
      
      const result = await app.request({
        url: '/test'
      });
      
      if (result.success) {
        wx.showToast({ 
          title: '连接正常', 
          icon: 'success' 
        });
      } else {
        wx.showToast({ 
          title: '连接异常', 
          icon: 'error' 
        });
      }
    } catch (error) {
      console.error('连接测试失败:', error);
      wx.showToast({ 
        title: '连接失败', 
        icon: 'error' 
      });
    } finally {
      wx.hideLoading();
    }
  },

  // 刷新所有数据
  async refreshAllData() {
    try {
      await Promise.all([
        this.getSystemStatus(),
        this.getAD1Data(),
        this.getIO1Status()
      ]);
    } catch (error) {
      console.error('刷新数据失败:', error);
    }
  },

  // 启动自动刷新
  startAutoRefresh() {
    // 每30秒自动刷新一次
    this.data.refreshTimer = setInterval(() => {
      this.refreshAllData();
    }, 30000);
  },

  // 清除刷新定时器
  clearRefreshTimer() {
    if (this.data.refreshTimer) {
      clearInterval(this.data.refreshTimer);
      this.data.refreshTimer = null;
    }
  },

  // 重试
  retry() {
    this.initPage();
  },

  // 格式化时间
  formatTime(timestamp) {
    if (!timestamp) return '--';
    
    try {
      const date = new Date(timestamp);
      const now = new Date();
      const diff = now - date;
      
      if (diff < 60000) { // 1分钟内
        return '刚刚';
      } else if (diff < 3600000) { // 1小时内
        return `${Math.floor(diff / 60000)}分钟前`;
      } else if (diff < 86400000) { // 1天内
        return `${Math.floor(diff / 3600000)}小时前`;
      } else {
        return date.toLocaleDateString();
      }
    } catch (error) {
      return timestamp;
    }
  },

  // 导航到控制页面
  navigateToControl() {
    wx.switchTab({
      url: '/pages/control/control'
    });
  },

  // 导航到数据页面
  navigateToData() {
    wx.switchTab({
      url: '/pages/data/data'
    });
  },

  // 导航到个人中心
  navigateToProfile() {
    wx.switchTab({
      url: '/pages/profile/profile'
    });
  },

  // 查看历史
  viewHistory() {
    wx.switchTab({
      url: '/pages/data/data'
    });
  },

  // 查看控制历史
  viewControlHistory() {
    wx.switchTab({
      url: '/pages/control/control'
    });
  }
});
