import time
import requests
import pandas as pd
from database_config import MyDatabase
import creds

payload={}
headers = {
    'Ocp-Apim-Subscription-Key': f'{creds.cfb_api_key}'
}

df_cfb_games_total = pd.DataFrame()


# EXTRACT
cfb_season = 2023
cfb_weeks = list(range(1, 5))


for week in cfb_weeks:

    url = f"https://api.sportsdata.io/v3/cfb/scores/json/GamesByWeek/{cfb_season}/{week}"
    response = requests.request("GET", url, headers=headers, data=payload)
    res_json = response.json()
    print(res_json)
    
    try:
        df_cfb_games = pd.DataFrame(res_json)
        print(df_cfb_games)

        # TRANSFORM
        df_cfb_games = df_cfb_games.filter(items=[
        'GameID',
        'Season',
        'SeasonType',
        'Week',
        'Status',
        'Day',
        'AwayTeam',
        'HomeTeam',
        'AwayTeamID',
        'HomeTeamID',
        'AwayTeamName',
        'HomeTeamName',
        'AwayTeamScore',
        'HomeTeamScore',
        'PointSpread',
        'OverUnder',
        'StadiumID',
        'Title'
        ])

        # concat the extract dataframe to the global Dataframe
        df_cfb_games_total = pd.concat([df_cfb_games_total, df_cfb_games], axis=0, ignore_index=True) 

    except:
        print(f'No games in {week}')

    time.sleep(10)


# LOAD
# Save the data local as a CSV file
df_cfb_games_total.to_csv(f'Projekte/Football_Analytics/data/NCAA_games_{cfb_season}.csv', index=False)
df_cfb_games_total.to_excel(f'Projekte/Football_Analytics/data/NCAA_games{cfb_season}.xlsx', index=False)

# Loading the data in the Database
db = MyDatabase()

insert_ncaa_games = """INSERT INTO ncaa_games (
gameID,
season,
season_type,
week,
status,
day,
away_team,
home_team,
away_teamID,
home_teamID,
away_team_name,
home_team_name,
away_team_score,
home_team_score,
point_spread,
over_under,
stadiumID,
title)  
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
"""

for i, row in df_cfb_games_total.iterrows():
    db.query_func(insert_ncaa_games, list(row))