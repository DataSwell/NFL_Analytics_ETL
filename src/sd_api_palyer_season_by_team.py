import requests
import os
import pandas as pd
from database_config import MyDatabase

# getting the API-Key which is stored in the environment variables 
# api_key = os.environ.get('SD_API_Key')

# url = "https://api.sportsdata.io/v3/nfl/stats/json/PlayerSeasonStatsByTeam/{season}/{team}"

# payload={}
# headers = {
#     'Ocp-Apim-Subscription-Key': f'{api_key}'
# }

# response = requests.request("GET", url, headers=headers, data=payload)
# print(response.text)
# res_json = response.json()

# Extracting all teams from our database
db = MyDatabase

team_list = list()
team_query = """SELECT team_short FROM sd_teams"""

team_list = db.query_func(team_query)
print(team_list)

# Extracting playerstats for 


# Joinng all 32 team dataframes to one big dataframe


