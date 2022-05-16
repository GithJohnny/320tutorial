---
jupyter:
  kernelspec:
    display_name: Python 3 (ipykernel)
    language: python
    name: python3
  language_info:
    codemirror_mode:
      name: ipython
      version: 3
    file_extension: .py
    mimetype: text/x-python
    name: python
    nbconvert_exporter: python
    pygments_lexer: ipython3
    version: 3.9.7
  nbformat: 4
  nbformat_minor: 5
---

::: {.cell .raw}
```{=ipynb}
---
layout: post
title: Blogging Like a Hacker
---
```
:::

::: {.cell .code execution_count="182"}
``` {.python}
import requests
import json
import sys
import matplotlib.pyplot as plt
from matplotlib.dates import drange
from datetime import datetime, timedelta
import numpy as np
import pandas as pd
from tqdm import tqdm
import os
import math
import time
import statsmodels.api as sm
import matplotlib.dates as mdates
from patsy import dmatrices
```
:::

::: {.cell .raw}
```{=ipynb}
%matplotlib notebook
```
:::

::: {.cell .markdown}
# Introduction
:::

::: {.cell .markdown}
Many people play video games, but there is a growing community of people
who enjoy an extra challenge: finishing the game as fast as possible.
For practically every game, there is a speedrunning scene. In the early
days of speedrunning, the practice was incredibly niche and splintered
on various websites. But over the past 2 decades Speedrunning.com has
become the biggest congregation of speedrunning content on the internet.
The top players of my speedrunning scene, Minecraft: Java Edition, have
noted how the number of players/runs during quarantine has exploded, to
the point where moderation became backlogged. So I wanted to download
data from the website and see if this quarantine effect was real, and if
so was it the only variable involved?
:::

::: {.cell .markdown}
# Collecting the data
:::

::: {.cell .markdown}
Thankfully, Speedrun.com provides a rest API for us to pull information
about games, leaderboards, and even individual runs. The API requires a
header that briefly describes the use, which we do here:
:::

::: {.cell .code execution_count="2"}
``` {.python}
init_headers = {'User-Agent': 'uni-project-bot/1.0'}
```
:::

::: {.cell .markdown}
Now we can pull every game that is on Speedrun.com. We can request the
IDs of games, which are used to uniquely identify them, and are useful
for gaining more important information later.
:::

::: {.cell .code execution_count="3"}
``` {.python}
game_IDs = []
offset = 0
# Request every game in batches of 1000
while(True):
    # Request and unpack 1000 games
    URL = 'https://www.speedrun.com/api/v1/games?_bulk=yes&max=1000&offset=' + str(offset)
    response = requests.get(URL, init_headers)
    data = response.json()['data']
    # Add each game to array
    for game in data:
        game_IDs.append(game['id'])
    offset += 1000
    # If length is less than max, we break
    if len(data) < 1000:
        break
print(len(game_IDs))
```

::: {.output .stream .stdout}
    28755
:::
:::

::: {.cell .markdown}
We see that in all, there are over 28 thousand games on Speedrun.com!
With the IDs we can now pull and store all the data we need. Here is the
dataframe we will use, and we collect data in the following categories:

-   Game: This is the international name of the game

-   Category: The category of the speedrun, which defines the
    leaderboard. A game can have multiple types of speedruns, such as
    beating the full game vs. a signle level, and the category
    differentiates these types. It can be split into further
    subcategories with the values.

-   Run Time: The length of the speedrun, defined as whatever time is
    used for rankings on the leaderboard

-   Date: The date the speedrun was submitted (not always present)

-   Values: Set of aspects of a run that can put it in a subcategory,
    such as using glitches vs. glitchless. Only present if it creates a
    subcategory

-   Game ID, Cat ID: Unique identifiers the API uses for finding games
    and categories

Note that the API returns runs that are current to the date of data
collection, so future runs of data collection may look different as it
will include runs which did not exist at the time I collected.
:::

::: {.cell .code execution_count="4"}
``` {.python}
df = pd.DataFrame(columns = ['Game','Category','Run Time','Date','Values', 'Game ID', 'Cat ID'])
```
:::

::: {.cell .markdown}
Finally, we use our game IDs to collect the data! For each game, we
collect every *verified* run that was ever submitted to a leaderboard.
This means no runs that were rejected. This also means we are
essentially collecting the entire speedrun history of a game.
:::

