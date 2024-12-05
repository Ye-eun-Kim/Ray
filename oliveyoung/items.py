from scrapy.item import Item, Field
class OliveyoungItem(Item):
    _id = Field()
    name = Field()
    price = Field()
    brand = Field()
    url = Field()
    time = Field()
