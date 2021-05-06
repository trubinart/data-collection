import requests
import json
from config import settings

token = settings.GITHUB_TOKEN
url = 'https://api.github.com/user/repos'
token_headers = {'Authorization': 'token ' + token}
get_repo = requests.get(url, headers=token_headers)
repo_lists = {}

if get_repo.ok:
    for repo in get_repo.json():
        repo_lists[repo['id']] = repo['name']
else:
    print(get_repo.status_code)

with open('repo_lists.json', 'w') as file:
    json.dump(repo_lists, file)