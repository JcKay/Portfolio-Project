#!/usr/bin/python3

import os
import requests
from twilio.rest import Client
from datetime import date

## ------- Get Date -------- ##
today = date.today().strftime("%d/%m/%Y")

## ------- Top Layer Code ------- ##
## Fix Use for Cronjob 👇🏻 Uncomment Below
base = "MMK"                                 # change your base currency
to_me = "GBP,EUR,USD,AUD,KRW,JPY,CNY"        # change as you want
to_me_list = list(to_me.split(","))
## For Custom Use 👇🏻 Uncomment Below
# base = input("Source Currency Code : ")
# print("Can input multiple code using comma")
# print("example: USD,EUR,GBP,KRW,JPY,CNY,CHF,CAD,AUD,NZD,ZAR")
# exchange_to = input(f"Currency Code to Exchage : ")
# exchange_to_list = list(exchange_to.split(","))

## -------------- METHOD 2 ------------------ ##
API_KEY = os.environ['API_KEYS']
url = 'http://api.currencylayer.com/live'

data = requests.get(
    f"http://api.currencylayer.com/live?access_key={API_KEY}&currencies={base},{to_me}&format=1").json() # Change | exchange_to / to_me


quotes = data['quotes']
# print(f"From 1 currency of {exchange_to} to {base}")

source = quotes[f'USD{base}']


def excange_rate(exchange_code, base_currency=source):
    return base_currency / exchange_code


body_message = [f"{today} Exchange rate -\nOTR : {base}"]

for code in to_me_list:           # comment/uncomment upon you used (Fix Use)
# for code in exchange_to_list:       # comment/uncomment upon you used (Custom Use)
    rate = quotes[f'USD{code}']
    changed_rate = excange_rate(rate)
    output = f"{code} : {round(changed_rate, 2)}"
    body_message.append(output)

body_message = "\n".join(body_message)
print(body_message)                 # comment to no output

## ------------- PART 2 - SEND SMS USING TWILIO ------------- ##
## NO SEND SMS, COMMENT BELOW 👇🏻 ##
account_sid = os.environ['ACCOUNT_SID']
auth_token = os.environ['AUTH_TOKEN']
twillo_phone = os.environ['TWILIO_PHONE']
my_phone = os.environ['MY_PHONE']

client = Client(account_sid, auth_token)
message = client.messages \
    .create(
    body=body_message,
    from_=twillo_phone,
    to=my_phone
)
print(message.status)
