document.getElementById('playGame').addEventListener('click', function(e) {
    e.preventDefault()

    const { exec } = require('child_process')

    exec(`python ./games/snake.py ${userId}`, (err, stdout, stderr) => {
        if (err) {
            console.error(`Error: ${err.message}`)
            console.error(`Error Code: ${err.code}`)
            console.error(`Signal Received: ${err.signal}`)
            return
        }
        console.log(`Output: ${stdout}`)
        if (stderr) {
            console.error(`Error Output: ${stderr}`)
        }
    })
})
