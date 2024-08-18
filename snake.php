<?php
$servername = "localhost";
$username = "root";
$password = "";
$dbname = "desktopapp";

$conn = new mysqli($servername, $username, $password, $dbname);

$game_id = 1;

$sql_game = "SELECT nombre, img_juego FROM juegos WHERE id_juego = $game_id";
$result_game = $conn->query($sql_game);
$game = $result_game->fetch_assoc();

$sql_leaderboard = "
    SELECT usuario.name_user, actividad.puntaje 
    FROM actividad 
    JOIN usuario ON actividad.id_user = usuario.id_user 
    WHERE actividad.id_juego = $game_id 
    ORDER BY actividad.puntaje DESC 
    LIMIT 10";
$result_leaderboard = $conn->query($sql_leaderboard);

$sql_achievements = "SELECT nombre, reto, img, Completado FROM logros WHERE id_juego = $game_id";
$result_achievements = $conn->query($sql_achievements);
?>
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="pregame.css">
    <title>Snake</title>
</head>

<body>

    <div class="container">
        <div class="game-holder">
            <a href="#" id="playGame">
                <img src="<?php echo $game['img_juego']; ?>" alt="Game Image" style="width: 67vw;">
            </a>
        </div>
        <div class="leaderboard">
            <div class="title">
                <div class="line"></div>
                <h2>Ranking</h2>
                <div class="line"></div>
            </div>
            <ul>
                <li><h3>Name</h3><h3>Score</h3></li>
                <?php
                if ($result_leaderboard->num_rows > 0) {
                    $rank = 1;
                    while ($row = $result_leaderboard->fetch_assoc()) {
                        echo "<li>{$rank}. {$row['name_user']}</span><span>{$row['puntaje']} PTS</span></li>";
                        $rank++;
                    }
                } else {
                    echo "<li>No data available</li>";
                }
                ?>
            </ul>
        </div>
    </div>

    <div class="archivements">
        <?php
        if ($result_achievements->num_rows > 0) {
            while ($achievement = $result_achievements->fetch_assoc()) {
                $status = $achievement['Completado'] ? 'Completed' : 'Incomplete';
                echo "
                <div class=\"archivement\">
                    <img src=\"{$achievement['img']}\" alt=\"Achievement Image\">
                    <div class=\"info\">
                        <h2>{$achievement['nombre']}</h2>
                        <h4>{$achievement['reto']}</h4>
                        <p>Status: $status</p>
                    </div>
                </div>";
            }
        } else {
            echo "<p>No achievements available</p>";
        }
        ?>
        <div class="a-holder">
            <a class="underline-btn" href="index.php">
                <h3 class="animated-text">
                    <span class="static-text">Go</span>
                    <ul>
                        <li>b</li>
                        <li>a</li>
                        <li>c</li>
                        <li>k</li>
                    </ul>
                </h3>
            </a>
        </div>
    </div>

    <script>
        // Usamos la api de electron directamente para poder entrar (esperamos 3 parametros, err [error], stdout[salida], sterr[salida si error])
        document.getElementById('playGame').addEventListener('click', function(e) {
            e.preventDefault();
            const { exec } = require('child_process');
            exec('python ./games/snake.py', (err, stdout, stderr) => {
               /* if (err) {
                    console.error(`Error: ${err}`);
                    return;
                }
                console.log(`Output: ${stdout}`);
                console.error(`Error Output: ${stderr}`); debugging */ 
            });
        });
    </script>
        
</body>

</html>
