<?php
session_start();

if (!isset($_SESSION['username'])) {
    header("Location: login.php");
    exit;
}

$servername = "localhost";
$username = "root";
$password = "";
$dbname = "desktopapp";

$conn = new mysqli($servername, $username, $password, $dbname);

if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

$currentUser = $_SESSION['username'];
$sql = "SELECT * FROM usuario WHERE name_user='$currentUser' or   mail='$currentUser'";
$result = $conn->query($sql);

if ($result->num_rows > 0) {
    $row = $result->fetch_assoc();
    $id = $row['id_user'];
    $_SESSION['user_id'] = $id;
    $name = $row['name_user'];
    $email = $row['mail'];
    $password = $row['password'];
    $registrationDate = date('m/d/y', strtotime($row['registration_date']));
    $coins = $row['monedas'];
    $pfp = $row['current_profile_picture'];
} else {
    echo "User not found.";
}

$sql = "SELECT * FROM actividad WHERE id_user='$id'";
$result = $conn->query($sql);

$activities = [];

if ($result->num_rows > 0) {
    while ($row = $result->fetch_assoc()) {
        $activities[] = [
            'id_user' => $row['id_user'],
            'id_juego' => $row['id_juego'],
            'archivements' => $row['logro'],
            'time' => $row['tiempo'],
            'last_session' => date('m/d/y', strtotime($row['ult_ingreso'])),
        ];
    }
} else {
    echo "No activities found.";
}


$sql = "SELECT * FROM `juegos` WHERE id_juego >= 1;";
$result = $conn->query($sql);

$games = [];

if ($result->num_rows > 0) {
    while ($row = $result->fetch_assoc()) {
        $games[] = [
            'id_juego' => $row['id_juego'],
            'nombre' => $row['nombre'],
            'img_juego' => $row['img_juego'],
        ];
    }
}



$conn->close();
?>

<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Arcade</title>
    <link rel="stylesheet" href="style.css">
    <link rel="stylesheet" href="progress.css">
    <link rel="stylesheet" href="library.css">
</head>

