from Global.getData import generate_feature_dict
from Global.get_currency_name import get_symbols
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import pickle
from scipy import spatial
import seaborn as sns
import matplotlib.pyplot as plt
import os


def get_data(interval=None, save_pkl=False, from_pkl=False):
    if from_pkl:
        with open(f'../Compare/{from_pkl}', 'rb') as f:
            data = pickle.load(f)
        return data
    else:
        all_coins = get_symbols()['NORMAL']
        data = generate_feature_dict(all_coins, interval=interval)
        if save_pkl:
            pickle.dump(data, open(f'../Compare/{save_pkl}', "wb"))
        return data


# data = get_data(interval='DAY1', save_pkl='day_data.p')
data = get_data(from_pkl='day_data.p')


# Get the ideal number of LAST_LENGTH. will return the length of all coin arrays
def get_len_list(data):
    len_list = list(map(lambda x: len(x), data.values()))
    len_list.sort()
    print(len_list)


# Ensure all coin lists have the same number of days/hours/etc... (Remove those with less days, and strip those with more days)
def get_updated_data(LAST_LENGTH):
    '''
    :param LAST_DAYS: Number of days to consider
    :return: Updated list with all the same number of days
    '''
    updated_data = {}
    for coin, values in data.items():
        if len(values) < LAST_LENGTH:
            continue
        else:
            updated_data[coin] = values[:LAST_LENGTH]
    return updated_data

#  IF its days
updated_data = get_updated_data(LAST_LENGTH=180)

# If its hours
# updated_data = get_updated_data(LAST_LENGTH=1999)

# Get the percent change
pc_movement = {}
for coin in updated_data:
    pc_movement[coin] = [(i[4]-i[3])/i[3] for i in updated_data[coin]]

df = pd.DataFrame(pc_movement)


def save_corr_matrix(file):
    df.corr().to_csv(file)


def compare_correlation(coin, threshold, print_corr=True):
    '''
    :param coin: Coin to compare against
    :param threshold: Must be above this threshold to be considered. (0 to 1, higher means more correlated)
    :return:
    '''
    df_corr = df.corr()
    sorted_corr = df_corr[df_corr[coin] > threshold][coin].sort_values(ascending=False)
    coin_names = sorted_corr.index.values
    corr_values = sorted_corr.values
    corr_dict = dict(zip(coin_names, corr_values))
    if print_corr:
        print(sorted_corr)
    return corr_dict


def compare_similarity(coin_to_consider, top_k):
    '''
    :param coin_to_consider: The coin you want to compare against the rest
    :param top_k: The closest k number of coins to return
    :return: A DataFrame showing the closest k coins to the coin_to_consider
    '''
    if not coin_to_consider.endswith('usdt'):
        coin_to_consider += 'usdt'

    # List of other coins to compare against
    other_coins = [i for i in pc_movement if i != coin_to_consider]

    similarity_dict = {}
    # get cosine similarity
    for coin in other_coins:
        similarity_score = 1 - spatial.distance.cosine(pc_movement[coin_to_consider], pc_movement[coin])
        similarity_dict[coin] = [similarity_score]

    # print(similarity_dict)
    similarity_df = pd.DataFrame(similarity_dict).transpose()
    similarity_df.columns = ['similarity']

    print(similarity_df.sort_values(by='similarity', ascending=False).head(top_k))


def compare_all(coin, similarity_top_k, corr_threshold):
    if not coin.endswith('usdt'):
        coin += 'usdt'
    print('CORRELATION')
    compare_correlation(coin, corr_threshold)
    print('\n')
    compare_similarity(coin, similarity_top_k)


compare_all('gt', similarity_top_k=10, corr_threshold=0.6)
