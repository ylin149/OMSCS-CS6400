USE CS6400_Summer2023_Team025; 
-- check if an user is added
SELECT *
FROM household
LEFT JOIN PublicUtility ON household.email = PublicUtility.email
WHERE household.email IN ('team025_2@gmail.com', 'team025_1@gmail.com');


-- check if an appliance is added for the user
SELECT *
FROM Appliance
WHERE email IN ('team025_2@gmail.com', 'team025_1@gmail.com');


SELECT *
FROM Appliance
LEFT JOIN WaterHeater ON Appliance.email = WaterHeater.email
WHERE Appliance.email IN ('team025_2@gmail.com', 'team025_1@gmail.com');

SELECT *
FROM Appliance
LEFT JOIN AirHandler ON Appliance.email = AirHandler.email
WHERE Appliance.email IN ('team025_2@gmail.com', 'team025_1@gmail.com');


-- check if an powergenerator is added for the user
SELECT *
FROM PowerGenerator
WHERE email IN ('team025_2@gmail.com', 'team025_1@gmail.com');

-- check if a waterheater is added for the user
SELECT *
FROM WaterHeater
WHERE email IN ('team025_2@gmail.com', 'team025_1@gmail.com');

-- check if an airhandler is added for the user
SELECT *
FROM AirHandler
WHERE email IN ('team025_2@gmail.com', 'team025_1@gmail.com');

-- check if an airconditioner is added for the user
SELECT *
FROM AirConditioner
WHERE email IN ('team025_2@gmail.com', 'team025_1@gmail.com');

-- check if a heater is added for the user
SELECT *
FROM Heater
WHERE email IN ('team025_2@gmail.com', 'team025_1@gmail.com');

-- check if a heatpump is added for the user
SELECT *
FROM HeatPump
WHERE email IN ('team025_2@gmail.com', 'team025_1@gmail.com');


SELECT COUNT(*)
FROM Appliance
WHERE email IN ('team025_2@gmail.com', 'team025_1@gmail.com');

