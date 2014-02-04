from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector

class BolSpider(BaseSpider):
    name = "bol"
    allowed_domains = ["bol.com"]
    start_urls = [
        "http://www.bol.com/nl/l/nederlandse-boeken/nederlandse-boeken-thrillers-fantasy-nieuw/N/255+8293+14033/No/12/section/books/index.html"
    ]

    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        sites = hxs.select('//img')
        for site in sites:
            coverlink = site.select('@src').extract()
            rating = site.select('@rating')
            print rating

