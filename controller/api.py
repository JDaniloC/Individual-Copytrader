import requests, json

arquivo = open("./config/data.json")
class Api:
    config = json.load(arquivo)
    main_url = f"http://{config.get('ip')}:5000/{config.get('id')}/"

    @staticmethod
    def write(content):
        req = requests.post(Api.main_url, 
            data = json.dumps(content), headers = {
                'Content-Type': 'application/json'
            })
        return req.json()
    
    @staticmethod
    def read():
        return requests.get(Api.main_url).json()
arquivo.close()
