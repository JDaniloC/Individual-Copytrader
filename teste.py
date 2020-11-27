import requests, json

res = requests.post("http://34.69.19.239:8000/", 
    data=json.dumps({"orders": [{"asset": "USDJPY", "order":"PUT"}]}))
res = requests.get("http://34.69.19.239:8000/")
print(res.text)