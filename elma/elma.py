import json
import requests
import os

from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv


class ELMA:
    ELMA_LOGIN = ''
    ELMA_PASSWORD = ''
    ELMA_API_TOKEN = ''
    AuthToken = ''
    SessionToken = ''

    def __init__(self):
        load_dotenv()
        self.ELMA_LOGIN = os.getenv("ELMA_LOGIN")
        self.ELMA_PASSWORD = os.getenv("ELMA_PASSWORD")
        self.ELMA_API_TOKEN = os.getenv("ELMA_API_TOKEN")
        self.auth()

    def auth(self):
        url = 'https://elma.eriskip.com/API/REST/Authorization/LoginWith?basic=1'

        headers = {'ApplicationToken': self.ELMA_API_TOKEN,
                   'WebData-Version': '2.0',
                   'Content-type': 'application/json'}

        r = requests.get(url, auth=HTTPBasicAuth(self.ELMA_LOGIN, self.ELMA_PASSWORD), headers=headers)
        print("url:", r.url, "\nstatus code: ", r.status_code)
        out = json.loads(r.content)
        print(out['AuthToken'], " ", out['SessionToken'])
        self.AuthToken = out['AuthToken']
        self.SessionToken = out['SessionToken']

    def elma_get_revenue(self):
        r = requests.get(
            'https://elma.eriskip.com/API/REST/Entity/Load?type=7414f89e-b840-4137-8256-3ad2c6213816&id=102',
            headers={'SessionToken': self.SessionToken,
                     'AuthToken': self.AuthToken,
                     'Content-type': 'application/json'})

        print("url:", r.url, "\nstatus code: ", r.status_code)
        out = json.loads(r.content)
        print(out)


elma = ELMA()
