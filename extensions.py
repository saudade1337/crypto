import telebot
import requests
import json
from config import exchanges

class ApiException(Exception):
    pass


class Converter:
    @staticmethod
    def get_price(base, target, amount):
        try:
            base_key = exchanges[base.lower()]
        except KeyError:
            return ApiException(f"Валюта {base} не найдена!")
        try:
            target_key = exchanges[target.lower()]
        except KeyError:
            raise APIException(f"Валюта {target} не найдена!")

        if base_key == target_key:
            raise APIException(f'Невозможно перевести одинаковые валюты {base}!')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать количество {amount}!')

        r = requests.get(f'https://v6.exchangerate-api.com/v6/319ea813432a78bb298f2a85/pair/{base_key}/{target_key}')
        resp = json.loads(r.content)
        new_price = resp['conversion_rate'] * float(amount)
        return round(new_price, 2)

