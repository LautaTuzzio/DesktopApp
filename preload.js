const { contextBridge, ipcRenderer } = require('electron')

contextBridge.exposeInMainWorld('electron', {
    send: (channel, data) => {
        const validChannels = ['restart-app', 'navigate-to']
        if (validChannels.includes(channel)) {
            ipcRenderer.send(channel, data)
        }
    }
})