# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from kitap_yurdu.models import create_table, connect_db
from sqlalchemy.orm import sessionmaker
from kitap_yurdu.models import Book_Library


class KitapYurduPipeline:
    def __init__(self):
        engine = connect_db()
        create_table(engine)
        self.Session = sessionmaker(bind=engine)

    def process_item(self, item, spider):
        session = self.Session()
        book = Book_Library()

        book.title = item["title"][0]
        book.writer = item["writer"][0]
        book.price = item["price"][0]
        book.publisher = item["publisher"][0]
        book.rating_score = item["rating_score"][0]
        book.publish_date = item["publish_date"][0]
        book.review_counts = item["review_counts"][0]
        book.description = item["description"][0]
        book.external_link = item["external_link"][0]
        book.page_number = item["page_number"][0]



        try:
            session.add(book)
            session.commit()

        except:
            session.rollback()
            raise ValueError

        finally:
            session.close()

        return item
