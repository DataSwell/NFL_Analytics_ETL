import os
import pandas as pd
from database_config import MyDatabase
import psycopg2 

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

teams = pd.read_csv('Projekte/NFL_Kaggle/data/teams.csv')
print(teams.head())

# encoding in latin instead of utf-8 because of some signs utf-8 doesn´t work
stadiums = pd.read_csv('Projekte/NFL_Kaggle/data/stadiums.csv', encoding='latin1')
# Replacing NaN Values to None which is equal to  NULL in postgres
stadiums = stadiums.where(pd.notnull(stadiums), None)
# saving only the necessary stadium rows
stadiums = stadiums[['stadium_name', 'stadium_location', 'stadium_open', 'stadium_close', 'stadium_type', 
'stadium_address', 'stadium_weather_station_code', 'stadium_weather_type', 'stadium_capacity', 'stadium_surface']]
# replacing the ',' in the column capacity with '', so the column can insert to postgres as integer
stadiums['stadium_capacity'] = stadiums['stadium_capacity'].str.replace(',','')
print(stadiums.head())

scores_bets = pd.read_csv('Projekte/NFL_Kaggle/data/scores_bets.csv')
# changing the dateformat from dd/mm/yyyy to yyyy-mm-dd for postgres insert
scores_bets['schedule_date'] = pd.to_datetime(scores_bets['schedule_date'])
# Replacing NaN Values to None which is equal to  NULL in postgres
scores_bets = scores_bets.where(pd.notnull(scores_bets), None)
print(scores_bets.tail())


##### LOADING the Kaggle datasets to the Postgres database #####

# Connecting to the new database nfl_scores_bets   
# password for the database from an environment variable
db_pw = os.environ.get('DB_PASS')
conn_str = "host=localhost user=postgres dbname=nfl_scores_bets password={}".format(db_pw)

try:
    conn = psycopg2.connect(f"host=localhost user=postgres dbname=nfl_scores_bets password={db_pw}")
except psycopg2.Error as e:
    print('Error: Cnnection to database failed')
    print(e)
    
try:
    cur = conn.cursor()
except psycopg2.Error as e:
    print('Cursor failed')
    print(e)
    
conn.set_session(autocommit=True)


stadium_table_insert = ("""INSERT INTO stadiums (
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

teams_table_insert = ("""INSERT INTO teams (
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

scores_bets_table_insert = ("""INSERT INTO scores_bets (
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

# works fine, if i create the datbase connection in this script
# for i, row in scores_bets.iterrows():
#     cur.execute(scores_bets_table_insert, list(row))

# doesn´t work when I do the insert with the method from the database_config script
db =MyDatabase()
for i, row in scores_bets.iterrows():
    db.query_func(scores_bets_table_insert, list(row))

    
    
# for i, row in stadiums.iterrows():
#     cur.execute(stadium_table_insert, list(row))

# for i, row in teams.iterrows():
#     cur.execute(teams_table_insert, list(row))