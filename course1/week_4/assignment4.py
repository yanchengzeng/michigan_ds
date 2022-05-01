#!/usr/bin/env python
# coding: utf-8

# # Assignment 4
# ## Description
# In this assignment you must read in a file of metropolitan regions and associated sports teams from [assets/wikipedia_data.html](assets/wikipedia_data.html) and answer some questions about each metropolitan region. Each of these regions may have one or more teams from the "Big 4": NFL (football, in [assets/nfl.csv](assets/nfl.csv)), MLB (baseball, in [assets/mlb.csv](assets/mlb.csv)), NBA (basketball, in [assets/nba.csv](assets/nba.csv) or NHL (hockey, in [assets/nhl.csv](assets/nhl.csv)). Please keep in mind that all questions are from the perspective of the metropolitan region, and that this file is the "source of authority" for the location of a given sports team. Thus teams which are commonly known by a different area (e.g. "Oakland Raiders") need to be mapped into the metropolitan region given (e.g. San Francisco Bay Area). This will require some human data understanding outside of the data you've been given (e.g. you will have to hand-code some names, and might need to google to find out where teams are)!
# 
# For each sport I would like you to answer the question: **what is the win/loss ratio's correlation with the population of the city it is in?** Win/Loss ratio refers to the number of wins over the number of wins plus the number of losses. Remember that to calculate the correlation with [`pearsonr`](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.pearsonr.html), so you are going to send in two ordered lists of values, the populations from the wikipedia_data.html file and the win/loss ratio for a given sport in the same order. Average the win/loss ratios for those cities which have multiple teams of a single sport. Each sport is worth an equal amount in this assignment (20%\*4=80%) of the grade for this assignment. You should only use data **from year 2018** for your analysis -- this is important!
# 
# ## Notes
# 
# 1. Do not include data about the MLS or CFL in any of the work you are doing, we're only interested in the Big 4 in this assignment.
# 2. I highly suggest that you first tackle the four correlation questions in order, as they are all similar and worth the majority of grades for this assignment. This is by design!
# 3. It's fair game to talk with peers about high level strategy as well as the relationship between metropolitan areas and sports teams. However, do not post code solving aspects of the assignment (including such as dictionaries mapping areas to teams, or regexes which will clean up names).
# 4. There may be more teams than the assert statements test, remember to collapse multiple teams in one city into a single value!

# ## Question 1
# For this question, calculate the win/loss ratio's correlation with the population of the city it is in for the **NHL** using **2018** data.

# In[18]:


import pandas as pd
import numpy as np
import scipy.stats as stats
import re

nhl_df=pd.read_csv("assets/nhl.csv")
cities=pd.read_html("assets/wikipedia_data.html")[1]
cities=cities.iloc[:-1,[0,3,5,6,7,8]]

nhl_team_region, nfl_team_region, nba_team_region, mlb_team_region = {}, {}, {}, {}
for index, row in cities.iterrows():
    nhl_str = re.sub("—|\[.*\]", "", row['NHL']).strip()
    nfl_str = re.sub("—|\[.*\]", "", row['NFL']).strip()
    nba_str = re.sub("—|\[.*\]", "", row['NBA']).strip()
    mlb_str = re.sub("—|\[.*\]", "", row['MLB']).strip()
    if bool(nhl_str):
        nhl_single = re.match('(?:.*\s)?(\w+)(?:\*?)', nhl_str).group(1)
        nhl_team_region[nhl_single] = row['Metropolitan area']
    if bool(nfl_str):
        nfl_team_region[nfl_str] = row['Metropolitan area']
    if bool(nba_str):
        nba_team_region[nba_str] = row['Metropolitan area']
    if bool(mlb_str):
        mlb_team_region[mlb_str] = row['Metropolitan area']

nhl_map_fix = {'Rangers': 'New York City', 'Islanders': 'New York City', 'Devils': 'New York City',
               'Kings': 'Los Angeles', 'Ducks': 'Los Angeles'}
nfl_map_fix = {'Giants': 'New York City', 'Jets': 'New York City',
               'Rams': 'Los Angeles', 'Chargers': 'Los Angeles',
               '49ers': 'San Francisco Bay Area', 'Raiders': 'San Francisco Bay Area'}
