from pprint import pprint
from lxml import html
import requests
from pymongo import MongoClient
import json
import hashlib

client = MongoClient('localhost', 27017)
db = client['news_db']
try:
    collection = db.create_collection('news')
except:
    collection = db.news

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'}

collection.delete_many({})

def get_lenta_ru():
    domain = 'https://lenta.ru'
    source = 'lenta.ru'
    responce = requests.get(domain, headers=headers)

    dom = html.fromstring(responce.text)
    new_block = dom.xpath('//section/div[contains(@class, "b-yellow-box__wrap")]/div[contains(@class, "item")]/a')
    for item in new_block:
        news = {}
        news['title'] = item.xpath('..//text()')[0].replace('\xa0', ' ')
        news['source'] = source
        link = domain + item.xpath('..//@href')[0]
        news['link'] = link

        responce_get_date = requests.get(link, headers=headers)
        dom_get_date = html.fromstring(responce_get_date.text)
        date = dom_get_date.xpath('//div[contains(@class, "topic__info")]/time/@datetime')[0]
        news['date'] = date

        news_binary = json.dumps(news).encode('utf-8')
        hash = hashlib.sha3_256(news_binary)
        id = hash.hexdigest()
        news['_id'] = id
        try:
            collection.insert_one(news)
        except Exception:
            continue


def get_mail_news():
    domain = 'https://news.mail.ru'
    responce = requests.get(domain, headers=headers)
    dom = html.fromstring(responce.text)
    news_block = dom.xpath('//table[@class="daynews__inner"]//a/@href')
    for link in news_block:
        news = {}
        responce_news = requests.get(link, headers=headers)
        dom_news = html.fromstring(responce_news.text)
        news['title'] = dom_news.xpath('//h1/text()')[0]
        news['link'] = link
        news['date'] = dom_news.xpath('//span[@datetime]/@datetime')[0]
        news['source'] = dom_news.xpath('//span[contains(text(), "источник")]/following-sibling::node()/@href')[0]

        news_binary = json.dumps(news).encode('utf-8')
        hash = hashlib.sha3_256(news_binary)
        id = hash.hexdigest()
        news['_id'] = id
        try:
            collection.insert_one(news)
        except Exception:
            continue


def get_yandex_news():
    domain = 'https://yandex.ru/news/'
    responce = requests.get(domain, headers=headers)
    dom = html.fromstring(responce.text)
    news_block = dom.xpath('//article')[:5]
    for item in news_block:
        news = {}
        news['title'] = item.xpath('..//h2/text()')[0].replace('\xa0', ' ')
        news['link'] = item.xpath('..//a/@href')[0]
        news['date'] = item.xpath('..//span[@class="mg-card-source__time"]/text()')[0]
        news['source'] = item.xpath('..//a/text()')[0]

        news_binary = json.dumps(news).encode('utf-8')
        hash = hashlib.sha3_256(news_binary)
        id = hash.hexdigest()
        news['_id'] = id
        try:
            collection.insert_one(news)
        except Exception:
            continue


get_lenta_ru()
get_mail_news()
get_yandex_news()

with open('results.txt', 'w') as file:
    for doc in collection.find({}):
        file.write(f'{str(doc)} \n')
