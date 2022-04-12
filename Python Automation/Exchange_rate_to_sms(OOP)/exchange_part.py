import requests
import os
from datetime import date


class ExchangePart:

    def __init__(self):
        self.today = date.today().strftime("%d/%m/%Y")
        self.API_KEY = os.environ['API_KEYS']
        url = 'http://api.currencylayer.com/live'
        self.base = ""
        self.body_message = [f"{self.today} Exchange rate -"]

    def exchage_rate(self, exchage_code, base_currency):
        return base_currency / exchage_code

    def fix_use(self):
        """ fix_use : return list of currencies code
        example : ['GBP', 'EUR', 'USD'] """

        self.base = "MMK"  # change your base currency
        self.to_me = "GBP,EUR,USD,AUD,CNY,JPY,KRW"  # change as you want
        self.to_me_list = list(self.to_me.split(","))
        return self.to_me_list

    def fix_use_currencies(self):
        """ fix_use_currencies : return dictionary of code and currency exchange
        example : {'USDMMK': 1851}"""

        self.data = requests.get(
            f"http://api.currencylayer.com/live?access_key={self.API_KEY}&currencies={self.base},{self.to_me}&format=1").json()
        return self.data['quotes']

    def custom_use(self):
        """ fix_use : return list of currencies code
                example : ['GBP', 'EUR', 'USD'] """

        self.base = input("Source Currency Code : ")
        print("Can input multiple code using comma")
        print("example: USD,EUR,GBP,KRW,JPY,CNY,CHF,CAD,AUD,NZD,ZAR")
        self.exchange_to = input(f"Currency Code to Exchage : ")
        self.exchange_to_list = list(self.exchange_to.split(","))
        return self.exchange_to_list

    def custom_use_currencies(self):
        """ fix_use_currencies : return dictionary of code and currency exchange
                example : {'USDMMK': 1851}"""

        data = requests.get(
            f"http://api.currencylayer.com/live?access_key={self.API_KEY}&currencies={self.base},{self.exchange_to}&format=1").json()
        quotes = data['quotes']
        return quotes

    def exchange_currency(self, exchanged, code_list):
        quotes = exchanged
        source = quotes[f'USD{self.base}']
        header = f"OTR : {self.base}"
        self.body_message.append(header)
        for code in code_list:
            rate = quotes[f'USD{code}']
            changed_rate = self.exchage_rate(rate, source)
            output = f"{code} : {round(changed_rate, 2)}"
            self.body_message.append(output)
