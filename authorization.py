import requests
from config import settings

# ПОЛУЧАЕМ CRF_TOKEN
url = 'https://po-polochkam.ru/login'
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'
}
username = settings.POPOLOCHKAM_USERNAME
password = settings.POPOLOCHKAM_PASSWORD


my_session = requests.session()
get_token = my_session.get(url, headers=headers)

csrf_token = get_token.text[1901:1944]
print(csrf_token)

# ЛОГИНИМСЯ
user_data = {'username': username, 'password': password, '_csrf_token': csrf_token}
url_2 = 'https://po-polochkam.ru/check'
try_access = my_session.post(url_2, data=user_data, headers=headers)
print(try_access.status_code)

# ЗАХОДИМ НА СТРАНИЦУ ДОКУМЕНТОВ
documents_control = my_session.get('https://po-polochkam.ru/document-sets-uploading?page=1')
print(documents_control.text)
