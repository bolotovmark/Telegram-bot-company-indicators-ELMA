import json
import requests
import os

from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv


class DictWithAttributeAccess(dict):
    def __getattr__(self, key):
        return self[key]

    def __setattr__(self, key, value):
        self[key] = value


def parse_response(response):
    return json.loads(response, object_hook=lambda dictionary: DictWithAttributeAccess(dictionary))


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

    def elma_requests_QueryTree(self, typeuid, eql, select):
        r = requests.get(f'https://elma.eriskip.com/API/REST/Entity/QueryTree?'
                         f'type={typeuid}&q={eql}&select={select}',
                         headers={'SessionToken': self.SessionToken,
                                  'AuthToken': self.AuthToken,
                                  'Content-type': 'application/json'})
        print(r.status_code)
        if r.status_code != 200:
            self.auth()
            return self.elma_requests_QueryTree(typeuid, eql, select)
        return parse_response(r.content.decode('utf-8'))


elma = ELMA()
out = elma.elma_requests_QueryTree('7414f89e-b840-4137-8256-3ad2c6213816',
                                   "Name = ’Выручка, без НДС’",
                                   "Name,Summa,Kommentariy")
print(out[0].Items[2].Value, out[0].Items[3].Value, out[0].Items[4].Value)