::: {.cell .code execution_count="5"}
``` {.python}
#game_IDs = ['j1npme6p']
path = os.getcwd()
path += '/FinalData(2)'
# If data is already in directory, load that
if os.path.isfile(path):
    df = pd.read_csv('FinalData(2)')
    df.drop('Unnamed: 0', axis=1, inplace=True)
# Else, collect the data
else:
    maxim = 200 # Max number of runs we pull at a time, 200 is maximum allowed
    sec = 15 # Cooldown time for when 
    track = 0
    # Extracts all runs for each game, stores them in df
    # Currently accounting for crash!!! Starting from where it crashed
    for game_ID in tqdm(game_IDs):
        # Every 100 games save the dataframe to disk
        track += 1
        if track % 500 == 0:
            cwd = os.getcwd()
            path = cwd + "/DataV" + str(track/500)
            df.to_csv(path)
        same = ''
        # Get info about game, categories, and variables
        URL = 'https://www.speedrun.com/api/v1/games/' + str(game_ID) + '?embed=categories.variables'
        response = requests.get(URL,init_headers)
        data = response.json() # This has failed exactly once for reasons unknown

        try:
            data = data['data']
        except:
            # Occurs if we get a throttling error. We wait 15 seconds then try again.
            if 'status' in data and data['status'] == 420:
                while 'status' in data and data['status'] == 420:
                    time.sleep(sec)
                    response = requests.get(URL,init_headers)
                    data = response.json()
                data = data['data']
            else:
                # If other error, print and move on
                # The only error in my case was a game not being found, presumably being deleted between pulling the game and pulling the runs
                print('1b')
                print(data)
                continue
        game = data['names']['international']
        cats = data['categories']['data']

        # Finds all the runs for each category
        for categ in cats:
            cat = categ['id'] # Category ID
            cat_name = categ['name'] # Category Name
            offset = 0
            dir = 'asc'
            fin = ''
            sub_categories = [] # Collection of the variables that define subcategories
            all_vars = categ['variables']['data'] # Collects all variables of a run

            for var in all_vars:
                if var['is-subcategory']:
                    sub_categories.append(var['values']['values'])
            sub_keys = {}
            for s in sub_categories:
                # Assumed no two sub-categories in the same category will have the same variable ID
                temp_dict = dict(s)
                for t in temp_dict.keys():
                    temp_dict[t] = temp_dict[t]['label']
                sub_keys.update(temp_dict)


            # Collect data on every run. 
            while(True):
                # Asks API for verified runs from this category, ordered by date submitted
                URL = 'https://www.speedrun.com/api/v1/runs?game=' + str(game_ID) + '&category=' + str(cat) + '&orderby=submitted&direction=' + str(dir) + '&status=verified&max=' + str(maxim) + '&offset=' + str(offset)
                response = requests.get(URL,init_headers)
                data2 = response.json()
                try:
                    data2 = data2['data']
                except:
                    # Throttling error. Wait 15 seconds and try again.
                    if 'status' in data2 and data2['status'] == 420:
                        while 'status' in data2 and data2['status'] == 420:
                            time.sleep(sec)
                            response = requests.get(URL,init_headers)
                            data2 = response.json()
                        data2 = data2['data']
                    elif 'times' in data2:
                        data2 = data2
                    else:
                        # If other error, print and move on
                        print(2)
                        print(data2)
                        continue


                for run in data2:
                    # Add game, category, time, date, and options
                    sub_cat = set()
                    # We store the label of the subcategory for ease of reading
                    for var in run['values'].values():
                        if var in sub_keys:
                            sub_cat.add(sub_keys[var])
                    df.loc[len(df.index)] = [game, cat_name, run['times']['primary_t'], run['date'], sub_cat, game_ID, cat]


                # If length of collected data is smaller than maximum we can collect, we're at the end of the list and break
                if len(data2) < maxim:
                    break

                # Need to work from the back of the list if the offset is more than 10k (known bug)
                if offset + maxim >= 10000:
                    fin = data2[-1]
                    dir = 'desc'
                    offset = 0
                    continue

                # If we're working backwords and find the run we ended on going forward, we've found all runs and break
                if dir == 'desc' and fin in data2:
                    dir = 'asc'
                    fin = ''
                    break

                # If we collect 0 runs we break immediately (happens when no runs in category)
                if(len(data2) == 0):
                    break

                offset += maxim
# Convert the dates from a string to a datetime object    
def time_convert(x):
        if pd.isna(x):
            return np.nan
        try:
            return datetime.strptime(x, '%Y-%m-%d')
        except:
            try:
                return datetime.strptime(x, '%Y-%m-%d')
            except:
                print(type(x))

df['Date'] = [time_convert(x) for x in df['Date']]
df
```

