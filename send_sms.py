import os
import logging
import requests
import time
from twilio.rest import Client
from dotenv import load_dotenv

logging.basicConfig(filename='.log', format='%(levelname)s %(asctime)s %(message)s')

load_dotenv()

TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
TWILIO_NUMBER = os.getenv('TWILIO_NUMBER')
MY_NUMBER = os.getenv('MY_NUMBER')
URL = os.getenv('URL')
client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

def status_check():
    response = requests.get(URL)
    if response.status_code == 200:
        logging.info('Service is available')
        time.sleep(60)
        status_check()
    elif response.status_code == 404 or 400 or 403 or 409:
        logging.info('Service is unavailable')
        time.sleep(60)
        status_check()
        client.messages.create(
            body='Service is unavailable',
            from_=TWILIO_NUMBER,
            to=MY_NUMBER
            )
    elif response.status_code == 500:
        logging.info('Internal Server Error')
        time.sleep(60)
        status_check()
