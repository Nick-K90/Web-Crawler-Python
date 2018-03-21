import scrapy
from web_crawler.database_connector import db_connector
from web_crawler.items import steam_item
from web_crawler.item_loaders import steam_item_loader
from datetime import datetime

database = db_connector.DBConnector
steam = steam_item.SteamItem()


class SteamSearchSpider(scrapy.Spider):
    name = "steam_search_spider"
    page_count = 1
    start_time = datetime.now()

    # Spider specific setting to convert from Unicode to UTF-8 for GBP sign.
    # custom_settings = {'FEED_EXPORT_ENCODING': 'utf-8'}

    start_urls = [
        'http://store.steampowered.com/search/?category1=998',
    ]
    # allowed_domains = ["steampowered.com"]

    def parse(self, response):

        # XPath for ID //*[contains(@id, 'tab_topsellers_content')] CSS Selector for ID 'div[id=tab_topsellers_content]'
        hooks = response.css('div[id=search_result_container] a.search_result_row')

        for hook in hooks:
            # Only way to iterate is to have selector=hook, instead of response=response
            loader = steam_item_loader.ProductItemLoader(item=steam, selector=hook)
            loader.add_css('game_title', 'span.title::text')
            loader.add_css('game_current_price', 'div.search_price::text')
            # loader.add_xpath('game_price', 'normalize-space(//*[contains(concat( " ", @class, " " ), concat( " ", "responsive_secondrow", " " ))])')

            yield loader.load_item()  # yield without brackets {} for pipeline.

            # print(loader.load_item())

        # print("Games added:", game_count)

        # next_page = response.css('div.search_pagination_right a.pagebtn a::attr(href)')
        # To get the last element using xpath use "and position()=last()"
        next_page = response.xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "pagebtn", " " )) and position()=last()]/@href').extract_first()
        print(next_page)
        if next_page is not None:
            print("Next page!!!!", next_page)
            SteamSearchSpider.page_count += 1
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse, dont_filter=True)
        else:
            time_elapsed = datetime.now() - SteamSearchSpider.start_time
            print("Crawling finished!. Pages crawled:", SteamSearchSpider.page_count, "Total time:", time_elapsed)

