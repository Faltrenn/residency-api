CREATE DATABASE IF NOT EXISTS residency;

USE residency;

CREATE TABLE IF NOT EXISTS roles (title VARCHAR(30), PRIMARY KEY (title));

INSERT INTO
  roles (title)
VALUES
  ("Admin"),
  ("Professor"),
  ("Residente");

CREATE TABLE IF NOT EXISTS institutions (
  name VARCHAR(100),
  short_name VARCHAR(10),
  PRIMARY KEY (short_name)
);

INSERT INTO
  institutions (name, short_name)
VALUES
  ("Escola Multicampi de Ciências Médicas", "EMCM"),
  (
    "Universidade Federal do Rio Grande do Norte",
    "UFRN"
  );

CREATE TABLE IF NOT EXISTS users (
  id INT AUTO_INCREMENT,
  name VARCHAR(50) NOT NULL,
  pass VARCHAR(255) NOT NULL,
  role_title VARCHAR(30) NOT NULL,
  institution_short_name VARCHAR(10) NOT NULL,
  FOREIGN KEY (role_title) REFERENCES roles (title),
  FOREIGN KEY (institution_short_name) REFERENCES institutions (short_name),
  PRIMARY KEY (id)
);

INSERT INTO
  users (name, role_title, pass, institution_short_name)
VALUES
  ("Emanuel", "Admin", "senha", "UFRN"),
  ("Emanuel Professor", "Professor", "senha", "UFRN"),
  ("Emanuel Residente", "Residente", "senha", "UFRN");

CREATE TABLE IF NOT EXISTS questions (
  id INT AUTO_INCREMENT,
  title TEXT NOT NULL,
  PRIMARY KEY (id)
);

INSERT INTO
  questions (title)
VALUES
  ("Pergunta muito massa 1"),
  ("Pergunta muito massa 2"),
  ("Pergunta muito massa 3"),
  ("Pergunta muito massa 4");

CREATE TABLE IF NOT EXISTS answers (
  id INT AUTO_INCREMENT,
  title TEXT NOT NULL,
  question_id INT NOT NULL,
  FOREIGN KEY (question_id) REFERENCES questions (id),
  PRIMARY KEY (id)
);

INSERT INTO
  answers (title, question_id)
VALUES
  ("alternativa 1 da pergunta 1", 1),
  ("alternativa 2 da pergunta 1", 1),
  ("alternativa 3 da pergunta 1", 1),
  ("alternativa 4 da pergunta 1", 1),
  ("alternativa 1 da pergunta 2", 2),
  ("alternativa 2 da pergunta 2", 2),
  ("alternativa 3 da pergunta 2", 2),
  ("alternativa 4 da pergunta 2", 2),
  ("alternativa 1 da pergunta 3", 3),
  ("alternativa 2 da pergunta 3", 3),
  ("alternativa 3 da pergunta 3", 3),
  ("alternativa 4 da pergunta 3", 3),
  ("alternativa 1 da pergunta 4", 4),
  ("alternativa 2 da pergunta 4", 4),
  ("alternativa 3 da pergunta 4", 4),
  ("alternativa 4 da pergunta 4", 4);

CREATE TABLE IF NOT EXISTS procedures (title VARCHAR(100), PRIMARY KEY (title));

INSERT INTO
  procedures (title)
VALUES
  ("Apendicectomia"),
  ("Colecistectomia"),
  ("Hérnia inguinal"),
  ("Histerectomia"),
  ("Cesárea"),
  ("Catarata"),
  ("Bariátrica"),
  ("Artroplastia de joelho"),
  ("Artroplastia de quadril"),
  ("Hemorrhoidectomia"),
  ("Ressecção do intestino"),
  ("Mastectomia"),
  ("Amigdalectomia"),
  ("Septoplastia"),
  ("Reparo de fratura óssea"),
  ("Endarterectomia carotídea"),
  ("Prostatectomia"),
  ("Vasectomia"),
  ("Laqueadura tubária"),
  ("Túnel do carpo");

CREATE TABLE IF NOT EXISTS questionnaire (
  id INT AUTO_INCREMENT,
  procedure_title VARCHAR(100) NOT NULL,
  professor_id INT NOT NULL,
  resident_id INT NOT NULL,
  created_at DATETIME,
  FOREIGN KEY (procedure_title) REFERENCES procedures (title),
  FOREIGN KEY (professor_id) REFERENCES users (id),
  FOREIGN KEY (resident_id) REFERENCES users (id),
  PRIMARY KEY (id)
);

INSERT INTO
  questionnaire (procedure_title, professor_id, resident_id)
VALUES
  ("vasectomia", 2, 3);

CREATE TABLE IF NOT EXISTS questions_answereds (
  questionnaire_id INT NOT NULL,
  question_id INT NOT NULL,
  answer_id INT NOT NULL,
  FOREIGN KEY (questionnaire_id) REFERENCES questionnaire (id),
  FOREIGN KEY (question_id) REFERENCES questions (id),
  FOREIGN KEY (answer_id) REFERENCES answers (id),
  PRIMARY KEY (questionnaire_id, question_id, answer_id)
);

INSERT INTO
  questions_answereds (questionnaire_id, question_id, answer_id)
VALUES
  (1, 1, 3),
  (1, 2, 4),
  (1, 3, 1),
  (1, 4, 2);
