-- Initialize the database.
-- Drop any existing data and create empty tables.

DROP TABLE IF EXISTS Events;
DROP TABLE IF EXISTS Cars;
DROP TABLE IF EXISTS Passengers;

CREATE TABLE Events
(
  id    INTEGER PRIMARY KEY AUTOINCREMENT,
  time  INTEGER,
  name  TEXT
);

CREATE TABLE Cars
(
  id          INTEGER PRIMARY KEY AUTOINCREMENT,
  event_fk    INTEGER,
  seats       INTEGER,
  is_default  BOOLEAN,
  FOREIGN KEY(event_fk) REFERENCES Events(id)
);

CREATE TABLE People
(
  id      INTEGER PRIMARY KEY AUTOINCREMENT,
  car_fk  INTEGER,
  name    TEXT,
  driver  BOOLEAN,
  FOREIGN KEY(car_fk) REFERENCES Cars(id)
);
