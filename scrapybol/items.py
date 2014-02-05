# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field

class ScrapybolItem(Item):
    # define the fields for your item here like:
    # name = Field()
    ratings = Field()
    languages = Field()
    pubdates = Field()
    covers = Field()
    isbns = Field()
    titles = Field()
    authors = Field()
    prices = Field()
    ebookprices = Field()
    bindingcodes = Field()
    pass
