CREATE DATABASE IF NOT EXISTS db_residency;

USE db_residency;

CREATE TABLE IF NOT EXISTS roles (title VARCHAR(30), PRIMARY KEY (title));

INSERT INTO
  roles (title)
VALUES
  ("Professor"),
  ("Residente");
