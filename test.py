
import requests

res = requests.delete("http://127.0.0.1:8000/users/1")

print(res.json())