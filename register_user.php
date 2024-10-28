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

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $user = $conn->real_escape_string($_POST['username']);
    $email = $conn->real_escape_string($_POST['email']);
    $pass = $conn->real_escape_string($_POST['password']);
    $registrationDate = date('Y-m-d'); 

    $sql = "INSERT INTO usuario (name_user, mail, password, registration_date, monedas, current_profile_picture) VALUES ('$user', '$email', '$pass', '$registrationDate', '0', 'https://cdn.pixabay.com/photo/2018/11/13/21/43/avatar-3814049_1280.png')";

    if ($conn->query($sql) === TRUE) {
        $last_id = $conn->insert_id;

        $_SESSION['username'] = $user;
        $_SESSION['logStatus'] = "True";

        $objects = [
            ['url_img' => 'https://png.pngtree.com/png-vector/20191101/ourmid/pngtree-cartoon-color-simple-male-avatar-png-image_1934459.jpg', 'nombre' => 'Icon 1', 'precio' => 5000, 'id_juego' => 0, 'comprado' => 0],
            ['url_img' => 'snakeBG1.png', 'nombre' => 'Snake fondo gris', 'precio' => 1000, 'id_juego' => 1, 'comprado' => 1],
            ['url_img' => 'snakeBG2.png', 'nombre' => 'Snake fondo rojo', 'precio' => 1000, 'id_juego' => 1, 'comprado' => 0], 
            ['url_img' => 'snakeBG3.png', 'nombre' => 'Snake fondo verde', 'precio' => 1000, 'id_juego' => 1, 'comprado' => 0], 
        ];

        $errorOccurred = false;
        foreach ($objects as $object) {
            $sql2 = "INSERT INTO objetos (url_img, nombre, precio, id_juego, userID, comprado) 
                     VALUES ('{$object['url_img']}', '{$object['nombre']}', {$object['precio']}, {$object['id_juego']}, $last_id, {$object['comprado']})";
            
            if ($conn->query($sql2) !== TRUE) {
                $errorOccurred = true;
                break;
            }
        }

        if (!$errorOccurred) {
            header("Location: index.php");
            exit();
        } else {
            echo '<script>alert("Failed to insert some items into objetos table. Please try again."); window.location.href="register.php";</script>';
        }
    } else {
        echo '<script>alert("Registration failed. Please try again."); window.location.href="register.php";</script>';
    }
}

$conn->close();
?>
