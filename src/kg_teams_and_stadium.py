import pandas as pd
from database_config import MyDatabase

##### TRANSFORMATION of Kaggle datasets teams and stadium which are loaded once a year ####
teams = pd.read_csv('Projekte/Football_Analytics/data/teams.csv')
print(teams.head())

# encoding in latin instead of utf-8 because of some signs utf-8 doesn´t work
stadiums = pd.read_csv('Projekte/Football_Analytics/data/stadiums.csv', encoding='latin1')
# Replacing NaN Values to None which is equal to  NULL in postgres
stadiums = stadiums.where(pd.notnull(stadiums), None)
# saving only the necessary stadium rows
stadiums = stadiums[['stadium_name', 'stadium_location', 'stadium_open', 'stadium_close', 'stadium_type', 
'stadium_address', 'stadium_weather_station_code', 'stadium_weather_type', 'stadium_capacity', 'stadium_surface']]
# replacing the ',' in the column capacity with '', so the column can insert to postgres as integer
stadiums['stadium_capacity'] = stadiums['stadium_capacity'].str.replace(',','')
print(stadiums.head())


##### LOADING the Kaggle datasets to the Postgres database #####
stadium_table_insert = ("""INSERT INTO kg_stadiums (
stadium_name,
stadium_location,
stadium_open_year,
stadium_close_year,
stadium_type,
stadium_address, 
stadium_weather_station_code,
stadium_weather_type,
stadium_capacity,
stadium_surface) 
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
""")

teams_table_insert = ("""INSERT INTO kg_teams (
team_name,
team_name_short,
team_id,
team_id_pfr,
team_conference,
team_division,
team_conference_pre2002,
team_division_pre2002)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
""")

scores_bets_table_insert = ("""INSERT INTO kg_scores_bets (
schedule_date,
schedule_season,
schedule_week,
schedule_playoff,
team_home,
score_home,
score_away,
team_away,
team_favorite_id,
spread_favorite,
over_under_line,
stadium_name,
stadium_neutral,
weather_temperature,
weather_wind_mph,
weather_humidity,
weather_detail) 
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
""")

db = MyDatabase()
  
for i, row in stadiums.iterrows():
    db.query_func(stadium_table_insert, list(row))

for i, row in teams.iterrows():
    db.query_func(teams_table_insert, list(row))