mlb_map_fix = {'Yankees': 'New York City', 'Mets': 'New York City',
               'Dodgers': 'Los Angeles', 'Angels': 'Los Angeles',
               'Giants': 'San Francisco Bay Area', 'Athletics': 'San Francisco Bay Area',
               'Cubs': 'Chicago', 'White Sox': 'Chicago'}
nba_map_fix = {'Knicks': 'New York City', 'Nets': 'New York City',
               'Lakers': 'Los Angeles', 'Clippers': 'Los Angeles'}

nhl_team_region = {**nhl_team_region, **nhl_map_fix}
nfl_team_region = {**nfl_team_region, **nfl_map_fix}
nba_team_region = {**nba_team_region, **nba_map_fix}
mlb_team_region = {**mlb_team_region, **mlb_map_fix}

# filter by 2018, numeric row
nhl_filtered = nhl_df[nhl_df['year'] == 2018][nhl_df['GP'].str.contains('\d+')]
nhl_filtered['team2'] = nhl_filtered['team'].transform(lambda x: re.match('(?:.*\s)?(\w+)(?:\*?)', x).group(1))
nhl_filtered['Metropolitan area'] = nhl_filtered['team2'].transform(lambda x: nhl_team_region[x])
nhl_filtered['nhl_ratio'] = nhl_filtered['W'].astype(int) / (nhl_filtered['L'].astype(int) + nhl_filtered['W'].astype(int))
nhl_win_loss = nhl_filtered.groupby('Metropolitan area')['nhl_ratio'].mean()
#print(nhl_win_loss)
cities = cities.rename(columns={'Population (2016 est.)[8]': 'population'}).set_index('Metropolitan area')
cities = pd.merge(cities, nhl_win_loss, how='left', left_index=True, right_index=True)
#print(cities[['population', 'nhl_ratio']])


def nhl_correlation():

    global cities
    population_by_region = cities[cities['nhl_ratio'] > 0]['population'].astype(int)  # pass in metropolitan area population from cities
    win_loss_by_region = cities[cities['nhl_ratio'] > 0]['nhl_ratio'].astype(float)  # pass in win/loss ratio from nhl_df in the same order as cities["Metropolitan area"]

    assert len(population_by_region) == len(win_loss_by_region), "Q1: Your lists must be the same length"
    assert len(population_by_region) == 28, "Q1: There should be 28 teams being analysed for NHL"

    return stats.pearsonr(population_by_region, win_loss_by_region)[0]


# In[ ]:





# In[21]:


nhl_correlation()


# ## Question 2
# For this question, calculate the win/loss ratio's correlation with the population of the city it is in for the **NBA** using **2018** data.

# In[19]:


import pandas as pd
import numpy as np
import scipy.stats as stats
import re

nba_df=pd.read_csv("assets/nba.csv")
cities=pd.read_html("assets/wikipedia_data.html")[1]
cities=cities.iloc[:-1,[0,3,5,6,7,8]]

nhl_team_region, nfl_team_region, nba_team_region, mlb_team_region = {}, {}, {}, {}
for index, row in cities.iterrows():
    nhl_str = re.sub("—|\[.*\]", "", row['NHL']).strip()
    nfl_str = re.sub("—|\[.*\]", "", row['NFL']).strip()
    nba_str = re.sub("—|\[.*\]", "", row['NBA']).strip()
    mlb_str = re.sub("—|\[.*\]", "", row['MLB']).strip()
    if bool(nhl_str):
        nhl_single = re.match('(?:.*\s)?(\w+)(?:\*?)', nhl_str).group(1)
        nhl_team_region[nhl_single] = row['Metropolitan area']
    if bool(nfl_str):
        nfl_team_region[nfl_str] = row['Metropolitan area']
    if bool(nba_str):
        nba_single = re.match('(?:.*\s)?(\w+)(?:.*)', nba_str).group(1)
        nba_team_region[nba_single] = row['Metropolitan area']
    if bool(mlb_str):
        mlb_team_region[mlb_str] = row['Metropolitan area']

nhl_map_fix = {'Rangers': 'New York City', 'Islanders': 'New York City', 'Devils': 'New York City',
               'Kings': 'Los Angeles', 'Ducks': 'Los Angeles'}
nfl_map_fix = {'Giants': 'New York City', 'Jets': 'New York City',
               'Rams': 'Los Angeles', 'Chargers': 'Los Angeles',
               '49ers': 'San Francisco Bay Area', 'Raiders': 'San Francisco Bay Area'}
