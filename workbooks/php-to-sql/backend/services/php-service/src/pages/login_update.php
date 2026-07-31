<?php
include "../logic/db_connection.php";
include '../logic/functions.php';
include "../structure/head.php";
include "../structure/footer.php";
setDatabaseConnection(); ?>


<div class='container p-5'>
  <div class='row'>
    <div class="col">
      <form action="login_update.php" method="post">
        <div class="form-group">
          <label class="form-label" for="username">Username</label>
          <input type="text" class="form-control" name="username">
        </div>
        <div class="form-group">
          <label class="form-label" for="password">Password</label>
          <input type="password" class="form-control" name="password">
        </div>
        <div class="form-group">
          <select name="id">
            <?php
            setDatabaseConnection();
            showAllIds($connection);
            ?>
          </select>
        </div>
        <br>
        <input class="btn btn-primary" type="submit" value="Update" name="submit">
      </form>

      <?php

      if (isset($_POST['submit'])) {
        $sub_username = $_POST['username'];
        $sub_password = $_POST['password'];
        $sub_id = $_POST['id'];

        if ($sub_username && $sub_password) {
          echo "<p>" . $sub_username . " your password is " . $sub_password . "</p>";
          echo '<hr>';

          updateUser($sub_username, $sub_password, $sub_id, $connection);
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
</body>

</html>