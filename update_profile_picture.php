<?php
session_start(); 

$servername = "localhost";
$username = "root";
$password = "";
$dbname = "desktopapp";

$newProfilePicture = $_POST['newProfilePicture'];

$id = $_SESSION['user_id'];

$conn = new mysqli($servername, $username, $password, $dbname);

if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

$sql = "UPDATE users SET current_profile_picture = ? WHERE id_user = ?";
$stmt = $conn->prepare($sql);
$stmt->bind_param("si", $newProfilePicture, $id);
$stmt->execute();

if ($stmt->affected_rows > 0) {
    echo "Profile picture updated successfully!";
} else {
    echo "Error updating profile picture.";
}

$stmt->close();
$conn->close();
?>
