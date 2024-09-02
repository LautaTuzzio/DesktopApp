document.getElementById('playGame').addEventListener('click', function(e) {
    e.preventDefault()

    const { exec } = require('child_process')

    exec(`python ./games/pong/pong.py ${userId}`, (err, stdout, stderr) => {
        if (err) {
            console.error(`Error: ${err}`)
            return
        }
        console.log(`Output: ${stdout}`)
        console.error(`Error Output: ${stderr}`)
    })
})
