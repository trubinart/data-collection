from dataclasses import dataclass
import requests
from bs4 import BeautifulSoup as bs
import re


@dataclass
class Vacancy:
    name = str
    domain = str
    link = str
    min_salary = int
    maх_salary = int
    currency = str

    def get_salary_hh(self, salary_string):
        if salary_string.find('от') != -1:
            split_string = salary_string.replace('\u202f', '').split(' ')
            self.min_salary = split_string[1]
            self.maх_salary = None
            self.currency = split_string[2].replace('.', '')

        elif salary_string.find('до') != -1:
            split_string = salary_string.replace('\u202f', '').split(' ')
            self.min_salary = None
            self.maх_salary = split_string[1]
            self.currency = split_string[2].replace('.', '')

        else:
            split_string = salary_string.replace('\u202f', '').split(' ')
            self.min_salary = split_string[0]
            self.maх_salary = split_string[2]
            self.currency = split_string[3].replace('.', '')

    def get_salary_superjob(self, salary_string):
        if salary_string.find('По договорённости') != -1:
            self.min_salary = None
            self.maх_salary = None
            self.currency = None

        elif salary_string.find('от') != -1:
            split_string = salary_string.split('\xa0')
            self.min_salary = split_string[1] + split_string[2]
            self.maх_salary = None
            self.currency = split_string[3].replace('.', '')

        elif salary_string.find('до') != -1:
            split_string = salary_string.split('\xa0')
            self.min_salary = None
            self.maх_salary = split_string[1] + split_string[2]
            self.currency = split_string[3].replace('.', '')

        elif len(salary_string.split('\xa0')) == 3:
            split_string = salary_string.split('\xa0')
            self.min_salary = split_string[0] + split_string[1]
            self.maх_salary = None
            self.currency = split_string[2].replace('.', '')

        else:
            split_string = salary_string.split('\xa0')
            self.min_salary = split_string[0] + split_string[1]
            self.maх_salary = split_string[3] + split_string[4]
            self.currency = split_string[5].replace('.', '')

    def __str__(self):
        return f'Вакансия {self.name}'


class VacancyList:
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/90.0.4430.93 Safari/537.36'
    }

    def __init__(self, vacancy_text, page=5):
        self.all_vacancy = []
        self.vacancy_text = vacancy_text
        self.page_count = page
        self.add_hh()
        self.add_superjob()

    def add_vacancy(self, vacancy):
        self.all_vacancy.append(vacancy)

    def add_hh(self):
        domain = 'https://hh.ru'
        url = '/search/vacancy'
        params = {'clusters': 'true',
                  'area': 1,
                  'enable_snippets': 'true',
                  'st': 'searchVacancy',
                  'text': self.vacancy_text,
                  'page': 0
                  }

        for page_number in range(0, self.page_count):
            params['page'] = page_number
            response = requests.get(domain + url, params=params, headers=self.headers)
            dom = bs(response.text, 'html.parser')

            card_list = dom.find_all('div', {'class': 'vacancy-serp-item'})

            for card in card_list:
                vacancy = Vacancy()
                vacancy.name = card.find('a', {'data-qa': 'vacancy-serp__vacancy-title'}).text
                vacancy.domain = domain
                vacancy.link = card.find('a', {'data-qa': 'vacancy-serp__vacancy-title'})['href']

                try:
                    salary = card.find('span', {'data-qa': 'vacancy-serp__vacancy-compensation'}).text
                    vacancy.get_salary_hh(salary)

                except  AttributeError:
                    vacancy.min_salary = None
                    vacancy.maх_salary = None
                    vacancy.currency = None

                self.all_vacancy.append(vacancy)

    def add_superjob(self):
        domain = 'https://www.superjob.ru'
        url = '/vacancy/search/'
        params = {
            'keywords': self.vacancy_text,
            'page': 0
        }

        for page_number in range(0, self.page_count):
            params['page'] = page_number
            response = requests.get(domain + url, params=params, headers=self.headers)
            dom = bs(response.text, 'html.parser')

            card_list = dom.find_all('div', {'class': re.compile('f-test-vacancy-item')})
            for card in card_list:
                vacancy = Vacancy()
                try:
                    vacancy.name = card.find('span', {'class': '_1rS-s'}).text \
                                   + card.find('span', {'class': '_1rS-s'}).next_sibling
                    vacancy.domain = domain
                    vacancy.link = domain + card.find('span', {'class': '_1rS-s'}).parent['href']

                except  AttributeError:
                    vacancy.name = card.find('a', {'class': re.compile('f-test-link')}).text
                    vacancy.domain = domain
                    vacancy.link = domain + card.find('a', {'class': re.compile('f-test-link')})['href']

                try:
                    salary = card.find('span', {'class': 'f-test-text-company-item-salary'}).next.text
                    vacancy.get_salary_superjob(salary)

                except  AttributeError:
                    vacancy.min_salary = None
                    vacancy.maх_salary = None
                    vacancy.currency = None

                self.all_vacancy.append(vacancy)

    def __str__(self):
        return f'Все вакансии {self.all_vacancy}'

    @property
    def vacancy_count(cls):
        return len(cls.all_vacancy)
