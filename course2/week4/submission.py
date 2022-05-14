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
#import seaborn as sns

df = pd.read_csv('DisasterDeclarationsSummaries.csv')
df = df[(df['state'] == 'MI')]
df['year'] = df['declarationDate'].apply(lambda x: re.match('(\d{4})(?:.*)', x).group(1))
df['month'] = df['declarationDate'].apply(lambda x: re.match('(\d{4})-(\d{2})(?:.*)', x).group(2))
df = df[['disasterNumber', 'month']]
df.loc[-1] = [0, '11']
rolled = df.groupby('month').count()['disasterNumber'].to_frame('num').sort_values(by='month').reset_index()
rolled.at[10, 'num'] = 0

monthly_data = [0 for _ in range(12)]
with open('weather.csv') as weather_file:
    for line in weather_file:
        values = line.split()
        for i in range(1, 13):
            monthly_data[i - 1] = monthly_data[i - 1] + float(values[i])

monthly_data = (pd.Series(monthly_data) / 69).to_frame('temp')
merged = pd.merge(monthly_data, rolled, left_index=True, right_index=True)
merged['month'] = pd.Series(['Jan', 'Feb', 'Mar', 'Apr',
                             'May', 'Jun', 'Jul', 'Aug',
                             'Sep', 'Oct', 'Nov', 'Dec'])

fig = plt.figure(figsize=(9, 6))
plt.style.use('seaborn-colorblind')
sc = plt.scatter(merged['month'], merged['temp'], s=merged['num']*3+3, c=merged['num'], cmap='plasma')
cb = plt.colorbar(sc)
cb.ax.set_ylabel('Number of Natural Disasters')
cb.ax.tick_params(size=0)
plt.tick_params(
    axis='both',
    bottom=False,
    left=False
)
plt.ylabel('Average Monthly Temperature in Celsius')
plt.title('Average Monthly Temperature vs. Total Monthly Number of Natural Disasters \n in Michigan between 1953-2021')
annotation = 'Total Monthly Number\nis the sum of\nall disasters for\na given month\nacross 1953-2021.\n\n'\
                  'Average Monthly\nTemperature is\nthe average for\na given month\nacross 1953-2021.'
print(plt.xlim())
print(plt.ylim())
plt.gca().annotate(annotation, xy=(13.8, 55), xycoords='data', annotation_clip=False)
plt.show()
