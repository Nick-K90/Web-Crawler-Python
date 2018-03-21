from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose
from w3lib.html import replace_escape_chars


class ProductItemLoader(ItemLoader):
    default_input_processor = MapCompose(replace_escape_chars)  # replaces \n \t \r very handy!
    default_output_processor = TakeFirst()
