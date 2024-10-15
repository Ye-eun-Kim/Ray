from scrapy.item import Item, Field
from scrapy.loader.processors import Join
class OliveyoungItem(Item):
    _id = Field()
    name = Field()
    price = Field()
    brand = Field()
    url = Field()
