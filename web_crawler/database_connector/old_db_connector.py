import mysql.connector
from mysql.connector import errorcode



config = {'user': 'root', 'password': '', 'host': '127.0.0.1', 'database': 'testdb', 'raise_on_warnings': True}
count = 0

class DBConnector:

    def connect_to_database(self, item):
        try:
            cnx = mysql.connector.connect(**config)
            cursor = cnx.cursor()             # item['game_name] instead of item.game_name
            #self.insert_data(self, cursor, cnx, item['game_name'], item['game_price'])
            check_for_duplicates(cursor, cnx, item['game_title'], item['game_current_price'])
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                    print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                    print("Database does not exist")
            else:
                print(err)
        else:
            cnx.close()


def check_for_duplicates(cursor, cnx, name, price):
    check_duplicates = 'SELECT Title FROM test_table WHERE Title = "%s"' % name
    cursor.execute(check_duplicates)
    result = cursor.fetchone()
    if result:
        print("Duplicate item found: %s" % result)
    else:
        insert_data(cursor, cnx, name, price)


# the i=[0] trick is to keep count of how many times the function was called
def insert_data(cursor, cnx, name, price, i=[0]):

    add_row = "INSERT INTO test_table" "(A_I, Title, Price)" "VALUES (%s, %s, %s)"
    A_I = cursor.lastrowid
    # sql = """INSERT INTO test_table(A_I, Title, Price) VALUES(%s, %s, %s)""" % (A_I, 'Title', "Price")
    game = (A_I, name, price)
    cursor.execute(add_row, game)
    print("Database updated")
    cnx.commit()
    cursor.close()
    i[0] += 1
    print("Games added:", i[0])


if __name__ == '__main__':
    print("This only executes when %s is executed rather than imported" % __file__)
