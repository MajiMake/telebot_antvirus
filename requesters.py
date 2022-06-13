import pprint

import requests
import json


def get_code(username, password):
    print(username, password)
    get_code = requests.get(f'/api/0.1/keys/pass/get/{password}/{username} HTTP/1.1')
    print(get_code.content)






get_list = requests.get('http://37.252.5.91:8989/api/1.0/products?page=1', headers={"Accept": "application/json"})
key_list = json.loads(get_list.content)



