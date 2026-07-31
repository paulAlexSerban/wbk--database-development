<?php

function setDatabaseConnection()
{
  global $connection;

  // these are the defined authentication environment in db service
  $host = 'database-in-php_mysql'; // the MySQL service named in the docker-compose.yml
  $user = 'root'; // database user-name defined in .env
  $pass = 'root'; // database password defined in .env
  $mydatabase = 'database-in-php';

  // check the MySQL connection status
  $connection = new mysqli($host, $user, $pass, $mydatabase);
  if (!$connection) {
    die("Connection failed: " . $connection->connect_error);
  }
}

function addUser($username, $password, $connection)
{
  $query = "INSERT INTO `users`(username, password)";
  $query .= "VALUES ('$username', '$password')";
  $result_query = $connection->query($query);

  if (!$result_query) {
    die('Query FAILED - ' . mysqli_error($connection));
  }
}

function getUsers($connection)
{
  // select query fro database
  $sql = "SELECT * FROM `users`";
  $users = [];

  // if ($result = $connection->query($sql)) {
  //   while ($data = $result->fetch_object()) {
  //     $users[] = $data;
  //   }
  // }

  // foreach ($users as $user) {
  //   echo "<ul>";
  //   echo "<li>" . $user->username . " ---- " . $user->password . "</li>";
  //   echo "</ul";
  // }

  if ($result = $connection->query($sql)) {
    while ($row = $result->fetch_assoc()) {
?>
      <pre>
        <?php
        print_r($row);
        ?> 
      </pre>
<?php
    }
  }
}

function showAllIds($connection)
{
  $sql = "SELECT * FROM users";
  if ($result = $connection->query($sql)) {
    while ($row = $result->fetch_assoc()) {
      $id = $row['id'];
      echo "<option value='" . $id . "'>" . $id . "</option>";
    }
  }
}
# Eg. UPDATE `users` SET `username` = 'paasdfasdf', `password` = 'asasdf' WHERE `users`.`id` = 1;
function updateUser($username, $password, $id, $connection) {
  $query = "UPDATE `users` SET ";
  $query .= "`username` = '$username', ";
  $query .= "`password` = '$password' ";
  $query .= "WHERE `users`.`id` = $id ";

  echo $query;

  $result = $connection->query($query);

  if(!$result) {
    die("<p>Query failed</p>");
  }
}

function deleteUser($id, $connection) {
  # Eg. DELETE FROM `users` WHERE `users`.`id` = 1"
  $query = "DELETE FROM `users` WHERE ";
  $query .= "`users`.`id` = $id";

  $result = $connection->query($query);

  if(!$result) {
    die("<p>Query failed</p>");
  }
}

function securePassword($unEncrypted) {
  $hashFormat = "$2y$10$";
  $salt = "iusesomecrazystrings22";
  $hashF_and_salt = $hashFormat.$salt;
  $encrypt_password = crypt($unEncrypted, $hashF_and_salt);
  return $encrypt_password;
}
