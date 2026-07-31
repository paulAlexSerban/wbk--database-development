<?php 
include "../logic/db_connection.php";
include '../logic/functions.php';
include "../structure/head.php";
include "../structure/footer.php";
setDatabaseConnection(); ?>


<div class='container p-5'>
  <div class='row '>
    <div class="col">
      <form action="login_add.php" method="post">
        <div class="form-group">
          <label class="form-label" for="username">Username</label>
          <input type="text" class="form-control" name="username">
        </div>
        <div class="form-group">
          <label class="form-label" for="password">Password</label>
          <input type="password" class="form-control" name="password">
        </div>
        <br>
        <input class="btn btn-primary" type="submit" value="Submit" name="submit">
      </form>

      <?php

      if (isset($_POST['submit'])) {
        $sub_username = $_POST['username'];
        $sub_password = $_POST['password'];

        $sub_username = mysqli_real_escape_string($connection, $sub_username);
        $sub_password = mysqli_real_escape_string($connection, $sub_password);

        if ($sub_username && $sub_password) {
          echo "<p>" . $sub_username . " your password is " . $sub_password . "</p>";
          echo '<hr>';

          addUser($sub_username, securePassword($sub_password), $connection);
        } else {
          echo '<p>NO field should be left blank</p>';
        }
      }

      ?>
    </div>

    <div class="col">
      <?php
      getUsers($connection);
      ?>
    </div>

  </div>
</div>
<hr>
<div class="container">

</div>
</body>

</html>