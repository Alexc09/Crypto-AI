import joblib

import numpy as np
import time
from datetime import datetime

from huobi.client.generic import GenericClient
from huobi.client.market import MarketClient
from huobi.constant import *
from huobi.utils import *
from huobi.constant import *
from huobi.exception.huobi_api_exception import HuobiApiException
from huobi.model.market.candlestick_event import CandlestickEvent

import pandas as pd


df = pd.DataFrame()

#Getting past data
def callback(candlestick_event: 'CandlestickEvent'):
    candlestick_event.print_object()
    print("\n")

def error(e: 'HuobiApiException'):
    print(e.error_code + e.error_message)

market_client = MarketClient()

coins_to_consider = ['1inchusdt', 'oxtusdt', 'grtusdt', 'solusdt', 'kavausdt', 'fisusdt', 'hbarusdt', 'woousdt', 'filusdt', 'aaveusdt']
feature_dict = {}
feature_df = pd.DataFrame()


def generate_feature_dict(coins_to_consider, TIMEFRAME=2000, feature_dic=None, interval='DAY1'):
    '''
    :param coins_to_consider: The ctyptos to include in the Dataset
    :param feature_dict: The dictionary to populate with the features. Features will be in format [Time, High, Low, Open, Close, Volume]
    :param INTERVAL: The interval to collect data [MIN1, MIN5, DAY1, etc.]
    :param TIMEFRAME: How much data to collect (Maximum is 1999 entries)
    :param error: Boolean, whether to output the error message or supress. Defaults to false (Supress output)
    :return: the populated Feature dictionary where the key is the coin name and value is the list of values [Time, High, Low, Open, Close, Volume].
    Latest entry is the first in the list
    '''
    if feature_dic is None:
        feature_dic = {}
    for coin in coins_to_consider:
        try:
            feature_list = []
            # Change the interval [MIN1,MIN5,DAY1, etc]
            if interval == 'DAY1':
                inter = CandlestickInterval.DAY1
            elif interval == 'MIN1':
                inter = CandlestickInterval.MIN1
            elif interval == 'MIN5':
                inter = CandlestickInterval.MIN5
            elif interval == 'MIN15':
                inter = CandlestickInterval.MIN15
            elif interval == 'MIN30':
                inter = CandlestickInterval.MIN30
            elif interval == 'MIN60' or "HOUR1":
                inter = CandlestickInterval.MIN60
            elif interval == "HOUR4":
                inter = CandlestickInterval.HOUR4
            elif interval == 'WEEK1':
                inter = CandlestickInterval.WEEK1
            elif interval == 'MON1':
                inter = CandlestickInterval.MON1
            elif interval == "YEAR1":
                inter = CandlestickInterval.YEAR1

            x = market_client.get_candlestick(coin, inter, TIMEFRAME)

            for obj in x:
                feature_list.append(obj.get_feature_list())
            feature_dict[coin] = feature_list
        except:
            print(f'{coin} threw an error')
            continue

    return feature_dict


def generate_feature_csv(main_df, feature_dict, coins_to_consider, output_csv = False, csv_path = ''):
    '''

    :param main_df: The Dataframe to save the features to
    :param feature_dict: The feature dict obtained from the generate_feature_dict function
    :param coins_to_consider: The ctyptos to include in the Dataset
    :param output_csv: Boolean, whether to output the Dataframe into a csv file. Default = False
    :param csv_path: If output_csv = True, specify the path of the .csv file to create
    :return: Feature DataFrame
    '''
    for coin in coins_to_consider:
        feature_list = np.array(feature_dict[coin])
        df = pd.DataFrame(data=feature_list, columns=[f'time', f'{coin}_high', f'{coin}_low', f'{coin}_open', f'{coin}_close', f'{coin}_vol'])
        df.set_index(f'time', inplace=True)
        if len(main_df) == 0:
            main_df = df
        else:
            main_df = main_df.join(df)

    #TO REVERSE THE ORDER OF THE ROWS (SO THEY GO FAR TO NEARER TIME AS YOU GO DOWNWARD)
    main_df = main_df.iloc[::-1]
    print(main_df.head(5))
    print(main_df.columns)

    #COMMENT OUT IF DONT WANT TO OUTPUT THE CSV
    if output_csv == True:
        main_df.to_csv(csv_path)

    print(main_df.isna().sum())
    return main_df


def get_current_unix():
    current_unix = int(time.time())
    print(f'Current unix time is {current_unix}')
    return current_unix


def strip_datetime(x):
    return x.split(' ')[0]


def get_newCoins_profit(TIMEFRAME, coins_to_consider=['grtusdt', '1inchusdt']):
    '''

    :param TIMEFRAME: How much time to consider
    :param coins_to_consider: List of coins to consider
    :return: Dictionary with the key as coin name and value as a list of values (Opening, High)
    '''
    feature_dict = {}
    coins_release_date = []
    for coin in coins_to_consider:
        open_list = []
        high_list = []
        # Change the interval [MIN1,MIN5,DAY1, etc]
        x = market_client.get_candlestick(coin, CandlestickInterval.DAY1, TIMEFRAME)
        coins_release_date.append(x[-1].get_time())
        for obj in x:
            open_list.append(obj.get_open())
            high_list.append(obj.get_high())

        open_list.reverse()
        high_list.reverse()

        feature_dict[f'{coin}_open'] = open_list
        feature_dict[f'{coin}_high'] = high_list

    coins_release_date = list(map(datetime.fromtimestamp, coins_release_date))
    coins_release_date = list(map(str, coins_release_date))
    coins_release_date = list(map(strip_datetime, coins_release_date))

    return feature_dict, coins_release_date


def get_newCoins_profit_csv(feature_dict, coins_to_consider, coins_date, output_csv=''):
    '''

    :param feature_dict: Dictionary containing the new coins and their list of highs and openings
    :param coins_to_consider: List of coin names
    :param coins_date: List containing the date where the coins are released
    :param output_csv: If set, will output the dataframe into the desired .csv file
    :return: Dataframe containing the first opening, highest price and profit for each coin, as well as the average across all coins
    '''
    coins_name = []
    coins_open = []
    coins_highest = []
    coins_profit = []

    for coin in coins_to_consider:
        first_open = feature_dict[f'{coin}_open'][0]
        highest = max(feature_dict[f'{coin}_high'])
        profit = (highest - first_open) / first_open

        coins_name.append(coin)
        coins_open.append(first_open)
        coins_highest.append(highest)
        coins_profit.append(profit)

    df = pd.DataFrame(data={'Open': coins_open, 'Highest': coins_highest, 'Profit': coins_profit}, index=coins_name)
    df.loc[-1] = df.mean().values
    df.rename({-1:'AVG'}, inplace=True)
    #Append 0 for the AVG row
    coins_date.append(0)
    df['Coins_Release'] = coins_date

    if output_csv:
        df.to_csv(output_csv)


    return df

#C:\Users\alexc\PycharmProjects\Crypto\venv\Scripts\activate
