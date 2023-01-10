import requests
import pandas as pd
from database_config import MyDatabase
import creds


# getting the API-Key which is stored in the environment variables 

# Examples: 2017, 2017
seasons = [2021, 2022, 2023]

url = f"https://api.sportsdata.io/v3/cfb/scores/json/TeamSeasonStats/{season}"

payload={}
headers = {
    'Ocp-Apim-Subscription-Key': f'{creds.cfb_api_key}'
}

response = requests.request("GET", url, headers=headers, data=payload)
res_json = response.json()
print(res_json)

df_teams_season = pd.DataFrame(res_json)
print(df_teams_season)

# Save the data local as a CSV file
df_teams_season.to_csv(f'Projekte/Football_Analytics/data/NCAA_teams_season.csv', index=False)
df_teams_season.to_excel(f'Projekte/Football_Analytics/data/NCAA_teams_season.xlsx', index=False)

