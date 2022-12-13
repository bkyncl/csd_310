# Group 4 - Brittany Kyncl, Holly McFarland, Riese Bohnak, Mark Witt
# CSD 310 - Module 11 - Milestone 3
# 12/11/2022

import mysql.connector
from mysql.connector import errorcode
from tabulate import tabulate

#Display the average assets from all clients.
def averageAssets(cursor):

    cursor.execute("select count(client_ID), concat('$ ', avg(round(a.assets,2))) from assets as a")
    selection = cursor.fetchall()

    h1=[["Displaying the average asset possession for clients"]]
    h2=["Total Accounts", "AVG Asset Possesion"]
    print(tabulate(h1,tablefmt="fancy_grid"))
    print(tabulate(selection, headers=h2, tablefmt="fancy_grid"))
    
 
# Display all clients and their total assets
def assetAccounts(cursor):

    cursor.execute("SELECT b.client_id, CONCAT('$ ', SUM(b.transaction_fee)) AS total_transaction_fees, " +
                    "CONCAT('$ ', a.assets) AS assets FROM billing b " +
                    "INNER JOIN assets a ON b.client_id = a.client_id GROUP BY client_id")
    clients = cursor.fetchall()

    h1=[["Displaying total fees paid for each client\nCompared to current asset possession"]]
    h2=["Client ID","Total Fees Paid","Assets"]
    print(tabulate(h1,tablefmt="fancy_grid"))
    print(tabulate(clients, headers=h2, tablefmt="fancy_grid"))
    

#Display the amount of new clients in the last x months.
def monthlyNewUsers(cursor, months):
    #multiple by the average amount of days in a month
    days = months * 30.417
    cursor.execute(f"SELECT SUM(datediff(curdate(), initialization_date) <= {days}) AS clients_count,"+
                    "DATE(curdate() - INTERVAL 6 month) AS checking_period_start,"+
                    "DATE(curdate()) AS checking_period_end FROM clients")
    selection = cursor.fetchall()

    h1=[["How many clients have been added within the last 6 months?"]]
    h2=["Account(s)","Start Date","End Date"]
    print(tabulate(h1,tablefmt="fancy_grid"))
    print(tabulate(selection, headers=h2, tablefmt="fancy_grid"))


# Display total number of clients added in each 6 mnth period since first client initialization date
def acquisitionRate(cursor):
    
    cursor.execute("select count(client_id) as 'Number of Clients Added', initialization_date as 'Start Date'," +
                "date_add(initialization_date, interval 6 month) as 'End Date'"+
                "from clients where initialization_date between '2022-06-01' and curdate()"+
                "union all select count(client_id) as 'Number of Clients', initialization_date as 'Start Date'," +
                "date_add(initialization_date, interval 6 month) as 'End Date'" +
                "from clients where initialization_date between '2021-12-01' and '2022-06-01'" +
                "union all select count(client_id) as 'Number of Clients', initialization_date as 'Start Date'," +
                "date_add(initialization_date, interval 6 month) as 'End Date'" +
                "from clients where initialization_date between '2021-06-01' and '2021-12-01'" +
                "union all select count(client_id) as 'Number of Clients', initialization_date as 'Start Date',"+
                "date_add(initialization_date, interval 6 month) as 'End Date'"+
                "from clients where initialization_date between '2020-12-01' and '2021-06-01'"+
                "union all select count(client_id) as 'Number of Clients', initialization_date as 'Start Date'," +
                "date_add(initialization_date, interval 6 month) as 'End Date'"+
                "from clients where initialization_date between '2019-12-01' and '2020-12-01'")
    client_dates = cursor.fetchall()

    h1=[["Displaying new client acquisition(s) every 6 months\nStarting as first account initialization date"]]
    h2=["New Client(s)","Start Date","End Date"]
    print(tabulate(h1,tablefmt="fancy_grid"))
    print(tabulate(client_dates, headers=h2, tablefmt="fancy_grid"))

# display transaction activity per month
def transactionsPerMonth(cursor):

    cursor.execute("SELECT DATE_FORMAT(transaction_date, '%Y-%m') AS month, COUNT(*) AS transaction_count, LAG(COUNT(*), 1) "+
                    "OVER (ORDER BY EXTRACT(YEAR_MONTH FROM transaction_date)) AS prev_transaction_count, CONCAT(ROUND((COUNT(*)"+
                    " - LAG(COUNT(*), 1) OVER (ORDER BY EXTRACT(YEAR_MONTH FROM transaction_date))) / LAG(COUNT(*), 1) "+
                    "OVER (ORDER BY EXTRACT(YEAR_MONTH FROM transaction_date)) * 100, 2), '%') AS rate_of_increase FROM transactions "+
                    "GROUP BY (EXTRACT(YEAR_MONTH FROM transaction_date))")
    transactions = cursor.fetchall()

    h1=[["Displaying transaction activity per month\nCompared to previous months activity"]]
    h2=["Month","Count","Prev. Count","% Increase/Decrease"]
    print(tabulate(h1,tablefmt="fancy_grid"))
    print(tabulate(transactions, headers=h2, tablefmt="fancy_grid"))
    

