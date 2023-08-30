CREATE DATABASE CS6400_Summer2023_Team025; 

USE CS6400_Summer2023_Team025; 

CREATE TABLE Household ( 

    email varchar(320) NOT NULL, 

    square_footage INT NOT NULL, 

    household_type ENUM('house', 'apartment', 'townhome', 'condominium', 'modular home', 'tiny house') NOT NULL,

    postal_code INT(5) NOT NULL, 

    heating_setting INT NULL, 

    cooling_setting INT NULL, 

    PRIMARY KEY(email) 

); 
 

CREATE TABLE Location( 

    postal_code varchar(5) NOT NULL, 

    city varchar(50) NOT NULL, 

    state varchar(2) NOT NULL, 

    latitude DECIMAL NOT NULL, 

    longitude DECIMAL NOT NULL, 

    PRIMARY KEY (postal_code) 

); 


CREATE TABLE PowerGenerator (  

email varchar(320) NOT NULL, 

generatorID INT AUTO_INCREMENT, 

generator_type ENUM('solar','wind-turbine','mixed') NOT NULL,  

average_monthly_kilowatt_hours_generated INT NOT NULL,  

battery_storage_capacity_kilowatt_hours INT NULL,  

PRIMARY KEY(generatorID),  

FOREIGN KEY (email) REFERENCES Household(email), 

Unique key (email, generatorID) 

); 

 

CREATE TABLE Manufacturer (  

	manufacturer_name varchar(255) Not NULL, 

	PRIMARY KEY(manufacturer_name)  

);  

  

CREATE TABLE Appliance(  

	email varchar(320) NOT NULL,  

	applianceID INT, 

    appliance_type ENUM('water_heater','air_handler') NOT NULL,  

	manufacturer_name varchar(255) NOT NULL,  

	model varchar(50) NULL,  

	BTU INT Not NULL,  

	PRIMARY KEY(email, applianceID),  

	FOREIGN KEY (email) REFERENCES Household(email),  

	FOREIGN KEY (manufacturer_name) REFERENCES Manufacturer(manufacturer_name),
    
    Unique key (email, applianceID)

);  

  

CREATE TABLE WaterHeater(  

	email varchar(320) NOT NULL,  

	applianceID INT Not NULL,  

	tank_size DECIMAL(6,1) Not NULL,  

	current_temperature INT NULL,  

	energy_source ENUM('electric', 'gas', 'fuel oil', 'heat pump') NOT NULL,  

	PRIMARY KEY(email, applianceID),  

	FOREIGN KEY (email, applianceID) REFERENCES Appliance(email, applianceID) 

);  

  

-- CREATE TYPE AirHandlerType AS ENUM('AirConditioner', 'Heater', 'Heat pump');  

  
CREATE TABLE AirHandler(  

	email varchar(320) NOT NULL,  

	applianceID INT Not NULL,  

	RPM INT Not NULL,  

	PRIMARY KEY(email, applianceID),  

	FOREIGN KEY (email, applianceID) REFERENCES Appliance(email, applianceID) 

);  

   

CREATE TABLE AirConditioner(  

	email varchar(320) NOT NULL,  

	applianceID INT Not NULL,  

	EER DECIMAL(6,1) Not NULL,  

	PRIMARY KEY(email, applianceID),  

	FOREIGN KEY (email, applianceID) REFERENCES AirHandler(email, applianceID) 

);  

  

CREATE TABLE Heater(  

	email varchar(320) NOT NULL,  

	applianceID INT Not NULL,  

	energy_source varchar(50) NOT NULL,  

	PRIMARY KEY(email, applianceID),  

	FOREIGN KEY (email, applianceID) REFERENCES AirHandler(email, applianceID) 

);  

  
CREATE TABLE HeatPump(  

	email varchar(320) NOT NULL,  

	applianceID INT Not NULL,  

	SEER DECIMAL(6,1) Not NULL,  

	HSPF DECIMAL(6,1) Not NULL,  

	PRIMARY KEY(email, applianceID),  

	FOREIGN KEY (email, applianceID) REFERENCES AirHandler(email, applianceID) 

); 



CREATE TABLE PublicUtility ( 

email varchar(320) NOT NULL, 

    	public_utility ENUM ('electric', 'gas', 'steam', 'liquid fuel') Not NULL, 

    	PRIMARY KEY(email, public_utility), 

FOREIGN KEY (email) REFERENCES Household(email) 

); 

 