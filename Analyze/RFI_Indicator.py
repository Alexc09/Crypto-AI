import numpy as np

from talib import RSI
from Global.getData import generate_feature_dict
from Global.get_currency_name import get_symbols

# coins_to_consider = ['ltcusdt', 'nulsusdt', 'nanousdt', 'btcusdt']
coins_to_consider = get_symbols(currency='usdt')
# print(coins_to_consider['ALL'])


def get_rsi(coins_to_consider, rsi_day=14):
    '''
    :param coins_to_consider: List of coin symbols to consider
    :param rsi_day: Integer. How many days for RSI to use. Defaults to RSI-14
    :return: close_dict. Dictionary containing the last RSI values for the coins
    '''
    # Dictionary containing the closing prices
    rsi_dict = {}
    data = generate_feature_dict(coins_to_consider, TIMEFRAME=1999)
    for coin, values in data.items():

        tmp = []
        # Check that there is enough days for the RSI indicator
        if len(values) >= rsi_day + 1:
            for value in values:
                # Append the close value to the dictionary
                tmp.append(value[4])

            tmp.reverse()

            # Use RSI 14 day
            rsi = RSI(np.array(tmp), timeperiod=rsi_day)
            rsi = [round(i, 5) for i in rsi if str(i) != 'nan']
            rsi_dict[coin] = rsi[-1]
        else:
            continue

    rsi_dict_sorted = {}

    rsi_dict_sorted_keys = sorted(rsi_dict, key=rsi_dict.get, reverse=True)
    for i in rsi_dict_sorted_keys:
        rsi_dict_sorted[i] = rsi_dict[i]

    return rsi_dict_sorted

# rsi_dict = {'lunausdt': 93.43492, 'ocnusdt': 93.10858, 'htusdt': 92.78432, 'maticusdt': 92.2369, 'mxusdt': 91.00803,
#             'gtusdt': 89.56289, 'hptusdt': 88.47042, 'adausdt': 88.29963, 'avaxusdt': 88.14392, 'qtumusdt': 87.82813}


def get_rsi_report(coins_to_consider, sorted_rsi_dict, top_k=5):
    '''
    :param coins_to_consider: A dictionary containing 3 kinds of symbols: ALL, ETP, NON-ETP. Used to identify the type of asset (Not used to give any number value, whatsoever)
    :param rsi_dict: The sorted RSI dict. If set to AUTO, will automatically fetch the RSI dict from Huobi API
    :param top_k: Top number of coins to return (Defaults to top 5)
    :return:
    '''
    if sorted_rsi_dict == 'AUTO':
        sorted_rsi_dict = get_rsi(coins_to_consider['ALL'])

    report = ''
    dict_items = sorted_rsi_dict.items()

    report += f'<h1><b>Top ALL assets today</b></h1> \n'
    report += f'<h2><b>{top_k} Highest RSI today</b></h2> \n'
    for i in list(dict_items)[:top_k]:
        report += f'{i[0]} - {i[1]} \n'

    report += '\n'

    report += f'<h2><b>{top_k} Lowest RSI today</b></h2> \n'
    for i in list(dict_items)[-top_k:]:
        report += f'{i[0]} - {i[1]} \n'

    report += '\n\n'
    report += '<h1><b>Top Non-ETPs today</b></h1> \n'

    report += f'<h2><b>{top_k} Highest RSI today</b></h2> \n'
    highest_counter = 1
    for i in list(dict_items):
        # If the coin is not an ETP
        if i[0] not in coins_to_consider['ETP'] and highest_counter <= top_k:
            report += f'{i[0]} - {i[1]} \n'
            highest_counter += 1
        else:
            pass

    report += '\n'

    lowest_counter = 1
    report += f'<h2><b>{top_k} Lowest RSI today</b></h2> \n'
    # Reverse the list
    tmp_list = []

    for i in list(dict_items)[::-1]:
        # If the coin is not an ETP
        if i[0] not in coins_to_consider['ETP'] and lowest_counter <= top_k:
            print(f'I IS: {i}')
            tmp_list.append(i)
            lowest_counter += 1
        else:
            pass

    print(tmp_list)

    for i in tmp_list[::-1]:
        report += f'{i[0]} - {i[1]} \n'

    report += '\n'

    return report


# if __name__== '__main__':
#     report = get_rsi_report(coins_to_consider=coins_to_consider, sorted_rsi_dict='AUTO')
#     print(report)
