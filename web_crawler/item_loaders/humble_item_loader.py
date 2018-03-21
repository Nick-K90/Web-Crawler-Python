from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose, Join
from w3lib.html import replace_escape_chars


# TODO make a superclass for this and the steam item loader and any other in the future?
class ProductItemLoader(ItemLoader):
    default_input_processor = MapCompose(replace_escape_chars)  # replaces \n \t \r very handy!
    default_output_processor = TakeFirst()
    game_platform_out = Join(' - ')  # custom output for humble items to join multiple platforms name_out =
    game_operating_system_out = Join(', ')
    game_full_link_out = Join('')
