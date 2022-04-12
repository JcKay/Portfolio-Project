import time
from datetime import datetime
from exchange_part import ExchangePart
from twilio_sms import TwilioSMS

while True:
    ## ------- Get TIME -------- ##
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print("\r", "Current Time =", current_time, end="")

    ## WHEN THE TIME RIGHT!
    if current_time == "22:51:30":

        ## ------- Exchange Currency -------- ##
        # Create ExchangePart Object
        exchangePart = ExchangePart()
        codes = exchangePart.fix_use()
        quotes = exchangePart.fix_use_currencies()
        exchange = exchangePart.exchange_currency(quotes, codes)
        body_message = "\n".join(exchangePart.body_message)
        print(f"\n{body_message}")
        time.sleep(2)

        # -------- Send SMS -------- ##
        sms = TwilioSMS()
        sms.send_now(body_message)