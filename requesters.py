import pprint

import requests
import json


def get_code(username, password):
    get_code = requests.get(f'http://37.252.5.91:8989/api/0.1/keys/pass/get/{password}/{username}')
    return get_code.content

def buy_key(productUUID, telegramUserID):
    key = requests.get(f'http://37.252.5.91:8989/api/0.1/keys/buy/{productUUID}/{telegramUserID}')
    return key.content

def add_key(keys):
    requests.post('http://37.252.5.91:8989/api/0.1/keys/add', data=keys)





get_list = requests.get('http://37.252.5.91:8989/api/1.0/products?page=1', headers={"Accept": "application/json"})
key_list = json.loads(get_list.content)