# display transaction activity per year
def transactionsPerYear(cursor):
    cursor.execute("SELECT EXTRACT(YEAR FROM transaction_date) AS year, COUNT(*) AS transaction_count, LAG(COUNT(*), 1) OVER "+
                    "(ORDER BY EXTRACT(YEAR FROM transaction_date)) AS prev_transaction_count, CONCAT(ROUND((COUNT(*) - LAG(COUNT(*), 1) OVER "+
                    "(ORDER BY EXTRACT(YEAR FROM transaction_date))) / LAG(COUNT(*), 1)  OVER (ORDER BY EXTRACT(YEAR FROM transaction_date)) * 100,2), '%') "+
                    "AS rate_of_increase FROM transactions GROUP BY EXTRACT(YEAR FROM transaction_date)")
    transactions = cursor.fetchall()

    h1=[["Displaying transaction activity per year\nCompared to previous years activity"]]
    h2=["Year","Count","Prev. Count","% Increase/Decrease"]
    print(tabulate(h1,tablefmt="fancy_grid"))
    print(tabulate(transactions, headers=h2, tablefmt="fancy_grid"))
    

def monthlyFeeRevenue(cursor):
    cursor.execute("SELECT DATE_FORMAT(transaction_date, '%Y-%m') AS month, SUM(b.transaction_fee) AS fee_revenue, "+
                    "CONCAT(FORMAT((SUM(b.transaction_fee) - LAG(SUM(b.transaction_fee), 1) OVER (ORDER BY t.transaction_date)) / LAG(SUM(b.transaction_fee), 1) "+
                    "OVER (ORDER BY t.transaction_date) *100, 2), '%') AS pct_increase FROM transactions t INNER JOIN billing b ON t.transaction_id = b.transaction_id "+
                    "GROUP BY month ORDER BY t.transaction_date")
    fees = cursor.fetchall()

    h1=[["Displaying total transaction fee revenue per month"]]
    h2=["Month","Fee Revenue","% Increase/Decrease"]
    print(tabulate(h1,tablefmt="fancy_grid"))
    print(tabulate(fees, headers=h2, tablefmt="fancy_grid"))

    count = 0
    rev = 0
    for fee in fees:
        count += 1
        rev += fee[1]
    h3=[[f"Monthly Fee Revenue AVG: ${rev/count:.2f}"]]
    print(tabulate(h3,tablefmt="fancy_grid"))


def yearlyFeeRevenue(cursor):
    cursor.execute("SELECT DATE_FORMAT(transaction_date, '%Y') AS year, SUM(b.transaction_fee) AS fee_revenue, CONCAT(FORMAT((SUM(b.transaction_fee) - "+
                    "LAG(SUM(b.transaction_fee), 1) OVER (ORDER BY t.transaction_date)) / LAG(SUM(b.transaction_fee), 1) OVER (ORDER BY t.transaction_date) *100, 2), '%') "+
                    "AS pct_increase FROM transactions t INNER JOIN billing b ON t.transaction_id = b.transaction_id GROUP BY year ORDER BY t.transaction_date")
    fees = cursor.fetchall()

    h1=[["Displaying total transaction fee revenue per year"]]
    h2=["Year","Fee Revenue","% Increase/Decrease"]
    print(tabulate(h1,tablefmt="fancy_grid"))
    print(tabulate(fees, headers=h2, tablefmt="fancy_grid"))

    count = 0
    rev = 0
    for fee in fees:
        count += 1
        rev += fee[1]
    h3=[[f"Yearly Fee Revenue AVG: ${rev/count:.2f}"]]
    print(tabulate(h3,tablefmt="fancy_grid"))


#Display how many clients have had over x amount of transactions in a month
def userTransactions(cursor, transactions):
    cursor.execute(f"select client_id,COUNT(*) >= {transactions} as count, extract(year from transaction_date) as year, extract(month from transaction_date) as month from transactions group by client_id, month(transaction_date), year(transaction_date)")
    selection = cursor.fetchall()
    x = 0
    for i in selection:
        x += i[1]
    h1=[[f"How many clients have a high number of transactions per month?\n{x} clients have had at most {transactions} transactions in a month"]]
    print(tabulate(h1,tablefmt="fancy_grid"))

    cursor.execute("SELECT client_id, COUNT(*) as count, DATE_FORMAT(transaction_date, '%Y-%m') AS Date FROM transactions "+
                    "GROUP BY client_id, month(transaction_date), year(transaction_date) HAVING COUNT(*) >= 2")
    users = cursor.fetchall()
    h2=["Client ID","Count","Date"]
    print(tabulate(users,h2,tablefmt="fancy_grid"))

config = {
    "user": "financial_user",
    "password": "finance",
    "host": "localhost",
    "database": "wilson_financial",
    "port": "3306",
    "raise_on_warnings": True
}

try:
    db = mysql.connector.connect(**config)
    print("\n Database user {} connected to MySQL on host {} with database {}".format(config["user"], config["host"], config["database"]))
    input("\n\n Press any key to continue...\n")
    myCursor = db.cursor()

    #Averages the assets of all clients
    #Total fees paid by each client
    print("\n-----------------------------------------------------------------")
    print("Report 1")
    print("-----------------------------------------------------------------")
    averageAssets(myCursor)
    assetAccounts(myCursor)

    #Displaying transaction acticity
    print("\n-----------------------------------------------------------------")
    print("Report 2")
    print("-----------------------------------------------------------------")
    userTransactions(myCursor,2)
    transactionsPerMonth(myCursor)
    transactionsPerYear(myCursor)
    
    #Number of clients added in each 6 month period since first account initialization date
    print("\n-----------------------------------------------------------------")
    print("Report 3")
    print("-----------------------------------------------------------------")
    monthlyNewUsers(myCursor, 6)
    acquisitionRate(myCursor)
    
    #Displaying fee revenue monthly and yearly trends
    print("\n-----------------------------------------------------------------")
    print("Report 4")
    print("-----------------------------------------------------------------")
    monthlyFeeRevenue(myCursor)
    yearlyFeeRevenue(myCursor)

    print()

except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print(" The supplied username or password are invalid")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print(" The specified database does not exist")
    else:
        print(err)
finally:
    db.close()