::: {.output .execute_result execution_count="5"}
```{=html}
<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Game</th>
      <th>Category</th>
      <th>Run Time</th>
      <th>Date</th>
      <th>Values</th>
      <th>Game ID</th>
      <th>Cat ID</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Bibi &amp; Tina: New Adventures With Horses</td>
      <td>Main Missions</td>
      <td>3531.0</td>
      <td>2022-04-21</td>
      <td>set()</td>
      <td>ldej22j1</td>
      <td>wdmm094d</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Bibi &amp; Tina: New Adventures With Horses</td>
      <td>Main Missions</td>
      <td>3482.0</td>
      <td>2022-04-22</td>
      <td>set()</td>
      <td>ldej22j1</td>
      <td>wdmm094d</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Bibi &amp; Tina: New Adventures With Horses</td>
      <td>Main Missions</td>
      <td>3396.0</td>
      <td>2022-04-23</td>
      <td>set()</td>
      <td>ldej22j1</td>
      <td>wdmm094d</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Bibi &amp; Tina: New Adventures With Horses</td>
      <td>Main Missions</td>
      <td>3346.0</td>
      <td>2022-04-26</td>
      <td>set()</td>
      <td>ldej22j1</td>
      <td>wdmm094d</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Burger &amp; Frights</td>
      <td>Any%</td>
      <td>906.0</td>
      <td>2021-09-01</td>
      <td>set()</td>
      <td>3698y4ld</td>
      <td>zdnzx59d</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>2580131</th>
      <td>暖雪 Warm Snow</td>
      <td>White Ash% NMG</td>
      <td>1045.0</td>
      <td>2022-04-19</td>
      <td>set()</td>
      <td>v1pxz946</td>
      <td>ndxnwvvk</td>
    </tr>
    <tr>
      <th>2580132</th>
      <td>暖雪 Warm Snow</td>
      <td>Fresh File% NMG</td>
      <td>2569.0</td>
      <td>2022-02-10</td>
      <td>set()</td>
      <td>v1pxz946</td>
      <td>vdoy5my2</td>
    </tr>
    <tr>
      <th>2580133</th>
      <td>暖雪 Warm Snow</td>
      <td>Fresh File% NMG</td>
      <td>2351.0</td>
      <td>2022-04-21</td>
      <td>set()</td>
      <td>v1pxz946</td>
      <td>vdoy5my2</td>
    </tr>
    <tr>
      <th>2580134</th>
      <td>暖雪 Warm Snow</td>
      <td>Fresh File% NMG</td>
      <td>1676.0</td>
      <td>2022-04-21</td>
      <td>set()</td>
      <td>v1pxz946</td>
      <td>vdoy5my2</td>
    </tr>
    <tr>
      <th>2580135</th>
      <td>鬼神童子ZENKI</td>
      <td>Any%</td>
      <td>1390.0</td>
      <td>2021-08-10</td>
      <td>set()</td>
      <td>9d387701</td>
      <td>5dw180ek</td>
    </tr>
  </tbody>
</table>
<p>2580136 rows × 7 columns</p>
</div>
```
:::
:::

::: {.cell .markdown}
Do note how the Run Time column is in seconds. We\'ve collected over 2.5
million runs! Now we want to convert the dates column from strings to
datetime objects
:::

::: {.cell .markdown}
After collecting this data, I realized the genre of a game may be
interesting for this analysis, and so we add that to our data as well.
:::

::: {.cell .code}
``` {.python}
```
:::

::: {.cell .code}
``` {.python}
```
:::

::: {.cell .markdown}
I realized the current world record at the day the run was made could be
important for an analysis, as it is commonly known that how challenging
a world record is to achieve has a big impact in the motivation to break
it, and thus possibly increase the number of runs.
:::

::: {.cell .markdown}
# Exploratory Data Analysis
:::

::: {.cell .markdown}
First, let\'s plot the number of speedruns that were uploaded
approximately every month, for the runs which do have a date.
:::

::: {.cell .code execution_count="6"}
``` {.python}
# Split range of dates in to approximately 1 month bins
bins = int(round((max(df['Date'])-min(df['Date']))/timedelta(weeks = 4.345),0))
```
:::

::: {.cell .markdown}
Note: There is one date in the set which appears wrong (stating it
appears several decades before Speedrun.com existed), and so we will
replace it with an interpolated date from the
:::

::: {.cell .code execution_count="7"}
``` {.python}
print(bins)
```

::: {.output .stream .stdout}
    605
:::
:::

::: {.cell .markdown}
We see we have about 605 months worth of runs, now we can split the data
between these months.
:::

::: {.cell .code execution_count="8"}
``` {.python}
# Cut data into the bins based on submission date
df['Date_Cut'] = pd.cut(df.Date, bins = bins)
# We don't need to know full interval for graphing, take left endpoints
def relabel(x):
    if pd.isna(x):
        return np.nan
    else:
        return x.left

df['Date_Cut'] = [relabel(x) for x in df['Date_Cut']]
```
:::

::: {.cell .markdown}
Finally, we plotthe runs as a bar chart, with a bar for each month.
:::

::: {.cell .code execution_count="9"}
``` {.python}
# Count how many runs fall in each of the cuts
counts = df['Date_Cut'].value_counts()
counts = dict(counts)
# Plot these counts
plt.bar(*zip(*counts.items()), width = 30)
plt.title('Runs Submitted to Speedrun.Com')
plt.xlabel('Date Submitted')
plt.ylabel('Number of runs submitted')
plt.show()
```

::: {.output .display_data}
![](vertopal_da926b06fd514d3083380e1a51185e77/ce4cec2b255983cc1f6fa5404e4d1c4ef0d7fc27.png)
:::
:::

::: {.cell .markdown}
Wow! This graph has several things which jump out, such as how there are
somehow runs which stretch back to the 70\'s. We can note though how
there are virtually no runs visible at this scale until 2005 or so, so
let\'s graph from there. Speedrun.com didn\'t exist until 2014, so
let\'s consider runs which were submitted from the start of that year
:::

::: {.cell .code execution_count="139"}
``` {.python}
# Subset of more recent data
rec = df[df['Date']  >= '01-01-14']

# Count how many runs fall in each of the cuts
tot_counts = rec['Date_Cut'].value_counts()
tot_counts = dict(tot_counts)
# Plot these counts
plt.bar(*zip(*tot_counts.items()), width = 31)
plt.title('Runs Submitted to Speedrun.Com')
plt.xlabel('Date Submitted')
plt.ylabel('Number of runs submitted')
plt.show()
```

