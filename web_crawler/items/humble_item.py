import scrapy
from scrapy.loader.processors import MapCompose, Compose

class StripText:
    def __init__(self, chars=' \r\t\n()£%-'):
        self.chars = chars

    def __call__(self, value):  # This makes an instance callable!
        try:
            return value.strip(self.chars)
        except:
            return value


class HumbleItem(scrapy.Item):

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

    game_title = scrapy.Field()
    game_platform = scrapy.Field()
    game_operating_system = scrapy.Field()
    game_discount_percentage = scrapy.Field(output_processor=Compose(MapCompose(StripText(), str_to_int), max))
    game_current_price = scrapy.Field(output_processor=Compose(MapCompose(StripText(), str_to_float), max))
    game_full_link = scrapy.Field()

