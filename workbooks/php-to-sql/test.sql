DROP TABLE IF EXISTS `users`;
CREATE TABLE `users` (
    id int NOT null AUTO_INCREMENT,
    username text NOT null,
    password text NOT null,
    PRIMARY KEY (id)
);
INSERT INTO `users` (username, password) VALUES
	("admin","password"),
    ("Alice","this is my password"),
    ("Job","123456789");