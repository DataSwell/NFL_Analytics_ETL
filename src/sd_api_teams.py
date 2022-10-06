import datetime
import requests
import os
import pandas as pd
from database_config import MyDatabase
from my_funcs import gameweek, season


# getting the API-Key which is stored in the environment variables 
api_key = os.environ.get('SD_API_Key')

url = "https://api.sportsdata.io/v3/nfl/scores/json/Teams"

payload={}
headers = {
    'Ocp-Apim-Subscription-Key': f'{api_key}'
}

response = requests.request("GET", url, headers=headers, data=payload)
res_json = response.json()
df_teams = pd.DataFrame(res_json)

# Transform the dataframe

df_teams = df_teams.filter(items=[
    'Key',
    'TeamID',
    'City',
    'Conference',
    'Division',
    'FullName',
    'StadiumID',
    'HeadCoach',
    'OffensiveCoordinator',
    'DefensiveCoordinator',
    'SpecialTeamsCoach',
    'OffensiveScheme',
    'DefensiveScheme'
])

print(df_teams.head())
print(df_teams.tail())

# Save the data local as a CSV file
df_teams.to_csv(f'Projekte/Football_Analytics/data/SD_teams_{season()}_{gameweek()}.csv', index=False)
df_teams.to_excel(f'Projekte/Football_Analytics/data/SD_teams_{season()}_{gameweek()}.xlsx', index=False)

# Loading the data in the Database
db = MyDatabase()

insert_teams_string = ("""INSERT INTO sd_teams (
team_short,
teamID,
city,
conference,
division,
fullname,
stadiumID,
head_coach,
offensive_coordinator, 
defensive_coordinator, 
special_teams_coordinator,
offensive_schema,
defensive_schema) 
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s)
""")

# for i, row in df_teams.iterrows():
#     db.query_func(insert_teams_string, list(row))