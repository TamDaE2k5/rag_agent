const { app, BrowserWindow } = require('electron');
const path = require('path');
const http = require('http');

let mainWindow;

function checkBackendHealth(retries = 10, delay = 1000) {
  return new Promise((resolve) => {
    const attempt = (remaining) => {
      http.get('http://127.0.0.1:8000/api/health', (res) => {
        if (res.statusCode === 200) {
          resolve(true);
        } else if (remaining > 0) {
          setTimeout(() => attempt(remaining - 1), delay);
        } else {
          resolve(false);
        }
      }).on('error', () => {
        if (remaining > 0) {
          setTimeout(() => attempt(remaining - 1), delay);
        } else {
          resolve(false);
        }
      });
    };
    attempt(retries);
  });
}

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1366,
    height: 860,
    minWidth: 1024,
    minHeight: 700,
    title: 'AI Trợ lý Tự động hóa Lưới điện Phân phối',
    backgroundColor: '#020617',
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      nodeIntegration: false,
      contextIsolation: true,
    },
  });

  // Tải giao diện Vite local dev server hoặc static build
  const devUrl = 'http://127.0.0.1:5173';
  const prodPath = path.join(__dirname, '../../frontend/dist/index.html');

  mainWindow.loadURL(devUrl).catch(() => {
    mainWindow.loadFile(prodPath);
  });

  mainWindow.on('closed', () => {
    mainWindow = null;
  });
}

app.whenReady().then(async () => {
  await checkBackendHealth();
  createWindow();

  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) createWindow();
  });
});

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});
