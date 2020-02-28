/*
 * Datenbankbenutzer anlegen
 */
CREATE USER IF NOT EXISTS "webuser" IDENTIFIED BY "password";

/*
 * Datenbank anlegen
 */
CREATE DATABASE IF NOT EXISTS webapp DEFAULT CHARACTER SET = "utf8";
GRANT ALL ON webapp.* TO webuser;

/*
 * Tabellen anlegen und mit Inhalten füllen
 */
USE webapp;

CREATE TABLE IF NOT EXISTS Persons (
    PersonID    INT,
    LastName    VARCHAR(255),
    FirstName   VARCHAR(255),
    Address     VARCHAR(255),
    City        VARCHAR(255),

    PRIMARY KEY(PersonID)
);

INSERT IGNORE INTO Persons
    SET PersonID  = 1,
        LastName  = "Mulder",
        FirstName = "Fox",
        Address   = "42 New Yersey Ave SE",
        City      = "Washington";

INSERT IGNORE INTO Persons
    SET PersonID  = 2,
        LastName  = "Scully",
        FirstName = "Dana",
        Address   = "138 Independence Ave SE",
        City      = "Washington";
