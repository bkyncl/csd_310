/*
    Title: 'wilson_financial_db_init_frame'.sql
    Author: Brittany Kyncl
    Date:   10.30.22
    Description: wilson_financial database initialization script.
*/

-- drop database user if exists 
-- DROP USER IF EXISTS 'financial_user'@'localhost';

-- -- create financial_user and grant them all privileges to the wilson_financial database 
-- CREATE USER 'financial_user'@'localhost' IDENTIFIED WITH mysql_native_password BY 'finance';

-- -- grant all privileges to the wilson_financial database to user financial_user on localhost 
-- GRANT ALL PRIVILEGES ON wilson_financial.* TO 'financial_user'@'localhost';


-- drop tables if they are present
DROP TABLE IF EXISTS Assets;
DROP TABLE IF EXISTS Transactions;
DROP TABLE IF EXISTS Clients;
DROP TABLE IF EXISTS Billing;
DROP TABLE IF EXISTS Rates;

-- create the Clients table 
CREATE TABLE Clients (
    client_id     INT             NOT NULL        AUTO_INCREMENT,
    client_name   VARCHAR(75)     NOT NULL,
    phone_number  VARCHAR(75)     NOT NULL,
    initialization_date  DATE     NOT NULL,

    PRIMARY KEY(client_id)
); 

-- create the Rates table 
CREATE TABLE Rates (
    transaction_type_id     INT             NOT NULL        AUTO_INCREMENT,
    transaction_type_name   VARCHAR(75)     NOT NULL,
    transaction_fee  INT    NOT NULL,

    PRIMARY KEY(transaction_type_id)
); 

-- create the Transactions table 
CREATE TABLE Transactions (
    transaction_id     INT             NOT NULL        AUTO_INCREMENT,
    transaction_type_id  INT     NOT NULL,
    client_id  INT NOT NULL,
    transaction_date DATE NOT NULL,
    transaction_amount INT NOT NULL,
     
    PRIMARY KEY(transaction_id),

    CONSTRAINT transaction_type_id
    FOREIGN KEY(transaction_type_id)
        REFERENCES Rates(transaction_type_id),
        
    FOREIGN KEY(client_id)
        REFERENCES Clients(client_id)
);  

-- create the Assets table
CREATE TABLE Assets (
    asset_acct_id   INT  NOT NULL        AUTO_INCREMENT,
    client_id  INT NOT NULL,
    assets   INT     NOT NULL,
    
    PRIMARY KEY(asset_acct_id),

	CONSTRAINT client_id
    FOREIGN KEY(client_id)
        REFERENCES Clients(client_id)
);

-- create the Billing table 
CREATE TABLE Billing (
    bill_id    INT             NOT NULL        AUTO_INCREMENT,
    transaction_id   INT    NOT NULL,
    client_id  INT    NOT NULL,
    transaction_type_id INT NOT NULL,
    transaction_fee    INT NOT NULL,

    PRIMARY KEY(bill_id),

    CONSTRAINT transaction_id
    FOREIGN KEY(transaction_id)
        REFERENCES Transactions(transaction_id),

    FOREIGN KEY(client_id)
        REFERENCES Clients(client_id),

   FOREIGN KEY(transaction_type_id)
        REFERENCES Rates(transaction_type_id)
);
-- insert to rates
INSERT INTO Rates(transaction_type_name, transaction_fee)
    VALUES
    ('MSA', '300'),
    ('Withdraw', '100'),
    ('Deposit', '50');

-- insert to clients
INSERT INTO clients(client_name, phone_number, initialization_date)
    VALUES
    ('Samuel Samethon', '402-569-5689', '2020-10-16'),
    ('Bartha Barthomieux', '402-321-5645', '2022-06-05'),
    ('Freudithan Fahrenheit', '402-489-6978', '2021-12-19'),
    ('Jasmine Donaldson', '402-546-2389', '2020-4-3'),
    ('Denise Tucker', '402-539-2356', '2022-5-7'),
    ('John Denton', '402-898-2245', '2020-6-4'),
    ('Samuel Stinson', '402-755-7899', '2022-1-30'),
    ('Patrick McMillan', '402-345-6644', '2021-10-20'),
    ('Cynthia Holloway', '402-235-4477', '2020-9-15'),
    ('Ana Rodriguez', '402-369-2311', '2021-2-20');

-- insert to assets
INSERT INTO assets(client_id, assets)
    VALUES
    ('1', '35000'),
    ('2', '60000'),
    ('3', '135000'),
    ('4', '7400'),
    ('5', '56000'),
    ('6', '13560'),
    ('7', '8697'),
    ('8', '45896'),
    ('9', '4786'),
    ('10', '17000');

