const { app, BrowserWindow, ipcMain } = require('electron')
const path = require('path')

function createWindow() {
  const mainWindow = new BrowserWindow({
    width: 1160,
    height: 800,
    resizable: false,
    frame: true, 

    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      nodeIntegration: true,
      contextIsolation: false,
    }
  })

  mainWindow.loadURL('http://localhost/register.php')

  ipcMain.on('navigate-to', (event, page) => {
    mainWindow.loadURL(`http://localhost/${page}`)
  })

  // Menu.setApplicationMenu(null)
}

app.whenReady().then(() => {
  createWindow()

  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
      createWindow()
    }
  })
})

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit()
  }
})
