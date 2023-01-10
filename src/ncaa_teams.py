import requests
import pandas as pd
from database_config import MyDatabase
import creds


# getting the API-Key which is stored in the environment variables 
url = "https://api.sportsdata.io/v3/cfb/scores/json/Teams"

payload={}
headers = {
    'Ocp-Apim-Subscription-Key': f'{creds.cfb_api_key}'
}

response = requests.request("GET", url, headers=headers, data=payload)
res_json = response.json()
print(res_json)

df_teams = pd.DataFrame(res_json)
print(df_teams)

# Transform the dataframe
df_teams = df_teams.filter(items=[
    'TeamID',
    'team_short',
    'Active',
    'School',
    'Name',
    'StadiumID',
    'ApRank',
    'Wins',
    'Losses',
    'ConferenceWins',
    'ConferenceLosses',
    'GlobalTeamID',
    'CoachesRank',
    'PlayoffRank',
    'ConferenceID',
    'Conference',
    'ShortDisplayName'
])

# Replacing NaN Values to None which is equal to  NULL in postgres
# the games which haven´t started can be filtered 
df_teams = df_teams.fillna(0)
print(df_teams)

# Save the data local as a CSV file
df_teams.to_csv(f'Projekte/Football_Analytics/data/NCAA_teams.csv', index=False)
df_teams.to_excel(f'Projekte/Football_Analytics/data/NCAA_teams.xlsx', index=False)

# Loading the data in the Database
db = MyDatabase()

insert_ncaa_teams = """INSERT INTO ncaa_teams (
teamID,
team_short,
active,
school,
name, 
stadiumID,
ap_rank,
wins,
losses,
conference_wins,
conference_losses,
global_teamID,
coaches_rank,
playoff_rank,
conferenceID,
conferencer, 
short_display_name)  
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
"""

for i, row in df_teams.iterrows():
    db.query_func(insert_ncaa_teams, list(row))