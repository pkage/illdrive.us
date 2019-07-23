-- Initialize the database.
-- Drop any existing data and create empty tables.

DROP TABLE IF EXISTS Events;
DROP TABLE IF EXISTS Cars;
DROP TABLE IF EXISTS Passengers;

CREATE TABLE Events
(
  id    INTEGER PRIMARY KEY,
  time  INTEGER,
  name  TEXT
);

CREATE TABLE Cars
(
  id        INTEGER PRIMARY KEY,
  event_fk  INTEGER,
  name      TEXT,
  seats     INTEGER,
  FOREIGN KEY(event_fk) REFERENCES Events(id)
);

CREATE TABLE Passengers
(
  id      INTEGER PRIMARY KEY,
  car_fk  INTEGER,
  name    TEXT,
  FOREIGN KEY(car_fk) REFERENCES Cars(id)
);
