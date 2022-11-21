INSERT INTO `USER` (`USERID`, `ADMIN`, `CREATION_TIME`, `LINK_HASH`, `MAIL_ADDRESS`, `USER_NAME`)
VALUES (1, 1, null, 1, 'test@test.test', 'test');
INSERT INTO `USER` (`USERID`, `ADMIN`, `CREATION_TIME`, `LINK_HASH`, `MAIL_ADDRESS`, `USER_NAME`)
VALUES (2, 1, null, 1, 'test2@test2.test2', 'test2');

INSERT INTO `SENSOR_TYPE` (`TYPEID`, `TYPE_NAME`)
VALUES (1, 'Temperatuur'),
       (2, 'Stikstof'),
       (3, 'Koolstofdioxide'),
       (4, 'Fijnstof'),
       (5, 'Luchtvochtigheid'),
       (6, 'Windsnelheid');

INSERT INTO `LOCATION` (`LOCATIONID`, `LATITUDE`, `LONGITUDE`, `LOCATION_NAME`)
VALUES (1, 51.581124, 4.994231, 'Reeshof'),
       (2, 51.575043, 5.002305, 'Reeshof'),
       (3, 51.539151, 5.079001, 'Stappegoor');

INSERT INTO `STATION` (`STATIONID`, `NAME`, `HEIGHT`, `LOCATION_LOCATIONID`, `USERID`, `IS_PUBLIC`)
VALUES (1, 'Voortuin', 1.0, 1, 2, true),
       (2, 'Industrieterrein', 6.0, 2, 1, false),
       (3, 'Fontys dak', 38.2, 3, 1, true);

INSERT INTO `SENSOR` (`SENSORID`, `SENSOR_DATA`, `SENSOR_TYPEID`, `STATIONID`)
VALUES (1, 2, 1, 1),
       (2, 3, 1, 2),
       (3, 4, 1, 3),
       (4, 1, 2, 1),
       (5, 5, 2, 2),
       (6, 3, 2, 3),
       (7, 4, 3, 1),
       (8, 6, 3, 2),
       (9, 2, 3, 3),
       (10, 4, 4, 1),
       (11, 1, 4, 2),
       (12, 1, 4, 3),
       (13, 10, 5, 1),
       (14, 1, 5, 2),
       (15, 4, 5, 3),
       (16, 6, 6, 1),
       (17, 5, 6, 2),
       (18, 3, 6, 3);