-- insert to transactions
INSERT INTO transactions(transaction_type_id, client_id, transaction_date, transaction_amount)
    VALUES
    ('1', '1', '2020-10-16', '5000'),
    ('2', '1', '2020-12-13', '500'),
    ('3', '1', '2021-6-14', '1000'),
    ('2', '1', '2022-10-13', '500'),
    ('2', '1', '2022-7-13', '650'),

    ('1', '2', '2022-6-5', '1000'),
    ('3', '2', '2022-11-10', '500'),
    ('3', '2', '2022-6-14', '600'),
    ('1', '2', '2022-8-6', '300'),
    ('1', '2', '2022-5-13', '2000'),

    ('1', '3', '2021-12-19', '300'),
    ('3', '3', '2021-12-13', '500'),
    ('3', '3', '2022-6-15', '2000'),
    ('2', '3', '2022-10-16', '450'),
    ('3', '3', '2022-7-13', '670'),

    ('1', '4', '2020-04-03', '400'),
    ('2', '4', '2020-12-13', '5000'),
    ('3', '4', '2021-6-14', '1000'),
    ('2', '4', '2022-10-13', '500'),
    ('2', '4', '2022-7-13', '650'),

    ('1', '5', '2022-05-07', '200'),
    ('3', '5', '2022-6-13', '50'),
    ('2', '5', '2022-12-14', '300'),
    ('2', '5', '2022-10-13', '500'),
    ('2', '5', '2022-7-13', '700'),

    ('1', '6', '2020-06-04', '250'),
    ('1', '6', '2020-12-13', '500'),
    ('1', '6', '2021-6-14', '750'),
    ('1', '6', '2022-10-13', '500'),
    ('1', '6', '2022-7-13', '650'),

    ('1', '7', '2022-01-30', '5000'),
    ('2', '7', '2022-5-13', '500'),
    ('3', '7', '2022-10-14', '1000'),
    ('2', '7', '2022-11-13', '500'),
    ('2', '7', '2022-12-13', '650'),

    ('1', '8', '2021-10-20', '200'),
    ('3', '8', '2021-12-13', '500'),
    ('3', '8', '2021-6-14', '350'),
    ('3', '8', '2022-10-13', '6000'),
    ('1', '8', '2022-7-13', '100'),

    ('1', '9', '2020-09-15', '120'),
    ('2', '9', '2020-10-13', '50'),
    ('2', '9', '2021-6-1', '1000'),
    ('3', '9', '2022-9-15', '6000'),
    ('3', '9', '2022-7-3', '135'),

    ('1', '10', '2021-02-20', '400'),
    ('3', '10', '2021-6-4', '500'),
    ('2', '10', '2022-9-14', '60'),
    ('3', '10', '2022-10-20', '5000'),
    ('3', '10', '2022-12-13', '456');

-- insert to transactions
INSERT INTO billing(transaction_id, client_id, transaction_type_id, transaction_fee)
    VALUES
    ('1', '1', '1', '300'),
    ('2', '1', '2', '100'),
    ('3', '1', '3', '50'),
    ('4', '1', '2', '100'),
    ('5', '1', '2', '100'),

    ('6', '2', '1', '300'),
    ('7', '2', '3', '50'),
    ('8', '2', '3', '50'),
    ('9', '2', '1', '300'),
    ('10', '2', '1', '300'),

    ('11', '3', '1', '300'),
    ('12', '3', '3', '50'),
    ('13', '3', '3', '50'),
    ('14', '3', '2', '100'),
    ('15', '3', '3', '50'),

    ('16', '4', '1', '300'),
    ('17', '4', '2', '100'),
    ('18', '4', '3', '50'),
    ('19', '4', '2', '100'),
    ('20', '4', '2', '100'),

    ('21', '5', '1', '300'),
    ('22', '5', '3', '50'),
    ('23', '5', '2', '100'),
    ('24', '5', '2', '100'),
    ('25', '5', '2', '100'),

    ('26', '6', '1', '300'),
    ('27', '6', '1', '300'),
    ('28', '6', '1', '300'),
    ('29', '6', '1', '300'),
    ('30', '6', '1', '300'),

    ('31', '7', '1', '300'),
    ('32', '7', '2', '100'),
    ('33', '7', '3', '50'),
    ('34', '7', '2', '100'),
    ('35', '7', '2', '100'),

    ('36', '8', '1', '300'),
    ('37', '8', '3', '50'),
    ('38', '8', '3', '50'),
    ('39', '8', '3', '50'),
    ('40', '8', '1', '300'),

    ('41', '9', '1', '300'),
    ('42', '9', '2', '100'),
    ('43', '9', '2', '100'),
    ('44', '9', '3', '50'),
    ('45', '9', '3', '50'),

    ('46', '10', '1', '300'),
    ('47', '10', '3', '50'),
    ('48', '10', '2', '100'),
    ('49', '10', '3', '50'),
    ('50', '10', '3', '50');
