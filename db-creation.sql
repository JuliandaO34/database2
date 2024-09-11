CREATE DATABASE IF NOT EXISTS actors_performances;

USE actors_performances;


CREATE TABLE IF NOT EXISTS performances (
    id INT AUTO_INCREMENT PRIMARY KEY,
    Performances_Date DATE NOT NULL,
    Performances_Hour TIME NOT NULL,
    Name_Performances VARCHAR(255),
    Performances_Price INT NOT NULL
);


CREATE TABLE IF NOT EXISTS actors (
    id INT AUTO_INCREMENT PRIMARY KEY,
    FullName VARCHAR(255),
    Code VARCHAR(255),
    Phone_Number VARCHAR(255),
    Email VARCHAR(255),
    performances_id INT, 
    FOREIGN KEY (performances_id) REFERENCES performances(id) ON DELETE CASCADE
);


