# Group 4
# CSD 310 - Module 10
# 12/3/2022
# Purpose:  Displaying the records of each table in the Wilson Financial Database

import mysql.connector
from mysql.connector import errorcode

config = {
    "user": "financial_user",
    "password": "finance",
    "host": "127.0.0.1",
    "database": "wilson_financial",
    "port": "3006",
    "raise_on_warnings": True
}

try:
    db = mysql.connector.connect(**config)
    print("\n Database user {} connected to MySQL on host {} with database {}".format(config["user"],
                                                                                      config["host"],
                                                                                      config["database"]))
    input("\n\n Press any key to continue...")

    # Selecting and displaying the records from the clients table 
    cursor = db.cursor()
    cursor.execute("SELECT client_id, client_name, phone_number, initialization_date FROM clients")
    clients = cursor.fetchall()
    print("-- DISPLAYING CLIENTS RECORDS --")
    for client in clients:
        print("Client ID: ", client[0], )
        print("Client Name: ", client[1], )
        print("Phone Number: ", client[2], )
        print("Initialization Date: ", client[3], "\n")

    # Selecting and displaying the records from the rates table 
    cursor.execute("SELECT transaction_type_id, transaction_type_name, transaction_fee FROM rates")
    rates = cursor.fetchall()
    print("-- DISPLAYING Rates RECORDS --")
    for rate in rates:
        print ("Transaction Type ID: ", rate[0], )
        print("Transaction Type Name: ", rate[1], )
        print("Transaction Fee: $", rate[2], "\n")

    # Selecting and displaying the records from the transactions table 
    cursor.execute("SELECT transaction_id, transaction_type_id, client_id, transaction_date, transaction_amount FROM transactions")
    transactions = cursor.fetchall()
    print ("-- DISPLAYING Transactions RECORDS --")
    for transaction in transactions:
        print ("Transaction ID: ", transaction[0], )
        print("Transaction Type ID: ", transaction[1], )
        print("Client ID: ", transaction[2], )
        print("Transaction Date: ", transaction[3], )
        print("Transaction Amount: $", transaction[4], "\n")

    # Selecting and displaying the records from the assets table 
    cursor.execute("SELECT asset_acct_id, client_id, assets FROM assets")
    assets = cursor.fetchall()
    print ("-- DISPLAYING Assets RECORDS --")
    for asset in assets:
        print ("Asset Account ID: ", asset[0], )
        print ("Client ID: ", asset[1], )
        print ("Assets: ", asset[2], "\n")

    # Selecting and displaying the records from the billing table 
    cursor.execute("SELECT bill_id, transaction_id, client_id, transaction_type_id, transaction_fee FROM billing")
    billings = cursor.fetchall()
    print ("-- DISPLAYING Billing RECORDS --")
    for billing in billings:
        print ("Bill ID: ", billing[0], )
        print ("Transaction ID: ", billing[1], )
        print ("Client ID: ", billing[2], )
        print ("Transaction Type ID: ", billing[3], )
        print ("Transaction Fee: $", billing[4], "\n")


except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("   The supplied username and password are invalid")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("   The specified database does not exist")
    else:
        print(err)

finally:
    db.close()