<body>

    <aside>
        <div class="top">
            <img id="user-pfp" src="<?php echo $pfp; ?>" height="60px" width="60px" alt="logo">
            <div class="text-top">
                <h3><?php echo htmlspecialchars($name); ?></h3>
            </div>
        </div>

        <div class="main">
            <h1>Arcade</h1>
            <ul>
                <li>
                    <div class="option" onclick="showSection('profile', this)">
                        <svg height="25px" width="25px" viewBox="0 0 20 20" version="1.1"
                            xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"
                            fill="#000000">
                            <g id="SVGRepo_bgCarrier" stroke-width="0"></g>
                            <g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g>
                            <g id="SVGRepo_iconCarrier">
                                <defs> </defs>
                                <g id="Page-1" stroke="none" stroke-width="1" fill="none" fill-rule="evenodd">
                                    <g id="Dribbble-Light-Preview" transform="translate(-140.000000, -2159.000000)"
                                        fill="#e0dddd">
                                        <g id="icons" transform="translate(56.000000, 160.000000)">
                                            <path
                                                d="M100.562548,2016.99998 L87.4381713,2016.99998 C86.7317804,2016.99998 86.2101535,2016.30298 86.4765813,2015.66198 C87.7127655,2012.69798 90.6169306,2010.99998 93.9998492,2010.99998 C97.3837885,2010.99998 100.287954,2012.69798 101.524138,2015.66198 C101.790566,2016.30298 101.268939,2016.99998 100.562548,2016.99998 M89.9166645,2004.99998 C89.9166645,2002.79398 91.7489936,2000.99998 93.9998492,2000.99998 C96.2517256,2000.99998 98.0830339,2002.79398 98.0830339,2004.99998 C98.0830339,2007.20598 96.2517256,2008.99998 93.9998492,2008.99998 C91.7489936,2008.99998 89.9166645,2007.20598 89.9166645,2004.99998 M103.955674,2016.63598 C103.213556,2013.27698 100.892265,2010.79798 97.837022,2009.67298 C99.4560048,2008.39598 100.400241,2006.33098 100.053171,2004.06998 C99.6509769,2001.44698 97.4235996,1999.34798 94.7348224,1999.04198 C91.0232075,1998.61898 87.8750721,2001.44898 87.8750721,2004.99998 C87.8750721,2006.88998 88.7692896,2008.57398 90.1636971,2009.67298 C87.1074334,2010.79798 84.7871636,2013.27698 84.044024,2016.63598 C83.7745338,2017.85698 84.7789973,2018.99998 86.0539717,2018.99998 L101.945727,2018.99998 C103.221722,2018.99998 104.226185,2017.85698 103.955674,2016.63598"
                                                id="profile_round-[#e0dddd]"> </path>
                                        </g>
                                    </g>
                                </g>
                            </g>
                        </svg>
                        <h4>Perfil</h4>
                    </div>
                </li>
                <li>
                    <div class="option" id="activity-button" onclick="showSection('activity', this)">
                        <svg fill="#e0dddd" width="25px" height="25px" viewBox="0 0 24 24" id="Outline"
                            xmlns="http://www.w3.org/2000/svg">
                            <g id="SVGRepo_bgCarrier" stroke-width="0"></g>
                            <g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g>
                            <g id="SVGRepo_iconCarrier">
                                <title>194 restore</title>
                                <path
                                    d="M12,6a1,1,0,0,0-1,1v5a1,1,0,0,0,.293.707l3,3a1,1,0,0,0,1.414-1.414L13,11.586V7A1,1,0,0,0,12,6Z M23.812,10.132A12,12,0,0,0,3.578,3.415V1a1,1,0,0,0-2,0V5a2,2,0,0,0,2,2h4a1,1,0,0,0,0-2H4.827a9.99,9.99,0,1,1-2.835,7.878A.982.982,0,0,0,1,12a1.007,1.007,0,0,0-1,1.1,12,12,0,1,0,23.808-2.969Z">
                                </path>
                            </g>
                        </svg>
                        <h4>Actividad</h4>
                    </div>
                </li>
                <li>
                    <div class="option" onclick="showSection('library', this)">
                        <svg fill="#e0dddd" width="25px" height="25px" version="1.1" id="Capa_1"
                            xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"
                            viewBox="0 0 606.877 606.877" xml:space="preserve">
                            <g id="SVGRepo_bgCarrier" stroke-width="0"></g>
                            <g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g>
                            <g id="SVGRepo_iconCarrier">
                                <g>
                                    <g>
                                        <g>
                                            <path
                                                d="M58.64,280.154h162.654c32.058,0,58.14-26.082,58.14-58.14V59.36c0-32.059-26.082-58.14-58.14-58.14H58.64 C26.582,1.22,0.5,27.301,0.5,59.36v162.654C0.5,254.072,26.582,280.154,58.64,280.154z M43.34,59.36c0-8.45,6.85-15.3,15.3-15.3 h162.654c8.45,0,15.3,6.85,15.3,15.3v162.654c0,8.45-6.85,15.3-15.3,15.3H58.64c-8.45,0-15.3-6.85-15.3-15.3V59.36z">
                                            </path>
                                            <path
                                                d="M221.294,280.654H58.64c-32.334,0-58.64-26.306-58.64-58.64V59.36C0,27.025,26.306,0.72,58.64,0.72h162.654 c32.334,0,58.64,26.306,58.64,58.64v162.654C279.934,254.348,253.628,280.654,221.294,280.654z M58.64,1.72 C26.857,1.72,1,27.577,1,59.36v162.654c0,31.783,25.857,57.64,57.64,57.64h162.654c31.783,0,57.64-25.857,57.64-57.64V59.36 c0-31.783-25.857-57.64-57.64-57.64H58.64z M221.294,237.813H58.64c-8.712,0-15.8-7.088-15.8-15.8V59.36 c0-8.712,7.088-15.8,15.8-15.8h162.654c8.712,0,15.8,7.088,15.8,15.8v162.654C237.094,230.726,230.006,237.813,221.294,237.813z M58.64,44.56c-8.161,0-14.8,6.639-14.8,14.8v162.654c0,8.161,6.639,14.8,14.8,14.8h162.654c8.161,0,14.8-6.639,14.8-14.8V59.36 c0-8.161-6.639-14.8-14.8-14.8H58.64z">
                                            </path>
                                        </g>
                                        <g>
                                            <path
                                                d="M548.238,1.22H385.584c-32.059,0-58.141,26.082-58.141,58.14v162.654c0,32.058,26.082,58.14,58.141,58.14h162.654 c32.059,0,58.139-26.082,58.139-58.14V59.36C606.377,27.301,580.297,1.22,548.238,1.22z M563.537,222.014 c0,8.45-6.85,15.3-15.299,15.3H385.584c-8.449,0-15.301-6.85-15.301-15.3V59.36c0-8.45,6.852-15.3,15.301-15.3h162.654 c8.449,0,15.299,6.85,15.299,15.3V222.014z">
                                            </path>
                                            <path
                                                d="M548.238,280.654H385.584c-32.335,0-58.641-26.306-58.641-58.64V59.36c0-32.334,26.306-58.64,58.641-58.64h162.654 c32.333,0,58.639,26.306,58.639,58.64v162.654C606.877,254.348,580.571,280.654,548.238,280.654z M385.584,1.72 c-31.783,0-57.641,25.857-57.641,57.64v162.654c0,31.783,25.857,57.64,57.641,57.64h162.654c31.782,0,57.639-25.857,57.639-57.64 V59.36c0-31.783-25.856-57.64-57.639-57.64H385.584z M548.238,237.813H385.584c-8.713,0-15.801-7.088-15.801-15.8V59.36 c0-8.712,7.088-15.8,15.801-15.8h162.654c8.712,0,15.799,7.088,15.799,15.8v162.654 C564.037,230.726,556.95,237.813,548.238,237.813z M385.584,44.56c-8.161,0-14.801,6.639-14.801,14.8v162.654 c0,8.161,6.64,14.8,14.801,14.8h162.654c8.16,0,14.799-6.639,14.799-14.8V59.36c0-8.161-6.639-14.8-14.799-14.8H385.584z">
                                            </path>
                                        </g>
                                        <g>
                                            <path
                                                d="M58.64,605.657h162.654c32.058,0,58.14-26.08,58.14-58.139V384.864c0-32.059-26.082-58.141-58.14-58.141H58.64 c-32.058,0-58.14,26.082-58.14,58.141v162.654C0.5,579.577,26.582,605.657,58.64,605.657z M43.34,384.864 c0-8.449,6.85-15.301,15.3-15.301h162.654c8.45,0,15.3,6.852,15.3,15.301v162.654c0,8.449-6.85,15.299-15.3,15.299H58.64 c-8.45,0-15.3-6.85-15.3-15.299V384.864z">
                                            </path>
                                            <path
                                                d="M221.294,606.157H58.64C26.306,606.157,0,579.852,0,547.519V384.864c0-32.335,26.306-58.641,58.64-58.641h162.654 c32.334,0,58.64,26.306,58.64,58.641v162.654C279.934,579.852,253.628,606.157,221.294,606.157z M58.64,327.224 C26.857,327.224,1,353.081,1,384.864v162.654c0,31.782,25.857,57.639,57.64,57.639h162.654c31.783,0,57.64-25.856,57.64-57.639 V384.864c0-31.783-25.857-57.641-57.64-57.641H58.64z M221.294,563.317H58.64c-8.712,0-15.8-7.087-15.8-15.799V384.864 c0-8.713,7.088-15.801,15.8-15.801h162.654c8.712,0,15.8,7.088,15.8,15.801v162.654 C237.094,556.23,230.006,563.317,221.294,563.317z M58.64,370.063c-8.161,0-14.8,6.64-14.8,14.801v162.654 c0,8.16,6.639,14.799,14.8,14.799h162.654c8.161,0,14.8-6.639,14.8-14.799V384.864c0-8.161-6.639-14.801-14.8-14.801H58.64z">
                                            </path>
                                        </g>
                                        <g>
                                            <path
                                                d="M548.238,326.724H385.584c-32.059,0-58.141,26.082-58.141,58.141v162.654c0,32.059,26.082,58.139,58.141,58.139h162.654 c32.059,0,58.139-26.08,58.139-58.139V384.864C606.377,352.806,580.297,326.724,548.238,326.724z M563.537,547.519 c0,8.449-6.85,15.299-15.299,15.299H385.584c-8.449,0-15.301-6.85-15.301-15.299V384.864c0-8.449,6.852-15.301,15.301-15.301 h162.654c8.449,0,15.299,6.852,15.299,15.301V547.519z">
                                            </path>
                                            <path
                                                d="M548.238,606.157H385.584c-32.335,0-58.641-26.306-58.641-58.639V384.864c0-32.335,26.306-58.641,58.641-58.641h162.654 c32.333,0,58.639,26.306,58.639,58.641v162.654C606.877,579.852,580.571,606.157,548.238,606.157z M385.584,327.224 c-31.783,0-57.641,25.857-57.641,57.641v162.654c0,31.782,25.857,57.639,57.641,57.639h162.654 c31.782,0,57.639-25.856,57.639-57.639V384.864c0-31.783-25.856-57.641-57.639-57.641H385.584z M548.238,563.317H385.584 c-8.713,0-15.801-7.087-15.801-15.799V384.864c0-8.713,7.088-15.801,15.801-15.801h162.654c8.712,0,15.799,7.088,15.799,15.801 v162.654C564.037,556.23,556.95,563.317,548.238,563.317z M385.584,370.063c-8.161,0-14.801,6.64-14.801,14.801v162.654 c0,8.16,6.64,14.799,14.801,14.799h162.654c8.16,0,14.799-6.639,14.799-14.799V384.864c0-8.161-6.639-14.801-14.799-14.801 H385.584z">
                                            </path>
                                        </g>
                                    </g>
                                </g>
                            </g>
                        </svg>
                        <h4>Biblioteca</h4>
                    </div>
                </li>
                <li>
                    <div class="option" onclick="showSection('shop', this)">
                        <svg viewBox="0 0 24 24" fill="none" width="25px" height="25px"
                            xmlns="http://www.w3.org/2000/svg">
                            <g id="SVGRepo_bgCarrier" stroke-width="0"></g>
                            <g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g>
                            <g id="SVGRepo_iconCarrier">
                                <path
                                    d="M22.3596 8.27L22.0696 5.5C21.6496 2.48 20.2796 1.25 17.3497 1.25H14.9896H13.5097H10.4697H8.98965H6.58965C3.64965 1.25 2.28965 2.48 1.85965 5.53L1.58965 8.28C1.48965 9.35 1.77965 10.39 2.40965 11.2C3.16965 12.19 4.33965 12.75 5.63965 12.75C6.89965 12.75 8.10965 12.12 8.86965 11.11C9.54965 12.12 10.7097 12.75 11.9997 12.75C13.2896 12.75 14.4197 12.15 15.1096 11.15C15.8797 12.14 17.0696 12.75 18.3096 12.75C19.6396 12.75 20.8396 12.16 21.5896 11.12C22.1896 10.32 22.4597 9.31 22.3596 8.27Z"
                                    fill="#e0dddd"></path>
                                <path
                                    d="M11.3491 16.6602C10.0791 16.7902 9.11914 17.8702 9.11914 19.1502V21.8902C9.11914 22.1602 9.33914 22.3802 9.60914 22.3802H14.3791C14.6491 22.3802 14.8691 22.1602 14.8691 21.8902V19.5002C14.8791 17.4102 13.6491 16.4202 11.3491 16.6602Z"
                                    fill="#e0dddd"></path>
                                <path
                                    d="M21.3709 14.3981V17.3781C21.3709 20.1381 19.1309 22.3781 16.3709 22.3781C16.1009 22.3781 15.8809 22.1581 15.8809 21.8881V19.4981C15.8809 18.2181 15.4909 17.2181 14.7309 16.5381C14.0609 15.9281 13.1509 15.6281 12.0209 15.6281C11.7709 15.6281 11.5209 15.6381 11.2509 15.6681C9.47086 15.8481 8.12086 17.3481 8.12086 19.1481V21.8881C8.12086 22.1581 7.90086 22.3781 7.63086 22.3781C4.87086 22.3781 2.63086 20.1381 2.63086 17.3781V14.4181C2.63086 13.7181 3.32086 13.2481 3.97086 13.4781C4.24086 13.5681 4.51086 13.6381 4.79086 13.6781C4.91086 13.6981 5.04086 13.7181 5.16086 13.7181C5.32086 13.7381 5.48086 13.7481 5.64086 13.7481C6.80086 13.7481 7.94086 13.3181 8.84086 12.5781C9.70086 13.3181 10.8209 13.7481 12.0009 13.7481C13.1909 13.7481 14.2909 13.3381 15.1509 12.5981C16.0509 13.3281 17.1709 13.7481 18.3109 13.7481C18.4909 13.7481 18.6709 13.7381 18.8409 13.7181C18.9609 13.7081 19.0709 13.6981 19.1809 13.6781C19.4909 13.6381 19.7709 13.5481 20.0509 13.4581C20.7009 13.2381 21.3709 13.7181 21.3709 14.3981Z"
                                    fill="#e0dddd"></path>
                            </g>
                        </svg>
                        <h4>Tienda</h4>
                    </div>
                </li>

                <li>
                    <a id="logout-link" onclick="return confirmLogout(event)">
                        <div class="option" onclick="showSection('shop', this)">
                            <svg fill="#e0dddd" version="1.1" id="Layer_1" xmlns="http://www.w3.org/2000/svg"
                                xmlns:xlink="http://www.w3.org/1999/xlink" width="25px" height="25px"
                                viewBox="0 0 70 70" enable-background="new 0 0 70 70" xml:space="preserve">
                                <g id="SVGRepo_bgCarrier" stroke-width="0"></g>
                                <g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g>
                                <g id="SVGRepo_iconCarrier">
                                    <g>
                                        <path
                                            d="M62.666,32.316L57.758,21.53c-0.457-1.007-1.646-1.449-2.648-0.992c-1.006,0.457-1.45,1.644-0.992,2.648l3.365,7.397 H44.481c-1.104,0-2,0.896-2,2s0.896,2,2,2h13.69l-4.055,8.912c-0.458,1.004-0.014,2.191,0.992,2.648 c0.269,0.121,0.55,0.18,0.827,0.18c0.76,0,1.486-0.436,1.821-1.172l4.939-10.855c0.104-0.196,0.172-0.407,0.206-0.625 C62.988,33.207,62.901,32.726,62.666,32.316z">
                                        </path>
                                        <path
                                            d="M51.583,47.577c-1.104,0-2,0.895-2,2v8.006h-11V15.269c0-1.722-0.81-3.25-2.445-3.795L24.536,7.583h25.047v9.994 c0,1.104,0.896,2,2,2s2-0.896,2-2v-12c0-1.104,0.003-1.994-1.102-1.994H12.609l-0.325-0.109c-0.413-0.138-0.694-0.205-1.119-0.205 c-0.829,0-1.94,0.258-2.63,0.755C7.492,4.776,6.583,5.983,6.583,7.269v47.572c0,1.721,1.393,3.25,3.026,3.795l24.146,8 c0.413,0.137,0.913,0.205,1.337,0.205c0.83,0,1.395-0.258,2.084-0.756c1.043-0.752,1.407-1.959,1.407-3.244v-1.258h13.898 c1.104,0,1.102-0.902,1.102-2.006v-10C53.583,48.472,52.688,47.577,51.583,47.577z M34.583,62.841l-24-8V7.583V7.504L10.8,7.345 l23.783,7.924V62.841z">
                                        </path>
                                        <path
                                            d="M30.583,47.577c0.553,0,1-0.447,1-1v-6c0-0.553-0.447-1-1-1s-1,0.447-1,1v6C29.583,47.13,30.03,47.577,30.583,47.577z">
                                        </path>
                                    </g>
                                </g>
                            </svg>
                            <h4>Salir</h4>
                        </div>
                    </a>
                    <script>
                        function confirmLogout(event) {
                            event.preventDefault();
                            
                            if (confirm('¿Estás seguro que quieres salir?')) {
                                const { ipcRenderer } = require('electron');
                                ipcRenderer.send('restart-app');
                            } else {
                                const { ipcRenderer } = require('electron');
                                ipcRenderer.send('navigate-to', 'index.php');
                            }
                            
                            return false;
                        }
                    </script>
                </li>
            </ul>
        </div>
        <div class="bottom">
            <h3>Colaboradores</h3>
            <div class="colaboradores">
                <div class="colaborador-wrapper">
                    <img src="colab1.png" alt="logo" style="height=30px; width=30px;">
                    <span class="tooltip">Lautaro Tuzzio</span>
                </div>
                <div class="colaborador-wrapper">
                    <img src="colab2.png" alt="logo" style="height=30px; width=30px;">
                    <span class="tooltip">Maximo Mayorga</span>
                </div>
                <div class="colaborador-wrapper">
                    <img src="colab3.png" alt="logo" style="height=30px; width=30px;">
                    <span class="tooltip">Candela Molinari</span>
                </div>
                <div class="colaborador-wrapper">
                    <img src="colab4.png" alt="logo" style="height=30px; width=30px;">
                    <span class="tooltip">Carlos Insaurralde</span>
                </div>
            </div>
        </div>
    </aside>
    <main>

        <section id="profile" class="content" style="margin-left:200px;">
            <div class="profile-top" onclick="openPopup()">
                <div class="image-container">
                    <img id="user-pfp" src="<?php echo $pfp; ?>" alt="logo">
                </div>
                <div class="profile-desc">
                    <h1><?php echo htmlspecialchars($name); ?></h1>
                    <h3>Fecha de registro<?php echo htmlspecialchars($registrationDate); ?></h3>
                </div>
            </div>

            <div class="profile-personal">
                <h1>Informacion de la cuenta</h1>
                <div class="detail-holder">
                    <label for="email">Email</label>
                    <input type="text" id="email" value="<?php echo htmlspecialchars($email); ?>" readonly>

                    <label for="password">Contraseña</label>
                    <div class="password-group">
                        <input type="password" id="password" value="<?php echo htmlspecialchars($password); ?>"
                            readonly>
                        <span class="icon eye-icon" onclick="togglePasswordVisibility()">&#128065;</span>
                    </div>
                </div>
            </div>

            <div id="popup" class="popup">
                <div class="popup-content">
                    <span class="close-btn" onclick="closePopup()">&times;</span>
                    <h2 style="text-align: center; color: #e0dddd; margin-bottom: 20px; ">Fotos de perfil</h2>
                    <div class="pfp-holder"
                        style="display: flex; justify-content:center; align-items:center; gap:20px;">
                        <?php
                        $servername = "localhost";
                        $username = "root";
                        $password = "";
                        $dbname = "desktopapp";

                        $conn = new mysqli($servername, $username, $password, $dbname);

                        if ($conn->connect_error) {
                            die("Connection failed: " . $conn->connect_error);
                        }

                        $sql = "SELECT * FROM objetos WHERE userID = $id AND id_juego = 0";
                        $result = $conn->query($sql);

                        if ($result->num_rows > 0) {
                            while ($row = $result->fetch_assoc()) {
                                $isBought = $row['comprado'] == 1;

                                $imageClass = $isBought ? "bought" : "not-bought";

                                echo '<div class="image-container ' . $imageClass . '">';
                                echo '<img src="' . htmlspecialchars($row['url_img']) . '" alt="' . htmlspecialchars($row['nombre']) . '" style="width:200px; height:200px; margin-bottom:10px;" onclick="updateProfilePicture(\'' . htmlspecialchars($row['url_img']) . '\', ' . ($isBought ? 'true' : 'false') . ')">';
                                echo '</div>';
                            }
                        } else {
                            echo "<p>No images found.</p>";
                        }

                        $conn->close();
                        ?>
                    </div>
                </div>
            </div>

        </section>



        <section id="activity" class="content" style="margin-left: 200px;">
            <?php foreach ($games as $game): ?>
                <div class="profile-top" style="margin-left: -200px">
                    <img src="<?php echo $game['img_juego']; ?>" alt="logo"
                        style="border-radius: 10px; height:260px; width:200px;">
                    <div class="profile-desc" style="display:flex; flex-direction: column; gap:20px">
                        <?php
                        $time = "0";
                        $last_session = "N/A";
                        $archivements = "000";

                        foreach ($activities as $activity) {
                            if ($activity['id_juego'] == $game['id_juego']) {
                                $time = $activity['time'];
                                $last_session = $activity['last_session'];
                                $archivements = $activity['archivements'];
                                break;
                            }
                        }

                        $appears = substr_count($archivements, '1');
                        ?>

                        <div class="test" style="display: flex;">
                            <svg width="70px" height="70px" viewBox="0 0 24 24" fill="none"
                                xmlns="http://www.w3.org/2000/svg" transform="rotate(180)">
                                <g id="SVGRepo_bgCarrier" stroke-width="0"></g>
                                <g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g>
                                <g id="SVGRepo_iconCarrier">
                                    <path
                                        d="M13 8L9 12M9 12L13 16M9 12H21M19.4845 7C17.8699 4.58803 15.1204 3 12 3C7.02944 3 3 7.02944 3 12C3 16.9706 7.02944 21 12 21C15.1204 21 17.8699 19.412 19.4845 17"
                                        stroke="#6CA67E" stroke-width="1" stroke-linecap="round" stroke-linejoin="round">
                                    </path>
                                </g>
                            </svg>
                            <div class="game-data" style="display: flex; flex-direction: column;">
                                <h2 style="color:#e0dddd; margin-top:9px; margin-left:-2px;">Ultima sesion</h2>
                                <p style="font-size:0.9em; color:#b4afaf; margin-left:-1px"><?php echo $last_session; ?></p>
                            </div>
                        </div>
                        <div class="test" style="display: flex;">
                            <svg style="margin-left:6px" fill="#6CA67E" height="56px" width="56px" version="1.1" id="Capa_1"
                                xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"
                                viewBox="0 0 125.668 125.668" xml:space="preserve">
                                <g id="SVGRepo_bgCarrier" stroke-width="0"></g>
                                <g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g>
                                <g id="SVGRepo_iconCarrier">
                                    <g>
                                        <path
                                            d="M84.17,76.55l-16.9-9.557V32.102c0-2.541-2.061-4.601-4.602-4.601s-4.601,2.061-4.601,4.601v37.575 c0,0.059,0.016,0.115,0.017,0.174c0.006,0.162,0.025,0.319,0.048,0.479c0.021,0.146,0.042,0.291,0.076,0.433 c0.035,0.141,0.082,0.277,0.129,0.414c0.051,0.146,0.1,0.287,0.164,0.426c0.061,0.133,0.134,0.257,0.208,0.383 c0.075,0.127,0.148,0.254,0.234,0.374c0.088,0.122,0.188,0.235,0.288,0.349c0.097,0.11,0.192,0.217,0.299,0.317 c0.107,0.101,0.222,0.19,0.339,0.28c0.126,0.098,0.253,0.191,0.39,0.276c0.052,0.031,0.092,0.073,0.145,0.102L79.64,84.562 c0.716,0.404,1.493,0.597,2.261,0.597c1.605,0,3.163-0.841,4.009-2.337C87.161,80.608,86.381,77.801,84.17,76.55z">
                                        </path>
                                        <path
                                            d="M62.834,0C28.187,0,0,28.187,0,62.834c0,34.646,28.187,62.834,62.834,62.834c34.646,0,62.834-28.188,62.834-62.834 C125.668,28.187,97.48,0,62.834,0z M66.834,115.501v-9.167h-8v9.167c-24.77-1.865-44.823-20.872-48.292-45.167h9.459v-8h-9.988 c0.258-27.558,21.716-50.126,48.821-52.167v9.167h8v-9.167c27.104,2.041,48.563,24.609,48.821,52.167h-9.487v8h8.958 C111.657,94.629,91.605,113.636,66.834,115.501z">
                                        </path>
                                    </g>
                                </g>
                            </svg>
                            
                        <div class="game-data" style="display: flex; flex-direction: column; margin-left:9px; margin-top:3px;">
                            <div style="display: flex; align-items: center;">
                                <h2 style="color:#e0dddd; margin-top:2px; margin-left:-4px;">Tiempo registrado</h2>
                            </div>
                            <p class="time-row" style="font-size:0.9em; color:#b4afaf; margin-left:-1px">
                                <span id="time-<?php echo $game['id_juego']; ?>" data-real-time="<?php echo $time; ?>">??:??:??</span>
                                <label class="time-toggle">
                                    <input type="checkbox" onchange="toggleTime(this, '<?php echo $game['id_juego']; ?>')">
                                    <span class="checkmark"></span>
                                    <span style="color: #b4afaf; font-size: 1em; transform: translateY(3px); margin-left:2px;">Mostrar tiempo</span>
                                </label>
                            </p>
                        </div>

                        </div>
                        <div class="test" style="display: flex;">
                            <svg width="70px" height="70px" viewBox="0 0 16 16" version="1.1"
                                xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"
                                fill="#000000">
                                <g id="SVGRepo_bgCarrier" stroke-width="0"></g>
                                <g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g>
                                <g id="SVGRepo_iconCarrier">
                                    <path fill="#6CA67E"
                                        d="M10 12.2c-0.3 0-0.5-0.1-0.8-0.2l-1.2-0.5-1.2 0.5c-0.2 0.1-0.5 0.2-0.8 0.2-0.2 0-0.3 0-0.5-0.1l-0.5 3.9 3-2 3 2-0.6-3.9c-0.1 0.1-0.3 0.1-0.4 0.1z">
                                    </path>
                                    <path fill="#6CA67E"
                                        d="M12.9 5.9c-0.1-0.2-0.1-0.5 0-0.7l0.6-1.2c0.2-0.4 0-0.9-0.5-1.1l-1.3-0.5c-0.2-0.1-0.4-0.3-0.5-0.5l-0.5-1.3c-0.1-0.4-0.4-0.6-0.7-0.6-0.1 0-0.3 0-0.4 0.1l-1.3 0.6c-0.1 0-0.2 0-0.3 0s-0.2 0-0.3-0.1l-1.3-0.5c-0.1-0.1-0.3-0.1-0.4-0.1-0.3 0-0.6 0.2-0.8 0.5l-0.5 1.4c0 0.2-0.2 0.4-0.4 0.5l-1.4 0.5c-0.4 0.1-0.6 0.6-0.4 1.1l0.6 1.3c0.1 0.2 0.1 0.5 0 0.7l-0.6 1.2c-0.2 0.4 0 0.9 0.5 1.1l1.3 0.5c0.2 0.1 0.4 0.3 0.5 0.5l0.5 1.3c0.1 0.4 0.4 0.6 0.7 0.6 0.1 0 0.2 0 0.3-0.1l1.3-0.6c0.1 0 0.2-0.1 0.3-0.1s0.2 0 0.3 0.1l1.3 0.6c0.1 0.1 0.2 0.1 0.3 0.1 0.3 0 0.6-0.2 0.8-0.5l0.5-1.3c0.1-0.2 0.3-0.4 0.5-0.5l1.3-0.5c0.4-0.2 0.7-0.7 0.5-1.1l-0.5-1.4zM8 9.6c-2.2 0-4-1.8-4-4s1.8-4 4-4 4 1.8 4 4c0 2.2-1.8 4-4 4z">
                                    </path>
                                    <path fill="#6CA67E"
                                        d="M11 5.6c0 1.657-1.343 3-3 3s-3-1.343-3-3c0-1.657 1.343-3 3-3s3 1.343 3 3z">
                                    </path>
                                </g>
                            </svg>
                            <div class="game-data" style="display: flex; flex-direction: column; margin-top:5px;">
                                <h2>Logros</h2>
                                <div style="display: flex; margin-top:2px;">
                                    <p style="font-size:0.9em; color:#b4afaf; margin-left:2px">
                                        <?php echo $appears; ?>/3
                                    </p>
                                    <progress max="3" value="<?php echo $appears; ?>" style="margin-left:4px;"></progress>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            <?php endforeach; ?>
        </section>

        <script>
            function toggleTime(checkbox, gameId) {
                const timeElement = document.getElementById('time-' + gameId);
                let realTime = timeElement.getAttribute('data-real-time');

                if (realTime === "0") {
                    realTime = "00:00:00";
                }

                if (checkbox.checked) {
                    timeElement.textContent = realTime;
                } else {
                    timeElement.textContent = '??:??:??';
                }
            }
        </script>

        <section id="library" class="content library" style="margin-right: 60px">
            <div class="game-grid-container" style="gap: 60px;">

                <?php
                $servername = "localhost";
                $username = "root";
                $password = "";
                $dbname = "desktopapp";

                $conn = new mysqli($servername, $username, $password, $dbname);

                $sql = "SELECT * FROM juegos WHERE id_juego >= 1";
                $result = $conn->query($sql);

                if ($result->num_rows > 0) {
                    while ($row = $result->fetch_assoc()) {
                        echo <<<JUEGO
                        <div class="game-holder" style="cursor: pointer;" onclick="window.location.href='{$row['url']}'">
                            <img src="{$row['img_juego']}" alt="logo" style="height:260px; width:200px; border-radius: 10px">
                            <p style="margin-top:5px; margin-left:15px; font-size: 1.3em;">{$row['nombre']}</p>
                        </div>
                    JUEGO;
                    }
                } else {
                    echo "0 results";
                }
                $conn->close();
                ?>




            </div>

        </section>



        <section id="shop" class="content"
            style="margin-left:200px; display:flex; flex-direction:column; margin-top: 10px;">

            <div class="head">
                <div class="info">
                    <svg width="50px" height="50px" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <g id="SVGRepo_bgCarrier" stroke-width="0"></g>
                        <g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g>
                        <g id="SVGRepo_iconCarrier">
                            <path
                                d="M11.5805 4.77604C12.2752 3.00516 12.6226 2.11971 13.349 2.01056C14.0755 1.90141 14.6999 2.64083 15.9488 4.11967L16.2719 4.50226C16.6268 4.9225 16.8042 5.13263 17.0455 5.25261C17.2868 5.37259 17.5645 5.38884 18.1201 5.42135L18.6258 5.45095C20.5808 5.56537 21.5583 5.62258 21.8975 6.26168C22.2367 6.90079 21.713 7.69853 20.6656 9.29403L20.3946 9.7068C20.097 10.1602 19.9482 10.3869 19.908 10.6457C19.8678 10.9045 19.9407 11.1662 20.0866 11.6895L20.2195 12.166C20.733 14.0076 20.9898 14.9284 20.473 15.4325C19.9562 15.9367 19.0081 15.6903 17.1118 15.1975L16.6213 15.07C16.0824 14.93 15.813 14.86 15.5469 14.8999C15.2808 14.9399 15.0481 15.0854 14.5828 15.3763L14.1591 15.6412C12.5215 16.6649 11.7027 17.1768 11.0441 16.8493C10.3854 16.5217 10.3232 15.5717 10.1987 13.6717L10.1665 13.1801C10.1311 12.6402 10.1134 12.3702 9.98914 12.1361C9.86488 11.902 9.64812 11.7302 9.21459 11.3867L8.8199 11.0739C7.29429 9.86506 6.53149 9.26062 6.64124 8.55405C6.751 7.84748 7.66062 7.50672 9.47988 6.8252L9.95054 6.64888C10.4675 6.45522 10.726 6.35839 10.9153 6.17371C11.1046 5.98903 11.2033 5.73742 11.4008 5.23419L11.5805 4.77604Z"
                                fill="#6CA67E"></path>
                            <g opacity="0.5">
                                <path
                                    d="M5.31003 9.59277C2.87292 11.9213 1.27501 15.8058 2.33125 22.0002C3.27403 19.3966 5.85726 17.2407 8.91219 15.9528C8.80559 15.3601 8.7583 14.6364 8.70844 13.8733L8.66945 13.2782C8.66038 13.1397 8.65346 13.0347 8.64607 12.9443C8.643 12.9068 8.64012 12.8754 8.63743 12.8489C8.61421 12.829 8.58591 12.8053 8.55117 12.7769C8.47874 12.7177 8.39377 12.6503 8.28278 12.5623L7.80759 12.1858C7.11448 11.6368 6.46884 11.1254 6.02493 10.6538C5.77182 10.385 5.48876 10.0304 5.31003 9.59277Z"
                                    fill="#6CA67E"></path>
                                <path
                                    d="M10.3466 15.4231C10.3415 15.3857 10.3365 15.3475 10.3316 15.3086L10.3877 15.41C10.374 15.4144 10.3603 15.4187 10.3466 15.4231Z"
                                    fill="#6CA67E"></path>
                            </g>
                        </g>
                    </svg>
                    <h2><?php echo htmlspecialchars($coins); ?></h2>
                </div>
            </div>
            <div class="game-grid-container" style="gap: 60px;">

                <?php
                $servername = "localhost";
                $username = "root";
                $password = "";
                $dbname = "desktopapp";

                $conn = new mysqli($servername, $username, $password, $dbname);

                $sql = "SELECT * FROM objetos WHERE userID = $id";
                $_SESSION['userID'] = $id;
                $result = $conn->query($sql);

                if ($result->num_rows > 0) {
                    while ($row = $result->fetch_assoc()) {
                        $id_objeto = $row['id_objeto'];
                        $comprado = $row['comprado'];
                        $precio = $row['precio'];
                        $blackoutClass = $comprado ? 'blackout' : '';
                        $display = $comprado ? 'none' : 'block';
                        $blackoutText = $comprado ? '<div class="blackout-text">COMPRADO</div>' : '';


                        echo <<<TIENDA
                        <div class="game-holder" style="position: relative;">
                            <a href="comprar.php?id_objeto=$id_objeto&precio=$precio" style="display: block; text-decoration: none; color: inherit;">
                                <div class="image-container" style="position: relative; width: 200px; height: 260px; border-radius: 10px; overflow: hidden;">
                                    <img src="{$row['url_img']}" alt="logo" style="height: 100%; width: 100%;">
                                    $blackoutText
                                </div>
                                <p style="margin-top: 5px; font-size: 1.3em; display: $display;">{$row['nombre']}</p>
                                <div class="price-holder" style="display: $display;">
                                    <svg width="25px" height="25px" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                                        <g id="SVGRepo_bgCarrier" stroke-width="0"></g>
                                        <g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g>
                                        <g id="SVGRepo_iconCarrier">
                                            <path
                                                d="M11.5805 4.77604C12.2752 3.00516 12.6226 2.11971 13.349 2.01056C14.0755 1.90141 14.6999 2.64083 15.9488 4.11967L16.2719 4.50226C16.6268 4.9225 16.8042 5.13263 17.0455 5.25261C17.2868 5.37259 17.5645 5.38884 18.1201 5.42135L18.6258 5.45095C20.5808 5.56537 21.5583 5.62258 21.8975 6.26168C22.2367 6.90079 21.713 7.69853 20.6656 9.29403L20.3946 9.7068C20.097 10.1602 19.9482 10.3869 19.908 10.6457C19.8678 10.9045 19.9407 11.1662 20.0866 11.6895L20.2195 12.166C20.733 14.0076 20.9898 14.9284 20.473 15.4325C19.9562 15.9367 19.0081 15.6903 17.1118 15.1975L16.6213 15.07C16.0824 14.93 15.813 14.86 15.5469 14.8999C15.2808 14.9399 15.0481 15.0854 14.5828 15.3763L14.1591 15.6412C12.5215 16.6649 11.7027 17.1768 11.0441 16.8493C10.3854 16.5217 10.3232 15.5717 10.1987 13.6717L10.1665 13.1801C10.1311 12.6402 10.1134 12.3702 9.98914 12.1361C9.86488 11.902 9.64812 11.7302 9.21459 11.3867L8.8199 11.0739C7.29429 9.86506 6.53149 9.26062 6.64124 8.55405C6.751 7.84748 7.66062 7.50672 9.47988 6.8252L9.95054 6.64888C10.4675 6.45522 10.726 6.35839 10.9153 6.17371C11.1046 5.98903 11.2033 5.73742 11.4008 5.23419L11.5805 4.77604Z"
                                                fill="#6CA67E"></path>
                                            <g opacity="0.5">
                                                <path
                                                    d="M5.31003 9.59277C2.87292 11.9213 1.27501 15.8058 2.33125 22.0002C3.27403 19.3966 5.85726 17.2407 8.91219 15.9528C8.80559 15.3601 8.7583 14.6364 8.70844 13.8733L8.66945 13.2782C8.66038 13.1397 8.65346 13.0347 8.64607 12.9443C8.643 12.9068 8.64012 12.8754 8.63743 12.8489C8.61421 12.829 8.58591 12.8053 8.55117 12.7769C8.47874 12.7177 8.39377 12.6503 8.28278 12.5623L7.80759 12.1858C7.11448 11.6368 6.46884 11.1254 6.02493 10.6538C5.77182 10.385 5.48876 10.0304 5.31003 9.59277Z"
                                                    fill="#6CA67E"></path>
                                                <path
                                                    d="M10.3466 15.4231C10.3415 15.3857 10.3365 15.3475 10.3316 15.3086L10.3877 15.41C10.374 15.4144 10.3603 15.4187 10.3466 15.4231Z"
                                                    fill="#6CA67E"></path>
                                            </g>
                                        </g>
                                    </svg>
                                    <span class="number">{$row['precio']}</span>
                                </div>
                            </a>
                        </div>
                        TIENDA;
                    }
                } else {
                    echo "0 results";
                }

                $conn->close();
                ?>





            </div>
        </section>
    </main>

    <script src="script.js"></script>
    <script>
        function togglePasswordVisibility() {
            var passwordField = document.getElementById("password")
            if (passwordField.type === "password") {
                passwordField.type = "text"
            } else {
                passwordField.type = "password"
            }
        }
        function openPopup() {
            var popup = document.getElementById("popup");
            popup.style.display = "block";
        }

        function closePopup() {
            var popup = document.getElementById("popup");
            popup.style.display = "none";
        }

        function updateProfilePicture(imageUrl, isBought) {
            if (isBought) {
                var xhr = new XMLHttpRequest();
                xhr.open("POST", "update_profile_picture.php", true);
                xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");

                xhr.onreadystatechange = function () {
                    if (xhr.readyState === 4) {
                        console.log("Ready State: " + xhr.readyState);
                        console.log("Status: " + xhr.status);
                        console.log("Response Text: " + xhr.responseText);
                        if (xhr.status === 200) {
                            var placeholders = document.querySelectorAll("#user-pfp");
                            placeholders.forEach(function (placeholder) {
                                placeholder.src = imageUrl;
                            });
                        } else {
                            console.error("Error: " + xhr.status + " - " + xhr.statusText);
                        }
                    }
                };

                xhr.send("newProfilePicture=" + encodeURIComponent(imageUrl));
            } else {
                alert("Aun no compraste esta imagen");
            }
        }
    </script>
</body>

</html>