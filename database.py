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
# query = "SELECT * FROM zamowienie"
# db.execute_query(query)
# db.print_query()
# ans = db.db_to_list(query)
# print(ans[0][1])

# query = "INSERT INTO zamowienie(samochod_id) VALUES ('2')"
# db.execute_query(query)
# print(db.cur.lastrowid)
# query2 = "SELECT * FROM zamowienie"
# db.execute_query(query2)
# db.print_query()

# PRZYKLAD POBRANIA DANYCH W ZALEZNOSCI OD ZMIENNEJ
# query = "SELECT samochod_id FROM samochod WHERE nr_rejestracyjny='DZA38FJ'"
# ans = db.db_data_to_list(query)[0][0]
# print(ans)
# query_2 = f"SELECT * FROM samochod WHERE samochod_id = '{ans[0][0]}'"
# ans2 = db.db_data_to_list(query_2)
# print(ans2)
