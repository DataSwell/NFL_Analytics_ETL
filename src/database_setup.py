from database_config import MyDatabase

# generating the database object
db = MyDatabase()


# Strings for Creating the tables for the content of the Kaggle Dataset

create_stadiums_table = """CREATE TABLE IF NOT EXISTS stadiums 
    (stadium_name varchar NOT NULL, 
    stadium_location varchar, 
    stadium_open_year int, 
    stadium_close_year int, 
    stadium_type varchar, 
    stadium_address varchar, 
    stadium_weather_station_code varchar, 
    stadium_weather_type varchar, 
    stadium_capacity int, 
    stadium_surface varchar, 
    PRIMARY KEY (stadium_name))
"""

create_teams_table = """CREATE TABLE IF NOT EXISTS teams 
    (team_name varchar PRIMARY KEY, 
    team_name_short varchar, 
    team_id varchar NOT NULL, 
    team_id_pfr varchar, 
    team_conference varchar, 
    team_division varchar, 
    team_conference_pre2002 varchar, 
    team_division_pre2002 varchar)
"""

create_scores_bets_table = """CREATE TABLE IF NOT EXISTS scores_bets 
    (schedule_date date, 
    schedule_season varchar, 
    schedule_week varchar, 
    schedule_playoff bool, 
    team_home varchar, 
    score_home smallint, 
    score_away smallint, 
    team_away varchar, 
    team_favorite_id varchar, 
    spread_favorite varchar, 
    over_under_line varchar, 
    stadium_name varchar, 
    stadium_neutral bool, 
    weather_temperature numeric, 
    weather_wind_mph numeric, 
    weather_humidity numeric, 
    weather_detail varchar, 
    foreign key (team_home) references teams(team_name), 
    foreign key (team_away) references teams(team_name),
    PRIMARY KEY (schedule_date, team_home, team_away))
"""

db.query_func(create_stadiums_table)
db.query_func(create_teams_table)
db.query_func(create_scores_bets_table)
db.close()


# Cretaing the tables for the content of the SportsData-API