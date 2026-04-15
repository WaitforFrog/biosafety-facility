const { app, BrowserWindow, ipcMain } = require('electron');
const path = require('path');
const { spawn } = require('child_process');
const fs = require('fs');
const log = require('electron-log');

// 配置日志
log.transports.file.level = 'info';
log.transports.console.level = 'info';

log.info('应用启动...');

// 配置路径
const SCRIPTS_DIR = '/Users/guot/Desktop/杰昊/AI推广/域名推广/Code';
const LOGS_DIR = path.join(SCRIPTS_DIR, '文章', '汇总日志');

// 可运行的脚本（相对于 SCRIPTS_DIR）
const AVAILABLE_SCRIPTS = {
  'Produce/Trust_EN_html.py': '翻译并生成英文HTML（中立科普）',
  'Produce/Compare_EN_html.py': '市场分析类文章生成器',
  'Translate.py': '翻译脚本',
  'Produce/Tool/build_preview_site.py': '构建预览站点',
  'Produce/Tool/build_category_indexes.py': '构建分类索引',
  'Produce/Tool/build_articles_index.py': '构建文章索引',
  'delete_chinese_articles.py': '删除中文文章'
};

let mainWindow = null;
let currentProcess = null;

function createWindow() {
  log.info('创建主窗口...');
  
  mainWindow = new BrowserWindow({
    width: 1000,
    height: 700,
    minWidth: 800,
    minHeight: 600,
    webPreferences: {
      nodeIntegration: false,
      contextIsolation: true,
      preload: path.join(__dirname, 'preload.js')
    },
    icon: path.join(__dirname, 'icon.png'),
    title: '脚本运行器'
  });

  mainWindow.loadFile(path.join(__dirname, 'renderer', 'index.html'));

  mainWindow.on('closed', () => {
    mainWindow = null;
  });

  log.info('窗口创建完成');
}

// 获取脚本列表
ipcMain.handle('get-scripts', () => {
  return Object.entries(AVAILABLE_SCRIPTS).map(([file, desc]) => ({
    file,
    desc
  }));
});

// 运行脚本
ipcMain.handle('run-script', async (event, scriptFile) => {
  const scriptPath = path.join(SCRIPTS_DIR, scriptFile);
  
  log.info(`运行脚本: ${scriptPath}`);
  
  return new Promise((resolve) => {
    // 如果有进程在运行，返回错误
    if (currentProcess) {
      resolve({ success: false, error: '已有脚本在运行中' });
      return;
    }

    currentProcess = spawn('python3', [scriptPath], {
      cwd: SCRIPTS_DIR,
      env: { ...process.env }
    });

    let output = '';
    
    currentProcess.stdout.on('data', (data) => {
      const text = data.toString();
      output += text;
      mainWindow?.webContents.send('script-output', text);
    });

    currentProcess.stderr.on('data', (data) => {
      const text = data.toString();
      output += text;
      mainWindow?.webContents.send('script-output', text);
    });

    currentProcess.on('close', (code) => {
      log.info(`脚本结束，退出码: ${code}`);
      currentProcess = null;
      mainWindow?.webContents.send('script-finished', code);
      resolve({ success: code === 0, output, exitCode: code });
    });

    currentProcess.on('error', (err) => {
      log.error(`脚本运行错误: ${err.message}`);
      currentProcess = null;
      resolve({ success: false, error: err.message });
    });
  });
});

// 停止脚本
ipcMain.handle('stop-script', () => {
  if (currentProcess) {
    currentProcess.kill('SIGTERM');
    currentProcess = null;
    return { success: true };
  }
  return { success: false, error: '没有运行的脚本' };
});

// 获取日志列表
ipcMain.handle('get-logs', async () => {
  try {
    if (!fs.existsSync(LOGS_DIR)) {
      return [];
    }
    
    const files = fs.readdirSync(LOGS_DIR)
      .filter(f => f.endsWith('.json'))
      .sort((a, b) => {
        const statA = fs.statSync(path.join(LOGS_DIR, a));
        const statB = fs.statSync(path.join(LOGS_DIR, b));
        return statB.mtime - statA.mtime;
      });

    const logs = [];
    for (const file of files) {
      try {
        const content = fs.readFileSync(path.join(LOGS_DIR, file), 'utf-8');
        const data = JSON.parse(content);
        logs.push({
          filename: file,
          run_time: data.run_time,
          total_products: data.total_products,
          success_count: data.success_count,
          error_count: data.error_count
        });
      } catch (e) {
        log.warn(`读取日志文件失败: ${file}`, e.message);
      }
    }
    
    return logs;
  } catch (e) {
    log.error('获取日志列表失败:', e.message);
    return [];
  }
});

// 获取日志详情
ipcMain.handle('get-log-detail', async (event, filename) => {
  try {
    const filePath = path.join(LOGS_DIR, filename);
    if (!fs.existsSync(filePath)) {
      return null;
    }
    
    const content = fs.readFileSync(filePath, 'utf-8');
    return JSON.parse(content);
  } catch (e) {
    log.error('读取日志详情失败:', e.message);
    return null;
  }
});

app.whenReady().then(() => {
  log.info('Electron 应用就绪');
  createWindow();

  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
      createWindow();
    }
  });
});

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});
