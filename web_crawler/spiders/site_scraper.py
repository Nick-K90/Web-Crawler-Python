import scrapy


class SiteScraper(scrapy.Spider):
    name = "steam_scrapper"

    # Spider specific setting to convert from Unicode to UTF-8 for GBP sign.
    # custom_settings = {'FEED_EXPORT_ENCODING': 'utf-8'}

    # start_urls = [
    #     'http://store.steampowered.com/search/?category1=998',
    # ]
    def start_requests(self):
        urls = [
            'https://www.humblebundle.com/store/search?sort=bestselling',

        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = '%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)