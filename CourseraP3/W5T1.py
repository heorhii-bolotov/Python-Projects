import base64
from requests import post, put


URL = "http://79.137.175.13/"
USER_NAME = 'alladin'
PASSWORD = 'opensesame'

res = post(f'{URL}submissions/1/', auth=(USER_NAME, PASSWORD)).json()
res = put(f'{URL}{res.get("path")}', auth=(res.get("login"), res.get("password"))).json().get('answer')

with open('/Users/macair/Desktop/f.txt', 'w') as file:
    file.write(res)

