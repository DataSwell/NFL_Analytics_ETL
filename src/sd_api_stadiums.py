import requests
import os
import pandas as pd
from database_config import MyDatabase

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

# Save the data local as a CSV file
df_stadiums.to_csv('Projekte/Football_Analytics/data/SD_stadiums.csv', index=False)
df_stadiums.to_excel('Projekte/Football_Analytics/data/SD_stadiums.xlsx', index=False)

# Loading the data in the Database
db = MyDatabase()

insert_stadiums_string = """INSERT INTO sd_stadiums (
stadiumID,
stadium_name,
stadium_city,
stadium_state,
stadium_country,
stadium_capacity,
stadium_surface,
stadium_type) 
VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
"""

for i, row in df_stadiums.iterrows():
    db.query_func(insert_stadiums_string, list(row))
