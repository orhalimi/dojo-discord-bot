import requests
import json
from requests.auth import HTTPBasicAuth
import logging


class Core:
    def __init__(self):
        self.logger = logging.basicConfig(filename="logs/log.txt", level=logging.DEBUG, format="%(asctime)s | %(message)s")
        self.auth_info = {"username": "shlomi","password": "1"}


    def exist(self, endpoint: str, id: int) -> bool:
        url = f"http://127.0.0.1:8000/api/{endpoint}/"
        response = requests.get(url)
        json_data = json.loads(response.text)
        for index in range(len(json_data)):
            if id == json_data[index]['id']:
                return True
        return False


    def post(self, endpoint: str, obj: tuple) -> bool:
        url = f"http://127.0.0.1:8000/api/{endpoint}/"
        
        response = requests.post(url, data=obj,auth=HTTPBasicAuth(self.auth_info["username"], self.auth_info["password"]))
        print(f"POST: to {endpoint} status code:", response.status_code)
    
        if response.status_code == 400:
            print(response.text)
        return response.ok

    def update(self,endpoint:str,obj:tuple,profile_number) -> bool:
        url = f"http://127.0.0.1:8000/api/{endpoint}/{profile_number}/"
        response = requests.put(url,data=obj,auth=HTTPBasicAuth(self.auth_info["username"], self.auth_info["password"]))
        print (f'PUT: to {profile_number} in {endpoint} status code:', response.status_code)
        if response.status_code == 400:
            print(response.text)
        return response.ok

