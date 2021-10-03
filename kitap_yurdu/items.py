# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy import Field
from scrapy import Item


class KitapYurduItem(Item):
    title = Field()
    writer = Field()
    publisher = Field()
    price = Field()
    publish_date = Field()
    page_number = Field()
    external_link = Field()
    rating_score = Field()
    review_counts = Field()
    description = Field()
