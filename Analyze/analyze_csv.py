import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('newcoins.csv')

coins_to_consider = ['1inchusdt', 'oxtusdt', 'grtusdt', 'solusdt', 'kavausdt', 'fisusdt', 'hbarusdt', 'woousdt', 'filusdt', 'aaveusdt']

#Only want to analyze the opening and high


def insert_open(x):
    return x + '_open'


def insert_high(x):
    return x + '_high'


def get_percent_change(open, high):
    return float((high - open) / open)


coins_open = list(map(insert_open, coins_to_consider))
coins_high = list(map(insert_high, coins_to_consider))
coins_open.extend(coins_high)

df = df[coins_open]
print(df.columns)

pc_df = pd.DataFrame()
for coin in coins_to_consider:
    first_open = df[f'{coin}_open'].values[0]
    print(first_open)



