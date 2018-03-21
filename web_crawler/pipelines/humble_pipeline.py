from scrapy.exceptions import DropItem
from web_crawler.database_connector import humble_db_connector

database = humble_db_connector.HumbleDBConnector


class HumblePipeline(object):

    def __init__(self):
        self.names_seen = set()

    def process_item(self, item, spider):
        if item['game_title'] in self.names_seen:
            raise DropItem("Duplicate item found: %s" % item)
        else:
            self.names_seen.add(item['game_title'])
            return database.connect_to_database(database, item)
