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

        headers = {'ApplicationToken': '65FF88E5B87B497CCEE581A5312C0476019098C2F4D161CDC6636C3A63992BBC19B3AA1F00C67'
                                       '54BA9F98E9317A5B5E8F93F51599E545A6C8004446BD7E9FAFD',
                   'WebData-Version': '2.0',
                   'Content-type': 'application/json'}

        r = requests.get(url, auth=HTTPBasicAuth('bolotovmd', '#13678686Az@#'), headers=headers)
        print("url:", r.url, "\nstatus code: ", r.status_code)
        out = json.loads(r.content)
        print(out['AuthToken'], " ", out['SessionToken'])
        self.AuthToken = out['AuthToken']
        self.SessionToken = out['SessionToken']




        # # AuthToken = 'b600bb95-b000-4c27-97d0-b05700dc8c5f'
        # # SessionToken = '55FF673AFDC67FDA7E0E3E55F6FFD340BB504523B333129ACC4DC791B478BE10A82A2E2346DEBFD019611BCE50263E0A5B3CD2AD3CDF0C479D5700412A8D7F1B'
        #
        # r = requests.get(
        #     'https://elma.eriskip.com/API/REST/Entity/Load?type=7414f89e-b840-4137-8256-3ad2c6213816&id=102',
        #     headers={'SessionToken': SessionToken,
        #              'AuthToken': AuthToken,
        #              'Content-type': 'application/json'})
        #
        # print("url:", r.url, "\nstatus code: ", r.status_code)
        # print(r.content.decode())