::: {.output .display_data}
![](vertopal_da926b06fd514d3083380e1a51185e77/4f3273abebc505bfcaf86e69542138897c2c543c.png)
:::
:::

::: {.cell .markdown}
We see a rather large spike in 2020, that increases so rapidly it could
be exponential. We can test this theory with a graph with a logarithmic
y-axis:
:::

::: {.cell .code execution_count="179"}
``` {.python}
plt.bar(*zip(*tot_counts.items()), width = 31)
plt.title('Runs Submitted to Speedrun.Com')
plt.xlabel('Date Submitted')
plt.yscale('log')
plt.ylabel('Number of runs submitted (log scale)')
plt.show()
```

::: {.output .display_data}
![](vertopal_da926b06fd514d3083380e1a51185e77/3194875d36f781125b56e19b1331d7c99d44c43d.png)
:::
:::

::: {.cell .markdown}
Look at that! We can see a nearly linear relationship with this scale,
suggesting the number of runs submitted to Speedrun.com is approximately
exponential. Let\'s do the same thing with Minecraft
:::

::: {.cell .markdown}
At this scale, we can see an explosion in the speedrunning scene as a
whole, starting gradually from 2014, slowing around 2018, before a huge
and sustained spike in submitted speedruns in 2020. We can also see if
this matches for Minecraft as well.
:::

::: {.cell .code}
``` {.python}
```
:::

::: {.cell .code execution_count="142"}
``` {.python}
# All runs with game ID associated with Minecraft: JE
mine = rec[rec['Game ID'] == 'j1npme6p']

# Count how many runs fall in each of the cuts
counts = mine['Date_Cut'].value_counts()
counts = dict(counts)
# Plot these counts
plt.bar(*zip(*counts.items()), width = 31)
plt.title('Runs Submitted to Minecraft Leaderboards')
plt.xlabel('Date Submitted')
plt.ylabel('Number of runs submitted')
plt.show()
plt.bar(*zip(*counts.items()), width = 31)
plt.title('Runs Submitted to Minecraft Leaderboards')
plt.yscale('log')
plt.xlabel('Date Submitted')
plt.ylabel('Number of runs submitted')
plt.show()
```

::: {.output .display_data}
![](vertopal_da926b06fd514d3083380e1a51185e77/49e730d82ab1175b2a5804626668dd4f1e8f5bbd.png)
:::

::: {.output .display_data}
![](vertopal_da926b06fd514d3083380e1a51185e77/5bd7b2c8ae265a3c70c7e9ca1973d24250b6bad5.png)
:::
:::

::: {.cell .markdown}
Here we can see why people believed Minecraft speedrunning really took
off after quarantine began. We see a modest number of runs continuously
submitted up until 2019, then a gradual growth through 2020, then an
explosion going into 2021. However the log graph shows the key
differences between Minecraft and the Speedrun.com as a whole. While we
could draw a general linear trend from 2013 to 2020, it appears to be
quite weak. More importantly, we see a huge spike starting in 2020 and
going into 2021, even on the log graph. This suggests that Minecraft
surged in popularity exceedingly much, compared to its earlier years.
Further, we see a sharp decline starting in 2021 and leading into 2022.
These last two features differ drastically from the results in the
overall Speedrun.com. This suggests that Minecraft\'s speedrunning
popularity is different from the site as a whole, and we can show this
quantitatively with linear regressions.
:::

::: {.cell .markdown}
# Linear Regression
:::

::: {.cell .markdown}
We can use a linear regression to make an exponential fit of the
Speedrun.com data by taking the log of the number of runs per month,
then fitting a linear regression with respect to time. First, let\'s
copy the data we want: the months and the number of runs in those months
:::

::: {.cell .code execution_count="143"}
``` {.python}
tot_freq = pd.DataFrame.from_dict([dict(tot_counts)]).melt()
tot_freq.rename(columns = {'variable': 'Month', 'value': 'Count'}, inplace = True)
# Take log
log_count = {k: math.log(v) for k, v in counts.items()}
#log_count = counts.apply(lambda x: math.log(x))
tot_freq["Count"] = tot_freq['Count'].apply(lambda x: math.log10(x))
# Change how time is represented as datetime objects don't fit well with statsmodels
copy = tot_freq['Month'].copy()
tot_freq['Month']=mdates.date2num(tot_freq['Month'])
X = tot_freq['Month']
X = sm.add_constant(X)
mod = sm.OLS(tot_freq['Count'], X)
res = mod.fit()
```
:::

::: {.cell .code execution_count="144"}
``` {.python}
res.params
```

::: {.output .execute_result execution_count="144"}
    const   -5.562301
    Month    0.000554
    dtype: float64
:::
:::

::: {.cell .code execution_count="145"}
``` {.python}
res.summary2().tables[1]['P>|t|']
```

::: {.output .execute_result execution_count="145"}
    const    7.883564e-34
    Month    2.025207e-54
    Name: P>|t|, dtype: float64
:::
:::

::: {.cell .code execution_count="146"}
``` {.python}
tot_freq['res'] = res.resid
tot_freq['fit'] = res.fittedvalues
tot_freq['Month'] = copy
tot_freq = tot_freq.sort_values(by = 'Month')
fig,ax = plt.subplots()
ax.bar(tot_freq['Month'], tot_freq['Count'], width = 31)
plt.title('Runs Submitted to Speedrun.com')
plt.xlabel('Date Submitted')
plt.ylabel('Number of runs submitted (log$_{10}$)')
ax2 = plt.twinx()
ax2.set_ylim(ax.get_ylim())
ax2.plot(tot_freq['Month'], tot_freq['fit'], color='r', label='Regression')
plt.show()
```

