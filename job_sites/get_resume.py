from class_modul import VacancyList
import gc
from pymongo import MongoClient
import hashlib
import json
from pprint import pprint
from function_module import vacancy_filter_by_salary

# ЗАПИСЬ В ФАЙЛ
# final_list = VacancyList(vacancy_text='web', page=2)
#
# with open('parser_results.txt', 'w') as file:
#     file.write(f'Было обработано {final_list.page_count} страниц \n'
#                f'Всего вакансий: {final_list.vacancy_count}\n'
#                f'{"-" * 20}\n')
#
#     for vacancy in final_list.all_vacancy:
#         file.write(f'{vacancy.domain} | {vacancy.name} | {vacancy.min_salary}-{vacancy.maх_salary}-{vacancy.currency}\n'
#                    f'{vacancy.link}\n'
#                    f'{"-" * 20}\n')
# gc.collect()


# ЗАПИСЬ В MONGODB
client = MongoClient('localhost', 27017)
db = client['vacancy_db']

try:
    collection = db.create_collection('vacancy')
except:
    collection = db.vacancy

final_list = VacancyList(vacancy_text='повар', page=1)

for vacancy in final_list.all_vacancy:
    vacancy_for_mongo = {
        'name': vacancy.name,
        'domain': vacancy.domain,
        'link': vacancy.link,
        'min_salary': vacancy.min_salary,
        'maх_salary': vacancy.maх_salary,
        'currency': vacancy.currency,
    }
    vacancy_for_mongo_binary = json.dumps(vacancy_for_mongo, ).encode('utf-8')
    hash = hashlib.sha3_256(vacancy_for_mongo_binary)
    id = hash.hexdigest()

    vacancy_for_mongo['_id'] = id

    try:
        collection.insert_one(vacancy_for_mongo)
    except Exception:
        continue

for doc in collection.find({}):
    pprint(doc)

vacancy_filter_by_salary(150000, collection)