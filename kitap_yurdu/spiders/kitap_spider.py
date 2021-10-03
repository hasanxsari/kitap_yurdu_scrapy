import scrapy
from kitap_yurdu.items import KitapYurduItem
from scrapy.loader import ItemLoader


class KitapSpiderSpider(scrapy.Spider):
    name = 'kitap_spider'
    start_urls = ['https://www.kitapyurdu.com/index.php?route=product/category&filter_category_all=true&path=1_236&filter_in_stock=1&sort=purchased_365&order=DESC&limit=100']

    def parse(self, response):
        books = response.xpath("//div[@class='product-cr']")
        for book in books:
            rating = book.xpath(".//i[@class='fa fa-star active']").getall()
            if rating:
                rating_score = str(len(rating))
            else:
                rating_score = "-"
            title = book.xpath(".//div/@title").get()
            if title:
                title = title.split()[0]
                if title.isdigit():
                    review_counts = title.split()[0]
                else:
                    review_counts = 0

            url = book.xpath(".//a/@href").get()
            yield scrapy.Request(url,callback=self.parse_books,meta={"rating_score":rating_score,"review_counts":review_counts})
        
        next_btn = response.xpath("//a[@class='next']/@href").get()
        if next_btn:
            yield scrapy.Request(next_btn,callback=self.parse)


    def parse_books(self,response):
        item = ItemLoader(KitapYurduItem())

        title = response.xpath("//h1[@class='pr_header__heading']/text()").get()
        writer = response.xpath("//div[@class='pr_producers__manufacturer']/div/a/text()").get()
        publisher = response.xpath("//div[@class='pr_producers__publisher']/div/a/text()").get()
        price_int = response.xpath("//div[@class='price__item']/text()").get()
        price_coin = response.xpath("//div[@class='price__item']/small/text()").get()
        price = price_int + price_coin
        publish_date = response.xpath("//td[contains(text(),'Yayın')]/following-sibling::td/text()").get()
        page_number = response.xpath("//td[contains(text(),'Sayfa')]/following-sibling::td/text()").get()
        desc = response.xpath("//span[@class='info__text']/text()").getall()
        if desc:
            description = " ".join(desc)
            item.add_value("description",description)


        if title:
            item.add_value("title",title)
        if writer:
            item.add_value("writer",writer)
        if publisher:
            item.add_value("publisher",publisher)
        if price:
            item.add_value("price",price)
        if publish_date:
            item.add_value("publish_date",publish_date)
        if page_number:
            item.add_value("page_number",page_number)
        
        item.add_value("external_link",response.url)
        item.add_value("rating_score",response.meta.get("rating_score"))
        item.add_value("review_counts",response.meta.get("review_counts"))
        
        yield item.load_item()