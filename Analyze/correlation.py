import numpy as np

from Global.getData import generate_feature_dict
from talib import RSI

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from pandas_profiling import ProfileReport
import sweetviz as sv


def get_rsi(data, rsi_day):
    close = []
    for i in data:
        close.append(i[4])
    close.reverse()
    if len(close) >= rsi_day + 1:
        # Use RSI 14 day
        rsi = RSI(np.array(close), timeperiod=rsi_day)
    else:
        rsi = [0 * len(close)]
    return rsi


def movement_pc(open, close):
    return float((close-open)/open)*100


def movement(open, close):
    # If the price went up, return 1
    if float(close) > float(open):
        return 1
    else:
        return 0


coin = 'btcusdt'
x = generate_feature_dict([coin], TIMEFRAME=1999)

btc_rsi = get_rsi(x[coin], rsi_day=14)

df = pd.DataFrame(x[coin])
df.set_axis(['Time', 'High', 'Low', 'Open', 'Close', 'Volume'], axis=1, inplace=True)
df.drop(['Time', 'High', 'Low', 'Volume'], axis=1, inplace=True)
df = df.iloc[::-1]

df['RSI'] = btc_rsi
df['future_open'] = df['Open'].shift(-1)
df['future_close'] = df['Close'].shift(-1)
df['future_movement'] = list(map(movement, df['future_open'], df['future_close']))
df['movement_pc'] = list(map(movement_pc, df['future_open'], df['future_close']))
df.drop(['future_open', 'future_close'], axis=1, inplace=True)

df.dropna(inplace=True)

plt.figure(figsize=(16, 6))
heatmap = sns.heatmap(df.corr(), vmin=-1, vmax=1, annot=True, cmap='GnBu')
heatmap.set_title(f'{coin} Correlation Heatmap', fontdict={'fontsize':12}, pad=12)

# os.mkdir('/report/pandas_profiling-report.html')
prof = ProfileReport(df)
prof.to_file(output_file='Reports/pandas_profiling-report.html')

# os.mkdir('/report/sweet_viz-report.html')
advert_report = sv.analyze(df)
advert_report.show_html('sweet_viz-report.html')

print(df)
plt.show()

