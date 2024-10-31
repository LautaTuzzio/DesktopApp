<?php
session_start();

$servername = "localhost";
$username = "root";
$password = "";
$dbname = "desktopapp";

$conn = new mysqli($servername, $username, $password, $dbname);

if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

$currentUser = $_SESSION['username'];
$sql = "SELECT * FROM usuario WHERE name_user='$currentUser' OR mail='$currentUser'";
$result = $conn->query($sql);

if ($result->num_rows > 0) {
    $row = $result->fetch_assoc();
    $id_usuario = $row['id_user'];
    $name = $row['name_user'];
    $email = $row['mail'];
    $password = $row['password'];
    $registrationDate = date('m/d/y', strtotime($row['registration_date']));
    $coins = $row['monedas'];
} else {
    echo "User not found.";
    exit;
}

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

$sql_user_achievements = "SELECT logro FROM actividad WHERE id_user = $id_usuario AND id_juego = $game_id";
$result_user_achievements = $conn->query($sql_user_achievements);

$user_achievements = [];
if ($result_user_achievements->num_rows > 0) {
    $row = $result_user_achievements->fetch_assoc();
    $logro = str_pad($row['logro'], 3, '0', STR_PAD_RIGHT);
    $user_achievements = str_split($logro); 
}

$sql_achievements = "SELECT nombre, reto, img FROM logros WHERE id_juego = $game_id";
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
                <li><h3>Nombre</h3><h3>Puntaje</h3></li>
                <?php
                if ($result_leaderboard->num_rows > 0) {
                    $rank = 1;
                    while ($row = $result_leaderboard->fetch_assoc()) {
                        $highlightClass = ($row['name_user'] === $currentUser) ? 'highlight' : '';
                        echo "<li class='$highlightClass'>{$rank}. {$row['name_user']}<span>{$row['puntaje']} PTS</span></li>";
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
            $i = 0;
            while ($achievement = $result_achievements->fetch_assoc()) {
                $status = (isset($user_achievements[$i]) && $user_achievements[$i] == '1') ? 'Completado' : 'Incompleto';
                echo "
                <div class=\"archivement\">
                    <img src=\"{$achievement['img']}\" alt=\"Achievement Image\">
                    <div class=\"info\">
                        <h2>{$achievement['nombre']}</h2>
                        <h4>{$achievement['reto']}</h4>
                        <p>Estado: $status</p>
                    </div>
                </div>";
                $i++;
            }
        } else {
            echo "<p>No achievements available</p>";
        }
        ?>
        <div class="a-holder">
            <a class="underline-btn" href="index.php">
                <h3 class="animated-text">
                <span class="static-text">Volver</span>
                </h3>
            </a>
        </div>
    </div>

    <script>
    const userId = <?php echo $id_usuario; ?>
    </script>
    <script src="snakeRender.js"></script>

</body>
</html>
