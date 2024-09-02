<?php
session_start();

$servername = "localhost";
$username = "root";
$password = "";
$dbname = "desktopapp";

$newProfilePicture = isset($_POST['newProfilePicture']) ? $_POST['newProfilePicture'] : '';
$id = isset($_SESSION['user_id']) ? $_SESSION['user_id'] : 0;

error_log("Received newProfilePicture: " . $newProfilePicture);
error_log("Session user_id: " . $id);

if (empty($newProfilePicture)) {
    echo "No profile picture provided.";
    exit;
}

if ($id <= 0) {
    echo "Invalid user ID.";
    exit;
}

$conn = new mysqli($servername, $username, $password, $dbname);

if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

$sql = "UPDATE usuario SET current_profile_picture = ? WHERE id_user = ?";
$stmt = $conn->prepare($sql);

if ($stmt === false) {
    die("Prepare failed: " . $conn->error);
}

$stmt->bind_param("si", $newProfilePicture, $id);

if ($stmt->execute()) {
    if ($stmt->affected_rows > 0) {
        echo "Profile picture updated successfully!";
    } else {
        echo "No changes made to the profile picture.";
    }
} else {
    echo "Error executing statement: " . $stmt->error;
}

$stmt->close();
$conn->close();
?>