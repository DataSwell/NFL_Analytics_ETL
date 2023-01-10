import requests
import pandas as pd
from database_config import MyDatabase
import creds


# getting the API-Key which is stored in the environment variables 
url = "https://api.sportsdata.io/v3/cfb/scores/json/Stadiums"

payload={}
headers = {
    'Ocp-Apim-Subscription-Key': f'{creds.cfb_api_key}'
}

response = requests.request("GET", url, headers=headers, data=payload)
res_json = response.json()
df_stadiums = pd.DataFrame(res_json)

# Transform the dataframe
df_stadiums = df_stadiums.drop(['GeoLat', 'GeoLong'], axis=1)

print(df_stadiums.head())
print(df_stadiums.tail())


# Save the data local as a CSV file
df_stadiums.to_csv(f'Projekte/Football_Analytics/data/NCAA_stadiums.csv', index=False)
df_stadiums.to_excel(f'Projekte/Football_Analytics/data/NCAA_stadiums.xlsx', index=False)

# Loading the data in the Database
db = MyDatabase()

insert_stadiums_string = """INSERT INTO ncaa_stadiums (
stadiumID, 
stadium_active, 
stadium_name, 
stadium_dome, 
stadium_city, 
stadium_state) 
VALUES (%s, %s, %s, %s, %s, %s)
"""

for i, row in df_stadiums.iterrows():
    db.query_func(insert_stadiums_string, list(row))
