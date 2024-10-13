from scrapy.item import Item, Field
class OliveyoungItem(Item):
    name = Field()
    price = Field()
    brand = Field()
    url = Field()
