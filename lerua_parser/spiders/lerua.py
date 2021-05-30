import scrapy
from scrapy.loader import ItemLoader
from lerua_parser.items import LeruaParserItem


class LeruaSpider(scrapy.Spider):
    name = 'lerua'
    allowed_domains = ['leroymerlin.ru']
    url = 'https://leroymerlin.ru'

    def __init__(self, searchInput):
        super(LeruaSpider, self).__init__()
        self.start_urls = [self.url + f'/search/?q={searchInput}&suggest=true']
        print(self.start_urls)

    def parse(self, response):
        product_links = response.xpath('//a[@data-qa="product-name"]/@href').extract()
        for link in product_links:
            yield response.follow(f'{self.url + link}', callback=self.parse_goods)

        next_link = response.xpath('//a[contains(@aria-label, "Следующая страница")]/@href').extract()
        if next_link != None:
            next_page = self.url + next_link
            yield response.follow(next_page, callback=self.parse)

    def parse_goods(self, response):
        # name = response.xpath('//h1/text()')
        # link = response.url
        # price = response.xpath('//span[@slot= "price"]/text()')
        # article = response.xpath('//span[@slot= "article"]/text()')
        # text = response.xpath('//uc-pdp-section-layout/uc-pdp-section-vlimited/div/p/text()')
        # photo = response.xpath('//img[@alt="image thumb"]/@src')

        loader = ItemLoader(item=LeruaParserItem(), response=response)
        loader.add_xpath('name', '//h1/text()')
        loader.add_value('url', response.url)
        loader.add_xpath('price', '//span[@slot="price"]/text()')
        loader.add_xpath('article', '//span[@slot="article"]/text()')
        loader.add_xpath('text', '//uc-pdp-section-layout/uc-pdp-section-vlimited/div/p/text()')
        loader.add_xpath('photo', '//img[@alt="image thumb"]/@src')

        yield loader.load_item()