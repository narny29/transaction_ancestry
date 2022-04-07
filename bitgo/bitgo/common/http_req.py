import requests
import json

class HttpReq:
    def get(self, url, is_json_body=False):
        try:
            response = requests.get(url)
            status_code = response.status_code
            if status_code!=200:
                raise Exception("get call failed")

            if is_json_body:
                return json.loads(response.content)
            else: return response.content.decode('UTF-8')
        except:
            print("couldn't get data for the url: %s" % url)