::: {.output .display_data}
![](vertopal_da926b06fd514d3083380e1a51185e77/a37a3ae5a296f55a7359250fde8d85e01335307a.png)
:::
:::

::: {.cell .code execution_count="147"}
``` {.python}
res.rsquared
```

::: {.output .execute_result execution_count="147"}
    0.913492334019323
:::
:::

::: {.cell .code execution_count="148"}
``` {.python}
res.mse_resid
```

::: {.output .execute_result execution_count="148"}
    0.023263681546275207
:::
:::

::: {.cell .code execution_count="149"}
``` {.python}
res.mse_model
```

::: {.output .execute_result execution_count="149"}
    24.320021315512843
:::
:::

::: {.cell .code execution_count="150"}
``` {.python}
res.ssr
```

::: {.output .execute_result execution_count="150"}
    2.3031044730812456
:::
:::

::: {.cell .code execution_count="151"}
``` {.python}
freq = pd.DataFrame.from_dict([dict(counts)]).melt()
freq.rename(columns = {'variable': 'Month', 'value': 'Count'}, inplace = True)
# Take log
log_count = {k: math.log(v) for k, v in counts.items()}
#log_count = counts.apply(lambda x: math.log(x))
freq["Count"] = freq['Count'].apply(lambda x: math.log10(x))
# Change how time is represented as datetime objects don't fit well with statsmodels
copy = freq['Month'].copy()
freq['Month']=mdates.date2num(freq['Month'])
X = freq['Month']
X = sm.add_constant(X)
mod = sm.OLS(freq['Count'], X)
res = mod.fit()
```
:::

::: {.cell .code execution_count="154"}
``` {.python}
res.params
```

::: {.output .execute_result execution_count="154"}
    const   -13.530621
    Month     0.000842
    dtype: float64
:::
:::

::: {.cell .code execution_count="152"}
``` {.python}
freq['res'] = res.resid
freq['fit'] = res.fittedvalues
freq['Month'] = copy
freq = freq.sort_values(by = 'Month')
fig,ax = plt.subplots()
plt.title('Runs Submitted to Minecraft Leaderboards')
plt.xlabel('Date Submitted')
plt.ylabel('Number of runs submitted (log$_{10}$)')
ax.bar(freq['Month'], freq['Count'], width = 31)
ax2 = plt.twinx()
ax2.set_ylim(ax.get_ylim())
ax2.plot(freq['Month'], freq['fit'], color='r', label='Regression')
plt.show()
```

::: {.output .display_data}
![](vertopal_da926b06fd514d3083380e1a51185e77/6411276ae6773a00ed6e3efcb5896b13a66d7923.png)
:::
:::

::: {.cell .markdown}
We see it roughly follows the data, let\'s look at the p-values:
:::

::: {.cell .code execution_count="155"}
``` {.python}
res.summary2().tables[1]['P>|t|']
```

::: {.output .execute_result execution_count="155"}
    const    8.032060e-21
    Month    3.208438e-23
    Name: P>|t|, dtype: float64
:::
:::

::: {.cell .markdown}
These are miniscule, showing there is certainly a relationship between
number of speedruns and time. However these values are quite different
than those of the overall speedrunning community (STANDARDIZE BOTH AND
COMPARE) so there must be something about minecraft affecting its
results
:::

::: {.cell .code execution_count="156"}
``` {.python}
res.mse_model
```

::: {.output .execute_result execution_count="156"}
    53.560719204703645
:::
:::

::: {.cell .code execution_count="157"}
``` {.python}
res.rsquared
```

::: {.output .execute_result execution_count="157"}
    0.6472904994983575
:::
:::

::: {.cell .code execution_count="158"}
``` {.python}
res.ssr
```

::: {.output .execute_result execution_count="158"}
    29.185310972183814
:::
:::

