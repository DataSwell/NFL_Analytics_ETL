import os
import pandas as pd
from database_config import MyDatabase
import psycopg2 
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


#### archiving old datasets ####
# moving the old csv files to archiv folder


#### EXTRACTING Kaggle datasets  with selenium #####
# driver = webdriver.Chrome(executable_path='D:/SeleniumDriver')
# stadiums_url = 'https://www.kaggle.com/datasets/tobycrabtree/nfl-scores-and-betting-data?resource=download&select=nfl_stadiums.csv'
# teams_url = 'https://www.kaggle.com/datasets/tobycrabtree/nfl-scores-and-betting-data?resource=download&select=nfl_teams.csv'
# spread_scores = 'https://www.kaggle.com/datasets/tobycrabtree/nfl-scores-and-betting-data?resource=download&select=spreadspoke_scores.csv'
# dl_button_xpath = '/html/body/main/div[1]/div/div[5]/div[2]/div[5]/div[2]/div[2]/div/div[1]/div/div[1]/div[1]/i'

# driver.get(stadiums_url)
# stadiums_btn = driver.find_element_by_xpath
# stadiums_btn


# saving the new csv files in the folder data 


##### TRANSFORMATION of Kaggle datasets ####

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

scores_bets = pd.read_csv('Projekte/Football_Analytics/data/scores_bets.csv')
# changing the dateformat from dd/mm/yyyy to yyyy-mm-dd for postgres insert
scores_bets['schedule_date'] = pd.to_datetime(scores_bets['schedule_date'])
# Replacing NaN Values to None which is equal to  NULL in postgres
scores_bets = scores_bets.where(pd.notnull(scores_bets), None)
print(scores_bets.tail())


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
  
# for i, row in stadiums.iterrows():
#     db.query_func(stadium_table_insert, list(row))

# for i, row in teams.iterrows():
#     db.query_func(teams_table_insert, list(row))

for i, row in scores_bets.iterrows():
    db.query_func(scores_bets_table_insert, list(row))