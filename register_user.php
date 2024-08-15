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

    $sql = "INSERT INTO usuario (name_user, mail, password, registration_date) VALUES ('$user', '$email', '$pass', '$registrationDate')";

    if ($conn->query($sql) === TRUE) {
        $_SESSION['username'] = $user; 
        $_SESSION['logStatus']= "True";
        header("Location: index.php");
        exit();
    } else {
        echo '<script>alert("Registration failed. Please try again."); window.location.href="register.php";</script>';
    }
}

$conn->close();
?>