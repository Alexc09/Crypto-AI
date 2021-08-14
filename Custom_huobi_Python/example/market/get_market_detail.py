from huobi.client.market import MarketClient

market_client = MarketClient()
obj = market_client.get_market_detail("ethusdt")
obj.print_object()



