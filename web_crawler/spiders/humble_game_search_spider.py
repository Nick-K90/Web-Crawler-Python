import scrapy
from web_crawler.items import humble_item
from web_crawler.item_loaders import humble_item_loader
from datetime import datetime
from scrapy_splash import SplashRequest
import logging

humble = humble_item.HumbleItem()
logger = logging.getLogger("HumbleGameSearchSpider")


class HumbleSearchSpider(scrapy.Spider):

    def __init__(self, *args, **kwargs):

        logger.setLevel(logging.INFO)
        # create the logging file handler
        fh = logging.FileHandler("../logs/humble_game_search_spider.log")
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        # add handler to logger object
        logger.addHandler(fh)
        logger.info({"Started: ", datetime.now()})

        super().__init__(*args, **kwargs)

    name = "humble_game_search_spider"
    page_count = 0
    start_time = datetime.now()
    custom_settings = {
        'ITEM_PIPELINES': {
            'web_crawler.pipelines.humble_pipeline.HumblePipeline': 300
        },
        'DOWNLOADER_MIDDLEWARES' : {
                'scrapy_splash.SplashCookiesMiddleware': 723,
                'scrapy_splash.SplashMiddleware': 725,
                'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,
        },
        'SPIDER_MIDDLEWARES' : {
            'scrapy_splash.SplashDeduplicateArgsMiddleware': 100,
        },
        'DUPEFILTER_CLASS' : 'scrapy_splash.SplashAwareDupeFilter'
    }

    start_urls = [
        'https://www.humblebundle.com/store/search?sort=newest&filter=new',
    ]

    # allowed_domains = ["steampowered.com"]


    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url, self.test,
                endpoint='render.html',
                args={'wait': 0.5},
            )

    def test(self, response):
        next_page = response.css('div.pagination a.js-grid-page::text').extract()
        # # print("next_page:", next_page)
        # # # Seems to be working, avoids an error too that appears when i downcast directly to int
        # next_page_str = str(next_page)
        # # print("next_page_str:", next_page_str)
        # next_page_int = int(next_page_str)
        # # #next_page = response.xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "grid-page", " " ))]/text() and position()=last()').extract_first()
        # print(next_page_int)
        print(len(next_page))
        # print("Games added:", game_count)
        while self.page_count < len(next_page):
            #next_page = "https://www.humblebundle.com/store/search?sort=bestselling&page=" + str(i)
            self.page_count += 1
            #logger.info("Page: %s" % self.page_count)
            yield SplashRequest("https://www.humblebundle.com/store/search?sort=newest&filter=new&page=" + str(self.page_count), self.parse,
                endpoint='render.html',
                args={'wait': 0.5},
            )

    def parse(self, response):
        hooks = {
            'entity': response.css('li.entity-block-container'),
            'operating_systems': response.css('li.entity-block-container ul.operating-systems')
                 }

        for hook in hooks.get('entity'):
            # Only way to iterate is to have selector=hook, instead of response=response
            loader = humble_item_loader.ProductItemLoader(item=humble, selector=hook)

            loader.add_css('game_title', 'span.entity-title::text')

            self.add_platforms(loader)

            loader.add_css('game_operating_system', 'ul.operating-systems li.operating-system::attr(title)')

            if loader.get_css('span.discount-percentage'):
                loader.add_css('game_discount_percentage', 'span.discount-percentage::text')
            else:
                loader.add_value('game_discount_percentage', '0')

            loader.add_css('game_current_price', 'div.price-container span.price::text')

            loader.add_value('game_full_link', 'https://www.humblebundle.com')
            loader.add_css('game_full_link', 'a.entity-link::attr(href)')

            yield loader.load_item()  # yield without brackets {} for pipeline.
            print(loader.load_item())


        # next_page = response.css('div.search_pagination_right a.pagebtn a::attr(href)')
        # To get the last element using xpath use "and position()=last()"
        # next_page = response.xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "pagebtn", " " )) and position()=last()]/@href').extract_first()
        # print(next_page)
        # if next_page is not None:
        #     print("Next page!!!!", next_page)
        #     SteamSearchSpider.page_count += 1
        #     next_page = response.urljoin(next_page)
        #     yield scrapy.Request(next_page, callback=self.parse, dont_filter=True)
        # else:
        #     time_elapsed = datetime.now() - SteamSearchSpider.start_time
        #     print("Crawling finished!. Pages crawled:", SteamSearchSpider.page_count, "Total time:", time_elapsed)
        #


    def add_platforms(self, loader):
        if loader.get_xpath(".//li[contains(@class, 'platform') and contains(@class, 'hb-steam')]"):
            loader.add_value('game_platform', 'Steam')

        if loader.get_xpath(".//li[contains(@class, 'platform') and contains(@class, 'hb-uplay')]"):
            loader.add_value('game_platform', 'Uplay')

        if loader.get_xpath(".//li[contains(@class, 'platform') and contains(@class, 'hb-drmfree')]"):
            loader.add_value('game_platform', 'DRM-Free')

        if loader.get_xpath(".//li[contains(@class, 'platform') and contains(@class, 'hb-key')]"):
            loader.add_value('game_platform', 'Key')

        if loader.get_xpath(".//li[contains(@class, 'platform') and contains(@class, 'hb-bundle')]"):
            loader.add_value('game_platform', 'Bundle')

        if loader.get_xpath(".//li[contains(@class, 'platform') and contains(@class, 'hb-android')]"):
            loader.add_value('game_platform', 'Android')

        if loader.get_xpath(".//li[contains(@class, 'platform') and contains(@class, 'hb-star')]"):
            loader.add_value('game_platform', 'Star')
