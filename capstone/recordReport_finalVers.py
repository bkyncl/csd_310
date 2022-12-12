# Group 4 - Brittany Kyncl, Holly McFarland, Riese Bohnak, Mark Witt
# CSD 310 - Module 11 - Milestone 3
# 12/11/2022

import mysql.connector
from mysql.connector import errorcode
import tabulate

#Display the average assets from all clients.
def averageAssets(cursor, display):
    cursor.execute("select count(client_ID), avg(assets) from assets")
    selection = cursor.fetchall()

    print(display)
    for i in selection:
        print("{} accounts found with an average of ${:.2f} in possession.\n".format(i[0],i[1]))

# Display all clients and their total assets
def assetAccounts(cursor,display):
    cursor.execute("SELECT b.client_id, SUM(b.transaction_fee) AS total_transaction_fees, a.assets FROM billing b inner join assets a on b.client_id = a.client_id GROUP BY client_id")
    clients = cursor.fetchall()

    print(display)
    for client in clients:
        print("Client ID: {}\nTotal Fees Paid: ${}\nAssets: ${}\n".format(client[0],client[1],client[2]))

#Display the amount of new clients in the last x months.
def monthlyNewUsers(cursor, display, months):
    #multiple by the average amount of days in a month
    days = months * 30.417
    cursor.execute(f"select sum(datediff(curdate(), initialization_date) <= {days}) from clients")
    selection = cursor.fetchall()

    print(display)
    for i in selection:
        print("{} account(s) have been created in the last {} months.".format(i[0], months))

# Display total number of clients added in each 6 mnth period since first client initialization date
def acquisitionRate(cursor, display):
    period = ["'2022-06-01' and '2022-12-01'","'2021-12-01' and '2022-06-01'","'2021-06-01' and '2021-12-01'","'2020-12-01' and '2021-06-01'","'2020-04-03' and '2020-12-01'"]
  
    view = ' '.join(("select count(client_id) as 'Number of Clients Added', initialization_date as 'In Each 6 Mnth Prd' from clients",
                    "where initialization_date between "+period[0]+" union all",
                    "select count(client_id) as 'Number of Clients', initialization_date as 'In Each 6 Mnth Prd' from clients",
                    "where initialization_date between "+period[1]+" union all",
                    "select count(client_id) as 'Number of Clients', initialization_date as 'In Each 6 Mnth Prd' from clients",
                    "where initialization_date between "+period[2]+" union all",
                    "select count(client_id) as 'Number of Clients', initialization_date as 'In Each 6 Mnth Prd' from clients",
                    "where initialization_date between "+period[3]+" union all",
                    "select count(client_id) as 'Number of Clients', initialization_date as 'In Each 6 Mnth Prd' from clients",
                    "where initialization_date between "+period[4]))
    print(display)
    cursor.execute(view)
    client_dates = cursor.fetchall()
    x=0
    for client_date in client_dates:
        print("\nBetween the dates of {}\nThere were {} new client acquisition(s)".format(period[x],client_date[0]))
        x += 1

# display transaction activity per month
def transactionsPerMonth(cursor,display):
    cursor.execute(' '.join(("SELECT DATE_FORMAT(transaction_date, '%Y-%m') AS month, COUNT(*) AS transaction_count, LAG(COUNT(*), 1)",
                    "OVER (ORDER BY EXTRACT(YEAR_MONTH FROM transaction_date)) AS prev_transaction_count,",
                    "CONCAT(ROUND((COUNT(*) - LAG(COUNT(*), 1) OVER (ORDER BY EXTRACT(YEAR_MONTH FROM transaction_date))) / LAG(COUNT(*), 1)",
                    "OVER (ORDER BY EXTRACT(YEAR_MONTH FROM transaction_date)) * 100, 2), '%') AS rate_of_increase FROM transactions",
                    "GROUP BY (EXTRACT(YEAR_MONTH FROM transaction_date))")))

    

    print(display)
    transactions = cursor.fetchall()
    for transaction in transactions:
        print("Month: {}\t Count: {}\t Increase\Decrease: {}".format(transaction[0],transaction[1],transaction[3]))

