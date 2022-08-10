import json
import re

import requests


class RequestToApi(object):

    def __init__(self, url: str, auth: tuple = ('connexio@praesens.ru', 'uuD-mGY-VDj-69m')):
        self.url = url
        self.login = auth[0]
        self.password = auth[1]
        self.response = self.get_response()
        self.status_code = self.response.status_code
        self.json = self.get_json()
        self.results = self.get_results()

    def get_response(self):
        return requests.get(self.url, auth=(self.login, self.password))

    def get_json(self):
        if self.status_code == 200:
            return self.response.json()

    def get_results(self):
        if self.status_code == 200:
            return self.json['results'] if 'results' in self.json else None


def formatting_phone(phone: str) -> str:
    phone_without_pass = ''.join(filter(str.isdigit, phone))
    if phone_without_pass.__len__() == 11:
        return f'+{7} ({phone_without_pass[1:4]}) {phone_without_pass[4:7]} {phone_without_pass[7:9]} {phone_without_pass[9:11]}'
    elif phone_without_pass.__len__() == 12:
        return f'+{7} ({phone_without_pass[1:5]}) {phone_without_pass[5:8]} {phone_without_pass[8:10]} {phone_without_pass[10:12]}'
    else:
        return phone


def html_to_text(html: str) -> str:
    """Вырезание тегов html"""
    return re.sub('</?[^>]+>', '', html)


def formatting_query_param(param: str) -> list:
    """Преобразует строковый json из str в валидный json объект"""
    param = param.replace("\'", "\"")
    param = param.replace("None", "null")
    return json.loads(param)


def formatting_phone(phone: str) -> str:
    phone_without_pass = ''.join(filter(str.isdigit, phone))
    # телефон в формате ххх-ххх-хх-хх
    if phone_without_pass.__len__() == 10:
        return f'+{7} ({phone_without_pass[0:3]}) {phone_without_pass[3:6]} {phone_without_pass[6:8]} {phone_without_pass[8:10]}'
    # телефон в формате +7-ххх-ххх-хх-хх или 8-ххх-ххх-хх-хх
    elif phone_without_pass.__len__() == 11:
        return f'+{7} ({phone_without_pass[1:4]}) {phone_without_pass[4:7]} {phone_without_pass[7:9]} {phone_without_pass[9:11]}'
    # телефон в формате +7-хххх-ххх-хх-хх или 8-хххх-ххх-хх-хх
    elif phone_without_pass.__len__() == 12:
        return f'+{7} ({phone_without_pass[1:5]}) {phone_without_pass[5:8]} {phone_without_pass[8:10]} {phone_without_pass[10:12]}'
    else:
        return phone
