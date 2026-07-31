<?php 
include "../logic/db_connection.php";
include '../logic/functions.php';
include "../structure/footer.php";
setDatabaseConnection();

$name = 'SomeCookies';
$value = 100;
$expiration = time() + ((60*60*24*7)); // set expiration from current day of setting the cookie plus (60sec * 60min * 24hours * 7days = 1 week)
// set cookies by using the php pre-built function
setcookie($name, $value, $expiration);

include "../structure/head.php";

// read the cookies if it was set

if(isset($_COOKIE[$name])) {
  $someOne = $_COOKIE[$name];
  echo $someOne;
} else {
  $someOne = '';
}
?>


  
</body>
</html>