from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import time
from pprint import pprint
from pymongo import MongoClient
import json
import hashlib

# ЛОГИН В МОНГОБД
client = MongoClient('localhost', 27017)
db = client['email_db']
try:
    collection = db.create_collection('email')
except:
    collection = db.email

# ЗАПУСКАЮ ВЕБДРАЙВЕР
chrome_options = Options()
chrome_options.add_argument('start-maximized')
driver = webdriver.Chrome(options=chrome_options,
                          executable_path='/Users/macbookair/Documents/1 - GeekBrains/data-collection/'
                                          'data-collection/Selenium/chromedriver')
driver.get("https://mail.ru/")

# ЛОГИН
email_input = driver.find_element_by_name('login')
email_input.send_keys('study.ai_172')
email_input.send_keys(Keys.ENTER)

time.sleep(2)
password_input = driver.find_element_by_name('password')
password_input.send_keys('NextPassword172!')
password_input.send_keys(Keys.ENTER)

# СКРОЛЮ И ПОЛУЧАЮ СПИСОК ЭЛЕМЕНТОВ И ССЫЛОК НА ПИСЬМА
# С ПОМОЩЬЮ МНОЖЕСТВА КОНТРОЛИРУЮ КОНЕЦ СКРОЛЛА
link_all = set()
time.sleep(3)
email_list = driver.find_elements_by_class_name('js-tooltip-direction_letter-bottom')
link_list = list(map(lambda el: el.get_attribute('href'), email_list))
link_all = link_all.union(set(link_list))

while True:
    actions = ActionChains(driver)
    actions.move_to_element(email_list[-1])
    actions.perform()

    time.sleep(3)
    email_list = driver.find_elements_by_class_name('js-tooltip-direction_letter-bottom')
    link_list = list(map(lambda el: el.get_attribute('href'), email_list))

    if link_list[-1] not in link_all:
        link_all = link_all.union(set(link_list))
        continue
    else:
        break

#ЗАХОЖУ В ПИСЬМА / ЗАБИРАЮ КОНТЕНТ / СОЗДАЮ ID / ДОБАВЛЯЮ В МОНГО
for href in list(link_all):
    driver.get(href)
    time.sleep(4)
    email_for_mongo_db = {}
    email_for_mongo_db['sender'] = driver.find_element_by_class_name('letter-contact').get_attribute('title')
    email_for_mongo_db['date'] = driver.find_element_by_class_name('letter__date').text
    email_for_mongo_db['title'] = driver.find_element_by_xpath('//h2').text
    email_for_mongo_db['body'] = driver.find_element_by_class_name('letter-body').text

    email_binary = json.dumps(email_for_mongo_db).encode('utf-8')
    hash = hashlib.sha3_256(email_binary)
    id = hash.hexdigest()
    email_for_mongo_db['_id'] = id

    try:
        collection.insert_one(email_for_mongo_db)

    except Exception:
        continue

# ЗАКРЫВАЮ БРАУЗЕР
driver.quit()

# ВЫВОЖУ ЗАПИСИ ИЗ МОНГО В ФАЙЛ
with open('email_results.txt', 'w') as file:
    for doc in collection.find({}):
        file.write(f'{str(doc)} \n')



