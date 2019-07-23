-- Initialize the database.
-- Drop any existing data and create empty tables.

DROP TABLE IF EXISTS Events;
DROP TABLE IF EXISTS Cars;
DROP TABLE IF EXISTS Passengers;

CREATE TABLE `Events`
(
  `id` int PRIMARY KEY,
  `when` datetime,
  `name` varchar(200)
);

CREATE TABLE `Cars`
(
  `id` int PRIMARY KEY,
  `event_fk` int,
  `name` varchar(200),
  `seats` int
);

CREATE TABLE `Passengers`
(
  `id` int PRIMARY KEY,
  `car_fk` int,
  `name` varchar(200)
);

ALTER TABLE `Cars` ADD FOREIGN KEY (`event_fk`) REFERENCES `Events` (`id`);

ALTER TABLE `Passengers` ADD FOREIGN KEY (`car_fk`) REFERENCES `Cars` (`id`);
