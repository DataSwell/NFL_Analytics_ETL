import os
import pandas as pd
from database_config import MyDatabase

# Testcases for the database connection/class
# test_query = '''SELECT * from teams;'''
# create_test = '''CREATE TABLE test (ID int, name varchar)'''
# insert_test = """INSERT INTO teams (team_name, team_id) VALUES ('TestTeam', 'TT')"""
# delete_test = """DELETE FROM teams WHERE team_id = 'TT';"""
# drop_test = """DROP TABLE IF EXISTS test"""



#### EXTRACTING Kaggle datasets #####
# moving the old csv files to archiv
# automized download
# saving the new csv files in the folder data 


##### TRANSFORMATION of Kaggle datasets ####

teams = pd.read_csv('../data/teams.csv')
teams.head()

# encoding in latin instead of utf-8 because of some signs utf-8 doesn´t work
stadiums = pd.read_csv('data/stadiums.csv', encoding='latin1')
# Replacing NaN Values to None which is equal to  NULL in postgres
stadiums = stadiums.where(pd.notnull(stadiums), None)
# saving only the necessary stadium rows
stadiums = stadiums[['stadium_name', 'stadium_location', 'stadium_open', 'stadium_close', 'stadium_type', 
'stadium_address', 'stadium_weather_station_code', 'stadium_weather_type', 'stadium_capacity', 'stadium_surface']]
# replacing the ',' in the column capacity with '', so the column can insert to postgres as integer
stadiums['stadium_capacity'] = stadiums['stadium_capacity'].str.replace(',','')
stadiums.head()

scores_bets = pd.read_csv('data/scores_bets.csv')
# changing the dateformat from dd/mm/yyyy to yyyy-mm-dd for postgres insert
scores_bets['schedule_date'] = pd.to_datetime(scores_bets['schedule_date'])
# Replacing NaN Values to None which is equal to  NULL in postgres
scores_bets = scores_bets.where(pd.notnull(scores_bets), None)
scores_bets.tail()


##### LOADING the Kaggle datasets to the Postgres database #####

# creating database object from the class MyDatabase
db = MyDatabase()