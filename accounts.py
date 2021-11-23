import os
import jwt
import uuid
import hashlib
from urllib.parse import urlencode

import requests

access_key = os.environ["TlKLmK7jp8apGBVlKLbYyrQJjpJJsK2MJc1ZSNSC"]
secret_key = os.environ['AefE6iuSNwdyEvP5a85d2B4TkO3Fhbx0iXpCLapw']
server_url = os.environ['https://api.upbit.com/v1/']

payload = {
    'access_key': access_key,
    'nonce': str(uuid.uuid4()),
}

jwt_token = jwt.encode(payload, secret_key)
authorize_token = 'Bearer {}'.format(jwt_token)
headers = {"Authorization": authorize_token}

res = requests.get(server_url + "/v1/accounts", headers=headers)

print(res.json())