mlb_map_fix = {'Yankees': 'New York City', 'Mets': 'New York City',
               'Dodgers': 'Los Angeles', 'Angels': 'Los Angeles',
               'Giants': 'San Francisco Bay Area', 'Athletics': 'San Francisco Bay Area',
               'Cubs': 'Chicago', 'White Sox': 'Chicago'}
nba_map_fix = {'Knicks': 'New York City', 'Nets': 'New York City',
               'Lakers': 'Los Angeles', 'Clippers': 'Los Angeles'}

del nhl_team_region['RangersIslandersDevils']
del nhl_team_region['KingsDucks']
del nfl_team_region['GiantsJets']
del nfl_team_region['RamsChargers']
del nfl_team_region['49ersRaiders']
del nba_team_region['KnicksNets']
del nba_team_region['LakersClippers']
del mlb_team_region['DodgersAngels']
del mlb_team_region['YankeesMets']
del mlb_team_region['GiantsAthletics']
del mlb_team_region['CubsWhite Sox']

nhl_team_region = {**nhl_team_region, **nhl_map_fix}
nfl_team_region = {**nfl_team_region, **nfl_map_fix}
nba_team_region = {**nba_team_region, **nba_map_fix}
mlb_team_region = {**mlb_team_region, **mlb_map_fix}

cities = cities.rename(columns={'Population (2016 est.)[8]': 'population'}).set_index('Metropolitan area')

nhl_filtered = nhl_df[nhl_df['year'] == 2018][nhl_df['GP'].str.contains('\d+')]
nhl_filtered['team2'] = nhl_filtered['team'].transform(lambda x: re.match('(?:.*\s)?(\w+)(?:\*?)', x).group(1))
nhl_filtered['Metropolitan area'] = nhl_filtered['team2'].transform(lambda x: nhl_team_region[x])
nhl_filtered['nhl_ratio'] = nhl_filtered['W'].astype(int) / (nhl_filtered['L'].astype(int) + nhl_filtered['W'].astype(int))
nhl_win_loss = nhl_filtered.groupby('Metropolitan area')['nhl_ratio'].mean()
cities = pd.merge(cities, nhl_win_loss, how='left', left_index=True, right_index=True)

nba_filtered = nba_df[nba_df['year'] == 2018]
nba_filtered['team2'] = nba_filtered['team'].transform(lambda x: re.match('(?:.*\s)?(\w+)(?:.*)', x).group(1))
nba_filtered['Metropolitan area'] = nba_filtered['team2'].transform(lambda x: nba_team_region[x])
nba_filtered['nba_ratio'] = nba_filtered['W'].astype(int) / (nba_filtered['L'].astype(int) + nba_filtered['W'].astype(int))
nba_win_loss = nba_filtered.groupby('Metropolitan area')['nba_ratio'].mean()
cities = pd.merge(cities, nba_win_loss, how='left', left_index=True, right_index=True)


def nba_correlation():

    population_by_region = cities[cities['nba_ratio'] > 0]['population'].astype(int)  # pass in metropolitan area population from cities
    win_loss_by_region = cities[cities['nba_ratio'] > 0]['nba_ratio'].astype(float)  # pass in win/loss ratio from nba_df in the same order as cities["Metropolitan area"]

    assert len(population_by_region) == len(win_loss_by_region), "Q2: Your lists must be the same length"
    assert len(population_by_region) == 28, "Q2: There should be 28 teams being analysed for NBA"

    return stats.pearsonr(population_by_region, win_loss_by_region)[0]


# In[ ]:





# In[20]:


nba_correlation()


# ## Question 3
# For this question, calculate the win/loss ratio's correlation with the population of the city it is in for the **MLB** using **2018** data.

# In[23]:


import pandas as pd
import numpy as np
import scipy.stats as stats
import re

mlb_df=pd.read_csv("assets/mlb.csv")
cities=pd.read_html("assets/wikipedia_data.html")[1]
cities=cities.iloc[:-1,[0,3,5,6,7,8]]

