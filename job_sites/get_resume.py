from class_modul import VacancyList
import gc

final_list = VacancyList(vacancy_text='web', page=2)

with open('parser_results.txt', 'w') as file:
    file.write(f'Было обработано {final_list.page_count} страниц \n'
               f'Всего вакансий: {final_list.vacancy_count}\n'
               f'{"-" * 20}\n')

    for vacancy in final_list.all_vacancy:
        file.write(f'{vacancy.domain} | {vacancy.name} | {vacancy.min_salary}-{vacancy.maх_salary}-{vacancy.currency}\n'
                   f'{vacancy.link}\n'
                   f'{"-" * 20}\n')
gc.collect()
