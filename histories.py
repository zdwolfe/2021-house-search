from urllib.parse import urlparse


class HistoryRecord:
    def __init__(self, domain, url):
        self.domain = domain
        self.url = url

    @classmethod
    def fromUrl(cls, url):
        return HistoryRecord(
            domain=urlparse(url).netloc.replace("www.", ""),
            url=url
        )

    def __str__(self):
        return "domain=" + self.domain + ";" + "url=" + self.url

    __repr__ = __str__