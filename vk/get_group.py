import requests
from config import settings
from pprint import pprint
import json

token = settings.VK_TOKEN
method = 'groups.get'
user = settings.VK_USER_ID

url = f'https://api.vk.com/method/{method}?user_id={user}&extended=1&access_token={token}&v=5.130'

get_group = requests.get(url).json()

pprint(get_group)

group_lists = {}

for group in get_group['response']['items']:
    group_lists[group['id']] = group['name']

with open('group_lists.json', 'w') as file:
    json.dump(group_lists, file)