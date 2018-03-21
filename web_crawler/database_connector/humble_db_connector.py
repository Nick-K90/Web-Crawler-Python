import mysql.connector
from mysql.connector import errorcode
from datetime import datetime
import logging

config = {'user': 'root', 'password': '', 'host': '127.0.0.1', 'database': 'testdb', 'raise_on_warnings': True}
count = 0

logger = logging.getLogger("Humble_Database")


class StripText:
    def __init__(self, chars=' \r\t\n()£'):
        self.chars = chars

    def __call__(self, value):  # This makes an instance callable!
        try:
            return value.strip(self.chars)
        except:
            return value


class HumbleDBConnector:

    logger.setLevel(logging.INFO)
    # create the logging file handler
    fh = logging.FileHandler("../logs/humble_database.log")
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    # add handler to logger object
    logger.addHandler(fh)

    def connect_to_database(self, item):
        try:
            cnx = mysql.connector.connect(**config)
            cursor = cnx.cursor()             # item['game_title] instead of item.game_title
            # self.insert_data(self, cursor, cnx, item['game_title'], item['game_price'])
            check_for_duplicates(cursor, cnx, item)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                    logger.error("Something is wrong with your user name or password")
                    print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                    logger.error("Database does not exist")
                    print("Database does not exist")
            else:
                print(err)
        else:
            cnx.close()


def check_for_duplicates(cursor, cnx, item):
    check_duplicates = 'SELECT game_title FROM humble_first_test WHERE game_title = "%s"' % item['game_title']
    cursor.execute(check_duplicates)
    result = cursor.fetchone()
    if result:
        #logger.info({"Duplicate item found: %s" % result})
        print("Duplicate item found: %s" % result)
    else:
        insert_data(cursor, cnx, item)


def validate(game, date_text):
    try:
        acceptable_date_format = datetime.strptime(date_text, '%d %b, %Y')
        return acceptable_date_format
    except ValueError:
        logger.warning({"Incorrect data format! Date: ", date_text, " Game: ", game})
        acceptable_date_format = '1000-01-01'
        return acceptable_date_format


# the i=[0] trick is to keep count of how many times the function was called
def insert_data(cursor, cnx, item, i=[0]):

    add_row = "INSERT INTO humble_first_test" "(a_i, game_title, game_platform, game_operating_system," \
              " discount_percentage, current_price, full_link, date_scrapped)" \
              "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"

    a_i = cursor.lastrowid
    # sql = """INSERT INTO test_table(A_I, Title, Price) VALUES(%s, %s, %s)""" % (A_I, 'Title', "Price")

    game_details = (a_i, item['game_title'], item['game_platform'], item['game_operating_system'],
                    item['game_discount_percentage'], item['game_current_price'], item['game_full_link'],
                    datetime.now())

    cursor.execute(add_row, game_details)
    #logger.info("Database update")

    cnx.commit()
    cursor.close()
    i[0] += 1
    logger.info({"Games added:", i[0]})
    print("Games added:", i[0])


if __name__ == '__main__':
    print("This only executes when %s is executed rather than imported" % __file__)

