{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 1,
   "id": "98a8c835-8c11-4eb4-b4d3-7ce0505b201a",
   "metadata": {},
   "outputs": [
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "/opt/conda/lib/python3.9/site-packages/statsmodels/compat/pandas.py:65: FutureWarning: pandas.Int64Index is deprecated and will be removed from pandas in a future version. Use pandas.Index with the appropriate dtype instead.\n",
      "  from pandas import Int64Index as NumericIndex\n"
     ]
    }
   ],
   "source": [
    "import requests\n",
    "import json\n",
    "import sys\n",
    "import matplotlib.pyplot as plt\n",
    "from matplotlib.dates import drange\n",
    "from datetime import datetime, timedelta\n",
    "import numpy as np\n",
    "import pandas as pd\n",
    "from tqdm import tqdm\n",
    "import os\n",
    "import math\n",
    "import time\n",
    "import statsmodels.api as sm\n",
    "import matplotlib.dates as mdates\n",
    "from patsy import dmatrices"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "eaa2ddaa-2423-4471-92af-40889f1525d9",
   "metadata": {},
   "source": [
    "# Introduction"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "2c493cdf-0623-48be-b150-7f487474e09d",
   "metadata": {},
   "source": [
    "Many people play video games, but there is a growing community of people who enjoy an extra challenge: finishing the game as fast as possible. For practically every game, there is a speedrunning scene. In the early days of speedrunning, the practice was incredibly niche and splintered on various websites. But over the past 2 decades Speedrunning.com has become the biggest congregation of speedrunning content on the internet. The top players of my speedrunning scene, Minecraft: Java Edition, have noted how the number of players/runs during quarantine has exploded, to the point where moderation became backlogged. So I wanted to download data from the website and see if this quarantine effect was real, and if so was it the only variable involved?"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "166b956f-365e-40e4-8377-062028af977c",
   "metadata": {},
   "source": [
    "# Collecting the data"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "56d15fc2-66cf-46b4-983b-e6511f80d231",
   "metadata": {},
   "source": [
    "Thankfully, Speedrun.com provides a rest API for us to pull information about games, leaderboards, and even individual runs. The API requires a header that briefly describes the use, which we do here:"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 2,
   "id": "e076162e-8191-46cf-97ea-6219836b08d2",
   "metadata": {},
   "outputs": [],
   "source": [
    "init_headers = {'User-Agent': 'uni-project-bot/1.0'}"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "4012efb9-3551-480e-89b1-3630b31d93df",
   "metadata": {},
   "source": [
    "Now we can pull every game that is on Speedrun.com. We can request the IDs of games, which are used to uniquely identify them, and are useful for gaining more important information later. "
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 3,
   "id": "b858ee1a-a187-43d6-88c7-325a8d1724d1",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "28755\n"
     ]
    }
   ],
   "source": [
    "game_IDs = []\n",
    "offset = 0\n",
    "# Request every game in batches of 1000\n",
    "while(True):\n",
    "    # Request and unpack 1000 games\n",
    "    URL = 'https://www.speedrun.com/api/v1/games?_bulk=yes&max=1000&offset=' + str(offset)\n",
    "    response = requests.get(URL, init_headers)\n",
    "    data = response.json()['data']\n",
    "    # Add each game to array\n",
    "    for game in data:\n",
    "        game_IDs.append(game['id'])\n",
    "    offset += 1000\n",
    "    # If length is less than max, we break\n",
    "    if len(data) < 1000:\n",
    "        break\n",
    "print(len(game_IDs))"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "f723c081-75dd-4cf8-b60f-29a4798d31e1",
   "metadata": {},
   "source": [
    "We see that in all, there are over 28 thousand games on Speedrun.com! With the IDs we can now pull and store all the data we need. Here is the dataframe we will use, and we collect data in the following categories:\n",
    "\n",
    "* Game: This is the international name of the game\n",
    "\n",
    "* Category: The category of the speedrun, which defines the leaderboard. A game can have multiple types of speedruns, such as beating the full game vs. a signle level, and the category differentiates these types. It can be split into further subcategories with the values.\n",
    "\n",
    "* Run Time: The length of the speedrun, defined as whatever time is used for rankings on the leaderboard\n",
    "\n",
    "* Date: The date the speedrun was submitted (not always present)\n",
    "\n",
    "* Values: Set of aspects of a run that can put it in a subcategory, such as using glitches vs. glitchless. Only present if it creates a subcategory\n",
    "\n",
    "* Game ID, Cat ID: Unique identifiers the API uses for finding games and categories\n",
    "\n",
    "Note that the API returns runs that are current to the date of data collection, so future runs of data collection may look different as it will include runs which did not exist at the time I collected. "
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 4,
   "id": "4f802f5b-e67a-4fbb-8219-a4006a458dbe",
   "metadata": {},
   "outputs": [],
   "source": [
    "df = pd.DataFrame(columns = ['Game','Category','Run Time','Date','Values', 'Game ID', 'Cat ID'])"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "01fa6a41-9b98-44f9-8867-176ecdbc82ca",
   "metadata": {},
   "source": [
    "Finally, we use our game IDs to collect the data! For each game, we collect every *verified* run that was ever submitted to a leaderboard. This means no runs that were rejected. This also means we are essentially collecting the entire speedrun history of a game. "
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 5,
   "id": "78257e0a-dd3e-4e72-96a3-7b0fc29ec937",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>Game</th>\n",
       "      <th>Category</th>\n",
       "      <th>Run Time</th>\n",
       "      <th>Date</th>\n",
       "      <th>Values</th>\n",
       "      <th>Game ID</th>\n",
       "      <th>Cat ID</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>0</th>\n",
       "      <td>Bibi &amp; Tina: New Adventures With Horses</td>\n",
       "      <td>Main Missions</td>\n",
       "      <td>3531.0</td>\n",
       "      <td>2022-04-21</td>\n",
       "      <td>set()</td>\n",
       "      <td>ldej22j1</td>\n",
       "      <td>wdmm094d</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>1</th>\n",
       "      <td>Bibi &amp; Tina: New Adventures With Horses</td>\n",
       "      <td>Main Missions</td>\n",
       "      <td>3482.0</td>\n",
       "      <td>2022-04-22</td>\n",
       "      <td>set()</td>\n",
       "      <td>ldej22j1</td>\n",
       "      <td>wdmm094d</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>2</th>\n",
       "      <td>Bibi &amp; Tina: New Adventures With Horses</td>\n",
       "      <td>Main Missions</td>\n",
       "      <td>3396.0</td>\n",
       "      <td>2022-04-23</td>\n",
       "      <td>set()</td>\n",
       "      <td>ldej22j1</td>\n",
       "      <td>wdmm094d</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>3</th>\n",
       "      <td>Bibi &amp; Tina: New Adventures With Horses</td>\n",
       "      <td>Main Missions</td>\n",
       "      <td>3346.0</td>\n",
       "      <td>2022-04-26</td>\n",
       "      <td>set()</td>\n",
       "      <td>ldej22j1</td>\n",
       "      <td>wdmm094d</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>4</th>\n",
       "      <td>Burger &amp; Frights</td>\n",
       "      <td>Any%</td>\n",
       "      <td>906.0</td>\n",
       "      <td>2021-09-01</td>\n",
       "      <td>set()</td>\n",
       "      <td>3698y4ld</td>\n",
       "      <td>zdnzx59d</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>...</th>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>2580131</th>\n",
       "      <td>暖雪 Warm Snow</td>\n",
       "      <td>White Ash% NMG</td>\n",
       "      <td>1045.0</td>\n",
       "      <td>2022-04-19</td>\n",
       "      <td>set()</td>\n",
       "      <td>v1pxz946</td>\n",
       "      <td>ndxnwvvk</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>2580132</th>\n",
       "      <td>暖雪 Warm Snow</td>\n",
       "      <td>Fresh File% NMG</td>\n",
       "      <td>2569.0</td>\n",
       "      <td>2022-02-10</td>\n",
       "      <td>set()</td>\n",
       "      <td>v1pxz946</td>\n",
       "      <td>vdoy5my2</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>2580133</th>\n",
       "      <td>暖雪 Warm Snow</td>\n",
       "      <td>Fresh File% NMG</td>\n",
       "      <td>2351.0</td>\n",
       "      <td>2022-04-21</td>\n",
       "      <td>set()</td>\n",
       "      <td>v1pxz946</td>\n",
       "      <td>vdoy5my2</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>2580134</th>\n",
       "      <td>暖雪 Warm Snow</td>\n",
       "      <td>Fresh File% NMG</td>\n",
       "      <td>1676.0</td>\n",
       "      <td>2022-04-21</td>\n",
       "      <td>set()</td>\n",
       "      <td>v1pxz946</td>\n",
       "      <td>vdoy5my2</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>2580135</th>\n",
       "      <td>鬼神童子ZENKI</td>\n",
       "      <td>Any%</td>\n",
       "      <td>1390.0</td>\n",
       "      <td>2021-08-10</td>\n",
       "      <td>set()</td>\n",
       "      <td>9d387701</td>\n",
       "      <td>5dw180ek</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "<p>2580136 rows × 7 columns</p>\n",
       "</div>"
      ],
      "text/plain": [
       "                                             Game         Category  Run Time  \\\n",
       "0         Bibi & Tina: New Adventures With Horses    Main Missions    3531.0   \n",
       "1         Bibi & Tina: New Adventures With Horses    Main Missions    3482.0   \n",
       "2         Bibi & Tina: New Adventures With Horses    Main Missions    3396.0   \n",
       "3         Bibi & Tina: New Adventures With Horses    Main Missions    3346.0   \n",
       "4                                Burger & Frights             Any%     906.0   \n",
       "...                                           ...              ...       ...   \n",
       "2580131                              暖雪 Warm Snow   White Ash% NMG    1045.0   \n",
       "2580132                              暖雪 Warm Snow  Fresh File% NMG    2569.0   \n",
       "2580133                              暖雪 Warm Snow  Fresh File% NMG    2351.0   \n",
       "2580134                              暖雪 Warm Snow  Fresh File% NMG    1676.0   \n",
       "2580135                                 鬼神童子ZENKI             Any%    1390.0   \n",
       "\n",
       "              Date Values   Game ID    Cat ID  \n",
       "0       2022-04-21  set()  ldej22j1  wdmm094d  \n",
       "1       2022-04-22  set()  ldej22j1  wdmm094d  \n",
       "2       2022-04-23  set()  ldej22j1  wdmm094d  \n",
       "3       2022-04-26  set()  ldej22j1  wdmm094d  \n",
       "4       2021-09-01  set()  3698y4ld  zdnzx59d  \n",
       "...            ...    ...       ...       ...  \n",
       "2580131 2022-04-19  set()  v1pxz946  ndxnwvvk  \n",
       "2580132 2022-02-10  set()  v1pxz946  vdoy5my2  \n",
       "2580133 2022-04-21  set()  v1pxz946  vdoy5my2  \n",
       "2580134 2022-04-21  set()  v1pxz946  vdoy5my2  \n",
       "2580135 2021-08-10  set()  9d387701  5dw180ek  \n",
       "\n",
       "[2580136 rows x 7 columns]"
      ]
     },
     "execution_count": 5,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "#game_IDs = ['j1npme6p']\n",
    "path = os.getcwd()\n",
    "path += '/FinalData(2)'\n",
    "# If data is already in directory, load that\n",
    "if os.path.isfile(path):\n",
    "    df = pd.read_csv('FinalData(2)')\n",
    "    df.drop('Unnamed: 0', axis=1, inplace=True)\n",
    "# Else, collect the data\n",
    "else:\n",
    "    maxim = 200 # Max number of runs we pull at a time, 200 is maximum allowed\n",
    "    sec = 15 # Cooldown time for when \n",
    "    track = 0\n",
    "    # Extracts all runs for each game, stores them in df\n",
    "    # Currently accounting for crash!!! Starting from where it crashed\n",
    "    for game_ID in tqdm(game_IDs):\n",
    "        # Every 100 games save the dataframe to disk\n",
    "        track += 1\n",
    "        if track % 500 == 0:\n",
    "            cwd = os.getcwd()\n",
    "            path = cwd + \"/DataV\" + str(track/500)\n",
    "            df.to_csv(path)\n",
    "        same = ''\n",
    "        # Get info about game, categories, and variables\n",
    "        URL = 'https://www.speedrun.com/api/v1/games/' + str(game_ID) + '?embed=categories.variables'\n",
    "        response = requests.get(URL,init_headers)\n",
    "        data = response.json() # This has failed exactly once for reasons unknown\n",
    "\n",
    "        try:\n",
    "            data = data['data']\n",
    "        except:\n",
    "            # Occurs if we get a throttling error. We wait 15 seconds then try again.\n",
    "            if 'status' in data and data['status'] == 420:\n",
    "                while 'status' in data and data['status'] == 420:\n",
    "                    time.sleep(sec)\n",
    "                    response = requests.get(URL,init_headers)\n",
    "                    data = response.json()\n",
    "                data = data['data']\n",
    "            else:\n",
    "                # If other error, print and move on\n",
    "                # The only error in my case was a game not being found, presumably being deleted between pulling the game and pulling the runs\n",
    "                print('1b')\n",
    "                print(data)\n",
    "                continue\n",
    "        game = data['names']['international']\n",
    "        cats = data['categories']['data']\n",
    "\n",
    "        # Finds all the runs for each category\n",
    "        for categ in cats:\n",
    "            cat = categ['id'] # Category ID\n",
    "            cat_name = categ['name'] # Category Name\n",
    "            offset = 0\n",
    "            dir = 'asc'\n",
    "            fin = ''\n",
    "            sub_categories = [] # Collection of the variables that define subcategories\n",
    "            all_vars = categ['variables']['data'] # Collects all variables of a run\n",
    "\n",
    "            for var in all_vars:\n",
    "                if var['is-subcategory']:\n",
    "                    sub_categories.append(var['values']['values'])\n",
    "            sub_keys = {}\n",
    "            for s in sub_categories:\n",
    "                # Assumed no two sub-categories in the same category will have the same variable ID\n",
    "                temp_dict = dict(s)\n",
    "                for t in temp_dict.keys():\n",
    "                    temp_dict[t] = temp_dict[t]['label']\n",
    "                sub_keys.update(temp_dict)\n",
    "\n",
    "\n",
    "            # Collect data on every run. \n",
    "            while(True):\n",
    "                # Asks API for verified runs from this category, ordered by date submitted\n",
    "                URL = 'https://www.speedrun.com/api/v1/runs?game=' + str(game_ID) + '&category=' + str(cat) + '&orderby=submitted&direction=' + str(dir) + '&status=verified&max=' + str(maxim) + '&offset=' + str(offset)\n",
    "                response = requests.get(URL,init_headers)\n",
    "                data2 = response.json()\n",
    "                try:\n",
    "                    data2 = data2['data']\n",
    "                except:\n",
    "                    # Throttling error. Wait 15 seconds and try again.\n",
    "                    if 'status' in data2 and data2['status'] == 420:\n",
    "                        while 'status' in data2 and data2['status'] == 420:\n",
    "                            time.sleep(sec)\n",
    "                            response = requests.get(URL,init_headers)\n",
    "                            data2 = response.json()\n",
    "                        data2 = data2['data']\n",
    "                    elif 'times' in data2:\n",
    "                        data2 = data2\n",
    "                    else:\n",
    "                        # If other error, print and move on\n",
    "                        print(2)\n",
    "                        print(data2)\n",
    "                        continue\n",
    "\n",
    "\n",
    "                for run in data2:\n",
    "                    # Add game, category, time, date, and options\n",
    "                    sub_cat = set()\n",
    "                    # We store the label of the subcategory for ease of reading\n",
    "                    for var in run['values'].values():\n",
    "                        if var in sub_keys:\n",
    "                            sub_cat.add(sub_keys[var])\n",
    "                    df.loc[len(df.index)] = [game, cat_name, run['times']['primary_t'], run['date'], sub_cat, game_ID, cat]\n",
    "\n",
    "\n",
    "                # If length of collected data is smaller than maximum we can collect, we're at the end of the list and break\n",
    "                if len(data2) < maxim:\n",
    "                    break\n",
    "\n",
    "                # Need to work from the back of the list if the offset is more than 10k (known bug)\n",
    "                if offset + maxim >= 10000:\n",
    "                    fin = data2[-1]\n",
    "                    dir = 'desc'\n",
    "                    offset = 0\n",
    "                    continue\n",
    "\n",
    "                # If we're working backwords and find the run we ended on going forward, we've found all runs and break\n",
    "                if dir == 'desc' and fin in data2:\n",
    "                    dir = 'asc'\n",
    "                    fin = ''\n",
    "                    break\n",
    "\n",
    "                # If we collect 0 runs we break immediately (happens when no runs in category)\n",
    "                if(len(data2) == 0):\n",
    "                    break\n",
    "\n",
    "                offset += maxim\n",
    "# Convert the dates from a string to a datetime object    \n",
    "def time_convert(x):\n",
    "        if pd.isna(x):\n",
    "            return np.nan\n",
    "        try:\n",
    "            return datetime.strptime(x, '%Y-%m-%d')\n",
    "        except:\n",
    "            try:\n",
    "                return datetime.strptime(x, '%Y-%m-%d')\n",
    "            except:\n",
    "                print(type(x))\n",
    "\n",
    "df['Date'] = [time_convert(x) for x in df['Date']]\n",
    "df"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "a31721fa-a984-4bd4-9c63-fbf39240ba1a",
   "metadata": {},
   "source": [
    "Do note how the Run Time column is in seconds. We've collected over 2.5 million runs! Now we want to convert the dates column from strings to datetime objects"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "59644565-06bf-4910-9644-935a173b87eb",
   "metadata": {},
   "source": [
    "After collecting this data, I realized the genre of a game may be interesting for this analysis, and so we add that to our data as well. "
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "8e1d7d17-6a37-4126-828f-20d136ee6fcb",
   "metadata": {},
   "outputs": [],
   "source": []
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "b461f593-8bcd-41f2-8ddb-7ebd0ab672ff",
   "metadata": {},
   "outputs": [],
   "source": []
  },
  {
   "cell_type": "markdown",
   "id": "fb6c0a50-bbd7-43e8-9ce7-cea7d1017b23",
   "metadata": {},
   "source": [
    "I realized the current world record at the day the run was made could be important for an analysis, as it is commonly known that how challenging a world record is to achieve has a big impact in the motivation to break it, and thus possibly increase the number of runs. "
   ]
  },
  {
   "cell_type": "markdown",
   "id": "2335b1cc-d8ba-42be-888b-380abb6955e6",
   "metadata": {},
   "source": [
    "# Exploratory Data Analysis"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "f1be0569-c5ee-4274-91a0-dcd50ef0f77e",
   "metadata": {},
   "source": [
    "First, let's plot the number of speedruns that were uploaded approximately every month, for the runs which do have a date. "
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 6,
   "id": "78f2acd9-d923-4d6f-93b7-ec614d976268",
   "metadata": {},
   "outputs": [],
   "source": [
    "# Split range of dates in to approximately 1 month bins\n",
    "bins = int(round((max(df['Date'])-min(df['Date']))/timedelta(weeks = 4.345),0))"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "91e28141-dedc-4124-a1a8-b3f7b352af78",
   "metadata": {},
   "source": [
    "Note: There is one date in the set which appears wrong (stating it appears several decades before Speedrun.com existed), and so we will replace it with an interpolated date from the "
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 7,
   "id": "f10888ab-7d38-4262-bfca-bb235d2ebc48",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "605\n"
     ]
    }
   ],
   "source": [
    "print(bins)"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "cb87d160-e9a3-4d43-9b2e-7d0eb74cef27",
   "metadata": {},
   "source": [
    "We see we have about 605 months worth of runs, now we can split the data between these months. "
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 8,
   "id": "b0fe8418-3191-44a8-ae7c-ae343d5d31c2",
   "metadata": {},
   "outputs": [],
   "source": [
    "# Cut data into the bins based on submission date\n",
    "df['Date_Cut'] = pd.cut(df.Date, bins = bins)\n",
    "# We don't need to know full interval for graphing, take left endpoints\n",
    "def relabel(x):\n",
    "    if pd.isna(x):\n",
    "        return np.nan\n",
    "    else:\n",
    "        return x.left\n",
    "\n",
    "df['Date_Cut'] = [relabel(x) for x in df['Date_Cut']]"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "c8cf1853-add6-4545-82d4-78e586392ac5",
   "metadata": {},
   "source": [
    "Finally, we plotthe runs as a bar chart, with a bar for each month. "
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 9,
   "id": "3ee273df-d3b2-4b88-95cc-d6e4b30a7d91",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "image/png": "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\n",
      "text/plain": [
       "<Figure size 432x288 with 1 Axes>"
      ]
     },
     "metadata": {
      "needs_background": "light"
     },
     "output_type": "display_data"
    }
   ],
   "source": [
    "# Count how many runs fall in each of the cuts\n",
    "counts = df['Date_Cut'].value_counts()\n",
    "counts = dict(counts)\n",
    "# Plot these counts\n",
    "plt.bar(*zip(*counts.items()), width = 30)\n",
    "plt.title('Runs Submitted to Speedrun.Com')\n",
    "plt.xlabel('Date Submitted')\n",
    "plt.ylabel('Number of runs submitted')\n",
    "plt.show()"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "74c7db7d-c85e-400a-92e0-bad704dabf98",
   "metadata": {},
   "source": [
    "Wow! This graph has several things which jump out, such as how there are somehow runs which stretch back to the 70's. We can note though how there are virtually no runs visible at this scale until 2005 or so, so let's graph from there. Speedrun.com didn't exist until 2014, so let's consider runs which were submitted from the start of that year"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 139,
   "id": "fce89a55-9f23-48bc-ac24-a59954fe79e3",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "image/png": "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\n",
      "text/plain": [
       "<Figure size 432x288 with 1 Axes>"
      ]
     },
     "metadata": {
      "needs_background": "light"
     },
     "output_type": "display_data"
    }
   ],
   "source": [
    "# Subset of more recent data\n",
    "rec = df[df['Date']  >= '01-01-14']\n",
    "\n",
    "# Count how many runs fall in each of the cuts\n",
    "tot_counts = rec['Date_Cut'].value_counts()\n",
    "tot_counts = dict(tot_counts)\n",
    "# Plot these counts\n",
    "plt.bar(*zip(*tot_counts.items()), width = 31)\n",
    "plt.title('Runs Submitted to Speedrun.Com')\n",
    "plt.xlabel('Date Submitted')\n",
    "plt.ylabel('Number of runs submitted')\n",
    "plt.show()"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "886a4bd9-129a-46f7-b43e-d8f5867c580d",
   "metadata": {},
   "source": [
    "We see a rather large spike in 2020, that increases so rapidly it could be exponential. We can test this theory with a graph with a logarithmic y-axis:"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 179,
   "id": "4a3cc520-7d89-4031-b351-216086818446",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "image/png": "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\n",
      "text/plain": [
       "<Figure size 432x288 with 1 Axes>"
      ]
     },
     "metadata": {
      "needs_background": "light"
     },
     "output_type": "display_data"
    }
   ],
   "source": [
    "plt.bar(*zip(*tot_counts.items()), width = 31)\n",
    "plt.title('Runs Submitted to Speedrun.Com')\n",
    "plt.xlabel('Date Submitted')\n",
    "plt.yscale('log')\n",
    "plt.ylabel('Number of runs submitted (log scale)')\n",
    "plt.show()"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "ab329365-06ae-4002-8de1-719f00739f7f",
   "metadata": {},
   "source": [
    "Look at that! We can see a nearly linear relationship with this scale, suggesting the number of runs submitted to Speedrun.com is approximately exponential. Let's do the same thing with Minecraft"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "c41326ed-241d-49a3-9f0e-eac42b258432",
   "metadata": {},
   "source": [
    "At this scale, we can see an explosion in the speedrunning scene as a whole, starting gradually from 2014, slowing around 2018, before a huge and sustained spike in submitted speedruns in 2020. We can also see if this matches for Minecraft as well."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "8a5a3430-ea34-4f5c-b316-2ecb6b8db4c5",
   "metadata": {},
   "outputs": [],
   "source": []
  },
  {
   "cell_type": "code",
   "execution_count": 142,
   "id": "9de4ab73-363d-4201-bc8c-5aabf419f088",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "image/png": "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\n",
      "text/plain": [
       "<Figure size 432x288 with 1 Axes>"
      ]
     },
     "metadata": {
      "needs_background": "light"
     },
     "output_type": "display_data"
    },
    {
     "data": {
      "image/png": "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\n",
      "text/plain": [
       "<Figure size 432x288 with 1 Axes>"
      ]
     },
     "metadata": {
      "needs_background": "light"
     },
     "output_type": "display_data"
    }
   ],
   "source": [
    "# All runs with game ID associated with Minecraft: JE\n",
    "mine = rec[rec['Game ID'] == 'j1npme6p']\n",
    "\n",
    "# Count how many runs fall in each of the cuts\n",
    "counts = mine['Date_Cut'].value_counts()\n",
    "counts = dict(counts)\n",
    "# Plot these counts\n",
    "plt.bar(*zip(*counts.items()), width = 31)\n",
    "plt.title('Runs Submitted to Minecraft Leaderboards')\n",
    "plt.xlabel('Date Submitted')\n",
    "plt.ylabel('Number of runs submitted')\n",
    "plt.show()\n",
    "plt.bar(*zip(*counts.items()), width = 31)\n",
    "plt.title('Runs Submitted to Minecraft Leaderboards')\n",
    "plt.yscale('log')\n",
    "plt.xlabel('Date Submitted')\n",
    "plt.ylabel('Number of runs submitted')\n",
    "plt.show()"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "6ad59280-ea30-4af5-a7bf-7fb7f7448e87",
   "metadata": {},
   "source": [
    "Here we can see why people believed Minecraft speedrunning really took off after quarantine began. We see a modest number of runs continuously submitted up until 2019, then a gradual growth through 2020, then an explosion going into 2021. However the log graph shows the key differences between Minecraft and the Speedrun.com as a whole. While we could draw a general linear trend from 2013 to 2020, it appears to be quite weak. More importantly, we see a huge spike starting in 2020 and going into 2021, even on the log graph. This suggests that Minecraft surged in popularity exceedingly much, compared to its earlier years. Further, we see a sharp decline starting in 2021 and leading into 2022. These last two features differ drastically from the results in the overall Speedrun.com. This suggests that Minecraft's speedrunning popularity is different from the site as a whole, and we can show this quantitatively with linear regressions."
   ]
  },
  {
   "cell_type": "markdown",
   "id": "a32c8379-7d34-4c4a-a88f-facbae193ac5",
   "metadata": {},
   "source": [
    "# Linear Regression"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "ccd9bd6f-5c33-48e4-994c-1ca3f12755ef",
   "metadata": {},
   "source": [
    "We can use a linear regression to make an exponential fit of the Speedrun.com data by taking the log of the number of runs per month, then fitting a linear regression with respect to time. \n",
    "First, let's copy the data we want: the months and the number of runs in those months"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 143,
   "id": "3d6c6527-eb1d-41a5-a390-58b06346bc5d",
   "metadata": {},
   "outputs": [],
   "source": [
    "tot_freq = pd.DataFrame.from_dict([dict(tot_counts)]).melt()\n",
    "tot_freq.rename(columns = {'variable': 'Month', 'value': 'Count'}, inplace = True)\n",
    "# Take log\n",
    "log_count = {k: math.log(v) for k, v in counts.items()}\n",
    "#log_count = counts.apply(lambda x: math.log(x))\n",
    "tot_freq[\"Count\"] = tot_freq['Count'].apply(lambda x: math.log10(x))\n",
    "# Change how time is represented as datetime objects don't fit well with statsmodels\n",
    "copy = tot_freq['Month'].copy()\n",
    "tot_freq['Month']=mdates.date2num(tot_freq['Month'])\n",
    "X = tot_freq['Month']\n",
    "X = sm.add_constant(X)\n",
    "mod = sm.OLS(tot_freq['Count'], X)\n",
    "res = mod.fit()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 144,
   "id": "35804c6f-eb9b-40f3-a946-0b52975b1cc7",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "const   -5.562301\n",
       "Month    0.000554\n",
       "dtype: float64"
      ]
     },
     "execution_count": 144,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "res.params"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 145,
   "id": "e3f4527c-7e16-4749-a154-416fcaffa504",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "const    7.883564e-34\n",
       "Month    2.025207e-54\n",
       "Name: P>|t|, dtype: float64"
      ]
     },
     "execution_count": 145,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "res.summary2().tables[1]['P>|t|']"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 146,
   "id": "288925d2-0f6a-4502-88a6-96b96232ebad",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "image/png": "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\n",
      "text/plain": [
       "<Figure size 432x288 with 2 Axes>"
      ]
     },
     "metadata": {
      "needs_background": "light"
     },
     "output_type": "display_data"
    }
   ],
   "source": [
    "tot_freq['res'] = res.resid\n",
    "tot_freq['fit'] = res.fittedvalues\n",
    "tot_freq['Month'] = copy\n",
    "tot_freq = tot_freq.sort_values(by = 'Month')\n",
    "fig,ax = plt.subplots()\n",
    "ax.bar(tot_freq['Month'], tot_freq['Count'], width = 31)\n",
    "plt.title('Runs Submitted to Speedrun.com')\n",
    "plt.xlabel('Date Submitted')\n",
    "plt.ylabel('Number of runs submitted (log$_{10}$)')\n",
    "ax2 = plt.twinx()\n",
    "ax2.set_ylim(ax.get_ylim())\n",
    "ax2.plot(tot_freq['Month'], tot_freq['fit'], color='r', label='Regression')\n",
    "plt.show()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 147,
   "id": "b540b83e-8c7d-4377-96f7-2bb7c9d8c904",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "0.913492334019323"
      ]
     },
     "execution_count": 147,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "res.rsquared"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 148,
   "id": "b0b7e9aa-80f0-4d7e-8a45-54e6745d1a4f",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "0.023263681546275207"
      ]
     },
     "execution_count": 148,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "res.mse_resid"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 149,
   "id": "1809b39e-0b8e-41ab-b3cf-4f0e8be3c711",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "24.320021315512843"
      ]
     },
     "execution_count": 149,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "res.mse_model"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 150,
   "id": "d028e6e1-8af7-468f-a034-00809bb39de9",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "2.3031044730812456"
      ]
     },
     "execution_count": 150,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "res.ssr"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 151,
   "id": "81230519-69fd-4033-9955-7005f1717ae9",
   "metadata": {},
   "outputs": [],
   "source": [
    "freq = pd.DataFrame.from_dict([dict(counts)]).melt()\n",
    "freq.rename(columns = {'variable': 'Month', 'value': 'Count'}, inplace = True)\n",
    "# Take log\n",
    "log_count = {k: math.log(v) for k, v in counts.items()}\n",
    "#log_count = counts.apply(lambda x: math.log(x))\n",
    "freq[\"Count\"] = freq['Count'].apply(lambda x: math.log10(x))\n",
    "# Change how time is represented as datetime objects don't fit well with statsmodels\n",
    "copy = freq['Month'].copy()\n",
    "freq['Month']=mdates.date2num(freq['Month'])\n",
    "X = freq['Month']\n",
    "X = sm.add_constant(X)\n",
    "mod = sm.OLS(freq['Count'], X)\n",
    "res = mod.fit()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 154,
   "id": "62e98a70-1e15-4bf6-b7af-9dce379e7cc6",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "const   -13.530621\n",
       "Month     0.000842\n",
       "dtype: float64"
      ]
     },
     "execution_count": 154,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "res.params"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 152,
   "id": "4688d7f3-21c6-4ce1-baa2-af9e899a3308",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "image/png": "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\n",
      "text/plain": [
       "<Figure size 432x288 with 2 Axes>"
      ]
     },
     "metadata": {
      "needs_background": "light"
     },
     "output_type": "display_data"
    }
   ],
   "source": [
    "freq['res'] = res.resid\n",
    "freq['fit'] = res.fittedvalues\n",
    "freq['Month'] = copy\n",
    "freq = freq.sort_values(by = 'Month')\n",
    "fig,ax = plt.subplots()\n",
    "plt.title('Runs Submitted to Minecraft Leaderboards')\n",
    "plt.xlabel('Date Submitted')\n",
    "plt.ylabel('Number of runs submitted (log$_{10}$)')\n",
    "ax.bar(freq['Month'], freq['Count'], width = 31)\n",
    "ax2 = plt.twinx()\n",
    "ax2.set_ylim(ax.get_ylim())\n",
    "ax2.plot(freq['Month'], freq['fit'], color='r', label='Regression')\n",
    "plt.show()"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "30934386-90e3-4869-960d-d18dca40396b",
   "metadata": {},
   "source": [
    "We see it roughly follows the data, let's look at the p-values:"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 155,
   "id": "8d6efc5c-5fe0-4965-97bb-984dd68cae74",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "const    8.032060e-21\n",
       "Month    3.208438e-23\n",
       "Name: P>|t|, dtype: float64"
      ]
     },
     "execution_count": 155,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "res.summary2().tables[1]['P>|t|']"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "2d4ed919-3dc9-49f8-a039-80973b3cc79d",
   "metadata": {},
   "source": [
    "These are miniscule, showing there is certainly a relationship between number of speedruns and time. However these values are quite different than those of the overall speedrunning community (STANDARDIZE BOTH AND COMPARE) so there must be something about minecraft affecting its results"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 156,
   "id": "4724f19a-b352-4c4c-bd5f-b34cd173bd44",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "53.560719204703645"
      ]
     },
     "execution_count": 156,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "res.mse_model"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 157,
   "id": "c2590d88-80d0-43e7-873c-2f84b2867d2b",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "0.6472904994983575"
      ]
     },
     "execution_count": 157,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "res.rsquared"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 158,
   "id": "c99e707b-de3d-4040-ad1b-b536a225cec5",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "29.185310972183814"
      ]
     },
     "execution_count": 158,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "res.ssr"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "a66ef508-6128-4eee-8181-5026cd2c5607",
   "metadata": {},
   "source": [
    "There must be another variable involved that explains Minecraft's surge and decline in runs. While quarantine obviously played a part, I suggest another variable which boosted Minecraft only until its peak: Dream. To summarize, Dream is a very popular Minecraft Youtuber who, from 2019 through 2020, was Minecraft's most popular speedrunner. However, in December of 2020 it was found that [Dream had cheated](https://mcspeedrun.com/dream.pdf) on his speedruns leading to him publically disavowing the community on Speedrun.com. We can notice how close December 2020 is to the peak we see of Minecraft speedrunning, so perhaps this could be an explantory variable. "
   ]
  },
  {
   "cell_type": "markdown",
   "id": "61078257-cd57-417c-b7e9-ffc96ea4007d",
   "metadata": {},
   "source": [
    "Dream uploaded his [first world record](https://www.youtube.com/watch?v=CFkv6DtKf3w) on March 16, 2020, and the proof of his cheating were published on December 11, 2020. Thus we can consider time between these two to be \"peak dream influence.\" We can add whether a month occured between these two dates to our model."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 159,
   "id": "661333e7-2534-43ed-982a-00c26dbfa03a",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>Month</th>\n",
       "      <th>Count</th>\n",
       "      <th>res</th>\n",
       "      <th>fit</th>\n",
       "      <th>Dream</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>94</th>\n",
       "      <td>16078.661157</td>\n",
       "      <td>0.000000</td>\n",
       "      <td>-0.006438</td>\n",
       "      <td>0.006438</td>\n",
       "      <td>0</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>76</th>\n",
       "      <td>16109.054545</td>\n",
       "      <td>0.477121</td>\n",
       "      <td>0.445095</td>\n",
       "      <td>0.032027</td>\n",
       "      <td>0</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>90</th>\n",
       "      <td>16139.447934</td>\n",
       "      <td>0.301030</td>\n",
       "      <td>0.243414</td>\n",
       "      <td>0.057616</td>\n",
       "      <td>0</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>96</th>\n",
       "      <td>16169.841322</td>\n",
       "      <td>0.000000</td>\n",
       "      <td>-0.083205</td>\n",
       "      <td>0.083205</td>\n",
       "      <td>0</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>80</th>\n",
       "      <td>16200.234711</td>\n",
       "      <td>0.477121</td>\n",
       "      <td>0.368327</td>\n",
       "      <td>0.108794</td>\n",
       "      <td>0</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "           Month     Count       res       fit  Dream\n",
       "94  16078.661157  0.000000 -0.006438  0.006438      0\n",
       "76  16109.054545  0.477121  0.445095  0.032027      0\n",
       "90  16139.447934  0.301030  0.243414  0.057616      0\n",
       "96  16169.841322  0.000000 -0.083205  0.083205      0\n",
       "80  16200.234711  0.477121  0.368327  0.108794      0"
      ]
     },
     "execution_count": 159,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "freq['Month']=mdates.date2num(freq['Month'])\n",
    "start = mdates.datestr2num('03/16/2020')\n",
    "#mdates.date2num(freq['Month']) 'Mar 16, 2020'\n",
    "end = mdates.datestr2num('12/11/2020')\n",
    "freq['Dream'] = freq['Month'].between(start,end)\n",
    "freq['Dream'] = freq['Dream'].apply(lambda x: 1 if x else 0)\n",
    "freq.head()"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "819dcd2f-2ec6-4613-8e31-5c7056104831",
   "metadata": {},
   "source": [
    "We want to add an interaction term, as we are suggesting that the growth of speedrunning with respect to time changed when dream was popular."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 160,
   "id": "1b097f69-bdff-4e28-9647-455f98262868",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>Intercept</th>\n",
       "      <th>Month</th>\n",
       "      <th>Dream</th>\n",
       "      <th>Month:Dream</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>94</th>\n",
       "      <td>1.0</td>\n",
       "      <td>16078.661157</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>76</th>\n",
       "      <td>1.0</td>\n",
       "      <td>16109.054545</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>90</th>\n",
       "      <td>1.0</td>\n",
       "      <td>16139.447934</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>96</th>\n",
       "      <td>1.0</td>\n",
       "      <td>16169.841322</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>80</th>\n",
       "      <td>1.0</td>\n",
       "      <td>16200.234711</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "    Intercept         Month  Dream  Month:Dream\n",
       "94        1.0  16078.661157    0.0          0.0\n",
       "76        1.0  16109.054545    0.0          0.0\n",
       "90        1.0  16139.447934    0.0          0.0\n",
       "96        1.0  16169.841322    0.0          0.0\n",
       "80        1.0  16200.234711    0.0          0.0"
      ]
     },
     "execution_count": 160,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "y,X = dmatrices('Count ~ Month*Dream',freq, return_type = 'dataframe')\n",
    "y = np.ravel(y)\n",
    "X.head()"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "dca7b1a2-9e26-4f88-95e1-ec98650ab95b",
   "metadata": {},
   "source": [
    "Now we fit the model"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 161,
   "id": "04920352-8b2e-4e9c-ae00-9330e2a4fd7d",
   "metadata": {},
   "outputs": [],
   "source": [
    "mod = sm.OLS(y,X)\n",
    "fit = mod.fit()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 162,
   "id": "f0a82f02-861d-43bc-b374-2492e356752f",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "Intercept     -12.196165\n",
       "Month           0.000762\n",
       "Dream         -35.893774\n",
       "Month:Dream     0.001983\n",
       "dtype: float64"
      ]
     },
     "execution_count": 162,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "fit.params"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 166,
   "id": "608b0135-e12b-42f2-a297-d403ff28379f",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "image/png": "iVBORw0KGgoAAAANSUhEUgAAAYsAAAD4CAYAAAAdIcpQAAAAOXRFWHRTb2Z0d2FyZQBNYXRwbG90bGliIHZlcnNpb24zLjUuMSwgaHR0cHM6Ly9tYXRwbG90bGliLm9yZy/YYfK9AAAACXBIWXMAAAsTAAALEwEAmpwYAAApKElEQVR4nO3deXxU1f3/8dcnGwkJCbKoLMrmgkplLUoBxSpWUdSKFSh1af1KUWu1P62gNWVTK2gVKaLGohZFFFFERatVagERFRBxQRBEEKGGLSEhCdnO748Z7BgTZpLMzJ1k3s/HYx6ZuffMuZ+5Sc5nzrnLMeccIiIih5LgdQAiIhL7lCxERCQoJQsREQlKyUJERIJSshARkaCSvNpwQkKCS0tL82rzIiINUlFRkXPORf2LvmfJIi0tjf3793u1eRGRBsnMir3YroahREQkKCULEREJSslCRESCUrIQEZGglCxERCQoJQsREQlKyUJERIJSshARkaCULEREJCjPruAWEamvjuMWVbv8q7vPi3IkjZ96FiIiElTQZGFmqWb2vpl9ZGafmtnEasqYmU03s41mttbMekUmXBEROZRItdmhDEMdAH7qnCs0s2RgmZm95pxbEVDmXOBY/+MU4CH/TxGRsKpp6KmmMnE4JBWRNjtoz8L5FPpfJvsfrkqxC4HZ/rIrgOZm1iaUTyUiIuETqTY7pGMWZpZoZmuAXOBfzrn3qhRpB3wd8Hqbf1nVekab2UozW1leXh7KpkVEADhw4IDXIcSKpIPtqP8xumqBcLXZgUJKFs65CudcD6A90NfMulWNrbq3VVNPjnOuj3OuT1KSTsQSkdC88847ZGZmsmrVKq9DiQXlB9tR/yOnaoFwtdmBanU2lHMuD3gbOKfKqm3AUQGv2wPba1O3iEh1nHPcfPPNlJaWsnnzZq/DaVDC2WaHcjZUazNr7n+eBpwFfF6l2EvA5f4j7KcC+c65HcHqFhEJ5oUXXmDFCt+x2cLCwiClJVJttjl3yJ4HZnYy8A8gEV9ymeecm2RmYwCccw+bmQEz8GWvIuDXzrmVh6o3PT3daVpVETmUsrIyunXrxqYde6ko2MlhZ/2WzN5D61xfYzgzysyKnHPph1gfkTY76IED59xaoGc1yx8OeO6A64LVJSJSG7NmzWLDhg20unAcuxbejSsr8TqkmBepNltXcItITCosLGTChAkMGDCApsf3B0ugslTJwis6JUlEYkbgxXRXpa/m22+/ZcGCBYxcuAdLScOVFoet/sYwJBVN6lmISMyp2J/H1KlT+fnPf06/fv0ASEhO1TCUh5QsRCTm5L/7LMXFxfzlL3/5bpmlpFFZz56F1J2GoUQkppTt3UHBh68x+v+u4vjjj/9ueUJKeHsWGpKqHSULEYkpeUufxBITWZQ84HsNuiWnqmfhIQ1DiUjMOPDfjRStW0Jmn4tIymjxvXUJKWk6ZuEhJQsRiQnOOfLefoyEtEwyTxn2g/W+noWShVeULEQkJrzxxhuUbFlL1k9GkNCk6Q/WJ4Th1FmpOyULEfFcZWUlY8eOJSnrCJr1PLfaMpacSqWGoTyjZCEinpszZw4fffQRzU+7HEtMrrbMwYvygt3PTiJDyUJEPFVSUsLtt99Or169aHrCwBrLJSQ3AVcJFWVRjE4OUrIQEU/NnDmTrVu3MmXKFMxqbpIsJQ1Ap896RNdZiEhUBF4zcVBlSSH7n7yTs88+m7POOgve/GGZgxKSUwH8p89mRSw2XaBXPSULEfFM/or5FOzdy5QpU4KWVc/CWxqGEhFPlO/bRcGqlxg1ahQ9evQIWv67noWutfCEehYi4om8ZXNwrpLJkyeHVN5SfMki0qfPakiqekoWIhJ1pTu3sP+Tt2jW5wI6duwY0nsS/MNQXt3yo+oxl3hLJBqGEpGoy1vyDywljax+l4b8HvMPQ+mYhTfUsxCRqCr5+hOKN75P89OvIDEtM+T3mcc9i6ribbhKPQsRiRrnHHvffpzEjJY0631Brd77vwPc6ll4QT0LEYma4g3vUrp9PS3O+b3viuxaMH/5WLzzbDz0MpQsRCQqXEU5e5f8g+SWR5PxozO/W17dxXrVsYRELLlJVIehQo0tHmgYSkSiovDjf1G+5xuan34FlpBYpzosWfNweyVosjCzo8zs32a2zsw+NbMbqikzyMzyzWyN//HnyIQrIg3R/v37yV/2NE3an0jaMX3rXE+45+FujCLVZocyDFUO3OScW21mzYBVZvYv59xnVcotdc6dH9rHEZF4ct9991Gxfy+tf34bZlbnejQPd0gi0mYH7Vk453Y451b7nxcA64B2tQhcROLYzp07mTp1KmnH9aNJuxPqVZdvtjz1LA4lUm12rY5ZmFlHoCfwXjWr+5nZR2b2mpmdVMP7R5vZSjNbWV5eXvtoRaRB6ThuEV3OvYrC/UUcdtoV9a7PN1te3Pcskg62o/7H6JoK1rfN/t5GQ43OzDKA54EbnXP7qqxeDXRwzhWa2RDgReDYqnU453KAHID09HRNdyXSyJXt3UHBh6+R0f1sklu2r3d9CSlpVBTuCUNkDVq5c65PsELhaLMDhdSzMLNk/0bnOOdeqLreObfPOVfof/4qkGxmrUKpW0Qar7ylT2KJiWT1/2VY6rMUzcMdiki02aGcDWXALGCdc+6+Gsoc6S+HmfX117s7WN0i0nitXLmSonVLyOxzEUkZLcJSpyWn6QruICLVZocyDNUfuAz42MzW+JfdBhwN4Jx7GLgEuMbMyoFiYITTrOoiccs5x9ixY0lIyyTzlGFhq1enzoYkIm120GThnFsGHPJcN+fcDGBGsLpEJD68/vrrLF68mMPOHE1Ck6Zhq9eSU3HlpbjKijpf2NfYRarN1hXcIhJWlZWVjB07ls6dO9Os57lhrfv783BLNClZiEhYzZkzh7Vr13LHHXdgiclhrVvzcHtHyUJEwqakpITbb7+d3r17M3z48LDXn5Ciebi9omQhImEzc+ZMtm7dypQpU0hICH/zYsn+nkUDHIbKzc1l/vz5XodRZ0oWIhIWeXl53HnnnfzsZz/jzDPPDP6GOrCUhjcB0u7duxk3bhydOnXisssuY8+ehnlRoeazEJGwmDJlCnv37mVtm/MiNg/EwQPcDaFnkZeXx/3338/9999PYWEhI0eOZPz48bRoEZ5rTqJNyUJE6m3btm1MmzaNUaNGsfSIzhHbznfzcMdwz6KgoIDp06dz7733kpeXx7Bhw5g4cSInnRT09ksxTclCROrt4Ycfpry8nMmTJzPo4U8jtp2DB7hjcWrVyrISClYvolOnK9i9ezdDhw5l4sSJ9OzZ0+vQwkLJQkTqbcuWLbRv356OHTsCkUsWBw9wuxi686wrL6VgzT/Zt+I5Kvbv5eyzz2by5Mn07Vv3SZ5ikZKFiNRbbm4uhx9+eMS3E0unzrqKMgo/fpP85c9SUbCLJkd1o9VF43j9qVu8Di0ilCxEpN527txJu3aRnxPNEpMhIcnTOS1cZQX7P1lM3vJnqMj/liZtu9JyyI2kduher1kAY52ShYjUW25ubtTG5hNSUj3pWbjKCvavW0L+O3Mp37udlCOPoeXga0jt3LtRJ4mDlCxEpF6cc+Tm5tK6deuobM+S06J66qxzlRStX07+sqcp272V5NYdaX3x7aQdc0pcJImDlCxEpF7y8/MpKysj5/1dPBOh6ysCRatn4ZyjeOP75C2bQ1nulyS1aE+rC8bStGt/zGq+njnwGpOv7j4v4nFGi5KFiNTLzp07AUhIbx6V7flmy4vcMQvnHCWbV5O37ClKd3xBUvM2tDzv/5F+4ulxfVt0JQsRqZfc3FwAEtMyo7I932x5kelZlGxdS96SpzjwzWckZh5Oi3N+T0a3n2KJaiq1B0SkXr5LFlHqWSSkpFJREN5Zm0u2rSN/2ZOUbFlLYkYLWpx9LRknDw77LdYbMiULEamX74ahmmZFZXuWnBa2+SwO7PiCvKVPUbJ5FQlNm3PYT68mo8c5JCQ3CUv9jYmShYjUy3c9iygli3DMw12au5m8ZXMo/mIFCWmZNB90Jc16nv/dRX/yQ0oWIlIvubm5WJP0qA3ZWHJqnXsWZbu+Ju+dpyn6fCnWJJ2sAaPI7HNhWOcJb6yULESkXnJzc6PWqwDfbcpdaQnOuZCvcyjbu538d+ay/9O3sZRUsvoNp1nfn5OYmhHhaBsPJQsRqZedO3eS2LR51Lbnu025w5UfwJIPPWxUnv8tee88w/5P3sISk8k85WIy+14c1eTWWChZiEi95ObmktA0OqfNQpWbCdaQLMoLdpH/7jwKP3oDzGjW63yyTv0FiRmHRS3OxkbJQkTqJTc3l8Q27aO2vcB5uKteIldRuJf8Fc9RsOY1cI6MkweT1W84SZmtohZfY6VkISJ1VllZya5du2jWJXrDOtXNw11RlM++956nYPUiXEUZ6d3OpHn/ESRlHRG1uBq7oMnCzI4CZgNHApVAjnPugSplDHgAGAIUAVc651aHP1wRiSV79uyhsrIyarf6gIB5uEtLqCwpZN/7C9i36iVcaQnpJw0i6ycjSG4R+dulx6pItdmh9CzKgZucc6vNrBmwysz+5Zz7LKDMucCx/scpwEP+nyLSiEX7Vh/wv3m4Cz5YQPGWj3AH9tP0+AFkDfglKa2OjlocMSwibXbQZOGc2wHs8D8vMLN1QDsgcMMXArOdcw5YYWbNzayN/70i0kgdTBZR7Vn4k0XRhuWkHXsqzQf8kpTDO0dt+7EuUm12rY5ZmFlHoCfwXpVV7YCvA15v8y/73obNbDQwGiAlJaU2mxaRGBTtq7cBklt34LAzfkOTo7rRpM1xUdtuDEkys5UBr3OccznVFaxvm/29jYYanZllAM8DNzrn9lVdXc1b3A8W+D5QDkB6evoP1otIbOtYZb6KgtX/BqKbLMwSyOx7cdS2F4PKnXN9ghUKR5sdqOYZPL6/0WT/Ruc4516opsg24KiA1+2B7aHULSINV8X+fMBIiOIxCwkuEm120GThP2o+C1jnnLuvhmIvAZebz6lAvo5XiDR+FUV5JKQ1i+tJgWJNpNrsUIah+gOXAR+b2Rr/stuAowGccw8Dr+I7BWsjvtOwfh1CvSLSwFUW5Uf1Vh8Skoi02aGcDbWM6se3Ass44LpgdYlI41JRlB/VW31IcJFqs3UFt4gcUtWD2oEqivJJad0xesGIZ0I6wC0iUp3KojwS03UH13igZCEideIqyqksKSRBxyzigpKFiNRJRbHv1H3NDREflCxEpE4qi/IASFCyiAtKFiJSJ74L8tSziBdKFiJSJ5XFShbxRKfOijRCgae7fnX3eRHZxsGehQ5wxwf1LESkTiqK9kJCIgmp6V6HIlGgnoWI1Ep54R72vTuPgo/+SXKLdpjpO2c8ULKIsGgMB4hEw//muX4FV1FOxo/OIqv/CK/DkihRshCRQ6rwz3NdsHIhrryU9BNPJ6v/SJIPa+t1aBJFShYiUq38/HymTZvGNw9NxZUW0bTrQJoP+CXJLY8K/mZpdJQsROR7CgsLmTFjBvfccw979uwh7bh+NB8wSjcMjHNKFiINTKSOgxUXF/PQQw9x9913s3PnToYMGcKkSZMY9tx/w7YNabh0GoNInDtw4AAPPvggXbp04aabbqJ79+4sX76cRYsW0bt3b6/DkxihnoVInCorK+Mf//gHkydPZuvWrQwcOJC5c+dy+umnex2axCD1LETiTEVFBbNnz6Zr165cffXVtGnThjfeeIP//Oc/ShRSIyULkThRWVnJM888w0knncQVV1xBVlYWr7zyCu+++y6DBw/G7JAzcUqcU7IQaeSccyxYsIDu3bszcuRIkpKSmD9/PqtWreK8885TkpCQ6JiFSCPlnKP4y5WktrmB0m83kdSiHU8//TSXXnopiYmJXocnDYyShUgj45yj+Ks15C19ktLt60nKOoKWQ/5A+kmDGDnyAq/DiyuBpzkHaoi3/lGyEGlElixZQnZ2NrlLlpDYrDUtfvY7Mn50Fpaof3WpH/0FiTQCK1asIDs7mzfffJMjjzySw876Lc26n4MlJde6rpq+DUt80wFukQZs9erVnH/++fTr1481a9Zw7733smnTJjJ7D61TohCpSdCehZk9BpwP5DrnulWzfhCwENjsX/SCc25SGGMUiYqGdDv50p1fkbdsDr2nvMthhx3GXXfdxfXXX09GRobXoYnHItVmhzIM9QQwA5h9iDJLnXPnh1CXiNTD559/zs6FUyj6fBmWksaECRO48cYbycrSPNjynSeIQJsddBjKObcE2FObSkUkvDZt2sQVV1zBSSedRPGmD8g89RLajZnF+PHjlSjkeyLVZofrAHc/M/sI2A7c7Jz7tLpCZjYaGA2QkpISpk2LNF5bt25l8uTJPPHEEyQlJfGHP/yBZw/0JDG9udehiXeSzGxlwOsc51xOLesIqc3+3kZruYHqrAY6OOcKzWwI8CJwbHUF/R8oByA9Pd2FYdsijdL27du56667ePTRRwEYM2YMt956K23btmW+zlaKd+XOuT71eH/IbXagep8N5Zzb55wr9D9/FUg2s1b1rVckHuXm5nLTTTfRpUsXHnnkEa688kq++OIL/va3v9G2raYxlfqra5td756FmR0JfOucc2bWF18C2l3fekXiyZ49e7jnnnv429/+RnFxMZdffjnZ2dl07tzZ69Ckkalrmx3KqbNzgUFAKzPbBowHkgGccw8DlwDXmFk5UAyMcM5piEkkBPn5+dx///3cf//9FBQUMGLECMaPH8/xxx/vdWjSQEWqzQ6aLJxzI4Osn4HvNC0RCVFhYSHTp0/n3nvvZe/evVx88cVMnDiRbt1+cFq8SK1Eqs3W7T5EoqioqIiZM2cyZcoUdu3axfnnn8+kSZPo2bOn16GJHJJu9yESBSUlJUyfPp0uXbrwxz/+kZ49e/Luu+/y8ssvK1FIg6CehUgElZaW8vjjj3PHHXewbds2TjvtNObNm8fAgQPDvi3dAFAiST0LkQgoLy/niSeeoGvXrowZM4b27dvz5ptv8vbbb0ckUYhEmnoWEaBvePGroqKCZ599lokTJ7JhwwZ69+7NjBkzOPfcczV9qTRo6lmIhEFlZSXPP/883bt3Z9SoUTRp0oQFCxbwwQcfMGTIECUKafCULETqwTnHK6+8Qu/evbnkkkuoqKjgmWeeYc2aNVx00UVKEtJoKFmI1IFzjjfeeIN+/foxdOhQCgoKmD17Np988gnDhw8nIUH/WtK46C9apJbefvttTjvtNH72s5+xY8cO/v73v7Nu3Touu+wyEhMTvQ5PJCJ0gFskRMuXLyc7O5vFixfTtm1bZs6cyVVXXeXp7fZ1MoVEi5KFxJWqjWtN06cGlnv+F0eSnZ3Na6+9xuGHH87999/Pb3/7W9LS0iIaayQ0pKljJbYoWYjUoDR3M3nL5tBnygpatGjB3Xffze9+9zvS09O9Dk0k6pQsRKoo2/U1ee88TdHnS7Em6UyaNIkbbriBzMxMr0MT8YyShYhf2d7t5L8zl/2f/QdLbkJmv+Fk9v052dnDvQ5NxHNKFlGk8eLYtGXLFiZPnsz2xx7HEpPJ/PFFZJ4yjMSmWV6HJhIzlCwkbpUX7OK6667j0Ucfxcxo1us8sk69lMSMw7wOTSTmKFlI3KnYv5f8FfMp+PBVcsxx1VVX8ac//YmBD671OjSRmKVkIXFj9+7d7H37cQpWvYKrKCO920/5eGEOnTp18pdQshCpiZKFeC7Sx3Ly8vK47777mDZtGgUFhaSfeDpZ/UeS3KJdQKKIbbr4TrymZCGNVkFBAQ888AB//etfycvL45JLLuGdzDNIad3B69BEGhzdGyqGdRy36LuHhG7//v3cc889dOrUiezsbE477TQ+/PBDnnvuOSUKkTpSspBGo6SkhAceeIAuXbpwyy230KdPH9577z0WLlxIjx49vA5PpEHTMJQ0eKWlpcyaNYs777yTb775hjPOOIPnn3+e/v37R3S7NfX4dA2NNEbqWUiDVV5ezmOPPcZxxx3HtddeS8eOHVm8eDGLFy+OeKIQiTdBk4WZPWZmuWb2SQ3rzcymm9lGM1trZr3CH6bI/1RUVDBnzhxOOOEErrrqKlq3bs2rr77K0qVLOeOMM7wOT8RTkWqzQxmGegKYAcyuYf25wLH+xynAQ/6fImF1cJ7r8ePHs27dOrp3787ChQsZOnSopi+tJ51E0ag8QQTa7KA9C+fcEmDPIYpcCMx2PiuA5mbWJli9IqFyzrFw4UJ69erFpZdeCsC8efNYvXo1F1xwgRKFSIBItdnhOMDdDvg64PU2/7IdVQua2WhgNODp7GKxLBa/4Xl1A0TnHK+//jrZ2dmsXLmSY445hieffJKRI0dq+lKJZ0lmtjLgdY5zLqcW7w+5zf7eRmuxgZpU97XOVVfQ/4FyANLT06stIwKwePFisrOzWb58OR06dGDWrFlcfvnlJCXpBD6Je+XOuT71eH/IbXagcJwNtQ04KuB1e2B7GOqVOLRs2TLOOOMMzjzzTLZs2cJDDz3Ehg0b+M1vfqNEIRIedWqzw5EsXgIu9x9hPxXId84dsjsjUtWBHRv4dt6fGThwIJ999hnTpk1j48aNjBkzRkOWIuFVpzY76Fc1M5sLDAJamdk2YDyQDOCcexh4FRgCbASKgF/X9RNI7Av38Ys1a9aQ+/wkije+T0JaJlOnTuXaa68N6zzXhzoOFIvHiA6KdGyx/Nml7iLVZgdNFs65kUHWO+C6UDYmctBnn33G+PHjmT9/PglN0ska+Csye1/AH//4C69DE2nQItVmaxBYomrDhg1MnDiRuXPnkpGRQXZ2Nk/sO4mE1AyvQxORQ9DtPiQqNm/ezG9+8xtOPPFEXnzxRW655RY2b97MpEmTlChEGgD1LCSitm3bxh133MGsWbNITEzk+uuvZ9y4cRxxxBFehyYitaBkIRHx3//+l7/85S888sgjVFZWMnr0aG677TbatWvndWgiUgdKFhJWO3fuZOrUqTz44IOUlpby61//mttvv50OHTTpkEhDpmQRJrU9DdGrW2iEU+Bn+HDsT/jrX//KAw88QFFREaNGjeLPf/4zxxxzTNi31VD3l0hDpmQh9VJ5oIh9KxfSqdMo8vPzGT58OBMmTKBr165ehyYiYaRkIXVSWVpCweqX2ffeC1SWFHDRRRcxceJETj75ZK9DE5EIULKQWqksO0DhmtfIXzGfyqI8Ujv3pvnAy1jwxA1ehyYiEaRkISFx5WUUrn2d/HfnUVG4h9QOPWg+cBRN2p0A6JhCfWjfSUOgZCGHVFZWRsFHr5O//Bkq9u2kSfuTaDX0j6Qe/SOvQxORKFKykGodnOd64sSJ7PnyS1LaHEfLc64ntWNPzUwnEoeULOR7Kisree655xg/fjzr16+nR48etB72Z9K6/FhJQiSO6d5QAvimMF2wYAE9evRgxIgRJCUlMX/+fFatWkXTY/oqUYjEOSWLOOecY9GiRfTp04eLL76YkpIS5syZw0cffcSwYcNISNCfiIhoGCouzkSpenX5V3efh3OOt956i+zsbFasWEGnTp14/PHH+dWvflXv6UtD2ac1XfFe2/dG+3cW6Sv1NSGRxCp9bYxDS5YsYdCgQQwePJht27bxyCOPsH79eq688krNcy0i1VLLEEcObF9P3tKnOH3Khxx55JFMnz6dq6++mtTUVK9DE5EYp2QRB0q/3UTe0qco3vQBCWmZ3HvvvVxzzTU0bdrU69BEpIFQsmjEPvnkE8aPH8+OF14gITWD5qddTrPeQ7nppku8Dk1EGhgli0Zo/fr1TJgwgWeffZaMjAyy+o8k88cXkdAk3evQRKSBistkEcoZJ7F2llQo8Xz55ZdMmjSJJ598ktTUVMaOHcvNN99M73tWRCvMqKtpv4TzrKJw1RVrf1MitRGXyaKx+frrr5k8eTKPP/44SUlJ3HjjjYwdO5bDDz/c69BEpJFQsmjAduzYwV133UVOTg4AY8aM4dZbb6Vt27YeRyYijY2SRQOUm5vLlClTmDlzJuXl5d/Nc3300Ud7HZqINFIhXZRnZueY2Xoz22hm46pZP8jM8s1sjf/x5/CHKhXFBez9zxN07tyZadOmMXz4cNavX09OTo4ShYh8JxJtdtCehZklAg8Cg4FtwAdm9pJz7rMqRZc6584P8bNILVQe2M++D15k3wcLcaXFjBjhm+f6+OOP9zo0EYkxkWqzQxmG6gtsdM596Q/kGeBCoOqGJcwqS4spWPUy+95/gcqSQtKO60fzAaOYO+s6r0MTkdgVkTY7lGTRDvg64PU24JRqyvUzs4+A7cDNzrlPqxYws9HAaICUlJTaRxsnKssOUPjhIvLfe57KonzSuvyYrAGjaHLkMV6HJiLeSzKzlQGvc5xzOQGvw9Zmf2+jIQRW3UQGrsrr1UAH51yhmQ0BXgSO/cGbfB8oByA9Pb1qHXHvwIED7Fv1MvtWPOeb57pjT5oPGEWTdl29Dk1EYke5c67PIdaHrc0OFEqy2AYcFfC6Pb5M9L8onNsX8PxVM5tpZq2cc7tCqL9eqrv9dijlIrHtuurwx4UUfvwm+cufpaJgJ02O6karC24h9ahuYam/LmJ5f4nIIUWkzQ4lWXwAHGtmnYBvgBHALwMLmNmRwLfOOWdmffGdZbU7hLrjmqusYP+n/yb/nbmU539LStvjaTnkBlI7dNfMdCJSVxFps4MmC+dcuZn9DngdSAQec859amZj/OsfBi4BrjGzcqAYGOGc0zBTDZyrpGjdUvLeeZryPd+QckQXDh88htTOfZQkRKReItVmh3RRnnPuVeDVKsseDng+A5hRi88Tl5yrpHjDCvKWPUXZrq0kt+5I65//ibRjT1WSEJGwiUSbrSu4o8A5R/Gm98lbOoey3C9JatGeVhfcQtOuAzDTZIUiEvuULCLIOUfJVx+St/QpSndsIKn5kbQ87w+knzgIS0j0OjwRkZApWURIydaPyVv6FAe2fUpiZmtanHM9Gd3OxBK1y0Wk4VHLFWYHvllH3tKnKNnyEYkZLWgx+BoyTj4bS0r2OjQRkTpTsgiTA//dSN7SJyn5chUJTZtz2E//j4we55KQ3MTr0ERE6k3Jop5Kd35F3tKnKP5iBQmpzWh++hU06zWUhJRUr0MTEQkbJYs6+vzzz9m5cApFny/DUtLIGjCKzD4XktCkqdehiYiEnZJFLW3atImJEycyZ84cXGIKmf1+QWbfi0lMzfA6NBGRiGl0ySLw/kM13ScqlPdWtWXLFiZPnsysxx7HEpNp1uciMk8ZRmLTrDrHGg41fd5Q78NUn/0VabW9l1Ss3HsqVuIQCadGlyzCrbxgF9dddx2PPvooZkazXueReeovSMpo4XVoIiJRo2RRg4r9eeSveI6CD18lxxxXXXUVf/rTnxj44FqvQxMRiToliyoqivex770XKFj9Mq68jPRuP+XjhTl06tTJX0LJQkTij5KFX2VJoW+e65ULcaUlpJ94Oln9R5Lcol1AohARiU9xnywqDxT9b57rA/tpenx/svr/kpTWHbwOTUQkZsRtsqgsK6Fg9avse28+lcX7SDumL80H/IqUIzp7HZqISMyJu2ThykspWPNP3zzX+/eS2qmXb57rtsd7HZqISMyKm2ThKsooXPsv8t+dR0XBLpoc/SNaXTSO1PYneR2aiEjMa/TJory8nNmzZ/PNo7dRkf8tTdqdQMvz/kBah+5ehyYi0mA02mThKiuYM2cOEyZMYOPGjaQceSwtB19DaufemsJURKSWGl2ycK6SovXLyV/2NL/avZWTTz6ZF198kd8vT1SSEBGpo0aTLJxzFG98n7xlT1GWu5nklkcxb948hg0bRkJCAje8q/v1iIjUVYNPFs45SjavJm/ZU5Tu+IKkw9rQ8vybSD/hNH7xiwu8Dk9EpFFo0Mni3//+N9/OGcuBbz4jMfNwWp77e9K7nYklJHodmohIo9Igk4VzjqFDh7Jo0SLfPNdnX0vGyYOxRM1zLSISCQ0yWZgZP/nJTzjrrLO47+ujNc+1iEiEJYRSyMzOMbP1ZrbRzMZVs97MbLp//Voz6xX+UL/vtttu48Ybb1SiEBGpIhJtdtBkYWaJwIPAucCJwEgzO7FKsXOBY/2P0cBDIXweEREJs0i12aH0LPoCG51zXzrnSoFngAurlLkQmO18VgDNzaxNCHWLiEh4RaTNDuWYRTvg64DX24BTQijTDtgRWMjMRuPLYgDOzIpD2H5NkoDyQxWwKfWovW71BI0pHGqKp5rl1cZTi/fXW6gxeciTeILs61jbRxB7McVaPFCLmOr5v5ZmZisDXuc453ICXoetzQ4USrKo7rJnV4cy+D9QTjVla83MVjrn+oSjrnCJtZhiLR6IvZhiLR5QTKGItXggpmIKW5sdKJRhqG3AUQGv2wPb61BGREQiLyJtdijJ4gPgWDPrZGYpwAjgpSplXgIu9x9hPxXId87V2J0REZGIiUibHXQYyjlXbma/A14HEoHHnHOfmtkY//qHgVeBIcBGoAj4de0+W52EZTgrzGItpliLB2IvpliLBxRTKGItHoiRmCLVZptzhxymEhERCe2iPBERiW9KFiIiElTMJAszO8rM/m1m68zsUzO7wb+8hZn9y8y+8P88zL+8pb98oZnNqKHOl8zsk1iIycze9l9+v8b/ONzjeFLMLMfMNpjZ52Y2zMt9ZGbNAvbNGjPbZWbTPN5HI83sY/PdDuGfZtbKy33kXzfcH8+nZja1LvHUMabBZrbKvz9WmdlPA+rq7V++0Xy3kKj1LGNhjudOM/vazArrun/CGZOZNTWzRf7/s0/N7O76xOUZ51xMPIA2QC//82bABnyXqk8FxvmXjwOm+J+nAwOAMcCMauq7GHga+CQWYgLeBvrEyj4CJgJ3+J8nAK28jqlKvauA07yKB9/JH7kH94v//RO83EdAS2Ar0Nr/+h/AmVGKqSfQ1v+8G/BNQF3vA/3wnbv/GnCux/Gc6q+vMMr/b9XGBDQFzvA/TwGW1mUfef3wPIBD/KIWAoOB9UCbgF/e+irlruSHDWEGsMz/i61zsghzTG9Tz2QR5ni+BtJj6fcWsO5Yf3zmVTxAMrAT6ICvEXwYGO3lPgJ+DLwZ8PoyYGY0Y/IvN2A30MRf5vOAdSOBR7yKp8ryeiWLSMTkX/cAcHU4Y4vGI2aGoQKZWUd8Wfo94AjnP//X/zOU4ZvJwF/xnRIWKzEBPO4fYsmuS1c9XPGYWXP/08lmttrMnjOzI+oTT31jqmIk8Kzz/2d5EY9zrgy4BvgY38VKJwKz6hNPfWPCd5pjVzPraGZJwEV8/8KqaMU0DPjQOXcA3y0itgWsO3jbCK/iiYhwxeT/3xsKvBWpWCMl5pKFmWUAzwM3Ouf21eH9PYBjnHMLYiUmv1HOuR8BA/2PyzyMJwnfFZvvOOd6Ae8C99Y1njDFFGgEMNfLeMwsGV+y6Am0BdYCt3oZk3Nurz+mZ/ENZXxFPe+PVNuYzOwkYArw24OLqgvVw3jCLlwx+RP8XGC6c+7LSMQaSTGVLPz/oM8Dc5xzL/gXf2v+uyH6f+YGqaYf0NvMvsI3FHWcmb3tcUw4577x/yzAdyylr4fx7MbX6zqYUJ8D6jwHSbj2kb9sdyDJObfK43h6ADjnNvl7OPOAn3gcE865l51zpzjn+uEbDvkiWjGZWXt8fzOXO+c2+Rdvw/fF46A63+onTPGEVZhjygG+cM5Ni0SskRYzycI/LDMLWOecuy9g1UvAFf7nV+AbN6yRc+4h51xb51xHfAcJNzjnBnkZk5klmf9MGv8f3/lArc/SCuM+csDLwCD/ojOBz2obTzhjCjCSevQqwhjPN8CJZtba/3owsM7jmDD/WXT+M3CuBf4ejZj8wyeLgFudc+8cLOwfhikws1P9dV4eyueIVDzhFM6YzOwOIAu4MRKxRoXXB00OPvA17A5fd3+N/zEE3xkgb+H7BvUW0CLgPV8Be4BCfN9wTqxSZ0fqdzZUWGLCd3bLKn89n+I7wJXo5T7Cd+B2ib+ut4CjY+H3BnwJdPX6d+ZfPgZfgliLL7m2jIGY5uJL7J8BI6K1n4Dbgf0BZdcAh/vX9cH35WcTMIM6nJgQ5nim+vdZpf/nBC/3Eb7elvP/LR1c/n91/d159dDtPkREJKiYGYYSEZHYpWQhIiJBKVmIiEhQShYiIhKUkoWIiASlZCEiIkEpWYiISFD/H4Mn+byz3x5CAAAAAElFTkSuQmCC\n",
      "text/plain": [
       "<Figure size 432x288 with 2 Axes>"
      ]
     },
     "metadata": {
      "needs_background": "light"
     },
     "output_type": "display_data"
    }
   ],
   "source": [
    "freq['res'] = fit.resid\n",
    "freq['fit'] = fit.fittedvalues\n",
    "freq['Month'] = copy\n",
    "freq = freq.sort_values(by = 'Month')\n",
    "fig,ax = plt.subplots()\n",
    "ax.bar(freq['Month'], freq['Count'], width = 31)\n",
    "ax2 = plt.twinx()\n",
    "ax2.set_ylim(ax.get_ylim())\n",
    "ax2.plot(freq['Month'], freq['fit'], color='k', label='Regression')\n",
    "plt.show()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 167,
   "id": "09114e89-aefe-4056-bd0c-99398d56de3e",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "Intercept      1.069543e-18\n",
       "Month          6.716696e-21\n",
       "Dream          3.788544e-01\n",
       "Month:Dream    3.690292e-01\n",
       "Name: P>|t|, dtype: float64"
      ]
     },
     "execution_count": 167,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "fit.summary2().tables[1]['P>|t|']"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "e7d6ccf4-4f8d-48bb-9dc0-6cab888c817f",
   "metadata": {},
   "source": [
    "These p-values suggest the dream sweetspot is significant! but what if we also added the 5 month period before Dream admitted to cheating?This is the period after he was caught cheating, before he [admitted to it](https://www.looper.com/432321/dreams-minecraft-speedrun-cheating-scandal-explained/) on May 30, 2021."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "faf0b5d4-2528-4537-9a7e-36ed01de4454",
   "metadata": {},
   "outputs": [],
   "source": []
  },
  {
   "cell_type": "markdown",
   "id": "9ba326f9-e27d-4adf-bfbc-b17fad14c440",
   "metadata": {},
   "source": [
    "Let's also plot the residuals"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "b87320a0-a39f-44c8-bc3c-c8bf833e1593",
   "metadata": {},
   "outputs": [],
   "source": []
  },
  {
   "cell_type": "code",
   "execution_count": 169,
   "id": "c26bc587-b7a8-4b0c-a4ea-9b15950d0805",
   "metadata": {},
   "outputs": [],
   "source": [
    "#We see"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 170,
   "id": "36627f15-aa40-4837-8709-01bf6ea56513",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>Month</th>\n",
       "      <th>Count</th>\n",
       "      <th>res</th>\n",
       "      <th>fit</th>\n",
       "      <th>Dream</th>\n",
       "      <th>Cheat</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>94</th>\n",
       "      <td>16078.661157</td>\n",
       "      <td>0.000000</td>\n",
       "      <td>-0.058446</td>\n",
       "      <td>0.058446</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>76</th>\n",
       "      <td>16109.054545</td>\n",
       "      <td>0.477121</td>\n",
       "      <td>0.395511</td>\n",
       "      <td>0.081610</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>90</th>\n",
       "      <td>16139.447934</td>\n",
       "      <td>0.301030</td>\n",
       "      <td>0.196255</td>\n",
       "      <td>0.104775</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>96</th>\n",
       "      <td>16169.841322</td>\n",
       "      <td>0.000000</td>\n",
       "      <td>-0.127940</td>\n",
       "      <td>0.127940</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>80</th>\n",
       "      <td>16200.234711</td>\n",
       "      <td>0.477121</td>\n",
       "      <td>0.326016</td>\n",
       "      <td>0.151105</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "           Month     Count       res       fit  Dream  Cheat\n",
       "94  16078.661157  0.000000 -0.058446  0.058446      0      0\n",
       "76  16109.054545  0.477121  0.395511  0.081610      0      0\n",
       "90  16139.447934  0.301030  0.196255  0.104775      0      0\n",
       "96  16169.841322  0.000000 -0.127940  0.127940      0      0\n",
       "80  16200.234711  0.477121  0.326016  0.151105      0      0"
      ]
     },
     "execution_count": 170,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "freq['Month']=mdates.date2num(freq['Month'])\n",
    "very_end = mdates.datestr2num('05/30/2021')\n",
    "freq['Cheat'] = freq['Month'].apply(lambda x: 1 if x > end else 0)\n",
    "#freq['Cheat'] = freq['Cheat'].apply(lambda x: 1 if x else 0)\n",
    "freq.head()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 171,
   "id": "5faeded5-1f12-440f-92c0-186b7e04ad29",
   "metadata": {},
   "outputs": [],
   "source": [
    "y,X = dmatrices('Count ~ Month*Dream + Month*Cheat',freq, return_type = 'dataframe')\n",
    "y = np.ravel(y)\n",
    "mod = sm.OLS(y,X)\n",
    "fit = mod.fit()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 172,
   "id": "e670faf6-92a0-485b-ba5b-a6e5e6cfc1d1",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "Intercept      -6.464687\n",
       "Month           0.000423\n",
       "Dream         -41.625253\n",
       "Month:Dream     0.002322\n",
       "Cheat          61.912920\n",
       "Month:Cheat    -0.003224\n",
       "dtype: float64"
      ]
     },
     "execution_count": 172,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "fit.params"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 173,
   "id": "215bdf7a-e335-4bba-aa47-7febc2d052c3",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "Intercept      2.191631e-07\n",
       "Month          9.302297e-09\n",
       "Dream          1.660017e-01\n",
       "Month:Dream    1.535356e-01\n",
       "Cheat          5.530645e-06\n",
       "Month:Cheat    7.928875e-06\n",
       "Name: P>|t|, dtype: float64"
      ]
     },
     "execution_count": 173,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "fit.summary2().tables[1]['P>|t|']"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 174,
   "id": "b9383e35-0d0b-4c02-8bb7-c9b35b20b8e6",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "image/png": "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\n",
      "text/plain": [
       "<Figure size 432x288 with 2 Axes>"
      ]
     },
     "metadata": {
      "needs_background": "light"
     },
     "output_type": "display_data"
    }
   ],
   "source": [
    "freq['res'] = fit.resid\n",
    "freq['fit'] = fit.fittedvalues\n",
    "freq['Month'] = copy\n",
    "freq = freq.sort_values(by = 'Month')\n",
    "fig,ax = plt.subplots()\n",
    "ax.bar(freq['Month'], freq['Count'], width = 30)\n",
    "ax2 = plt.twinx()\n",
    "ax2.set_ylim(ax.get_ylim())\n",
    "ax2.plot(freq['Month'], freq['fit'], color='k', label='Regression')\n",
    "plt.show()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "de134298-6392-4268-9be2-c5b3cde8e066",
   "metadata": {},
   "outputs": [],
   "source": []
  },
  {
   "cell_type": "code",
   "execution_count": 36,
   "id": "09275c16-541b-4c6f-8178-b86b21624e5c",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>Month</th>\n",
       "      <th>Count</th>\n",
       "      <th>res</th>\n",
       "      <th>fit</th>\n",
       "      <th>Dream</th>\n",
       "      <th>Cheat</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>78</th>\n",
       "      <td>2013-02-08 08:00:47.603305728</td>\n",
       "      <td>1.098612</td>\n",
       "      <td>0.629268</td>\n",
       "      <td>0.469344</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>83</th>\n",
       "      <td>2013-03-10 17:27:16.363636480</td>\n",
       "      <td>1.098612</td>\n",
       "      <td>0.599834</td>\n",
       "      <td>0.498778</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>88</th>\n",
       "      <td>2013-04-10 02:53:45.123966976</td>\n",
       "      <td>0.693147</td>\n",
       "      <td>0.164936</td>\n",
       "      <td>0.528211</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>76</th>\n",
       "      <td>2013-05-10 12:20:13.884297472</td>\n",
       "      <td>1.098612</td>\n",
       "      <td>0.540967</td>\n",
       "      <td>0.557645</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>103</th>\n",
       "      <td>2013-06-09 21:46:42.644627968</td>\n",
       "      <td>0.000000</td>\n",
       "      <td>-0.587078</td>\n",
       "      <td>0.587078</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>...</th>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>15</th>\n",
       "      <td>2021-12-05 00:47:36.198347008</td>\n",
       "      <td>6.049733</td>\n",
       "      <td>0.669827</td>\n",
       "      <td>5.379907</td>\n",
       "      <td>0</td>\n",
       "      <td>1</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>16</th>\n",
       "      <td>2022-01-04 10:14:04.958677760</td>\n",
       "      <td>5.973810</td>\n",
       "      <td>0.789882</td>\n",
       "      <td>5.183928</td>\n",
       "      <td>0</td>\n",
       "      <td>1</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>21</th>\n",
       "      <td>2022-02-03 19:40:33.719008256</td>\n",
       "      <td>5.129899</td>\n",
       "      <td>0.141950</td>\n",
       "      <td>4.987949</td>\n",
       "      <td>0</td>\n",
       "      <td>1</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>31</th>\n",
       "      <td>2022-03-06 05:07:02.479338752</td>\n",
       "      <td>3.688879</td>\n",
       "      <td>-1.103091</td>\n",
       "      <td>4.791970</td>\n",
       "      <td>0</td>\n",
       "      <td>1</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>30</th>\n",
       "      <td>2022-04-05 14:33:31.239669504</td>\n",
       "      <td>3.688879</td>\n",
       "      <td>-0.907112</td>\n",
       "      <td>4.595991</td>\n",
       "      <td>0</td>\n",
       "      <td>1</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "<p>105 rows × 6 columns</p>\n",
       "</div>"
      ],
      "text/plain": [
       "                            Month     Count       res       fit  Dream  Cheat\n",
       "78  2013-02-08 08:00:47.603305728  1.098612  0.629268  0.469344      0      0\n",
       "83  2013-03-10 17:27:16.363636480  1.098612  0.599834  0.498778      0      0\n",
       "88  2013-04-10 02:53:45.123966976  0.693147  0.164936  0.528211      0      0\n",
       "76  2013-05-10 12:20:13.884297472  1.098612  0.540967  0.557645      0      0\n",
       "103 2013-06-09 21:46:42.644627968  0.000000 -0.587078  0.587078      0      0\n",
       "..                            ...       ...       ...       ...    ...    ...\n",
       "15  2021-12-05 00:47:36.198347008  6.049733  0.669827  5.379907      0      1\n",
       "16  2022-01-04 10:14:04.958677760  5.973810  0.789882  5.183928      0      1\n",
       "21  2022-02-03 19:40:33.719008256  5.129899  0.141950  4.987949      0      1\n",
       "31  2022-03-06 05:07:02.479338752  3.688879 -1.103091  4.791970      0      1\n",
       "30  2022-04-05 14:33:31.239669504  3.688879 -0.907112  4.595991      0      1\n",
       "\n",
       "[105 rows x 6 columns]"
      ]
     },
     "execution_count": 36,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "freq"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 37,
   "id": "aa44d8e0-396a-4f73-8324-92292507f255",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "0     2021-02-04 02:22:48.595041280\n",
       "1     2021-03-06 11:49:17.355371776\n",
       "2     2021-01-04 16:56:19.834710784\n",
       "3     2021-04-05 21:15:46.115702528\n",
       "4     2021-05-06 06:42:14.876033024\n",
       "                   ...             \n",
       "100   2015-12-08 17:01:05.454545408\n",
       "101   2016-03-08 21:20:31.735537152\n",
       "102   2014-04-09 20:11:30.247933952\n",
       "103   2013-06-09 21:46:42.644627968\n",
       "104   2013-12-09 06:25:35.206611456\n",
       "Name: Month, Length: 105, dtype: datetime64[ns]"
      ]
     },
     "execution_count": 37,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "copy"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 38,
   "id": "53c14d6e-f3e4-4222-8305-2db553c311e4",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "image/png": "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\n",
      "text/plain": [
       "<Figure size 432x288 with 1 Axes>"
      ]
     },
     "metadata": {
      "needs_background": "light"
     },
     "output_type": "display_data"
    }
   ],
   "source": [
    "freq['res'] = fit.resid\n",
    "fig,ax = plt.subplots()\n",
    "ax.bar(copy, freq['res'], width = 30)\n",
    "plt.show()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "4732ad6e-248e-442e-93d5-e2305b6f2764",
   "metadata": {},
   "outputs": [],
   "source": []
  },
  {
   "cell_type": "code",
   "execution_count": 39,
   "id": "c63ec98f-5581-4d32-9ac8-d8b86c16af47",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>Month</th>\n",
       "      <th>Count</th>\n",
       "      <th>res</th>\n",
       "      <th>fit</th>\n",
       "      <th>Dream</th>\n",
       "      <th>Cheat</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>78</th>\n",
       "      <td>2013-02-08 08:00:47.603305728</td>\n",
       "      <td>1.098612</td>\n",
       "      <td>0.629268</td>\n",
       "      <td>0.469344</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>83</th>\n",
       "      <td>2013-03-10 17:27:16.363636480</td>\n",
       "      <td>1.098612</td>\n",
       "      <td>0.599834</td>\n",
       "      <td>0.498778</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>88</th>\n",
       "      <td>2013-04-10 02:53:45.123966976</td>\n",
       "      <td>0.693147</td>\n",
       "      <td>0.164936</td>\n",
       "      <td>0.528211</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>76</th>\n",
       "      <td>2013-05-10 12:20:13.884297472</td>\n",
       "      <td>1.098612</td>\n",
       "      <td>0.540967</td>\n",
       "      <td>0.557645</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>103</th>\n",
       "      <td>2013-06-09 21:46:42.644627968</td>\n",
       "      <td>0.000000</td>\n",
       "      <td>-0.587078</td>\n",
       "      <td>0.587078</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>...</th>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>15</th>\n",
       "      <td>2021-12-05 00:47:36.198347008</td>\n",
       "      <td>6.049733</td>\n",
       "      <td>0.669827</td>\n",
       "      <td>5.379907</td>\n",
       "      <td>0</td>\n",
       "      <td>1</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>16</th>\n",
       "      <td>2022-01-04 10:14:04.958677760</td>\n",
       "      <td>5.973810</td>\n",
       "      <td>0.789882</td>\n",
       "      <td>5.183928</td>\n",
       "      <td>0</td>\n",
       "      <td>1</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>21</th>\n",
       "      <td>2022-02-03 19:40:33.719008256</td>\n",
       "      <td>5.129899</td>\n",
       "      <td>0.141950</td>\n",
       "      <td>4.987949</td>\n",
       "      <td>0</td>\n",
       "      <td>1</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>31</th>\n",
       "      <td>2022-03-06 05:07:02.479338752</td>\n",
       "      <td>3.688879</td>\n",
       "      <td>-1.103091</td>\n",
       "      <td>4.791970</td>\n",
       "      <td>0</td>\n",
       "      <td>1</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>30</th>\n",
       "      <td>2022-04-05 14:33:31.239669504</td>\n",
       "      <td>3.688879</td>\n",
       "      <td>-0.907112</td>\n",
       "      <td>4.595991</td>\n",
       "      <td>0</td>\n",
       "      <td>1</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "<p>105 rows × 6 columns</p>\n",
       "</div>"
      ],
      "text/plain": [
       "                            Month     Count       res       fit  Dream  Cheat\n",
       "78  2013-02-08 08:00:47.603305728  1.098612  0.629268  0.469344      0      0\n",
       "83  2013-03-10 17:27:16.363636480  1.098612  0.599834  0.498778      0      0\n",
       "88  2013-04-10 02:53:45.123966976  0.693147  0.164936  0.528211      0      0\n",
       "76  2013-05-10 12:20:13.884297472  1.098612  0.540967  0.557645      0      0\n",
       "103 2013-06-09 21:46:42.644627968  0.000000 -0.587078  0.587078      0      0\n",
       "..                            ...       ...       ...       ...    ...    ...\n",
       "15  2021-12-05 00:47:36.198347008  6.049733  0.669827  5.379907      0      1\n",
       "16  2022-01-04 10:14:04.958677760  5.973810  0.789882  5.183928      0      1\n",
       "21  2022-02-03 19:40:33.719008256  5.129899  0.141950  4.987949      0      1\n",
       "31  2022-03-06 05:07:02.479338752  3.688879 -1.103091  4.791970      0      1\n",
       "30  2022-04-05 14:33:31.239669504  3.688879 -0.907112  4.595991      0      1\n",
       "\n",
       "[105 rows x 6 columns]"
      ]
     },
     "execution_count": 39,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "freq"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "1ed91f7c-9f3b-4a89-8504-a05f54646fa3",
   "metadata": {},
   "source": [
    "However, unlike the general trend we saw before, Minecraft exceeded in popularity, even on the logarithmic scale. Weirder, we see a steep dropoff starting in 2021. This suggests Minecraft's speedrunning popularity may be different to the overall speedrunning scene. Let's investigate with a linear model. "
   ]
  },
  {
   "cell_type": "markdown",
   "id": "cd50c1cf-109d-4908-b86f-bde0dee25b51",
   "metadata": {},
   "source": [
    "So we see time plays an important factor here, but to what extent? Well, let's attempt a linear regression. Let's first begin with Minecraft, and can generalize for all the other games later. These are the variables I will immediately consider: the date submitted, the category, the variables (aka the subcategory), and if the date is after March 1, 2020 (meaning the runner would likely be living in quarantine and/or a pandemic). "
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.9.7"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
