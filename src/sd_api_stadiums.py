import requests
import os
import pandas as pd

from Projekte.NFL_Analytics.src.database_config import MyDatabase

# getting the API-Key which is stored in the environment variables 
api_key = os.environ.get('SD_API_Key')

url = "https://api.sportsdata.io/v3/nfl/scores/json/Stadiums"

payload={}
headers = {
    'Ocp-Apim-Subscription-Key': f'{api_key}'
}

response = requests.request("GET", url, headers=headers, data=payload)
res_json = response.json()
df_stadiums = pd.DataFrame(res_json)


# Transform the dataframe
df_stadiums = df_stadiums.drop(['GeoLat', 'GeoLong'], axis=1)

print(df_stadiums.head())
print(df_stadiums.tail())

# Loadig the newest Stadiums data to the data Folder
#df_stadiums.to_excel(r'D:\Projekte\NFL_Analytics\data\sd_stadiums.xlsx', index=False, header=True)

# Loading the data in the Database
db = MyDatabase

