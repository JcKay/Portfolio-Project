from twilio.rest import Client
import os

class TwilioSMS:
    def __init__(self):
        self.account_sid = os.environ['ACCOUNT_SID']
        self.auth_token = os.environ['AUTH_TOKEN']
        self.twillo_phone = os.environ['TWILIO_PHONE']
        self.my_phone = os.environ['MY_PHONE']

    def send_now(self, body_message):
        """ send_now : to send sms from Twilio SMS Service"""
        client = Client(self.account_sid, self.auth_token)
        message = client.messages \
            .create(
            body=body_message,
            from_=self.twillo_phone,
            to=self.my_phone
        )
        print(message.status)
