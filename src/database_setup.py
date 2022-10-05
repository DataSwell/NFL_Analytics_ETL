from database_config import MyDatabase

# generating the database object
db = MyDatabase()


# Strings for Creating the tables for the content of the Kaggle Dataset

create_KG_stadiums_table = """CREATE TABLE IF NOT EXISTS kg_stadiums 
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

create_KG_teams_table = """CREATE TABLE IF NOT EXISTS kg_teams 
    (team_name varchar PRIMARY KEY, 
    team_name_short varchar, 
    team_id varchar NOT NULL, 
    team_id_pfr varchar, 
    team_conference varchar, 
    team_division varchar, 
    team_conference_pre2002 varchar, 
    team_division_pre2002 varchar)
"""

create_KG_scores_bets_table = """CREATE TABLE IF NOT EXISTS kg_scores_bets 
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
    foreign key (team_home) references kg_teams(team_name), 
    foreign key (team_away) references kg_teams(team_name),
    PRIMARY KEY (schedule_date, team_home, team_away))
"""

db.query_func(create_KG_stadiums_table)
db.query_func(create_KG_teams_table)
db.query_func(create_KG_scores_bets_table)



# Cretaing the tables for the content of the SportsData-API

create_SD_stadiums_table = """CREATE TABLE IF NOT EXISTS sd_stadiums 
    (stadiumID int PRIMARY KEY,
    stadium_name varchar NOT NULL, 
    stadium_city varchar, 
    stadium_state varchar,
    stadium_country varchar,
    stadium_capacity int, 
    stadium_surface varchar, 
    stadium_type varchar)
"""

create_SD_teams_table = """CREATE TABLE IF NOT EXISTS sd_teams 
    (team_short varchar,
    teamID int PRIMARY KEY,
    city varchar NOT NULL, 
    conference varchar, 
    division varchar,
    fullname varchar,
    stadiumID int,
    head_coach varchar,
    offensive_coordinator varchar, 
    defensive_coordinator varchar, 
    special_teams_coordinator varchar,
    offensive_schema varchar,
    defensive_schema varchar,
    foreign key (stadiumID) references sd_stadiums(stadiumID))
"""

create_SD_standings = """CREATE TABLE IF NOT EXISTS sd_standings (
    season_type int, 
    season int, 
    conference varchar, 
    division varchar, 
    team varchar, 
    name varchar, 
    wins int, 
    losses int, 
    ties int, 
    percentage decimal, 
    points_for int, 
    points_against int, 
    net_points int, 
    touchdowns int, 
    division_wins int, 
    division_losses int, 
    conference_wins int, 
    conference_losses int, 
    teamID int, 
    division_ties int, 
    conference_ties int, 
    division_rank int, 
    conference_rank int,
    week int,
    foreign key (teamID) references sd_teams(teamID),
    PRIMARY KEY (season_type, season, teamID, week))
"""

create_SD_team_stats = """
"""

create_SD_player_season_by_team = """
"""


db.query_func(create_SD_stadiums_table)
db.query_func(create_SD_teams_table)
db.query_func(create_SD_standings)
db.close()