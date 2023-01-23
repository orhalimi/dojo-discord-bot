''' this interface created to mediate between django and our bot '''

import json
import requests
from requests.auth import HTTPBasicAuth

AUTH = {"username": "admin", "password": "admin4"}

ADDRESS = "http://46.101.46.130/api/"


class Core:
    ''' encapsulate all functionality into one class '''

    def __init__(self):
        self.auth = HTTPBasicAuth(AUTH["username"], AUTH["password"])

    def exist(self, endpoint: str, record_id: int) -> bool:
        ''' recive table name and id and return if the record is exist in db '''

        url = f'{ADDRESS}{endpoint}/'
        response = requests.get(url)
        json_data = json.loads(response.text)

        for index, record in enumerate(json_data):
            if record_id == record["id"]:
                return True

        return False

    def post(self, endpoint: str, obj: tuple) -> bool:
        ''' recive table name and data and return if the record is posted secssefuly in db'''

        url = f'{ADDRESS}{endpoint}/'
        response = requests.post(url, data=obj, auth=self.auth)
        print(f'response: {response}')
        print(f"POST: to {endpoint} status code:", response.status_code)

        if response.status_code == 400:
            print('post func failed')

        return response.ok

    def update(self, endpoint: str, obj: tuple, record_id) -> bool:
        ''' recive table name and data as tuple and return if the record is updated secssefuly'''

        url = f'{ADDRESS}{endpoint}/{record_id}/'
        response = requests.put(url, data=obj, auth=self.auth)
        print(f"PUT: to {record_id} in {endpoint} status code:", response.status_code)
        if response.status_code == 400:
            print(response.text)
        return response.ok

    def get(self, endpoint) -> dict:
        ''' return the fully response for now! '''
        url = f'{ADDRESS}{endpoint}'
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
