from w3lib.url import url_query_cleaner
from scrapy.dupefilters import RFPDupeFilter


class SteamDupeFilter(RFPDupeFilter):
    def request_fingerprint(self, request):
        url = url_query_cleaner(request.url, ['snr'], remove=True)
        request = request.replace(url=url)
        return super().request_fingerprint(request)
