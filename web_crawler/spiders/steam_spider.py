import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.http import FormRequest
from scrapy.linkextractors import LinkExtractor
from web_crawler.database_connector import db_connector
from web_crawler.items import steam_item
from web_crawler.item_loaders import steam_item_loader
from datetime import datetime
import logging
from scrapy.utils.log import configure_logging

database = db_connector.DBConnector
steam = steam_item.SteamItem()
logger = logging.getLogger("ProductSpider")


class SteamSpider(CrawlSpider):
    def __init__(self, *args, **kwargs):

        logger.setLevel(logging.INFO)
        # create the logging file handler
        fh = logging.FileHandler("../logs/steam_spider.log")
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        # add handler to logger object
        logger.addHandler(fh)
        logger.info({"Started: ", datetime.now()})

        super().__init__(*args, **kwargs)

    name = "steam_spider"
    page_count = 1
    start_time = datetime.now()

    # Spider specific setting to convert from Unicode to UTF-8 for GBP sign.
    # custom_settings = {'FEED_EXPORT_ENCODING': 'utf-8'}
    # custom_settings = {'LOG_FILE': 'steam_spider.log',}

    start_urls = [
        'http://store.steampowered.com/search/?category1=998',
    ]
    allowed_domains = ["steampowered.com"]

    rules = [
        Rule(
            LinkExtractor(
                allow='/app/(.+)/',
                restrict_css='#search_result_container'),
            callback='parse_product'),
        Rule(
            LinkExtractor(
                allow='page=(\d+)',
                restrict_css='.search_pagination_right'))
    ]

    def parse_product(self, response):
        # Circumvent age selection form.

        if '/agecheck/app' in response.url:

            logger.debug(f"Form-type age check triggered for {response.url}.")
            form = response.css('#agegate_box form')

            action = form.xpath('@action').extract_first()
            name = form.xpath('input/@name').extract_first()
            value = form.xpath('input/@value').extract_first()

            formdata = {
                name: value,
                'ageDay': '1',
                'ageMonth': '1',
                'ageYear': '1989'
                }
            yield FormRequest(
                    url=action,
                    method='POST',
                    formdata=formdata,
                    callback=self.parse_product
                )

        else:
            # I moved all parsing code into its own function for clarity.
            yield self.load_product(response)

    # Do not use 'parse' as the name of a function when CrawlSpider and Rules. Rules use it internally as a callback
    def load_product(self, response):

        # XPath for ID //*[contains(@id, 'tab_topsellers_content')] CSS Selector for ID 'div[id=tab_topsellers_content]'

        hook = {'id': response.css('div.glance_tags'),
                'title': response.css('div.apphub_HeaderStandardTop'),
                'price': response.css('div.game_purchase_action_bg:first-child'),
                'reviews': response.css('div.user_reviews'),
                'tags': response.css('div.glance_tags a'),
                'system': response.css('div.sysreq_tabs')}

        # for hook in hooks:
        # Only way to iterate is to have selector=hook, instead of response=response
        loader = steam_item_loader.ProductItemLoader(item=steam, selector=hook)
        loader.selector = hook.get('id')
        loader.add_css('game_id', 'div::attr(data-appid)')
        loader.selector = hook.get('title')
        loader.add_css('game_title', 'div.apphub_AppName::text')
        loader.selector = hook.get('price')

        loader.add_css('game_original_price', 'div.discount_original_price::text')
        # Needed in order to not have an empty value if game is not in discount
        if not loader.get_collected_values('game_original_price'):
            loader.add_css('game_original_price', 'div.game_purchase_price::text')
            if not loader.get_collected_values('game_original_price'):
                loader.add_xpath('game_original_price', '/html/body/div[1]/div[7]/div[3]/div[1]/div[2]'
                                                        '/div[5]/div[2]/div[1]/div[1]/div/div[2]/div[2]/div[1]')
                if not loader.get_collected_values('game_original_price'):
                        loader.add_value('game_original_price', '0.1')

        loader.add_css('game_current_price', 'div.game_purchase_price::text')
        # Needed in order to get the proper price that comes in order
        if not loader.get_collected_values('game_current_price'):
            loader.add_css('game_current_price', 'div.discount_final_price::text')
            if not loader.get_collected_values('game_current_price'):
                loader.add_xpath('game_original_price',
                                 '/html/body/div[1]/div[7]/div[3]/div[1]/div[2]/div[5]/div[2]/div[1]'
                                 '/div[1]/div/div[2]/div[2]/div[1]')
                if not loader.get_collected_values('game_current_price'):
                    loader.add_value('game_current_price', '0.1')

        loader.selector = hook.get('reviews')
        loader.add_css('game_all_reviews', 'div.user_reviews_summary_row:nth-child(2) span.responsive_hidden::text')
        loader.add_css('game_release_date', 'div.date::text')
        loader.add_css('game_developer', 'div[id=developers_list] a::text')
        loader.add_css('game_publisher', 'div.dev_row:last-child div.summary a::text')
        loader.selector = hook.get('tags')
        loader.add_css('game_tags', 'a::text')
        loader.selector = hook.get('system')
        loader.add_css('game_system', 'div.sysreq_tab::text')
        if not loader.get_collected_values('game_system'):
            loader.add_value('game_system', 'Windows')
        loader.add_value('game_full_link', response.request.url)

        print(loader.load_item())
        # loader.add_xpath('game_price', 'normalize-space(//*[contains(concat( " ", @class, " " ), concat( " ", "responsive_secondrow", " " ))])')

        return loader.load_item()  # yield without brackets {} for pipeline.
        #
        # # next_page = response.css('div.search_pagination_right a.pagebtn a::attr(href)')
        # # To get the last element using xpath use "and position()=last()"
        # next_page = response.xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "pagebtn", " " )) and position()=last()]/@href').extract_first()
        # print(next_page)
        # if next_page is not None:
        #     print("Next page!!!!", next_page)
        #     SteamSpider.page_count += 1
        #     next_page = response.urljoin(next_page)
        #     yield scrapy.Request(next_page, callback=self.parse, dont_filter=True)
        # else:
        #     time_elapsed = datetime.now() - SteamSpider.start_time
        #     print("Crawling finished!. Pages crawled:", SteamSpider.page_count, "Total time:", time_elapsed)
        #