nhl_team_region, nfl_team_region, nba_team_region, mlb_team_region = {}, {}, {}, {}
for index, row in cities.iterrows():
    nhl_str = re.sub("—|\[.*\]", "", row['NHL']).strip()
    nfl_str = re.sub("—|\[.*\]", "", row['NFL']).strip()
    nba_str = re.sub("—|\[.*\]", "", row['NBA']).strip()
    mlb_str = re.sub("—|\[.*\]", "", row['MLB']).strip()
    if bool(nhl_str):
        nhl_single = re.match('(?:.*\s)?(\w+)(?:\*?)', nhl_str).group(1)
        nhl_team_region[nhl_single] = row['Metropolitan area']
    if bool(nfl_str):
        nfl_team_region[nfl_str] = row['Metropolitan area']
    if bool(nba_str):
        nba_single = re.match('(?:.*\s)?(\w+)(?:.*)', nba_str).group(1)
        nba_team_region[nba_single] = row['Metropolitan area']
    if bool(mlb_str):
        mlb_single = re.match('(?:.*\s)?(\w+)(?:.*)', mlb_str).group(1)
        mlb_team_region[mlb_single] = row['Metropolitan area']

nhl_map_fix = {'Rangers': 'New York City', 'Islanders': 'New York City', 'Devils': 'New York City',
               'Kings': 'Los Angeles', 'Ducks': 'Los Angeles'}
nfl_map_fix = {'Giants': 'New York City', 'Jets': 'New York City',
               'Rams': 'Los Angeles', 'Chargers': 'Los Angeles',
               '49ers': 'San Francisco Bay Area', 'Raiders': 'San Francisco Bay Area'}
mlb_map_fix = {'Yankees': 'New York City', 'Mets': 'New York City',
               'Dodgers': 'Los Angeles', 'Angels': 'Los Angeles',
               'Giants': 'San Francisco Bay Area', 'Athletics': 'San Francisco Bay Area',
               'Cubs': 'Chicago'}
nba_map_fix = {'Knicks': 'New York City', 'Nets': 'New York City',
               'Lakers': 'Los Angeles', 'Clippers': 'Los Angeles'}
del nhl_team_region['RangersIslandersDevils']
del nhl_team_region['KingsDucks']
del nfl_team_region['GiantsJets']
del nfl_team_region['RamsChargers']
del nfl_team_region['49ersRaiders']
del nba_team_region['KnicksNets']
del nba_team_region['LakersClippers']
del mlb_team_region['DodgersAngels']
del mlb_team_region['YankeesMets']
del mlb_team_region['GiantsAthletics']
del mlb_team_region['Sox']


nhl_team_region = {**nhl_team_region, **nhl_map_fix}
nfl_team_region = {**nfl_team_region, **nfl_map_fix}
nba_team_region = {**nba_team_region, **nba_map_fix}
mlb_team_region = {**mlb_team_region, **mlb_map_fix}
mlb_team_region['WhiteSox'] = 'Chicago'
mlb_team_region['RedSox'] = 'Boston'
cities = cities.rename(columns={'Population (2016 est.)[8]': 'population'}).set_index('Metropolitan area')

nhl_filtered = nhl_df[nhl_df['year'] == 2018][nhl_df['GP'].str.contains('\d+')]
nhl_filtered['team2'] = nhl_filtered['team'].transform(lambda x: re.match('(?:.*\s)?(\w+)(?:\*?)', x).group(1))
nhl_filtered['Metropolitan area'] = nhl_filtered['team2'].transform(lambda x: nhl_team_region[x])
nhl_filtered['nhl_ratio'] = nhl_filtered['W'].astype(int) / (nhl_filtered['L'].astype(int) + nhl_filtered['W'].astype(int))
nhl_win_loss = nhl_filtered.groupby('Metropolitan area')['nhl_ratio'].mean()
cities = pd.merge(cities, nhl_win_loss, how='left', left_index=True, right_index=True)

nba_filtered = nba_df[nba_df['year'] == 2018]
nba_filtered['team2'] = nba_filtered['team'].transform(lambda x: re.match('(?:.*\s)?(\w+)(?:.*)', x).group(1))
nba_filtered['Metropolitan area'] = nba_filtered['team2'].transform(lambda x: nba_team_region[x])
nba_filtered['nba_ratio'] = nba_filtered['W'].astype(int) / (nba_filtered['L'].astype(int) + nba_filtered['W'].astype(int))
nba_win_loss = nba_filtered.groupby('Metropolitan area')['nba_ratio'].mean()
cities = pd.merge(cities, nba_win_loss, how='left', left_index=True, right_index=True)

mlb_filtered = mlb_df[nba_df['year'] == 2018]
mlb_filtered.loc[0, 'team'] = 'Boxton RedSox'
mlb_filtered.loc[8, 'team'] = 'Chicago WhiteSox'

