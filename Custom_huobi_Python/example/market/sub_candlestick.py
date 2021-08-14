import time

from huobi.constant import *
from huobi.utils import *

from huobi.client.market import MarketClient
from huobi.constant import *
from huobi.exception.huobi_api_exception import HuobiApiException
from huobi.model.market.candlestick_event import CandlestickEvent


def callback(candlestick_event: 'CandlestickEvent'):
    candlestick_event.print_object()
    print("\n")


def error(e: 'HuobiApiException'):
    print(e.error_code + e.error_message)

market_client = MarketClient()
x = market_client.get_candlestick("grtusdt", CandlestickInterval.DAY1, 3000)
for obj in x:
    print(obj.print_object())
    print(obj.get_close())
    print()

# market_client.sub_candlestick("grtusdt", CandlestickInterval.DAY1, callback, error)



