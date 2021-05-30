import scrapy
from urllib.parse import urlencode
from bs4 import BeautifulSoup as bs
import re
from scrapy_jobparser.items import ScrapyJobparserItem


class HhruSpider(scrapy.Spider):
    name = 'hhru'
    allowed_domains = ['hh.ru']

    params = {'clusters': 'true',
              'area': 1,
              'enable_snippets': 'true',
              'st': 'searchVacancy',
              'text': 'повар',
              'page': 0
              }
    url = 'http://hh.ru/search/vacancy/?' + urlencode(params)
    start_urls = [url]

    def parse(self, responce):
        dom = bs(responce.text, 'html.parser')

        vacancy_link = dom.find_all('a', {'data-qa': re.compile('vacancy-title')})
        vacancy_link = list(map(lambda item: item['href'], vacancy_link))
        for item in vacancy_link:
            yield responce.follow(item, callback=self.get_resume)

        domain = 'http://hh.ru/'
        next_link = dom.find('a', text='дальше')['href']

        if next_link != None:
            next_page = domain + next_link
            yield responce.follow(next_page, callback=self.parse)

    def get_resume(self, responce):
        dom = bs(responce.text, 'html.parser')
        domain = self.name
        link = responce.url
        name = dom.find('h1').text
        salary_string = dom.find('p', {'class': 'vacancy-salary'}).text.replace('\xa0', '')
        salary_list = salary_string.split()

        if salary_string.find('вычета') != -1:
            min_salary = int(salary_list[1])
            maх_salary = None
            currency = salary_list[2].replace('.', '')

        elif salary_string.find('от') != -1 and salary_string.find('до') != -1:
            min_salary = int(salary_list[1])
            maх_salary = int(salary_list[3])
            currency = salary_list[4].replace('.', '')

        elif salary_string.find('от') != -1:
            min_salary = int(salary_list[1])
            maх_salary = None
            currency = salary_list[2].replace('.', '')

        elif salary_string.find('до') != -1:
            min_salary = None
            maх_salary = int(salary_list[1])
            currency = salary_list[2].replace('.', '')

        elif salary_string.find('з/п не указана') != -1:
            min_salary = None
            maх_salary = None
            currency = None

        yield ScrapyJobparserItem(domain=domain,
                                  link=link,
                                  name=name,
                                  min_salary=min_salary,
                                  maх_salary=maх_salary,
                                  currency=currency, )