mlb_filtered['team2'] = mlb_filtered['team'].transform(lambda x: re.match('(?:.*\s)?(\w+)(?:.*)', x).group(1))
mlb_filtered['Metropolitan area'] = mlb_filtered['team2'].transform(lambda x: mlb_team_region[x])
mlb_filtered['mlb_ratio'] = mlb_filtered['W'].astype(int) / (mlb_filtered['L'].astype(int) + mlb_filtered['W'].astype(int))
mlb_win_loss = mlb_filtered.groupby('Metropolitan area')['mlb_ratio'].mean()
cities = pd.merge(cities, mlb_win_loss, how='left', left_index=True, right_index=True)


def mlb_correlation():


    population_by_region = cities[cities['mlb_ratio'] > 0]['population'].astype(int)  # pass in metropolitan area population from cities
    win_loss_by_region = cities[cities['mlb_ratio'] > 0]['mlb_ratio'].astype(float)  # pass in win/loss ratio from mlb_df in the same order as cities["Metropolitan area"]

    assert len(population_by_region) == len(win_loss_by_region), "Q3: Your lists must be the same length"
    assert len(population_by_region) == 26, "Q3: There should be 26 teams being analysed for MLB"

    return stats.pearsonr(population_by_region, win_loss_by_region)[0]


# In[ ]:





# ## Question 4
# For this question, calculate the win/loss ratio's correlation with the population of the city it is in for the **NFL** using **2018** data.

# In[25]:


import pandas as pd
import numpy as np
import scipy.stats as stats
import re

nfl_df=pd.read_csv("assets/nfl.csv")
cities=pd.read_html("assets/wikipedia_data.html")[1]
cities=cities.iloc[:-1,[0,3,5,6,7,8]]

nhl_team_region, nfl_team_region, nba_team_region, mlb_team_region = {}, {}, {}, {}
for index, row in cities.iterrows():
    nhl_str = re.sub("—|\[.*\]", "", row['NHL']).strip()
    nfl_str = re.sub("—|\[.*\]", "", row['NFL']).strip()
    nba_str = re.sub("—|\[.*\]", "", row['NBA']).strip()
    mlb_str = re.sub("—|\[.*\]", "", row['MLB']).strip()
    if bool(nhl_str):
        nhl_single = re.match('(?:.*\s)?(\w+)(?:\*?)', nhl_str).group(1)
        nhl_team_region[nhl_single] = row['Metropolitan area']
    if bool(nfl_str):
        nfl_team_region[nfl_str] = row['Metropolitan area']
    if bool(nba_str):
        nba_single = re.match('(?:.*\s)?(\w+)(?:.*)', nba_str).group(1)
        nba_team_region[nba_single] = row['Metropolitan area']
    if bool(mlb_str):
        mlb_single = re.match('(?:.*\s)?(\w+)(?:.*)', mlb_str).group(1)
        mlb_team_region[mlb_single] = row['Metropolitan area']

nhl_map_fix = {'Rangers': 'New York City', 'Islanders': 'New York City', 'Devils': 'New York City',
               'Kings': 'Los Angeles', 'Ducks': 'Los Angeles'}
nfl_map_fix = {'Giants': 'New York City', 'Jets': 'New York City',
               'Rams': 'Los Angeles', 'Chargers': 'Los Angeles',
               '49ers': 'San Francisco Bay Area', 'Raiders': 'San Francisco Bay Area'}
mlb_map_fix = {'Yankees': 'New York City', 'Mets': 'New York City',
               'Dodgers': 'Los Angeles', 'Angels': 'Los Angeles',
               'Giants': 'San Francisco Bay Area', 'Athletics': 'San Francisco Bay Area',
               'Cubs': 'Chicago'}
nba_map_fix = {'Knicks': 'New York City', 'Nets': 'New York City',
               'Lakers': 'Los Angeles', 'Clippers': 'Los Angeles'}
del nhl_team_region['RangersIslandersDevils']
del nhl_team_region['KingsDucks']
del nfl_team_region['GiantsJets']
del nfl_team_region['RamsChargers']
del nfl_team_region['49ersRaiders']
del nba_team_region['KnicksNets']
del nba_team_region['LakersClippers']
del mlb_team_region['DodgersAngels']
del mlb_team_region['YankeesMets']
del mlb_team_region['GiantsAthletics']
del mlb_team_region['Sox']


