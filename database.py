import sqlite3

# connection = sqlite3.connect(':memory:')
connection = sqlite3.connect('CarRepairShop.db')

cur = connection.cursor()
sql_query = "SELECT * FROM marka"

cur.execute(sql_query)


def print_query():
    for row in cur.execute(sql_query):
        print(row)
