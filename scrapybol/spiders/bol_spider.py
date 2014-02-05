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

        ratings = []
        sites = hxs.select('//meta[@itemprop="ratingValue"]')
        for site in sites:
            ratings.append(str(site.select('@content').extract()))

        languages = []
        sites = hxs.select('//meta[@itemprop="inLanguage"]')
        for site in sites:
            languages.append(str(site.select('@content').extract()))

        pubdates = []
        sites = hxs.select('//meta[@itemprop="datePublished"]')
        for site in sites:
            pubdates.append(str(site.select('@content').extract()))

        covers = []
        isbns = []
        sites = hxs.select('//img[@itemprop="image"]')
        for site in sites:
            isbns.append(str(site.select('@src').extract()).split('/')[11][:-6])
            covers.append(str(site.select('@src').extract()))

        titles = []
        sites = hxs.select('//a[@itemprop="name"]')
        for site in sites:
            titles.append(str(site.select('text()').extract()))

        authors = []
        sites = hxs.select('//a[@itemprop="author"]')
        for site in sites:
            authors.append(str(site.select('text()').extract()))

        prices = []
        sites = hxs.select('//strong[@itemprop="price"]')
        for site in sites:
            prices.append(str(site.select('text()').extract()))

        ebookprices = []
        sites = hxs.select('//span[@class="pricetag"]')
        for site in sites:
            ebookprices.append(str(site.select('text()').extract()))

        bindingcodes = []
        sites = hxs.select('//span[@data-attr-key="BINDINGCODE"]')
        for site in sites:
            bindingcodes.append(str(site.select('text()').extract_unquoted())[11:25])

        result = zip(isbns, ratings, languages, pubdates, covers, titles, authors, prices, ebookprices, bindingcodes)
        print result



