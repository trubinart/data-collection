from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from scrapy_jobparser import settings
from scrapy_jobparser.spiders.hhru import HhruSpider
from scrapy_jobparser.spiders.superjob import SuperjobSpider
from pymongo import MongoClient


if __name__ == '__main__':
	crawler_settings = Settings()
	crawler_settings.setmodule(settings)
	process = CrawlerProcess(settings=crawler_settings)
	process.crawl(HhruSpider)
	process.crawl(SuperjobSpider)
	process.start()

	client = MongoClient('localhost', 27017)
	db = client['vacancy_db_2']

	collection_superjob = db.superjob
	collection_hhru = db.hhru

	with open('results.txt', 'w') as file:
		for doc in collection_superjob.find({}):
			file.write(f'{str(doc)} \n')

	with open('results.txt', 'a') as file:
		for doc in collection_hhru.find({}):
			file.write(f'{str(doc)} \n')