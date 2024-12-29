CREATE DATABASE IF NOT EXISTS residency;

USE residency;

CREATE TABLE IF NOT EXISTS roles (title VARCHAR(30), PRIMARY KEY (title));

INSERT INTO
  roles (title)
VALUES
  ("Professor"),
  ("Residente");

CREATE TABLE IF NOT EXISTS institution (
  id AUTO_INCREMENT SMALLINT,
  name VARCHAR(50),
  short_name VARCHAR(10),
  PRIMARY KEY (id)
);

INSERT INTO
  intitution (name, short_name)
VALUES
  ("Escola Multicampi de Ciências Médicas", "EMCM"),
  ( "Universidade Federal do Rio Grande do Norte", "UFRN", "asdasd", "asdasdasdassd", "asdasdasdada")
