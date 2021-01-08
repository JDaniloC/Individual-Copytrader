import urllib.request as request
import urllib.parse as parse
import json

class Dontpad:
    main_url = "http://dontpad.com/"
    @staticmethod
    def write(page, content):
        url = Dontpad.main_url + page
        data = parse.urlencode(
            {"text" : content})
        data = data.encode("utf-8")
        req = request.Request(url, data)
        with request.urlopen(req) as response:
            timestamp = response.read()
        return timestamp
    
    @staticmethod
    def read(page, full_json=False):
        def read_raw(page):
            with request.urlopen(Dontpad.main_url + page + ".body.json?lastUpdate=0") as response:
                resp = response.read()
            return resp
        content = json.loads(read_raw(page).decode())
        if "body" in content:
            return content["body"] if not full_json else content
        return ""