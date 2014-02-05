import re
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector

from scrapybol.items import ScrapybolItem


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

    #total_nr_of_items = 2

    start_urls = []
    for eachItem in range(0, total_nr_of_items):
        new_url = 'http://www.bol.com/nl/l/nederlandse-boeken/nederlandse-boeken-thrillers-fantasy-thrillers/N/261+8293/No/' + str(eachItem * 12) + '/section/books/index.html'
        start_urls.append(new_url)


    def parse(self, response):
        items = []

        hxs = HtmlXPathSelector(response)

        sites = hxs.select('//div[@class="list_view"]')
        for site in sites:
            item = ScrapybolItem()
            #item['ratings'] 			= str(site.select('//meta[@itemprop="ratingValue"]/@content').extract())[3:-2]
            item['isbns']              	= str(site.select('//img[@itemprop="image"]/@src').extract())
            item['languages']           = str(site.select('//meta[@itemprop="inLanguage"]/@content').extract())
            item['pubdates']            = str(site.select('//meta[@itemprop="datePublished"]/@content').extract())
            item['covers']              = str(site.select('//img[@itemprop="image"]/@src').extract())
            item['titles']              = str(site.select('//a[@itemprop="name"]/text()').extract())
            item['authors']             = str(site.select('//a[@itemprop="author"]/text()').extract())
            item['bindingcodes']        = str(site.select('//span[@data-attr-key="BINDINGCODE"]/text()').extract())
            #item['prices']              = str(site.select('//strong[@itemprop="price"]/text()').extract())
            #item['ebookprices']         = str(site.select('//span[@class="pricetag"]/text()').extract())
            items.append(item)

        return items



        # result = zip(isbns, ratings, languages, pubdates, covers, titles, authors, prices, ebookprices, bindingcodes)



