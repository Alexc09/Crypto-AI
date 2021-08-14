from huobi.client.account import AccountClient
from huobi.client.trade import TradeClient
from huobi.constant import *
from huobi.utils import *

symbol_test = "ethusdt"


account_id = 168649803

trade_client = TradeClient(api_key='dbye2sf5t7-3a712192-497237af-6b766', secret_key='f74e2e19-03d85a90-b3fa43ec-31546')
order_id = trade_client.create_order(symbol=symbol_test, account_id=account_id, order_type=OrderType.BUY_LIMIT, source=OrderSource.API, amount=0.1, price=300)
LogInfo.output("created order id : {id}".format(id=order_id))

canceled_order_id = trade_client.cancel_order(symbol_test, order_id)
if canceled_order_id == order_id:
    LogInfo.output("cancel order {id} done".format(id=canceled_order_id))
else:
    LogInfo.output("cancel order {id} fail".format(id=canceled_order_id))

# order_id = trade_client.create_order(symbol=symbol_test, account_id=account_id, order_type=OrderType.BUY_MARKET, source=OrderSource.API, amount=5.0, price=1.292)
# LogInfo.output("created order id : {id}".format(id=order_id))
#
# order_id = trade_client.create_order(symbol=symbol_test, account_id=account_id, order_type=OrderType.SELL_MARKET, source=OrderSource.API, amount=1.77, price=None)
# LogInfo.output("created order id : {id}".format(id=order_id))

