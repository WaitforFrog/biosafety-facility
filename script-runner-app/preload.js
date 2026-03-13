const { contextBridge, ipcRenderer } = require('electron');

// 暴露安全的 API 给渲染进程
contextBridge.exposeInMainWorld('api', {
  // 获取脚本列表
  getScripts: () => ipcRenderer.invoke('get-scripts'),
  
  // 运行脚本
  runScript: (scriptFile) => ipcRenderer.invoke('run-script', scriptFile),
  
  // 停止脚本
  stopScript: () => ipcRenderer.invoke('stop-script'),
  
  // 获取日志列表
  getLogs: () => ipcRenderer.invoke('get-logs'),
  
  // 获取日志详情
  getLogDetail: (filename) => ipcRenderer.invoke('get-log-detail', filename),
  
  // 监听脚本输出
  onScriptOutput: (callback) => {
    ipcRenderer.on('script-output', (event, text) => callback(text));
  },
  
  // 监听脚本结束
  onScriptFinished: (callback) => {
    ipcRenderer.on('script-finished', (event, code) => callback(code));
  }
});