nhl_team_region = {**nhl_team_region, **nhl_map_fix}
nfl_team_region = {**nfl_team_region, **nfl_map_fix}
nba_team_region = {**nba_team_region, **nba_map_fix}
mlb_team_region = {**mlb_team_region, **mlb_map_fix}
mlb_team_region['WhiteSox'] = 'Chicago'
mlb_team_region['RedSox'] = 'Boston'
cities = cities.rename(columns={'Population (2016 est.)[8]': 'population'}).set_index('Metropolitan area')

nhl_filtered = nhl_df[nhl_df['year'] == 2018][nhl_df['GP'].str.contains('\d+')]
nhl_filtered['team2'] = nhl_filtered['team'].transform(lambda x: re.match('(?:.*\s)?(\w+)(?:\*?)', x).group(1))
nhl_filtered['Metropolitan area'] = nhl_filtered['team2'].transform(lambda x: nhl_team_region[x])
nhl_filtered['nhl_ratio'] = nhl_filtered['W'].astype(int) / (nhl_filtered['L'].astype(int) + nhl_filtered['W'].astype(int))
nhl_win_loss = nhl_filtered.groupby('Metropolitan area')['nhl_ratio'].mean()
cities = pd.merge(cities, nhl_win_loss, how='left', left_index=True, right_index=True)

nba_filtered = nba_df[nba_df['year'] == 2018]
nba_filtered['team2'] = nba_filtered['team'].transform(lambda x: re.match('(?:.*\s)?(\w+)(?:.*)', x).group(1))
nba_filtered['Metropolitan area'] = nba_filtered['team2'].transform(lambda x: nba_team_region[x])
nba_filtered['nba_ratio'] = nba_filtered['W'].astype(int) / (nba_filtered['L'].astype(int) + nba_filtered['W'].astype(int))
nba_win_loss = nba_filtered.groupby('Metropolitan area')['nba_ratio'].mean()
cities = pd.merge(cities, nba_win_loss, how='left', left_index=True, right_index=True)

mlb_filtered = mlb_df[nba_df['year'] == 2018]
mlb_filtered.loc[0, 'team'] = 'Boxton RedSox'
mlb_filtered.loc[8, 'team'] = 'Chicago WhiteSox'

mlb_filtered['team2'] = mlb_filtered['team'].transform(lambda x: re.match('(?:.*\s)?(\w+)(?:.*)', x).group(1))
mlb_filtered['Metropolitan area'] = mlb_filtered['team2'].transform(lambda x: mlb_team_region[x])
mlb_filtered['mlb_ratio'] = mlb_filtered['W'].astype(int) / (mlb_filtered['L'].astype(int) + mlb_filtered['W'].astype(int))
mlb_win_loss = mlb_filtered.groupby('Metropolitan area')['mlb_ratio'].mean()
cities = pd.merge(cities, mlb_win_loss, how='left', left_index=True, right_index=True)

nfl_filtered = nfl_df[nfl_df['year'] == 2018][nfl_df['PD'].str.contains('\d+')]
nfl_filtered['team2'] = nfl_filtered['team'].transform(lambda x: re.match('(?:.*\s)?(\w+)(?:.*)', x).group(1))
nfl_filtered['Metropolitan area'] = nfl_filtered['team2'].transform(lambda x: nfl_team_region[x])
nfl_filtered['nfl_ratio'] = nfl_filtered['W'].astype(int) / (nfl_filtered['L'].astype(int) + nfl_filtered['W'].astype(int))
nfl_win_loss = nfl_filtered.groupby('Metropolitan area')['nfl_ratio'].mean()
cities = pd.merge(cities, nfl_win_loss, how='left', left_index=True, right_index=True)


def nfl_correlation():

    population_by_region = cities[cities['nfl_ratio'] > 0]['population'].astype(int)  # pass in metropolitan area population from cities
    win_loss_by_region = cities[cities['nfl_ratio'] > 0]['nfl_ratio'].astype(float)  # pass in win/loss ratio from nfl_df in the same order as cities["Metropolitan area"]

    assert len(population_by_region) == len(win_loss_by_region), "Q4: Your lists must be the same length"
    assert len(population_by_region) == 29, "Q4: There should be 29 teams being analysed for NFL"

    return stats.pearsonr(population_by_region, win_loss_by_region)[0]


