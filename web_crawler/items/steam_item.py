import scrapy
from scrapy.loader.processors import Join, MapCompose, Compose


class StripText:
    def __init__(self, chars=' \r\t\n()£'):
        self.chars = chars

    def __call__(self, value):  # This makes an instance callable!
        try:
            return value.strip(self.chars)
        except:
            return value


class SteamItem(scrapy.Item):

    def str_to_int(x):
        try:
            return int(float(x))
        except ValueError:
            return x

    def str_to_float(x):
        try:
            float(x)
            return x
        except ValueError:
            return 0

    game_id = scrapy.Field()
    game_title = scrapy.Field()
    game_original_price = scrapy.Field(output_processor=Compose(MapCompose(StripText(), str_to_float), max))
    game_current_price = scrapy.Field(output_processor=Compose(MapCompose(StripText(), str_to_float), max))
    game_all_reviews = scrapy.Field(output_processor=Compose(MapCompose(StripText(), lambda x: x.replace(',', ''), str_to_int), max))
    game_release_date = scrapy.Field()
    game_developer = scrapy.Field()
    game_publisher = scrapy.Field()
    game_tags = scrapy.Field(output_processor=Join(', '))  # processors in items have higher priority than loader
    game_system = scrapy.Field(output_processor=Join(', '))
    game_full_link = scrapy.Field()

