import requests
import os
import pandas as pd
import datetime
from database_config import MyDatabase

# getting the API-Key which is stored in the environment variables 
api_key = os.environ.get('SD_API_Key')


url = "https://api.sportsdata.io/v3/nfl/scores/json/Standings/{2022REG}"

payload={}
headers = {
    'Ocp-Apim-Subscription-Key': f'{api_key}'
}

response = requests.request("GET", url, headers=headers, data=payload)
print(response.text)

res_json = response.json()
df_standings = pd.DataFrame(res_json)

# Transformation
df_standings = df_standings.drop(['GlobalTeamID'], axis=1)
# adding column for the week of the standings. Because the Seasonstarted in 36 week we have to reduce the actual calender week 
week = int(datetime.date.today().isocalendar()[1] - 36)
df_standings['week'] = week

print(df_standings.head())
print(df_standings.tail())

df_standings.to_csv('Projekte/Football_Analytics/data/SD_standings.csv', index=False)
df_standings.to_excel('Projekte/Football_Analytics/data/SD_standings.xlsx', index=False)

# Loading into Postgres
db = MyDatabase()

insert_standings_string = """INSERT INTO sd_standings (
    season_type, 
    season, 
    conference, 
    division, 
    team, 
    name, 
    wins, 
    losses, 
    ties, 
    percentage, 
    points_for, 
    points_against, 
    net_points, 
    touchdowns, 
    division_wins, 
    division_losses, 
    conference_wins, 
    conference_losses, 
    teamID, 
    division_ties, 
    conference_ties, 
    division_rank, 
    conference_rank,
    week)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
"""

for i, row in df_standings.iterrows():
    db.query_func(insert_standings_string, list(row))