# In[ ]:





# In[26]:


nfl_correlation()


# ## Question 5
# In this question I would like you to explore the hypothesis that **given that an area has two sports teams in different sports, those teams will perform the same within their respective sports**. How I would like to see this explored is with a series of paired t-tests (so use [`ttest_rel`](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.ttest_rel.html)) between all pairs of sports. Are there any sports where we can reject the null hypothesis? Again, average values where a sport has multiple teams in one region. Remember, you will only be including, for each sport, cities which have teams engaged in that sport, drop others as appropriate. This question is worth 20% of the grade for this assignment.

# In[32]:


import pandas as pd
import numpy as np
import scipy.stats as stats
import re

mlb_df=pd.read_csv("assets/mlb.csv")
nhl_df=pd.read_csv("assets/nhl.csv")
nba_df=pd.read_csv("assets/nba.csv")
nfl_df=pd.read_csv("assets/nfl.csv")
cities=pd.read_html("assets/wikipedia_data.html")[1]
cities=cities.iloc[:-1,[0,3,5,6,7,8]]


nhl_team_region, nfl_team_region, nba_team_region, mlb_team_region = {}, {}, {}, {}
for index, row in cities.iterrows():
    nhl_str = re.sub("—|\[.*\]", "", row['NHL']).strip()
    nfl_str = re.sub("—|\[.*\]", "", row['NFL']).strip()
    nba_str = re.sub("—|\[.*\]", "", row['NBA']).strip()
    mlb_str = re.sub("—|\[.*\]", "", row['MLB']).strip()
    if bool(nhl_str):
        nhl_single = re.match('(?:.*\s)?(\w+)(?:\*?)', nhl_str).group(1)
        nhl_team_region[nhl_single] = row['Metropolitan area']
    if bool(nfl_str):
        nfl_team_region[nfl_str] = row['Metropolitan area']
    if bool(nba_str):
        nba_single = re.match('(?:.*\s)?(\w+)(?:.*)', nba_str).group(1)
        nba_team_region[nba_single] = row['Metropolitan area']
    if bool(mlb_str):
        mlb_single = re.match('(?:.*\s)?(\w+)(?:.*)', mlb_str).group(1)
        mlb_team_region[mlb_single] = row['Metropolitan area']

nhl_map_fix = {'Rangers': 'New York City', 'Islanders': 'New York City', 'Devils': 'New York City',
               'Kings': 'Los Angeles', 'Ducks': 'Los Angeles'}
nfl_map_fix = {'Giants': 'New York City', 'Jets': 'New York City',
               'Rams': 'Los Angeles', 'Chargers': 'Los Angeles',
               '49ers': 'San Francisco Bay Area', 'Raiders': 'San Francisco Bay Area'}
mlb_map_fix = {'Yankees': 'New York City', 'Mets': 'New York City',
               'Dodgers': 'Los Angeles', 'Angels': 'Los Angeles',
               'Giants': 'San Francisco Bay Area', 'Athletics': 'San Francisco Bay Area',
               'Cubs': 'Chicago'}
nba_map_fix = {'Knicks': 'New York City', 'Nets': 'New York City',
               'Lakers': 'Los Angeles', 'Clippers': 'Los Angeles'}
del nhl_team_region['RangersIslandersDevils']
del nhl_team_region['KingsDucks']
del nfl_team_region['GiantsJets']
del nfl_team_region['RamsChargers']
del nfl_team_region['49ersRaiders']
del nba_team_region['KnicksNets']
del nba_team_region['LakersClippers']
del mlb_team_region['DodgersAngels']
del mlb_team_region['YankeesMets']
del mlb_team_region['GiantsAthletics']
del mlb_team_region['Sox']


nhl_team_region = {**nhl_team_region, **nhl_map_fix}
nfl_team_region = {**nfl_team_region, **nfl_map_fix}
nba_team_region = {**nba_team_region, **nba_map_fix}
mlb_team_region = {**mlb_team_region, **mlb_map_fix}
mlb_team_region['WhiteSox'] = 'Chicago'
mlb_team_region['RedSox'] = 'Boston'
cities = cities.rename(columns={'Population (2016 est.)[8]': 'population'}).set_index('Metropolitan area')

