import requests

from Custom_huobi_Python.huobi.client.trade import TradeClient
from Custom_huobi_Python.huobi.client.market import MarketClient
from Custom_huobi_Python.huobi.constant.definition import *

from Account_Info.account_info import get_bal_for_coins, get_acc_id, get_acc_client


class Trader():
    def __init__(self, api_key, secret_key):
        self.api_key = api_key
        self.secret_key = secret_key
        self.trade_client = TradeClient(api_key=api_key, secret_key=secret_key, url="https://api-aws.huobi.pro")
        self.account_client = get_acc_client(api_key, secret_key)
        self.account_id = get_acc_id(api_key, secret_key, type='spot')

    # Returns the current price of a coin
    def get_coin_price(self, coin):
        market_client = MarketClient()
        klines_json = requests.get(f'https://api.huobi.pro/market/history/kline?period=1min&size=1&symbol={coin}').json()
        price = klines_json['data'][0]['close']
        return price

    # Get the immediate percent change of a particular coin
    def get_pc_change(symbol, period='1min', size='2'):
        klines_json = requests.get(f'https://api.huobi.pro/market/history/kline?period={period}&size={size}&symbol={symbol}').json()
        klines = klines_json['data']
        # return klines[0]['close'], klines[1]['close'], ((klines[0]['close'] - klines[1]['close'])/klines[1]['close'])
        return ((klines[0]['close'] - klines[1]['close'])/klines[1]['close'])

    # Make an order (Arbitary)
    def make_order(self, symbol, type, limit_order=True, price_per_coin=None, amount_of_coins=None, cost_to_trade=None):
        '''
            :param amount_of_coins:  How many coins to buy (If amount is used, cost will be ignored)
            :param cost_to_trade: How much to money to spend (If cost is used, amount will be ignored)
            :param limit_order: True if it is limit order, else False if it is Market Order
            :param price_per_coin: At what price per coin. (Only used for Limit orders)
            :param type: Limit/Market order? (BUY_MARKET/SELL_LIMIT?etc...)
        '''
        if cost_to_trade and amount_of_coins:
            raise Exception('Cannot specify both Price and Amount. Specify one param only')
        elif amount_of_coins:
            order_id = self.trade_client.create_order(symbol=symbol, account_id=self.account_id, order_type=getattr(OrderType, type), source=OrderSource.API, amount=amount_of_coins, price=price_per_coin)
            print('OK!')
        # If price is given, will auto convert it to the amount by taking the current price per coin
        elif cost_to_trade:
            if limit_order:
                amount_of_coins = round(cost_to_trade/price_per_coin, 4)
                order_id = self.trade_client.create_order(symbol=symbol, account_id=self.account_id, order_type=getattr(OrderType, type), source=OrderSource.API, amount=amount_of_coins, price=price_per_coin)
            elif not limit_order:
                current_price = self.get_coin_price(symbol)
                amount_of_coins = round(cost_to_trade/current_price, 4)
                order_id = self.trade_client.create_order(symbol=symbol, account_id=self.account_id, order_type=getattr(OrderType, type), source=OrderSource.API, amount=amount_of_coins, price=price_per_coin)

        return order_id

    # Make a Market Order
    def market_order(self, coin, type, cost_to_trade=None, amount_to_trade=None):
        '''
        :param coin: Coin to trade
        :param type: Market 'sell' or 'buy'
        :param cost_to_trade: How much money to trade (If used, amount_to_trade should be blank)
        :param amount_to_trade: How many coins to trade (If used, cost_to_trade should be blank)
        :return:
        '''
        type = f'{type.upper()}_MARKET'
        if cost_to_trade and amount_to_trade:
            raise Exception('Cannot specify both Price and Amount. Specify one param only')
        elif cost_to_trade:
            current_price = self.get_coin_price(coin)
            amount = round(cost_to_trade / current_price, 4)
            order_id = self.trade_client.create_order(symbol=coin, account_id=self.account_id, order_type=getattr(OrderType, type),
                                                 source=OrderSource.API, amount=amount, price=None)
        elif amount_to_trade:
            order_id = self.trade_client.create_order(symbol=coin, account_id=self.account_id, order_type=getattr(OrderType, type),
                                                 source=OrderSource.API, amount=amount_to_trade, price=None)
        return order_id


    # Returns the amount of coins in balance
    def get_coin_amt(self, coins, pc=1):
        '''
        :param account_client: Account Client of the user
        :param coins: List of coins to check balance for
        :param pc: (Optional) Percentage of coin amount to return (E.g if pc=0.9, then return 90% of the amount of all coins)
        :return: dictionary containing the coins and their pc% amount of coins
        '''
        x = get_bal_for_coins(self.account_client, coins)
        total_amt_dict = {i['Currency']: i['Amt'] for i in x}
        custom_amt_dict = {i['Currency']: float(i['Amt']) * pc for i in x}
        return custom_amt_dict

    # Returns the price of one coin when bought
    def get_price(self, oid):
        '''
        :param oid: Order ID
        :return:
        '''
        x = self.trade_client.get_order(oid)
        return float(x.filled_cash_amount)/float(x.filled_amount)

    # Make a market/limit order at a specific profit
    def profit(self, COIN, AMOUNT, pc_profit, limit_sell=True, amt_sell=0.97):
        '''
        :param COIN: Crypto to buy
        :param AMOUNT: How many Crypto to buy
        :param pc_profit: At what percentage to sell more (After buying) (Will be a limit sell at 1+pc_profit% of the bought price). E.g if pc_profit=0.76, means you sell at 176% of what you bought it for
        :param limit_sell: Determine whether to make a limit_sell order immediately after buying. Defaults to True
        :param amt_sell: How many % of coins to sell. Defaults to 0.97 (Sell 97% of bought coins, as assume that 3% of coins go to Huobi fees)
        :return:
            oid: Order ID of the market buying
            sid: Order ID of the limit Selling
        '''
        global order_dict
        # Assume you sell 97% and 3% is taken as fee
        # Buy when the percentage goes up by 13%
        oid = self.make_order(self.acc_id, symbol=COIN, amount=AMOUNT, price=0, type='BUY_MARKET')
        buy_price = self.get_price(oid)
        if limit_sell:
            sid = self.make_order(self.acc_id, symbol=COIN, amount=AMOUNT*0.97, price=buy_price*(1 + pc_profit), type='SELL_LIMIT')
            order_dict = {'oid': oid, 'sid': sid, 'buy_price': buy_price}
        else:
            order_dict = {'oid': oid, 'buy_price': buy_price}