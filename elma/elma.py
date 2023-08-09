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
        out = json.loads(r.content)
        print("new AuthToken: ", out['AuthToken'], "\nnew SessionToken: ", out['SessionToken'], "\n")
        self.AuthToken = out['AuthToken']
        self.SessionToken = out['SessionToken']

    def elma_requests_QueryTree(self, typeuid, eql, select):
        r = requests.get(f'https://elma.eriskip.com/API/REST/Entity/QueryTree?'
                         f'type={typeuid}&q={eql}&select={select}',
                         headers={'SessionToken': self.SessionToken,
                                  'AuthToken': self.AuthToken,
                                  'Content-type': 'application/json'})
        if r.status_code != 200:
            self.auth()
            return self.elma_requests_QueryTree(typeuid, eql, select)
        return parse_response(r.content.decode('utf-8'))


elma = ELMA()


async def elma_get_list_indicators():
    rows = elma.elma_requests_QueryTree('f314b4dc-d36b-4f6f-8d8a-a43a095c1d7d', '', 'Pokazatelj')
    indicators = []
    for row in rows:
        indicators.append(str(row['Items'][2]['DataArray'][0]['Items'][4]['Value']).title())

    unique_numbers = list(set(indicators))
    return unique_numbers


async def elma_get_info_about_indicator(name_indicator):
    eql = f"Pokazatelj in (FROM PokazateliGKERIS_Pokazatelj SELECT Id WHERE Nazvanie LIKE ’{name_indicator}’)"
    rows = elma.elma_requests_QueryTree('f314b4dc-d36b-4f6f-8d8a-a43a095c1d7d', eql, 'YurLico,Tip,Summa')
    out = []
    for row in rows:
        tip = row['Items'][3]['Value']
        summa = split_float_into_triads(float(row['Items'][2]['Value']))
        yurlico = row['Items'][4]['Data']['Items'][3]['Value']

        out.append([yurlico, tip, summa])
    return out


def split_float_into_triads(number):
    # Преобразуем число в строку и разделяем на целую и дробную части
    integer_part, decimal_part = str(number).split('.')

    # Разбиваем целую часть на триады, начиная справа
    integer_triads = []
    while integer_part:
        triad = integer_part[-3:]  # Берем последние три символа
        integer_part = integer_part[:-3]  # Убираем последние три символа
        integer_triads.insert(0, triad)  # Вставляем triad в начало списка

    # Собираем результат в строку с разделителем ','
    result = ','.join(integer_triads)

    # Если есть дробная часть, добавляем ее в результат
    if decimal_part != '0':
        result += '.' + decimal_part

    return result
