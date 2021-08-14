import os
from huobi.client.generic import GenericClient
from huobi.utils import *
import datetime
import yagmail
import time
import datetime
import json

CONFIG = json.load(open("../Configs/secret.json"))

#Get today's date
date_object = datetime.date.today()

#Get current hour
now = datetime.datetime.now()
now_hour = now.hour

#Huobi Client
generic_client = GenericClient()
list_obj = generic_client.get_exchange_currencies()

current_no_coins = len(list_obj)

#For first time creation of noCoins.txt
if not os.path.exists('/venv/noCoins.txt'):
# Use this for the Ubuntu Server
# if not os.path.exists('/root/Huobi-bot/noCoins.txt'):
    print(f'First time writing to file')
    with open('/venv/noCoins.txt', 'w') as file:
        file.write(str(current_no_coins))
    print(f'File initialized with value {current_no_coins}')

#Get the previous number of coins (1 Hour previously)
fl = open('Files/noCoins.txt', 'r').read()
prev_no_coin = int(fl)

EMAIL_ADDR = CONFIG["BOT_EMAIL"]["EMAIL_ADDRESS"]
EMAIL_PASSR = CONFIG["BOT_EMAIL"]["PASSWORD"]

yag = yagmail.SMTP(EMAIL_ADDR, EMAIL_PASSR)

#If there are new coins
if current_no_coins != prev_no_coin:
    #Send email
    new_coin = list_obj[-1]
    content = f'New Coin is {new_coin} \n https://www.huobi.com/en-us/exchange/{new_coin}_usdt'

    users = CONFIG["NEW_COINS_EMAILS"]

    for user in users:
        yag.send(to=user, subject='New Huobi Coin Listing', contents=content)

    print('Mail Sent')
    #Update the new number of coins to be the current number
    with open('/venv/noCoins.txt', 'w') as file:
        file.write(str(current_no_coins))	
    print(f'Written value {current_no_coins} to file')

else:
    print('No Mail has to be sent')
    print(f'Current coins is {current_no_coins}')
    #Will auto send update at 9am
    if now_hour == 9:
        yag.send(to=CONFIG["DEV_EMAIL"], subject='Huobi bot is still up!', contents='I"m still here')


def is_time_between(begin_time, end_time, check_time=None):
    # If check time is not given, default to current UTC time
    check_time = check_time or datetime.utcnow().time()
    if begin_time < end_time:
        return check_time >= begin_time and check_time <= end_time
    else: # crosses midnight
        return check_time >= begin_time or check_time <= end_time

# Original test case from OP

now = datetime.datetime.now()
now_hour = now.hour

if now_hour == 9:
    print('yes')

