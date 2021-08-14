import requests
from datetime import datetime, timedelta
import hashlib
import hmac
import base64
import urllib
import time


def get_klines(period='1min', size='2000', symbol='ethusdt'):
    klines_json = requests.get(f'https://api.huobi.pro/market/history/kline?period={period}&size={size}&symbol={symbol}').json()
    klines = klines_json['data']
    return klines






