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
    $user = $_POST['username'];
    $pass = $_POST['password'];

    $sql = "SELECT * FROM usuario WHERE name_user='$user' or mail='$user'";
    $result = $conn->query($sql);

    if ($result->num_rows > 0) {
        $row = $result->fetch_assoc();
        if ($pass === $row['password']) {
            $_SESSION['username'] = $user;
            
            $_SESSION['logStatus']= "True";
            header("Location: index.php");
        } else {
            header("Location: register.php");
            $_SESSION['logStatus']= "False";
        }
    } else {
        header("Location: register.php");
    }
}

$conn->close();
?>