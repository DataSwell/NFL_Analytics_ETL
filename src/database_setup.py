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
    schedule_season int, 
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

create_SD_stadiums = """CREATE TABLE IF NOT EXISTS sd_stadiums 
    (stadiumID int PRIMARY KEY,
    stadium_name varchar NOT NULL, 
    stadium_city varchar, 
    stadium_state varchar,
    stadium_country varchar,
    stadium_capacity int, 
    stadium_surface varchar, 
    stadium_type varchar)
"""

create_SD_teams = """CREATE TABLE IF NOT EXISTS sd_teams 
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

create_SD_scores = """CREATE TABLE IF NOT EXISTS sd_scores (
    game_key varchar PRIMARY KEY,
    season_type integer,
    season integer,
    week integer,
    date date,
    away_team varchar,
    home_team varchar,
    away_score integer,
    home_score integer,
    point_spread decimal,
    over_under decimal,
    stadiumID integer,
    day date,
    away_teamID integer,
    home_teamID integer,
    scoreID integer,
    status varchar,
    UNIQUE (scoreID),
    foreign key (away_teamID) references sd_teams (teamID),
    foreign key (home_teamID) references sd_teams (teamID))
"""

create_SD_team_stats = """CREATE TABLE IF NOT EXISTS sd_team_stats (
    season_type integer,
    season integer,
    team varchar,
    score integer,
    opponent_score integer,
    total_score integer,
    score_q1 integer,
    score_q2 integer,
    score_q3 integer,
    score_q4 integer,
    score_overtime integer,
    time_of_possession varchar,
    opponent_score_q1 integer,
    opponent_score_q2 integer,
    opponent_score_q3 integer,
    opponent_score_q4 integer,
    opponent_score_Overtime integer,
    opponent_time_of_possession varchar,
    times_sacked_percentage decimal,
    team_name varchar,
    games integer,
    team_seasonID integer,
    teamID integer,
    team_statID integer,
    foreign key (teamID) references sd_teams (teamID),
    PRIMARY KEY (season_type, season, teamID, games))
"""

create_ncaa_stadiums = """CREATE TABLE IF NOT EXISTS ncaa_stadiums 
    (stadiumID int PRIMARY KEY,
    stadium_active boolean,
    stadium_name varchar NOT NULL, 
    stadium_dome boolean,
    stadium_city varchar, 
    stadium_state varchar)
"""

create_ncaa_teams = """CREATE TABLE IF NOT EXISTS ncaa_teams 
(teamID integer PRIMARY KEY,
team_short varchar,
active boolean,
school varchar,
name varchar, 
stadiumID integer,
ap_rank integer,
wins integer,
losses integer,
conference_wins integer,
conference_losses integer,
global_teamID integer,
coaches_rank integer,
playoff_rank integer,
conferenceID integer,
conference varchar, 
short_display_name varchar)
"""

create_ncaa_teams_season = """CREATE TABLE IF NOT EXISTS ncaa_teams_season 
(statID integer,
teamID integer, 
Season_type integer,
season integer,
name varchar,
team varchar,
wins integer,
losses integer,
points_for integer,
points_against integer,
Conference_Wins integer,
Conference_Losses integer,
Conference_Points_For integer,
Conference_Points_Against integer,
Home_Wins integer,
Home_Losses integer,
Road_Wins integer,
Road_Losses integer,
Streak integer,
Score integer,
Opponent_Score integer,
First_Downs integer,
Third_Down_Conversions integer,
Third_Down_Attempts integer,
Fourth_Down_Conversions integer,
Fourth_Down_Attempts integer,
Penalties integer,
Penalty_Yards integer,
Time_Of_Possession_Minutes integer,
Time_Of_Possession_Seconds integer,
Global_TeamID integer,
Conference_Rank integer,
Division_Rank integer,
Games integer,
Passing_Attempts decimal,
Passing_Completions decimal,
Passing_Yards decimal,
Passing_Completion_Percentage decimal,
Passing_Yards_Per_Attempt decimal,
Passing_Yards_Per_Completion decimal,
Passing_Touchdowns decimal,
Passing_Interceptions decimal,
Passing_Rating decimal,
Rushing_Attempts decimal,
Rushing_Yards decimal,
Rushing_Yards_Per_Attempt decimal,
Rushing_Touchdowns decimal,
Rushing_Long decimal,
Receptions decimal,
Receiving_Yards decimal,
Receiving_Yards_Per_Reception decimal,
Receiving_Touchdowns decimal,
Receiving_Long decimal,
FieldGoals_Attempted decimal,
FieldGoals_Made decimal,
FieldGoal_Percentage	decimal,
FieldGoals_Longest_Made decimal,
ExtraPoints_Attempted decimal,
ExtraPoints_Made decimal,
Interceptions decimal,
Interception_Return_Yards decimal,
Interception_Return_Touchdowns decimal,
Solo_Tackles decimal,
Assisted_Tackles decimal,
Tackles_For_Loss decimal,
Sacks decimal,
Passes_Defended decimal,
Fumbles_Recovered decimal,
Fumble_Return_Touchdowns decimal,
Quarterback_Hurries decimal,
Fumbles decimal,
Fumbles_Lost decimal)
"""

create_ncaa_games = """CREATE TABLE IF NOT EXISTS ncaa_games 
(gameID integer PRIMARY KEY,
season integer,
season_type integer,
week integer,
status varchar,
day	date,
away_team varchar,
home_team varchar,
away_teamID integer,
home_teamID integer,
away_team_name varchar,
home_team_name varchar,
away_team_score integer,
home_team_score integer,
point_spread decimal,
over_under decimal,
stadiumID integer,
title varchar)
"""


db.query_func(create_SD_stadiums)
db.query_func(create_SD_teams)
db.query_func(create_SD_standings)
db.query_func(create_SD_scores)
db.query_func(create_SD_team_stats)
db.query_func(create_ncaa_stadiums)
db.query_func(create_ncaa_teams)
db.query_func(create_ncaa_teams_season)
db.query_func(create_ncaa_games)
db.close()