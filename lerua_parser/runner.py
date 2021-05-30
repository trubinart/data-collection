from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from lerua_parser import settings
from lerua_parser.spiders.lerua import LeruaSpider
from pymongo import MongoClient

if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)
    process = CrawlerProcess(settings=crawler_settings)

    searchInput = 'растение'

    process.crawl(LeruaSpider, searchInput=searchInput)
    process.start()