# display transaction activity per year
def transactionsPerYear(cursor,display):
    cursor.execute(' '.join(("SELECT EXTRACT(YEAR FROM transaction_date) AS year, COUNT(*) AS transaction_count, LAG(COUNT(*), 1) OVER",
                            "(ORDER BY EXTRACT(YEAR FROM transaction_date)) AS prev_transaction_count, CONCAT(ROUND((COUNT(*) - LAG(COUNT(*), 1) OVER",
                            "(ORDER BY EXTRACT(YEAR FROM transaction_date))) / LAG(COUNT(*), 1)  OVER (ORDER BY EXTRACT(YEAR FROM transaction_date)) * 100,2), '%')",
                            "AS rate_of_increase FROM transactions GROUP BY EXTRACT(YEAR FROM transaction_date)")))

    print(display)
    transactions = cursor.fetchall()
    for transaction in transactions:
        print("Month: {}\t Count: {}\t Increase\Decrease: {}".format(transaction[0],transaction[1],transaction[3]))

def monthlyFeeRevenue(cursor,display):
    cursor.execute(' '.join(("SELECT DATE_FORMAT(transaction_date, '%Y-%m') AS month, SUM(b.transaction_fee) AS fee_revenue,",
                            "CONCAT(FORMAT((SUM(b.transaction_fee) - LAG(SUM(b.transaction_fee), 1) OVER (ORDER BY t.transaction_date)) / LAG(SUM(b.transaction_fee), 1)",
                            "OVER (ORDER BY t.transaction_date) *100, 2), '%') AS pct_increase FROM transactions t INNER JOIN billing b ON t.transaction_id = b.transaction_id",
                            "GROUP BY month ORDER BY t.transaction_date")))

    print(display)
    fees = cursor.fetchall()
    count = 0
    rev = 0
    for fee in fees:
        print("Month: {}\t   Fee Revenue: ${}\t Increase\Decrease: {}".format(fee[0],fee[1],fee[2]))
        count += 1
        rev += fee[1]

    print(f"Monthly Fee Revenue AVG: ${rev/count:.2f}")

def yearlyFeeRevenue(cursor,display):
    cursor.execute(' '.join(("SELECT DATE_FORMAT(transaction_date, '%Y') AS year, SUM(b.transaction_fee) AS fee_revenue, CONCAT(FORMAT((SUM(b.transaction_fee) -",
                            "LAG(SUM(b.transaction_fee), 1) OVER (ORDER BY t.transaction_date)) / LAG(SUM(b.transaction_fee), 1) OVER (ORDER BY t.transaction_date) *100, 2), '%')",
                            "AS pct_increase FROM transactions t INNER JOIN billing b ON t.transaction_id = b.transaction_id GROUP BY year ORDER BY t.transaction_date")))

    print(display)
    count = 0
    rev = 0
    fees = cursor.fetchall()
    count = 0
    rev = 0
    for fee in fees:
        print("Year: {}\t   Fee Revenue: ${}\t Increase\Decrease: {}".format(fee[0],fee[1],fee[2]))
        count += 1
        rev += fee[1]

    print(f"Yearly Fee Revenue AVG: ${rev/count:.2f}")


#Display how many clients have had over x amount of transactions in a month
def userTransactions(cursor, display, transactions):
    cursor.execute(f"select client_id,COUNT(*) >= {transactions} as count, extract(year from transaction_date) as year, extract(month from transaction_date) as month from transactions group by client_id, month(transaction_date), year(transaction_date)")
    selection = cursor.fetchall()
    x = 0

    print(display)
    for i in selection:
        x += i[1]

    print(f"{x} clients have had at most {transactions} transactions in a month")


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
    averageAssets(myCursor, "What is the average asset possesion for clients?")
    assetAccounts(myCursor,"Displaying all clients total fees paid compared to asset possession")

    #Displaying transaction acticity
    print("\n-----------------------------------------------------------------")
    print("Report 2")
    print("-----------------------------------------------------------------")
    userTransactions(myCursor,"How many clients have a high number of transactions per month?", 2)
    transactionsPerMonth(myCursor,"\nWhat is transaction activity per month?\n")
    transactionsPerYear(myCursor,"\nWhat is transaction activity per year?\n")
    
    #Number of clients added in each 6 month period since first account initialization date
    print("\n-----------------------------------------------------------------")
    print("Report 3")
    print("-----------------------------------------------------------------")
    monthlyNewUsers(myCursor,"How many clients have been added within the last 6 months?", 6)
    acquisitionRate(myCursor,"\nWhat is the rate of new client acquisition for every 6 month period?")
    
    #Displaying fee revenue monthly and yearly trends
    print("\n-----------------------------------------------------------------")
    print("Report 4")
    print("-----------------------------------------------------------------")
    monthlyFeeRevenue(myCursor,"What is total transaction fee revenue per month?\n")
    yearlyFeeRevenue(myCursor,"\nWhat is total transaction fee revenue per year?\n")

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


