import logging
import re
from w3lib.url import canonicalize_url, url_query_cleaner

from scrapy.http import FormRequest
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.utils.log import configure_logging
from datetime import datetime

import logging
logger = logging.getLogger("ProductSpider")

class ProductSpider(CrawlSpider):

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

    name = 'products'
    start_urls = ["http://127.0.0.1:50713/test.html"]

    # allowed_domains=["steampowered.com"]
    # custom_settings = {
    #     'LOG_FILE': 'spider.log',
    #
    # }

    def parse(self, response):
        # Circumvent age selection form.
        next_page = response.css('div.testdiv a::text').extract()

        for i in next_page:
            print(int(i)+1)
