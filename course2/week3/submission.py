import os.path
import re
import random
import pandas as pd
import scipy.stats as stats
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats
import matplotlib.colors as mcol
import matplotlib.cm as cm


np.random.seed(12345)

df = pd.DataFrame([np.random.normal(32000,200000,3650),
                   np.random.normal(43000,100000,3650),
                   np.random.normal(43500,140000,3650),
                   np.random.normal(48000,70000,3650)],
                  index=[1992,1993,1994,1995])

means = df.T.mean().tolist()

def mean_confidence_interval(data, confidence=0.95):
    a = 1.0 * np.array(data)
    n = len(a)
    m, se = np.mean(a), scipy.stats.sem(a)
    h = se * scipy.stats.t.ppf((1 + confidence) / 2., n-1)
    return m-h, m+h

confidence_intervals = [mean_confidence_interval(row) for index, row in df.iterrows()]

y_r = [means[i] - confidence_intervals[i][1] for i in range(len(confidence_intervals))]

bars = plt.bar(range(len(means)), means, yerr=y_r,
        width=1, color=['blue', 'yellow', 'red', 'green'],
        align='center', capsize=10)
plt.xticks(range(len(means)), [str(year) for year in df.index])
plt.gca().set_ylim([-10000, 70000])
horizontal_line = plt.gca().axhline(y=0.5, color='gray', alpha=0.5, linewidth=5)

cm1 = mcol.LinearSegmentedColormap.from_list("Color Scale", ['purple', 'blue', 'brown', 'green', 'cyan', 'yellow', 'orange', 'red'])
cpick = cm.ScalarMappable(cmap=cm1)
cpick.set_array([])
plt.colorbar(cpick, orientation='horizontal')

def percentage(data, sample):
    if sample is not None:
        return stats.percentileofscore(data,sample) / 100
    else:
        return 0.0

def reset_bar_color(y_position):
    for i in range(4):
        perf = percentage(df.iloc[i], y_position)
        color = cpick.to_rgba(perf)
        bars[i].set_color(color)

def mouse_move(event):
    horizontal_line.set_ydata(event.ydata)
    reset_bar_color(event.ydata)
    plt.gcf().canvas.draw_idle()


plt.gcf().canvas.mpl_connect('motion_notify_event', mouse_move)

plt.show()
