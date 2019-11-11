CREATE DATABASE IF NOT EXISTS leccion7;
USE leccion7;
CREATE TABLE usuarios (
  id integer UNSIGNED not null PRIMARY KEY auto_increment,
  nombre varchar(50),
  email varchar(50) not null unique,
  pass varchar(10) not null,
  active tinyint(1) default 1
);
INSERT INTO leccion7.usuarios(nombre, email, pass)
VALUES
  ("jose", "jaskjasd@gmail.com", "111");