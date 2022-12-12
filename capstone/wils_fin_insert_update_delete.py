# Group 4 - Brittany Kyncl, Holly McFarland, Riese Bohnak, Mark Witt
# CSD 310 - Module 10
# 12/5/2022
# Purpose:  to insert, update, and delete records within database

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
    mycursor = db.cursor()
    print("\n Database user {} connected to MySQL on host {} with database {}".format(config["user"], config["host"],
                                                                                      config["database"]))
    input("\n\n Press any key to continue....")

    def initialize(db):
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
            mycursor.execute(script)
            db.commit()
        print("database and tables created!")

    def bulk_insert(): # insert bulk amount of data into database

        rates_insert = ' '.join(("INSERT INTO Rates(transaction_type_name, transaction_fee)",
        "VALUES",
        "('MSA', '300'),",
        "('Withdraw', '100'),",
        "('Deposit', '50');"))

        clients_insert = ' '.join(("INSERT INTO clients(client_name, phone_number, initialization_date)",
        "VALUES",
        "('Samuel Samethon', '402-569-5689', '2020-10-16'),",
        "('Bartha Barthomieux', '402-321-5645', '2022-06-05'),",
        "('Freudithan Fahrenheit', '402-489-6978', '2021-12-19'),",
        "('Jasmine Donaldson', '402-546-2389', '2020-4-3'),",
        "('Denise Tucker', '402-539-2356', '2022-5-7'),",
        "('John Denton', '402-898-2245', '2020-6-4'),",
        "('Samuel Stinson', '402-755-7899', '2022-1-30'),",
        "('Patrick McMillan', '402-345-6644', '2021-10-20'),",
        "('Cynthia Holloway', '402-235-4477', '2020-9-15'),",
        "('Ana Rodriguez', '402-369-2311', '2021-2-20');"))

        assets_insert = ' '.join(("INSERT INTO assets(client_id, assets)",
        "VALUES",
        "('1', '35000'),",
        "('2', '60000'),",
        "('3', '135000'),",
        "('4', '7400'),",
        "('5', '56000'),",
        "('6', '13560'),",
        "('7', '8697'),",
        "('8', '45896'),",
        "('9', '4786'),",
        "('10', '17000');"))

        transactions_insert = ' '.join(("INSERT INTO transactions(transaction_type_id, client_id, transaction_date, transaction_amount)",
        "VALUES",
        "('1', '1', '2020-10-16', '5000'),('2', '1', '2020-12-13', '500'),('3', '1', '2021-6-14', '1000'),('2', '1', '2022-10-13', '500'),",
        "('2', '1', '2022-7-13', '650'),('1', '2', '2022-6-5', '1000'),('3', '2', '2022-11-10', '500'),('3', '2', '2022-6-14', '600'),",
        "('1', '2', '2022-8-6', '300'),('1', '2', '2022-5-13', '2000'),('1', '3', '2021-12-19', '300'),('3', '3', '2021-12-13', '500'),",
        "('3', '3', '2022-6-15', '2000'),('2', '3', '2022-10-16', '450'),('3', '3', '2022-7-13', '670'),('1', '4', '2020-04-03', '400'),",
        "('2', '4', '2020-12-13', '5000'),('3', '4', '2021-6-14', '1000'),('2', '4', '2022-10-13', '500'),('2', '4', '2022-7-13', '650'),",
        "('1', '5', '2022-05-07', '200'),('3', '5', '2022-6-13', '50'),('2', '5', '2022-12-14', '300'),('2', '5', '2022-10-13', '500'),",
        "('2', '5', '2022-7-13', '700'),('1', '6', '2020-06-04', '250'),('1', '6', '2020-12-13', '500'),('1', '6', '2021-6-14', '750'),",
        "('1', '6', '2022-10-13', '500'),('1', '6', '2022-7-13', '650'),('1', '7', '2022-01-30', '5000'),('2', '7', '2022-5-13', '500'),",
        "('3', '7', '2022-10-14', '1000'),('2', '7', '2022-11-13', '500'),('2', '7', '2022-12-13', '650'),('1', '8', '2021-10-20', '200'),",
        "('3', '8', '2021-12-13', '500'),('3', '8', '2021-6-14', '350'),('3', '8', '2022-10-13', '6000'),('1', '8', '2022-7-13', '100'),",
        "('1', '9', '2020-09-15', '120'),('2', '9', '2020-10-13', '50'),('2', '9', '2021-6-1', '1000'),('3', '9', '2022-9-15', '6000'),",
        "('3', '9', '2022-7-3', '135'),('1', '10', '2021-02-20', '400'),('3', '10', '2021-6-4', '500'),('2', '10', '2022-9-14', '60'),",
        "('3', '10', '2022-10-20', '5000'),('3', '10', '2022-12-13', '456');"))    

        billing_insert = ' '.join(("INSERT INTO billing(transaction_id, client_id, transaction_type_id, transaction_fee)",
        "VALUES",
        "('1', '1', '1', '300'),('2', '1', '2', '100'),('3', '1', '3', '50'),('4', '1', '2', '100'),('5', '1', '2', '100'),('6', '2', '1', '300'),",
        "('7', '2', '3', '50'),('8', '2', '3', '50'),('9', '2', '1', '300'),('10', '2', '1', '300'),('11', '3', '1', '300'),('12', '3', '3', '50'),",
        "('13', '3', '3', '50'),('14', '3', '2', '100'),('15', '3', '3', '50'),('16', '4', '1', '300'),('17', '4', '2', '100'),('18', '4', '3', '50'),",
        "('19', '4', '2', '100'),('20', '4', '2', '100'),('21', '5', '1', '300'),('22', '5', '3', '50'),('23', '5', '2', '100'),('24', '5', '2', '100'),",
        "('25', '5', '2', '100'),('26', '6', '1', '300'),('27', '6', '1', '300'),('28', '6', '1', '300'),('29', '6', '1', '300'),('30', '6', '1', '300'),",
        "('31', '7', '1', '300'),('32', '7', '2', '100'),('33', '7', '3', '50'),('34', '7', '2', '100'),('35', '7', '2', '100'),('36', '8', '1', '300'),",
        "('37', '8', '3', '50'),('38', '8', '3', '50'),('39', '8', '3', '50'),('40', '8', '1', '300'),('41', '9', '1', '300'),('42', '9', '2', '100'),",
        "('43', '9', '2', '100'),('44', '9', '3', '50'),('45', '9', '3', '50'),('46', '10', '1', '300'),('47', '10', '3', '50'),('48', '10', '2', '100'),",
        "('49', '10', '3', '50'),('50', '10', '3', '50');"))

        #list holding bulk insert statements strings for each table
        list =[rates_insert,clients_insert,assets_insert,transactions_insert,billing_insert]

        for insert in list:
            mycursor.execute(insert)
            db.commit()
        print("Bulk database records added")


    def insert_client(mycursor, client_name, phone_number, initialization_date):
        # sql insertion execution statement
        mycursor.execute("insert into clients(client_name, phone_number, initialization_date) values(%s,%s,%s)",
                        (client_name, phone_number, initialization_date))
        db.commit() #commit new change to database
        print("Insertion complete..")

        mycursor.execute("select * from clients")
        clients = mycursor.fetchall()
        for client in clients:
            print("client_id: {}\nclient_name: {}\nphone_number: {}\ninitialization_date: {}\n".format(client[0],client[1],client[2],client[3],))

    def insert_rate(mycursor, transaction_type_name, transaction_fee):
        # sql insertion execution statement
        mycursor.execute("insert into rates(transaction_type_name, transaction_fee) values(%s,%s)",
                        (transaction_type_name, transaction_fee))
        db.commit() #commit new change to database
        print("Insertion complete..")

        mycursor.execute("select * from rates")
        rates = mycursor.fetchall()
        for rate in rates:
            print(rate)

    def insert_transaction(mycursor,transaction_type_id, client_id, transaction_date, transaction_amount):
        # sql insertion execution statement
        mycursor.execute("insert into transactions(transaction_type_id, client_id, transaction_date, transaction_amount) values(%s,%s,%s,%s)",
                        (transaction_type_id, client_id, transaction_date, transaction_amount))
        db.commit() #commit new change to database
        print("Insertion complete..")

        mycursor.execute("select * from transactions")
        transactions = mycursor.fetchall()
        for transaction in transactions:
            print(transaction)

    def insert_asset(mycursor, client_id, assets):
        # sql insertion execution statement
        mycursor.execute("insert into assets(client_id, assets) values(%s,%s)",
                        (client_id, assets))
        db.commit() #commit new change to database
        print("Insertion complete..")

        mycursor.execute("select * from assets")
        assets = mycursor.fetchall()
        for asset in assets:
            print(asset)

    def insert_billing(mycursor, transaction_id, client_id, transaction_type_id, transaction_fee):
        # sql insertion execution statement
        mycursor.execute("insert into billing(transaction_id, client_id, transaction_type_id, transaction_fee) values(%s,%s,%s,%s)",
                        (transaction_id, client_id, transaction_type_id, transaction_fee))
        db.commit() #commit new change to database
        print("Insertion complete..")

        mycursor.execute("select * from transactions")
        billings = mycursor.fetchall()
        for billing in billings:
            print(billing)

    def delete(mycursor, table, column, record):
        #execute delete record statement
        mycursor.execute("delete from {} where {} = {}".format(table, column, record))
        db.commit() # commit new change to database
        mycursor.execute("alter table {} auto_increment =1".format(table))

        # deletion complete
        print("Deleted from {}: {} {}".format(table, column, record))

    def update(mycursor, table, column, setnew, atwhere, atrecord):
        # execute update statement
        mycursor.execute("update {} set {} = {} where {} = {}".format(table, column, setnew, atwhere, atrecord))
        db.commit() # commit new change to database

        # update complete
        print("Updated {} to {} where {} = {} in the {} table".format(column, setnew, atwhere, atrecord, table))

    def view_clients(mycursor):
        # Selecting and displaying the records from the clients table 
        mycursor.execute("SELECT client_id, client_name, phone_number, initialization_date FROM clients")
        clients = mycursor.fetchall()
        print("-- DISPLAYING CLIENTS RECORDS --")
        for client in clients:
            print("Client ID: ", client[0], )
            print("Client Name: ", client[1], )
            print("Phone Number: ", client[2], )
            print("Initialization Date: ", client[3], "\n")

    def view_rates(mycursor):
        # Selecting and displaying the records from the rates table 
        mycursor.execute("SELECT transaction_type_id, transaction_type_name, transaction_fee FROM rates")
        rates = mycursor.fetchall()
        print("-- DISPLAYING Rates RECORDS --")
        for rate in rates:
            print ("Transaction Type ID: ", rate[0], )
            print("Transaction Type Name: ", rate[1], )
            print("Transaction Fee: $", rate[2], "\n")

    def view_transactions(mycursor):
        # Selecting and displaying the records from the transactions table 
        mycursor.execute("SELECT transaction_id, transaction_type_id, client_id, transaction_date, transaction_amount FROM transactions")
        transactions = mycursor.fetchall()
        print ("-- DISPLAYING Transactions RECORDS --")
        for transaction in transactions:
            print ("Transaction ID: ", transaction[0], )
            print("Transaction Type ID: ", transaction[1], )
            print("Client ID: ", transaction[2], )
            print("Transaction Date: ", transaction[3], )
            print("Transaction Amount: $", transaction[4], "\n")

    def view_assets(mycursor):
        # Selecting and displaying the records from the assets table 
        mycursor.execute("SELECT asset_acct_id, client_id, assets FROM assets")
        assets = mycursor.fetchall()
        print ("-- DISPLAYING Assets RECORDS --")
        for asset in assets:
            print ("Asset Account ID: ", asset[0], )
            print ("Client ID: ", asset[1], )
            print ("Assets: ", asset[2], "\n")

    def view_billing(mycursor):
        # Selecting and displaying the records from the billing table 
        mycursor.execute("SELECT bill_id, transaction_id, client_id, transaction_type_id, transaction_fee FROM billing")
        billings = mycursor.fetchall()
        print ("-- DISPLAYING Billing RECORDS --")
        for billing in billings:
            print ("Bill ID: ", billing[0], )
            print ("Transaction ID: ", billing[1], )
            print ("Client ID: ", billing[2], )
            print ("Transaction Type ID: ", billing[3], )
            print ("Transaction Fee: $", billing[4], "\n")

    # initialize(db)
    # bulk_insert()

    # show all table options for db
    mycursor.execute("show tables")
    tables = mycursor.fetchall()
    print("\nTables in wilson_financial\n--------------------------")
    i = 0
    for table in tables:
        i += 1
        print("{}. {}".format(i, table[0]))
    print()
    
    while True:
        print("1. Insert")
        print("2. Update")
        print("3. Delete")
        print("4. View Records")
        print("5. Exit")
        choice = int(input("Enter Choice: "))
        if choice == 1:
            while True:
                print("1. Insert into Assets")
                print("2. Insert into Billing")
                print("3. Insert into Clients")
                print("4. Insert into Rates")
                print("5. Insert into Transactions")
                print("6. Return main menu")
                choice = int(input("Enter Choice: "))
                if choice == 1:
                    client_id = (input("client_id: "))
                    assets = (input("assets: "))
                    insert_asset(mycursor, client_id, assets)
                elif choice == 2:
                    transaction_id = (input("transaction_id: "))
                    client_id = (input("client_id: "))
                    transaction_type_id = (input("transaction_type_id: "))
                    transaction_fee = (input("transaction_fee: "))
                    insert_billing(mycursor, transaction_id, client_id, transaction_type_id, transaction_fee)
                elif choice == 3:
                    client_name = (input("client_name: "))
                    phone_number = (input("phone_number: "))
                    initialization_date = (input("initialization_date: "))
                    insert_client(mycursor, client_name, phone_number, initialization_date)
                elif choice == 4:
                    transaction_type_name = (input("transaction_type_name: "))
                    transaction_fee = (input("transaction_fee: "))
                    insert_rate(mycursor, transaction_type_name, transaction_fee)
                elif choice == 5:
                    transaction_type_id = (input("transaction_type_id: "))
                    client_id = (input("client_id: "))
                    transaction_date = (input("transaction_date: "))
                    transaction_amount = (input("transaction_amount: "))
                    insert_transaction(mycursor,transaction_type_id, client_id, transaction_date, transaction_amount)
                elif choice == 6:
                    break
                else:
                   continue
        elif choice ==2:
            table = (input("Table name: "))
            column = (input("Set in column: "))
            setnew = (input("Equal to: "))
            atwhere = (input("Where in column: "))
            atrecord = (input("Equals record name: "))
            update(mycursor, table, column, setnew, atwhere, atrecord)
        elif choice ==3:
            table = (input("Table name: "))
            column = (input("Column Name: "))
            record = (input("Record ID to delete: "))
            delete(mycursor, table, column, record)
        elif choice == 4:
            view_clients(mycursor)
            view_assets(mycursor)
            view_rates(mycursor)
            view_transactions(mycursor)
            view_billing(mycursor)
        elif choice ==5:
            break
        else:
            print("Invalid Input")

except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("The supplied username or password are invalid")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("The specified database does not exist")
    else:
        print(err)
finally:
    db.close()