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
db = client['mvideo_db']
try:
    collection = db.create_collection('new_products')
except:
    collection = db.new_products

# ЗАПУСКАЮ ВЕБДРАЙВЕР
chrome_options = Options()
chrome_options.add_argument('start-maximized')
driver = webdriver.Chrome(options=chrome_options,
                          executable_path='/Users/macbookair/Documents/1 - GeekBrains/data-collection/'
                                          'data-collection/Selenium/chromedriver')
driver.get("https://www.mvideo.ru/")
time.sleep(2)

# ИЩУ КОНТЕЙНЕР и СКРОЛЮ В НЕМУ ЧТОБЫ ПОЯВИЛИСЬ КНОПКИ ПРОКРУТКИ
conteiner = driver.find_elements_by_xpath('//div[@class="gallery-content accessories-new "]')[0]

actions = ActionChains(driver)
actions.move_to_element(conteiner)
actions.perform()
time.sleep(2)

# ЗАБИРАЮ ТОВАРЫ
final_list = []
button = conteiner.find_element_by_xpath('..//a[contains(@class,"next-btn")]')

for i in range(0,5):
    button.click()
    time.sleep(3)

products = conteiner.find_elements_by_xpath('..//a[@class="fl-product-tile-picture fl-product-tile-picture__link"]')
intermediate_list = list(map(lambda el: el.get_attribute('data-product-info'), products))
final_list += intermediate_list

for product in final_list:
    product = product.replace("\n''\t\t\t\t\t", '')
    product = json.loads(product)

    product_binary = json.dumps(product).encode('utf-8')
    hash = hashlib.sha3_256(product_binary)
    id = hash.hexdigest()
    product['_id'] = id

    try:
        collection.insert_one(product)

    except Exception:
        continue

# ЗАКРЫВАЮ БРАУЗЕР
driver.quit()

# ВЫВОЖУ ЗАПИСИ ИЗ МОНГО В ФАЙЛ
with open('mvideo_results.txt', 'w') as file:
    for doc in collection.find({}):
        file.write(f'{str(doc)} \n')




