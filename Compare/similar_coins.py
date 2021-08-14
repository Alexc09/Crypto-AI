from Global.getData import generate_feature_dict
from sklearn.decomposition import PCA
from sklearn.preprocessing import normalize
import itertools
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from Global.get_currency_name import get_symbols

coins_to_consider = get_symbols()['ALL']
# coins_to_consider = ['btcusdt', 'grtusdt', 'ethusdt']
data = generate_feature_dict(coins_to_consider, TIMEFRAME=2000, interval="HOUR1")


min = 0
for i in data:
    list_len = len(data[i])
    print(list_len)
    if min == 0:
        min = list_len
    elif list_len < min:
        min = list_len


for i in data:
    data[i] = data[i][:min]
    data[i] = normalize(data[i])
    data[i] = list(itertools.chain.from_iterable(data[i]))
    data[i] = np.array(data[i])

df = pd.DataFrame.from_dict(data)
vals = df.values.transpose()
pca = PCA(n_components=2)

reduced = pca.fit_transform(vals)


cmap = plt.cm.RdYlGn

fig,ax = plt.subplots()
sc = plt.scatter(reduced[:, 0], reduced[:, 1], cmap=cmap)

annot = ax.annotate("", xy=(0,0), xytext=(20,20),textcoords="offset points",
                    bbox=dict(boxstyle="round", fc="w"),
                    arrowprops=dict(arrowstyle="->"))
annot.set_visible(False)


def update_annot(ind):

    pos = sc.get_offsets()[ind["ind"][0]]
    annot.xy = pos
    text = "{}, {}".format(" ".join(list(map(str,ind["ind"]))),
                           " ".join([coins_to_consider[n] for n in ind["ind"]]))
    annot.set_text(text)
    # annot.get_bbox_patch().set_facecolor(cmap(norm(c[ind["ind"][0]])))
    annot.get_bbox_patch().set_alpha(0.4)


def hover(event):
    vis = annot.get_visible()
    if event.inaxes == ax:
        cont, ind = sc.contains(event)
        if cont:
            update_annot(ind)
            annot.set_visible(True)
            fig.canvas.draw_idle()
        else:
            if vis:
                annot.set_visible(False)
                fig.canvas.draw_idle()


fig.canvas.mpl_connect("motion_notify_event", hover)
plt.show()


