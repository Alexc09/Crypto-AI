import asyncio

import requests
from datetime import datetime, timedelta
import hashlib
import hmac
import base64
import urllib

from Custom_huobi_Python.huobi.client.account import AccountClient, AccountBalance
from Custom_huobi_Python.huobi.client.trade import TradeClient
from Custom_huobi_Python.huobi.client.market import MarketClient
from Custom_huobi_Python.huobi.client.wallet import WalletClient
from Custom_huobi_Python.huobi.constant.definition import *
from Custom_huobi_Python.huobi.constant.system import *
import json
# from Custom_huobi_Python.huobi.

CONFIG = json.load(open("../Configs/secret.json"))
ACCESS_KEY = CONFIG["ACCESS_KEY"]
SECRET_KEY = CONFIG["SECRET_KEY"]

trade_client = TradeClient(api_key=ACCESS_KEY, secret_key=SECRET_KEY, url="https://api-aws.huobi.pro")
market_client = MarketClient()
acc = AccountClient(api_key=ACCESS_KEY, secret_key=SECRET_KEY)


class Trader():
    def __init__(self, api_key, secret_key):
        self.api_key = api_key
        self.secret_key = secret_key
        self.acc


def get_acc_id(api_key, secret_key, type='all'):
    acc = AccountClient(api_key=api_key, secret_key=secret_key)
    for i in acc.get_accounts():
        if type == 'all':
            i.print_object()
        else:
            if i.type == type:
                return i.id


def get_acc_client(api_key, secret_key):
    return AccountClient(api_key=api_key, secret_key=secret_key)


def print_bal(bal_list):
    for i in bal_list:
        # Type 'frozen' means it is currently on orders, so you can't touch it (I.e you placed it on SellLimit order)
        print(f'Currency: {i["Currency"]}')
        print(f'Amount: {i["Amt"]}')
        print(f'Type: {i["Type"]}')
        print('\n')


def combine_bal(bal_list):
    # Combines the Frozen and Trade type of currencies
    updated_d = {}
    for i in bal_list:
        if i["Currency"] in updated_d:
            updated_d[i['Currency']]['Amt'] = float(updated_d[i['Currency']]['Amt']) + float(i['Amt'])
            # updated_d[i['Currency']] = updated_d[i['Currency']] + i['Currency']
        # If it doesnt exist yet
        else:
            updated_d[i["Currency"]] = {'Currency': i['Currency'], 'Amt': i['Amt']}

    return updated_d


ACC_ID = get_acc_id(type='spot', api_key=ACCESS_KEY, secret_key=SECRET_KEY)


def show_bal_dict(bal_list):
    bal_dict = combine_bal(bal_list)
    for i in bal_dict:
        try:
            bal_dict[i]['Price'] = market_client.get_market_detail(f'{bal_dict[i]["Currency"]}usdt').close
            bal_dict[i]['Total'] = (bal_dict[i]["Price"]) * bal_dict[i]["Amt"]
        except:
            print(f'Error: {bal_dict[i]["Currency"]}')
            bal_dict[i]['Price'] = 0
            bal_dict[i]['Total'] = (bal_dict[i]["Price"]) * bal_dict[i]["Amt"]

    for i in bal_dict:
        print(bal_dict[i])


def get_bal_for_coins(account_client, coin_list):
    bal_list = account_client.get_account_balance_custom()
    coins = [i for i in bal_list if i['Currency'] in coin_list]
    coins = [i for i in coins if i['Type'] == 'trade']
    return coins


# Limit is the amount of coins you must have at least in order to print its output
if __name__ == '__main__':
    x = get_bal_for_coins(acc, ['fil', 'eth'])
    print(x)
