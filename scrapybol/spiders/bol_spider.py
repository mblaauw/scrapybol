import re
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from bs4 import BeautifulSoup
from urllib2 import urlopen


class BolSpider(BaseSpider):
    name = "bol"
    allowed_domains = ["bol.com"]

    base_url = 'http://www.bol.com/nl/l/nederlandse-boeken/nederlandse-boeken-thrillers-fantasy-thrillers/N/261+8293/No/0/section/books/index.html'
    html = urlopen(base_url).read()
    soup = BeautifulSoup(html, 'lxml')

    total_nr_of_items = re.sub('<[^>]+>', '', str(soup.find('span', 'tst_searchresults_nrFoundItems')))
    total_nr_of_items = int(round(int(float(total_nr_of_items.replace('.', '')))/12))

    total_nr_of_items = 5

    start_urls = []
    for eachItem in range(0, total_nr_of_items):
        new_url = 'http://www.bol.com/nl/l/nederlandse-boeken/nederlandse-boeken-thrillers-fantasy-thrillers/N/261+8293/No/' + str(eachItem * 12) + '/section/books/index.html'
        start_urls.append(new_url)


    def parse(self, response):
        hxs = HtmlXPathSelector(response)

        ratings = []
        sites = hxs.select('//meta[@itemprop="ratingValue"]')
        for site in sites:
            ratings.append(str(site.select('@content').extract())[3:-2])

        languages = []
        sites = hxs.select('//meta[@itemprop="inLanguage"]')
        for site in sites:
            languages.append(str(site.select('@content').extract())[3:-2])

        pubdates = []
        sites = hxs.select('//meta[@itemprop="datePublished"]')
        for site in sites:
            pubdates.append(str(site.select('@content').extract())[3:-2])

        covers = []
        isbns = []
        sites = hxs.select('//img[@itemprop="image"]')
        for site in sites:
            isbn = str(site.select('@src').extract())
            isbn = str(isbn[len(isbn)-25:-6])

            # todo: clean the isbn further

            isbns.append(isbn)
            covers.append(str(site.select('@src').extract())[3:-2])

        titles = []
        sites = hxs.select('//a[@itemprop="name"]')
        for site in sites:
            titles.append(str(site.select('text()').extract())[3:-2])

        authors = []
        sites = hxs.select('//a[@itemprop="author"]')
        for site in sites:
            authors.append(str(site.select('text()').extract())[3:-2])

        prices = []
        sites = hxs.select('//strong[@itemprop="price"]')
        for site in sites:
            prices.append(str(site.select('text()').extract())[10:-2])

        ebookprices = []
        sites = hxs.select('//span[@class="pricetag"]')
        for site in sites:
            ebookprices.append(str(site.select('text()').extract())[10:-2])

        bindingcodes = []
        sites = hxs.select('//span[@data-attr-key="BINDINGCODE"]')
        for site in sites:
            bindingcodes.append(str(site.select('text()').extract_unquoted())[11:25])

        result = zip(isbns, ratings, languages, pubdates, covers, titles, authors, prices, ebookprices, bindingcodes)
        print result