nhl_filtered = nhl_df[nhl_df['year'] == 2018][nhl_df['GP'].str.contains('\d+')]
nhl_filtered['team2'] = nhl_filtered['team'].transform(lambda x: re.match('(?:.*\s)?(\w+)(?:\*?)', x).group(1))
nhl_filtered['Metropolitan area'] = nhl_filtered['team2'].transform(lambda x: nhl_team_region[x])
nhl_filtered['nhl_ratio'] = nhl_filtered['W'].astype(int) / (nhl_filtered['L'].astype(int) + nhl_filtered['W'].astype(int))
nhl_win_loss = nhl_filtered.groupby('Metropolitan area')['nhl_ratio'].mean()
cities = pd.merge(cities, nhl_win_loss, how='left', left_index=True, right_index=True)

nba_filtered = nba_df[nba_df['year'] == 2018]
nba_filtered['team2'] = nba_filtered['team'].transform(lambda x: re.match('(?:.*\s)?(\w+)(?:.*)', x).group(1))
nba_filtered['Metropolitan area'] = nba_filtered['team2'].transform(lambda x: nba_team_region[x])
nba_filtered['nba_ratio'] = nba_filtered['W'].astype(int) / (nba_filtered['L'].astype(int) + nba_filtered['W'].astype(int))
nba_win_loss = nba_filtered.groupby('Metropolitan area')['nba_ratio'].mean()
cities = pd.merge(cities, nba_win_loss, how='left', left_index=True, right_index=True)

mlb_filtered = mlb_df[nba_df['year'] == 2018]
mlb_filtered.loc[0, 'team'] = 'Boxton RedSox'
mlb_filtered.loc[8, 'team'] = 'Chicago WhiteSox'

mlb_filtered['team2'] = mlb_filtered['team'].transform(lambda x: re.match('(?:.*\s)?(\w+)(?:.*)', x).group(1))
mlb_filtered['Metropolitan area'] = mlb_filtered['team2'].transform(lambda x: mlb_team_region[x])
mlb_filtered['mlb_ratio'] = mlb_filtered['W'].astype(int) / (mlb_filtered['L'].astype(int) + mlb_filtered['W'].astype(int))
mlb_win_loss = mlb_filtered.groupby('Metropolitan area')['mlb_ratio'].mean()
cities = pd.merge(cities, mlb_win_loss, how='left', left_index=True, right_index=True)

nfl_filtered = nfl_df[nfl_df['year'] == 2018][nfl_df['PD'].str.contains('\d+')]
nfl_filtered['team2'] = nfl_filtered['team'].transform(lambda x: re.match('(?:.*\s)?(\w+)(?:.*)', x).group(1))
nfl_filtered['Metropolitan area'] = nfl_filtered['team2'].transform(lambda x: nfl_team_region[x])
nfl_filtered['nfl_ratio'] = nfl_filtered['W'].astype(int) / (nfl_filtered['L'].astype(int) + nfl_filtered['W'].astype(int))
nfl_win_loss = nfl_filtered.groupby('Metropolitan area')['nfl_ratio'].mean()
cities = pd.merge(cities, nfl_win_loss, how='left', left_index=True, right_index=True)

def sports_team_performance():
    global cities
    from scipy.stats import ttest_rel
    
    # Note: p_values is a full dataframe, so df.loc["NFL","NBA"] should be the same as df.loc["NBA","NFL"] and
    # df.loc["NFL","NFL"] should return np.nan
    sports = ['NFL', 'NBA', 'NHL', 'MLB']
    p_values = pd.DataFrame({k:np.nan for k in sports}, index=sports)
    
    def generate(cat_a, cat_b, p_values):
        first = cat_a.lower() + '_ratio'
        second = cat_b.lower()+'_ratio'

        qualified_df = cities[(cities[first] > 0) & (cities[second] > 0)]
        teststat, pval = ttest_rel(qualified_df[first], qualified_df[second])
        p_values.loc[cat_a][cat_b] = pval
        p_values.loc[cat_b][cat_a] = pval

    for k in sports:
        for j in sports:
            if (k != j):
                generate(k, j, p_values)
    
    assert abs(p_values.loc["NBA", "NHL"] - 0.02) <= 1e-2, "The NBA-NHL p-value should be around 0.02"
    assert abs(p_values.loc["MLB", "NFL"] - 0.80) <= 1e-2, "The MLB-NFL p-value should be around 0.80"
    return p_values


# In[ ]:





# In[33]:


sports_team_performance()


# In[ ]:




