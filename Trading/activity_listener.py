import requests

from Custom_huobi_Python.huobi.client.trade import TradeClient
from Custom_huobi_Python.huobi.client.market import MarketClient
from Custom_huobi_Python.huobi.constant.definition import *

from Account_Info.account_info import get_bal_for_coins, get_acc_client, get_acc_id
from Trading.trader import *
import json

CONFIG = json.load(open("../Configs/secret.json"))
ACCESS_KEY = CONFIG["ACCESS_KEY"]
SECRET_KEY = CONFIG["SECRET_KEY"]


trader = Trader(ACCESS_KEY, SECRET_KEY)

trigger_curreny = 'btcusdt'
trigger_price = 50000
pc_coins_to_sell = 0.9
coin_sheet = ['adausdt', 'btc3lusdt', 'dogeusdt', 'eth3lusdt', 'htusdt', 'linausdt', 'xrpusdt', 'yfiusdt']
coins = [i.replace('usdt', '') for i in coin_sheet]
print(coins)
coin_dict = trader.get_coin_amt(coins, 0.8)


while True:
    for coin, amt in coin_dict.items():
        try:
            # The selling mechanism should be here. If it fails, will go to except statement
            if amt <= 5:
                raise Exception()
            print(f'Sold {amt} {coin}')
        except:
            print(f'{coin} could not be sold')
    break

# if trader.get_coin_price(trigger_curreny) < trigger_price:
    # trader.market_order(coin, type='sell', amount_to_trade=)


order_dict = {}

run = False
run_sure = False
# COIN = 'mdsusdt'
AMOUNT = 1300
PC_TO_BUY = 13
PC_PROFIT = 45
LIMIT_SELL = True

# Run = Run the programme
# COIN = Coin to trade
# AMOUNT = Amount of coins to trade
# PC_TO_BUY = Percentage increase before market buying coin (Not in decimal, the percentage itself; i.e 13 if you want 13%)
# PC_PROFIT = Percentage increase before selling
# LIMIT_SEL = True if you want to immediately place a limit_sell after buying. False if you want to make a market sell (Python Will listen until sold)

PC_TO_BUY /= 100
PC_PROFIT /= 100

while run and run_sure:
    try:
        x = trader.get_pc_change(COIN)
        print(x)
        # Keep running until you buy
        if x >= PC_TO_BUY:
            trader.profit(COIN, AMOUNT, PC_PROFIT, limit_sell=LIMIT_SELL)
            print(order_dict["buy_price"])
            print(f'BOUGHT {AMOUNT} {COIN} at ${order_dict["buy_price"]}')
            # If it is a market sell
            if not LIMIT_SELL:
                print(f'Selling at {order_dict["buy_price"]*(1+PC_PROFIT)}...')
                while True:
                    try:
                        x = trader.get_pc_change(COIN)
                        if x >= PC_PROFIT:
                            trader.make_order(acc_id, symbol=COIN, amount=AMOUNT*0.97, price=0, type='SELL_MARKET')
                            print('SOLD! ')
                            break
                    except:
                        continue
            run = False
            break
    except Exception as err:
        print(err)
        print('Next')

# t = 0
# r = 50
# for i in range(r):
#     start = time.time()
#     x = get_pc_change()
#     print(x)
#     diff = time.time()-start
#     t += diff



# while True:
#     for i in coins:
#         x = get_pc_change(symbol=i)
#         print(x)
# # Current
# print(x[0]['close'])
