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
  name        TEXT,
  event_fk    INTEGER,
  seats       INTEGER CHECK(seats > 1),
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

CREATE TRIGGER IF NOT EXISTS unique_name_insert
  BEFORE INSERT ON People
  BEGIN
    SELECT CASE WHEN NEW.name IN (
      SELECT 
        p.name
      FROM People p
      INNER JOIN Cars c ON c.id = p.car_fk
      INNER JOIN Events e ON e.id = c.event_fk
      WHERE e.id = (
        SELECT e.id FROM Events e
        INNER JOIN CARS c on c.event_fk = e.id
        WHERE c.id = NEW.car_fk
      )
    )
    THEN RAISE (ABORT, "Person already in event") 
  END; 
END;

CREATE TRIGGER IF NOT EXISTS unique_name_update
  BEFORE UPDATE ON People
  BEGIN
    SELECT CASE WHEN NEW.name IN (
      SELECT 
        p.name
      FROM People p
      INNER JOIN Cars c ON c.id = p.car_fk
      INNER JOIN Events e ON e.id = c.event_fk
      WHERE e.id = (
        SELECT e.id FROM Events e
        INNER JOIN CARS c on c.event_fk = e.id
        WHERE c.id = NEW.car_fk
      )
    )
    THEN RAISE (ABORT, "Person already in event")
  END; 
END;

CREATE TRIGGER IF NOT EXISTS unique_car_name_insert
  BEFORE INSERT ON Cars
  BEGIN
    SELECT CASE WHEN NEW.name IN (
      SELECT 
        c.name
      FROM Cars c
      INNER JOIN Events e ON e.id = c.event_fk
      WHERE e.id = NEW.event_fk
    )
    THEN RAISE (ABORT, "Car name already in event") 
  END; 
END;

CREATE TRIGGER IF NOT EXISTS unique_car_name_update
  BEFORE UPDATE ON Cars
  BEGIN
    SELECT CASE WHEN NEW.name IN (
      SELECT 
        c.name
      FROM Cars c
      INNER JOIN Events e ON e.id = c.event_fk
      WHERE e.id = NEW.event_fk
    )
    THEN RAISE (ABORT, "Car name already in event") 
  END; 
END;


CREATE TRIGGER IF NOT EXISTS cant_fit_insert
  BEFORE INSERT ON People
  BEGIN
    SELECT CASE WHEN (SELECT c.seats FROM Cars c 
    WHERE c.id = NEW.car_fk)=(
      SELECT 
        COUNT(p.name)
      FROM People p
      INNER JOIN Cars c ON c.id = p.car_fk
      WHERE c.id = NEW.car_fk
    )
    THEN RAISE (ABORT, "Car is full") 
  END; 
END;

CREATE TRIGGER IF NOT EXISTS cant_fit_unique
  BEFORE INSERT ON People
  BEGIN
    SELECT CASE WHEN (SELECT c.seats FROM Cars c 
    WHERE c.id = NEW.car_fk)=(
      SELECT 
        COUNT(p.name)
      FROM People p
      INNER JOIN Cars c ON c.id = p.car_fk
      WHERE c.id = NEW.car_fk
    )
    THEN RAISE (ABORT, "Car is full") 
  END; 
END;