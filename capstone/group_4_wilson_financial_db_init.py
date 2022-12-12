# Group 4 - Brittany Kyncl, Holly McFarland, Riese Bohnak, Mark Witt
# CSD 310 - Module 10
# 12/4/2022
# Purpose:  python script to initialize and create the database and tables

import mysql.connector
from mysql.connector import errorcode

config = {
    "user": "root",
    "password": "September_176136",
    "host": "localhost",
    "database": "wilson_financial",
    "port": "3306",
    "raise_on_warnings": True
}
try:
    db = mysql.connector.connect(**config)

    print("\n Database user {} connected to MySQL on host {} with database {}".format(config["user"], config["host"],
                                                                                      config["database"]))
    input("\n\n Press any key to continue....")

    def initialize(db):
        cursor = db.cursor()
        #create user:
        dropUser = "DROP USER IF EXISTS 'financial_user'@'localhost';"
        createUser = "CREATE USER 'financial_user'@'localhost' IDENTIFIED WITH mysql_native_password BY 'finance';"
        userPrivilege = "GRANT ALL PRIVILEGES ON wilson_financial.* TO 'financial_user'@'localhost';"

        #drop database if it exists:
        dropDB = "DROP DATABASE wilson_financial;"
        #create new database:
        createDB = "CREATE DATABASE wilson_financial;"
        #select db to use:
        useDB = "USE wilson_financial;"

        #create tables:
        #create clients:
        createClient1 = "CREATE TABLE Clients (client_id INT NOT NULL AUTO_INCREMENT, client_name VARCHAR(75) NOT NULL, "
        createClient2 = "phone_number VARCHAR(75) NOT NULL, initialization_date DATE NOT NULL, PRIMARY KEY(client_id));"
        createClient = createClient1 + createClient2

        #create Rates:
        createRates1 = "CREATE TABLE Rates (transaction_type_id INT NOT NULL AUTO_INCREMENT, transaction_type_name VARCHAR(75) NOT NULL,"
        createRates2 =" transaction_fee INT NOT NULL, PRIMARY KEY(transaction_type_id));"
        createRates = createRates1+createRates2

        #create Transactions:
        createTransactions1 = "CREATE TABLE Transactions (transaction_id INT NOT NULL AUTO_INCREMENT, transaction_type_id INT NOT NULL,"
        createTransactions2 = " client_id INT NOT NULL, transaction_date DATE NOT NULL, transaction_amount INT NOT NULL, PRIMARY KEY(transaction_id),"
        createTransactions3 = " CONSTRAINT transaction_type_id FOREIGN KEY(transaction_type_id) REFERENCES Rates(transaction_type_id), FOREIGN KEY(client_id) REFERENCES Clients(client_id));"
        createTransactions = createTransactions1+createTransactions2+createTransactions3

        #create assets:
        createAssets1 = "CREATE TABLE Assets (asset_acct_id INT NOT NULL AUTO_INCREMENT, client_id  INT NOT NULL, assets   INT     NOT NULL, PRIMARY KEY(asset_acct_id),"
        createAssets2 = "CONSTRAINT client_id FOREIGN KEY(client_id) REFERENCES Clients(client_id));"
        createAssets = createAssets1+createAssets2

        #create Billing:
        createBilling1 = "CREATE TABLE Billing (bill_id INT NOT NULL AUTO_INCREMENT, transaction_id INT NOT NULL, client_id INT NOT NULL, transaction_type_id INT NOT NULL,"
        createBilling2 = " transaction_fee INT NOT NULL, PRIMARY KEY(bill_id), CONSTRAINT transaction_id FOREIGN KEY(transaction_id) REFERENCES Transactions(transaction_id),"
        createBilling3 = " FOREIGN KEY(client_id) REFERENCES Clients(client_id), FOREIGN KEY(transaction_type_id) REFERENCES Rates(transaction_type_id))"
        createBilling = createBilling1+createBilling2+createBilling3

        #create list of scripts:
        myList = [dropUser, createUser, userPrivilege, dropDB, createDB, useDB, createClient, createRates, createTransactions, createAssets, createBilling]

        #loop through scripts, executing & comitting each one:
        for script in myList:

            cursor.execute(script)
            db.commit()
        print("database and tables created!")
    initialize(db)
        
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("The supplied username or password are invalid")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("The specified database does not exist")
    else:
        print(err)

finally:
    db.close()