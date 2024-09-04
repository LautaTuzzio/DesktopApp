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

if (isset($_GET['id_objeto']) && isset($_GET['precio'])) {
    $id = $_SESSION['userID'];
    $id_objeto = intval($_GET['id_objeto']);
    $precio = floatval($_GET['precio']);

    $stmt = $conn->prepare("SELECT monedas FROM usuario WHERE id_user = ?");
    $stmt->bind_param("i", $id);
    $stmt->execute();
    $result = $stmt->get_result();
    $userCoins = $result->fetch_assoc()['monedas'];
    $stmt->close();

    if ($userCoins >= $precio) {
        $newCoins = $userCoins - $precio;
        $stmt = $conn->prepare("UPDATE usuario SET monedas = ? WHERE id_user = ?");
        $stmt->bind_param("di", $newCoins, $id);
        $stmt->execute();
        $stmt->close();

        $stmt = $conn->prepare("UPDATE objetos SET comprado = 1 WHERE id_objeto = ? AND userID = ?");
        $stmt->bind_param("ii", $id_objeto, $id);
        $stmt->execute();
        $stmt->close();

        echo "<script>alert('¡Compra exitosa!'); window.location.href='index.php';</script>";
    } else {
        echo "<script>alert('No tienes suficientes monedas.'); window.location.href='index.php';</script>";
    }
} else {
    echo "<script>alert('Datos insuficientes.'); window.location.href='index.php';</script>";
}

$conn->close();
?>
