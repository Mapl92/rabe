import requests
url = 'http://127.0.0.1:8000/get-auth-key'
payload = {'word': 'Rabe'}
response = requests.post(url, json=payload)

print(response.text)