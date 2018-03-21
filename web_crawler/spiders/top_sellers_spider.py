import scrapy
from web_crawler.database_connector import db_connector
from web_crawler.items import steam_item
from web_crawler.item_loaders import steam_item_loader


database = db_connector.DBConnector
steam = steam_item.SteamItem()


class TopSellersSpider(scrapy.Spider):
    name = "top_sellers_spider"


    # Spider specific setting to convert from Unicode to UTF-8 for GBP sign.
    # custom_settings = {'FEED_EXPORT_ENCODING': 'utf-8'}

    start_urls = [
        'http://127.0.0.1:57463/test.html',
    ]
    #allowed_domains = ["steampowered.com"]

    def parse(self, response):
        game_count = 0
        # XPath for ID //*[contains(@id, 'tab_topsellers_content')] CSS Selector for ID 'div[id=tab_topsellers_content]'
        hooks = response.css('div[id=tab_topsellers_content] a.tab_item')

        for hook in hooks:
            # Only way to iterate is to have selector=hook, instead of response=response
            loader = steam_item_loader.ProductItemLoader(item=steam, selector=hook)
            loader.add_css('game_name', 'div.tab_item_name::text')
            loader.add_css('game_price', 'div.discount_final_price::text')

            yield loader.load_item()  # yield without brackets {} for pipeline.

            #print(loader.load_item())
            game_count += 1

        print("Games added:", game_count)
        #
        # next_page = response.css('li.next web_crawler::attr(href)').extract_first()
        # if next_page is not None:
        #     next_page = response.urljoin(next_page)
        #     yield scrapy.Request(next_page, callback=self.parse)

