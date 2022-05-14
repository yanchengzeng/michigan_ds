import os.path
import re
from urllib.request import urlopen
import numpy as np
import xlrd
import openpyxl
import pandas as pd
import scipy.stats as stats
from scipy.stats import ttest_rel
import matplotlib.pyplot as plt


df = pd.read_csv('fb441e62df2d58994928907a91895ec62c2c42e6cd075c2700843b89.csv')#.sort_values(by='Date')
df = df[~df['Date'].str.contains('02-29')]
def capture_month_day(date):
    pat = '(?:\d{4})-(\d{2})-(\d{2})'
    res = re.match(pat, date)
    day = "{}-{}".format(res.group(1), res.group(2))
    return day

df['Day'] = df['Date'].apply(capture_month_day)
ten_year_df = df[~df['Date'].str.contains('2015')]
one_year_df = df[df['Date'].str.contains('2015')]
ten_year_low = ten_year_df[ten_year_df['Element'] == 'TMIN'].groupby('Day').min()['Data_Value'].transform(lambda x: x / 10).to_frame('T')
ten_year_high = ten_year_df[ten_year_df['Element'] == 'TMAX'].groupby('Day').min()['Data_Value'].transform(lambda x: x / 10).to_frame('T')
one_year_low = one_year_df[one_year_df['Element'] == 'TMIN'].groupby('Day').min()['Data_Value'].transform(lambda x: x / 10).to_frame('T')
one_year_high = one_year_df[one_year_df['Element'] == 'TMAX'].groupby('Day').min()['Data_Value'].transform(lambda x: x / 10).to_frame('T')
combined_low = pd.merge(ten_year_low, one_year_low, how='inner', left_index=True, right_index=True).rename(columns={'T_x': 'ten_low', 'T_y': 'one_low'})
combined_high = pd.merge(ten_year_high, one_year_high, how='inner', left_index=True, right_index=True).rename(columns={'T_x': 'ten_high', 'T_y': 'one_high'})
combined_low['qualified'] = combined_low.apply(lambda x: x['one_low'] < x['ten_low'], axis=1)
combined_high['qualified'] = combined_high.apply(lambda x: x['one_high'] > x['ten_high'], axis=1)
combined_low = combined_low[combined_low['qualified']]
combined_high = combined_high[combined_high['qualified']]

plt.figure(figsize=(12.8, 7.2))
plt.plot(ten_year_high.index, ten_year_high['T'], color='orange', label='2005-2014 Record Highs')
plt.plot(ten_year_low.index, ten_year_low['T'], color='green', label='2005-2014 Record Lows')

plt.gca().fill_between(range(len(ten_year_high['T'])),
                       ten_year_low['T'], ten_year_high['T'],
                       facecolor='gray',
                       alpha=0.25)
plt.scatter(combined_high.index, combined_high['one_high'], s=10, c='purple', label='2015 Record Highs')
plt.scatter(combined_low.index, combined_low['one_low'], s=10, c='blue', label='2015 Record Lows')
months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
x = ['01-15', '02-15', '03-15', '04-15', '05-15', '06-15', '07-15', '08-15', '09-15',
     '10-15', '11-15', '12-15']
plt.xticks(x, months)
plt.ylabel('Temperature in Celsius')
plt.title('2005-2015 Record Temperatures')
plt.tick_params(bottom=False, left=False)

plt.legend(loc=8)
plt.show()
