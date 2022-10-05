import requests
import os
import pandas as pd

# getting the API-Key which is stored in the environment variables 
api_key = os.environ.get('SD_API_Key')


url = "https://api.sportsdata.io/v3/nfl/scores/json/TeamSeasonStats/{2021REG}"

payload={}
headers = {
    'Ocp-Apim-Subscription-Key': f'{api_key}'
}

response = requests.request("GET", url, headers=headers, data=payload)
print(response.text)

res_json = response.json()
df_team_season_stats = pd.DataFrame(res_json)

# Transformation
required_columns = list()

print(df_team_season_stats.head())
print(df_team_season_stats.tail())

df_team_season_stats.to_csv('Projekte/Football_Analytics/data/SD_team_season_stats.csv', index=False)
df_team_season_stats.to_excel('Projekte/Football_Analytics/data/SD_team_season_stats.xlsx', index=False)
