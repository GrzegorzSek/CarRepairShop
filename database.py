import sqlite3

# connection = sqlite3.connect(':memory:')


class Database:
    def __init__(self):
        self.connection = sqlite3.connect('CarRepairShop.db')
        self.cur = self.connection.cursor()

    def execute_query(self, q):
        self.cur.execute(q)
        self.connection.commit()

    def print_query(self):
        for line in self.cur:
            print(line)

    def db_data_to_list(self, q):
        self.cur.execute(q)
        result = self.cur.fetchall()
        self.connection.commit()
        return result

    def close_connection(self):
        self.cur.close()


db = Database()
# ----------------------------------------------QUERIES TEST SECTION
# SELECT zamowienie_id, czas_razem FROM zamowienie ORDER BY data_mod DESC
# query = "SELECT zamowienie_id, czas_razem FROM zamowienie ORDER BY data_mod DESC"
# result = db.db_data_to_list(query)
# print(result)
# result.pop(1)
# print(result)