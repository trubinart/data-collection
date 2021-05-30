import scrapy
from urllib.parse import urlencode
from bs4 import BeautifulSoup as bs
import re
from scrapy_jobparser.items import ScrapyJobparserItem


class SuperjobSpider(scrapy.Spider):
    name = 'superjob'
    allowed_domains = ['superjob.ru']

    params = {'clusters': 'true',
              'keywords': 'Посудомойщик',
              'page': 0
              }
    url = 'https://www.superjob.ru/vacancy/search/?' + urlencode(params)
    start_urls = [url]

    def parse(self, responce):
        dom = bs(responce.text, 'html.parser')
        vacancy_link = dom.find_all('a', {'class': re.compile('icMQ_ _6AfZ9')})
        vacancy_link = list(map(lambda item: 'https://www.superjob.ru' + item['href'], vacancy_link))

        for item in vacancy_link:
            yield responce.follow(item, callback=self.get_resume)

        domain = 'https://www.superjob.ru/'
        next_link = dom.find('a', text='Дальше')['href']

        if next_link != None:
            next_page = domain + next_link
            yield responce.follow(next_page, callback=self.parse)

    def get_resume(self, responce):
        dom = bs(responce.text, 'html.parser')
        domain = self.name
        link = responce.url
        name = dom.find('h1').text
        salary_string = dom.find('span', {'class': '_1h3Zg _2Wp8I _2rfUm _2hCDz'}).text
        salary_list = salary_string.split()

        if salary_list[0] == 'до':
            min_salary = None
            maх_salary = int(salary_list[1] + salary_list[2])
            currency = salary_list[3].replace('.', '')

        elif salary_list[0] == 'от':
            min_salary = int(salary_list[1] + salary_list[2])
            maх_salary = None
            currency = salary_list[3].replace('.', '')

        elif salary_list[0].isdigit() and salary_list[2] == '-':
            min_salary = int(salary_list[0] + salary_list[1])
            maх_salary = int(salary_list[3] + salary_list[4])
            currency = salary_list[5].replace('.', '')

        elif salary_list[0].isdigit():
            min_salary = None
            maх_salary = int(salary_list[0] + salary_list[1])
            currency = salary_list[2].replace('.', '')

        elif salary_string.find('По договорённости') != -1:
            min_salary = None
            maх_salary = None
            currency = None

        yield ScrapyJobparserItem(domain=domain,
                                  link=link,
                                  name=name,
                                  min_salary=min_salary,
                                  maх_salary=maх_salary,
                                  currency=currency, )
