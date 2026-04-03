import urllib.request
import json

url = "http://localhost:8000/predict"
payload = json.dumps({"description": "The server is down and I am getting 502 errors when I try to login."}).encode('utf-8')
req = urllib.request.Request(url, data=payload, headers={'Content-Type': 'application/json'})

with urllib.request.urlopen(req) as response:
    body = response.read()
    print(json.dumps(json.loads(body), indent=2))