::: {.cell .markdown}
There must be another variable involved that explains Minecraft\'s surge
and decline in runs. While quarantine obviously played a part, I suggest
another variable which boosted Minecraft only until its peak: Dream. To
summarize, Dream is a very popular Minecraft Youtuber who, from 2019
through 2020, was Minecraft\'s most popular speedrunner. However, in
December of 2020 it was found that [Dream had
cheated](https://mcspeedrun.com/dream.pdf) on his speedruns leading to
him publically disavowing the community on Speedrun.com. We can notice
how close December 2020 is to the peak we see of Minecraft speedrunning,
so perhaps this could be an explantory variable.
:::

::: {.cell .markdown}
Dream uploaded his [first world
record](https://www.youtube.com/watch?v=CFkv6DtKf3w) on March 16, 2020,
and the proof of his cheating were published on December 11, 2020. Thus
we can consider time between these two to be \"peak dream influence.\"
We can add whether a month occured between these two dates to our model.
:::

::: {.cell .code execution_count="159"}
``` {.python}
freq['Month']=mdates.date2num(freq['Month'])
start = mdates.datestr2num('03/16/2020')
#mdates.date2num(freq['Month']) 'Mar 16, 2020'
end = mdates.datestr2num('12/11/2020')
freq['Dream'] = freq['Month'].between(start,end)
freq['Dream'] = freq['Dream'].apply(lambda x: 1 if x else 0)
freq.head()
```

::: {.output .execute_result execution_count="159"}
```{=html}
<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Month</th>
      <th>Count</th>
      <th>res</th>
      <th>fit</th>
      <th>Dream</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>94</th>
      <td>16078.661157</td>
      <td>0.000000</td>
      <td>-0.006438</td>
      <td>0.006438</td>
      <td>0</td>
    </tr>
    <tr>
      <th>76</th>
      <td>16109.054545</td>
      <td>0.477121</td>
      <td>0.445095</td>
      <td>0.032027</td>
      <td>0</td>
    </tr>
    <tr>
      <th>90</th>
      <td>16139.447934</td>
      <td>0.301030</td>
      <td>0.243414</td>
      <td>0.057616</td>
      <td>0</td>
    </tr>
    <tr>
      <th>96</th>
      <td>16169.841322</td>
      <td>0.000000</td>
      <td>-0.083205</td>
      <td>0.083205</td>
      <td>0</td>
    </tr>
    <tr>
      <th>80</th>
      <td>16200.234711</td>
      <td>0.477121</td>
      <td>0.368327</td>
      <td>0.108794</td>
      <td>0</td>
    </tr>
  </tbody>
</table>
</div>
```
:::
:::

::: {.cell .markdown}
We want to add an interaction term, as we are suggesting that the growth
of speedrunning with respect to time changed when dream was popular.
:::

::: {.cell .code execution_count="160"}
``` {.python}
y,X = dmatrices('Count ~ Month*Dream',freq, return_type = 'dataframe')
y = np.ravel(y)
X.head()
```

::: {.output .execute_result execution_count="160"}
```{=html}
<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Intercept</th>
      <th>Month</th>
      <th>Dream</th>
      <th>Month:Dream</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>94</th>
      <td>1.0</td>
      <td>16078.661157</td>
      <td>0.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>76</th>
      <td>1.0</td>
      <td>16109.054545</td>
      <td>0.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>90</th>
      <td>1.0</td>
      <td>16139.447934</td>
      <td>0.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>96</th>
      <td>1.0</td>
      <td>16169.841322</td>
      <td>0.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>80</th>
      <td>1.0</td>
      <td>16200.234711</td>
      <td>0.0</td>
      <td>0.0</td>
    </tr>
  </tbody>
</table>
</div>
```
:::
:::

::: {.cell .markdown}
Now we fit the model
:::

::: {.cell .code execution_count="161"}
``` {.python}
mod = sm.OLS(y,X)
fit = mod.fit()
```
:::

::: {.cell .code execution_count="162"}
``` {.python}
fit.params
```

::: {.output .execute_result execution_count="162"}
    Intercept     -12.196165
    Month           0.000762
    Dream         -35.893774
    Month:Dream     0.001983
    dtype: float64
:::
:::

::: {.cell .code execution_count="166"}
``` {.python}
freq['res'] = fit.resid
freq['fit'] = fit.fittedvalues
freq['Month'] = copy
freq = freq.sort_values(by = 'Month')
fig,ax = plt.subplots()
ax.bar(freq['Month'], freq['Count'], width = 31)
ax2 = plt.twinx()
ax2.set_ylim(ax.get_ylim())
ax2.plot(freq['Month'], freq['fit'], color='k', label='Regression')
plt.show()
```

::: {.output .display_data}
![](vertopal_da926b06fd514d3083380e1a51185e77/ba27d3a2d35dfa2a0b9a4520d64a2e2ce01a2d63.png)
:::
:::

::: {.cell .code execution_count="167"}
``` {.python}
fit.summary2().tables[1]['P>|t|']
```

::: {.output .execute_result execution_count="167"}
    Intercept      1.069543e-18
    Month          6.716696e-21
    Dream          3.788544e-01
    Month:Dream    3.690292e-01
    Name: P>|t|, dtype: float64
:::
:::

::: {.cell .markdown}
These p-values suggest the dream sweetspot is significant! but what if
we also added the 5 month period before Dream admitted to cheating?This
is the period after he was caught cheating, before he [admitted to
it](https://www.looper.com/432321/dreams-minecraft-speedrun-cheating-scandal-explained/)
on May 30, 2021.
:::

::: {.cell .code}
``` {.python}
```
:::

::: {.cell .markdown}
Let\'s also plot the residuals
:::

::: {.cell .code}
``` {.python}
```
:::

::: {.cell .code execution_count="169"}
``` {.python}
#We see
```
:::

::: {.cell .code execution_count="170"}
``` {.python}
freq['Month']=mdates.date2num(freq['Month'])
very_end = mdates.datestr2num('05/30/2021')
freq['Cheat'] = freq['Month'].apply(lambda x: 1 if x > end else 0)
#freq['Cheat'] = freq['Cheat'].apply(lambda x: 1 if x else 0)
freq.head()
```

::: {.output .execute_result execution_count="170"}
```{=html}
<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Month</th>
      <th>Count</th>
      <th>res</th>
      <th>fit</th>
      <th>Dream</th>
      <th>Cheat</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>94</th>
      <td>16078.661157</td>
      <td>0.000000</td>
      <td>-0.058446</td>
      <td>0.058446</td>
      <td>0</td>
      <td>0</td>
    </tr>
    <tr>
      <th>76</th>
      <td>16109.054545</td>
      <td>0.477121</td>
      <td>0.395511</td>
      <td>0.081610</td>
      <td>0</td>
      <td>0</td>
    </tr>
    <tr>
      <th>90</th>
      <td>16139.447934</td>
      <td>0.301030</td>
      <td>0.196255</td>
      <td>0.104775</td>
      <td>0</td>
      <td>0</td>
    </tr>
    <tr>
      <th>96</th>
      <td>16169.841322</td>
      <td>0.000000</td>
      <td>-0.127940</td>
      <td>0.127940</td>
      <td>0</td>
      <td>0</td>
    </tr>
    <tr>
      <th>80</th>
      <td>16200.234711</td>
      <td>0.477121</td>
      <td>0.326016</td>
      <td>0.151105</td>
      <td>0</td>
      <td>0</td>
    </tr>
  </tbody>
</table>
</div>
```
:::
:::

::: {.cell .code execution_count="171"}
``` {.python}
y,X = dmatrices('Count ~ Month*Dream + Month*Cheat',freq, return_type = 'dataframe')
y = np.ravel(y)
mod = sm.OLS(y,X)
fit = mod.fit()
```
:::

::: {.cell .code execution_count="172"}
``` {.python}
fit.params
```

::: {.output .execute_result execution_count="172"}
    Intercept      -6.464687
    Month           0.000423
    Dream         -41.625253
    Month:Dream     0.002322
    Cheat          61.912920
    Month:Cheat    -0.003224
    dtype: float64
:::
:::

::: {.cell .code execution_count="173"}
``` {.python}
fit.summary2().tables[1]['P>|t|']
```

::: {.output .execute_result execution_count="173"}
    Intercept      2.191631e-07
    Month          9.302297e-09
    Dream          1.660017e-01
    Month:Dream    1.535356e-01
    Cheat          5.530645e-06
    Month:Cheat    7.928875e-06
    Name: P>|t|, dtype: float64
:::
:::

::: {.cell .code execution_count="174"}
``` {.python}
freq['res'] = fit.resid
freq['fit'] = fit.fittedvalues
freq['Month'] = copy
freq = freq.sort_values(by = 'Month')
fig,ax = plt.subplots()
ax.bar(freq['Month'], freq['Count'], width = 30)
ax2 = plt.twinx()
ax2.set_ylim(ax.get_ylim())
ax2.plot(freq['Month'], freq['fit'], color='k', label='Regression')
plt.show()
```

::: {.output .display_data}
![](vertopal_da926b06fd514d3083380e1a51185e77/a1a65abd12308f0b7d4ee875055030eccbc62ccd.png)
:::
:::

::: {.cell .code}
``` {.python}
```
:::

::: {.cell .code execution_count="36"}
``` {.python}
freq
```

::: {.output .execute_result execution_count="36"}
```{=html}
<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Month</th>
      <th>Count</th>
      <th>res</th>
      <th>fit</th>
      <th>Dream</th>
      <th>Cheat</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>78</th>
      <td>2013-02-08 08:00:47.603305728</td>
      <td>1.098612</td>
      <td>0.629268</td>
      <td>0.469344</td>
      <td>0</td>
      <td>0</td>
    </tr>
    <tr>
      <th>83</th>
      <td>2013-03-10 17:27:16.363636480</td>
      <td>1.098612</td>
      <td>0.599834</td>
      <td>0.498778</td>
      <td>0</td>
      <td>0</td>
    </tr>
    <tr>
      <th>88</th>
      <td>2013-04-10 02:53:45.123966976</td>
      <td>0.693147</td>
      <td>0.164936</td>
      <td>0.528211</td>
      <td>0</td>
      <td>0</td>
    </tr>
    <tr>
      <th>76</th>
      <td>2013-05-10 12:20:13.884297472</td>
      <td>1.098612</td>
      <td>0.540967</td>
      <td>0.557645</td>
      <td>0</td>
      <td>0</td>
    </tr>
    <tr>
      <th>103</th>
      <td>2013-06-09 21:46:42.644627968</td>
      <td>0.000000</td>
      <td>-0.587078</td>
      <td>0.587078</td>
      <td>0</td>
      <td>0</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>15</th>
      <td>2021-12-05 00:47:36.198347008</td>
      <td>6.049733</td>
      <td>0.669827</td>
      <td>5.379907</td>
      <td>0</td>
      <td>1</td>
    </tr>
    <tr>
      <th>16</th>
      <td>2022-01-04 10:14:04.958677760</td>
      <td>5.973810</td>
      <td>0.789882</td>
      <td>5.183928</td>
      <td>0</td>
      <td>1</td>
    </tr>
    <tr>
      <th>21</th>
      <td>2022-02-03 19:40:33.719008256</td>
      <td>5.129899</td>
      <td>0.141950</td>
      <td>4.987949</td>
      <td>0</td>
      <td>1</td>
    </tr>
    <tr>
      <th>31</th>
      <td>2022-03-06 05:07:02.479338752</td>
      <td>3.688879</td>
      <td>-1.103091</td>
      <td>4.791970</td>
      <td>0</td>
      <td>1</td>
    </tr>
    <tr>
      <th>30</th>
      <td>2022-04-05 14:33:31.239669504</td>
      <td>3.688879</td>
      <td>-0.907112</td>
      <td>4.595991</td>
      <td>0</td>
      <td>1</td>
    </tr>
  </tbody>
</table>
<p>105 rows × 6 columns</p>
</div>
```
:::
:::

::: {.cell .code execution_count="37"}
``` {.python}
copy
```

::: {.output .execute_result execution_count="37"}
    0     2021-02-04 02:22:48.595041280
    1     2021-03-06 11:49:17.355371776
    2     2021-01-04 16:56:19.834710784
    3     2021-04-05 21:15:46.115702528
    4     2021-05-06 06:42:14.876033024
                       ...             
    100   2015-12-08 17:01:05.454545408
    101   2016-03-08 21:20:31.735537152
    102   2014-04-09 20:11:30.247933952
    103   2013-06-09 21:46:42.644627968
    104   2013-12-09 06:25:35.206611456
    Name: Month, Length: 105, dtype: datetime64[ns]
:::
:::

::: {.cell .code execution_count="38"}
``` {.python}
freq['res'] = fit.resid
fig,ax = plt.subplots()
ax.bar(copy, freq['res'], width = 30)
plt.show()
```

::: {.output .display_data}
![](vertopal_da926b06fd514d3083380e1a51185e77/463d2c19f663d6216ae62fd17646b5595cf9ac14.png)
:::
:::

::: {.cell .code}
``` {.python}
```
:::

::: {.cell .code execution_count="39"}
``` {.python}
freq
```

::: {.output .execute_result execution_count="39"}
```{=html}
<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Month</th>
      <th>Count</th>
      <th>res</th>
      <th>fit</th>
      <th>Dream</th>
      <th>Cheat</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>78</th>
      <td>2013-02-08 08:00:47.603305728</td>
      <td>1.098612</td>
      <td>0.629268</td>
      <td>0.469344</td>
      <td>0</td>
      <td>0</td>
    </tr>
    <tr>
      <th>83</th>
      <td>2013-03-10 17:27:16.363636480</td>
      <td>1.098612</td>
      <td>0.599834</td>
      <td>0.498778</td>
      <td>0</td>
      <td>0</td>
    </tr>
    <tr>
      <th>88</th>
      <td>2013-04-10 02:53:45.123966976</td>
      <td>0.693147</td>
      <td>0.164936</td>
      <td>0.528211</td>
      <td>0</td>
      <td>0</td>
    </tr>
    <tr>
      <th>76</th>
      <td>2013-05-10 12:20:13.884297472</td>
      <td>1.098612</td>
      <td>0.540967</td>
      <td>0.557645</td>
      <td>0</td>
      <td>0</td>
    </tr>
    <tr>
      <th>103</th>
      <td>2013-06-09 21:46:42.644627968</td>
      <td>0.000000</td>
      <td>-0.587078</td>
      <td>0.587078</td>
      <td>0</td>
      <td>0</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>15</th>
      <td>2021-12-05 00:47:36.198347008</td>
      <td>6.049733</td>
      <td>0.669827</td>
      <td>5.379907</td>
      <td>0</td>
      <td>1</td>
    </tr>
    <tr>
      <th>16</th>
      <td>2022-01-04 10:14:04.958677760</td>
      <td>5.973810</td>
      <td>0.789882</td>
      <td>5.183928</td>
      <td>0</td>
      <td>1</td>
    </tr>
    <tr>
      <th>21</th>
      <td>2022-02-03 19:40:33.719008256</td>
      <td>5.129899</td>
      <td>0.141950</td>
      <td>4.987949</td>
      <td>0</td>
      <td>1</td>
    </tr>
    <tr>
      <th>31</th>
      <td>2022-03-06 05:07:02.479338752</td>
      <td>3.688879</td>
      <td>-1.103091</td>
      <td>4.791970</td>
      <td>0</td>
      <td>1</td>
    </tr>
    <tr>
      <th>30</th>
      <td>2022-04-05 14:33:31.239669504</td>
      <td>3.688879</td>
      <td>-0.907112</td>
      <td>4.595991</td>
      <td>0</td>
      <td>1</td>
    </tr>
  </tbody>
</table>
<p>105 rows × 6 columns</p>
</div>
```
:::
:::

::: {.cell .markdown}
However, unlike the general trend we saw before, Minecraft exceeded in
popularity, even on the logarithmic scale. Weirder, we see a steep
dropoff starting in 2021. This suggests Minecraft\'s speedrunning
popularity may be different to the overall speedrunning scene. Let\'s
investigate with a linear model.
:::

::: {.cell .markdown}
So we see time plays an important factor here, but to what extent? Well,
let\'s attempt a linear regression. Let\'s first begin with Minecraft,
and can generalize for all the other games later. These are the
variables I will immediately consider: the date submitted, the category,
the variables (aka the subcategory), and if the date is after March 1,
2020 (meaning the runner would likely be living in quarantine and/or a
pandemic).
:::
