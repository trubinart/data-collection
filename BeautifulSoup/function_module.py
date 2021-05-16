from pprint import pprint
import json

def vacancy_filter_by_salary(salary, collection):
    select_search = collection.find({"$or": [{'min_salary': {"$gt": salary}}, {'max_salary': {"$gt": salary}}]})

    with open('filter_salary_results.txt', 'w') as file:
        for doc in select_search:
            file.write(f'{str(doc)} \n')

