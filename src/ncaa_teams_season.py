import requests
import pandas as pd
from database_config import MyDatabase
import creds
import time


df_teams_seasons_total = pd.DataFrame()

payload={}
headers = {
    'Ocp-Apim-Subscription-Key': f'{creds.cfb_api_key}'
}

# Examples: 2017, 2017
seasons = [2021, 2022]

for season in seasons:
    url = f"https://api.sportsdata.io/v3/cfb/scores/json/TeamSeasonStats/{season}"
    response = requests.request("GET", url, headers=headers, data=payload)
    res_json = response.json()
    print(res_json)

    df_teams_season = pd.DataFrame(res_json)
    print(df_teams_season)
    
    # Filter required informations
    df_teams_season = df_teams_season.filter(items=[
        'StatID', 
        'TeamID', 
        'SeasonType', 
        'Season', 
        'Name', 
        'Team', 
        'Wins', 
        'Losses', 
        'PointsFor', 
        'PointsAgainst', 
        'ConferenceWins', 
        'ConferenceLosses', 
        'ConferencePointsFor', 
        'ConferencePointsAgainst', 
        'HomeWins', 
        'HomeLosses', 
        'RoadWins', 
        'RoadLosses', 
        'Streak', 
        'Score', 
        'OpponentScore', 
        'FirstDowns', 
        'ThirdDownConversions', 
        'ThirdDownAttempts', 
        'FourthDownConversions', 
        'FourthDownAttempts', 
        'Penalties', 
        'PenaltyYards', 
        'TimeOfPossessionMinutes', 
        'TimeOfPossessionSeconds', 
        'GlobalTeamID', 
        'ConferenceRank', 
        'DivisionRank', 
        'Games', 
        'PassingAttempts', 
        'PassingCompletions', 
        'PassingYards', 
        'PassingCompletionPercentage', 
        'PassingYardsPerAttempt', 
        'PassingYardsPerCompletion', 
        'PassingTouchdowns', 
        'PassingInterceptions', 
        'PassingRating', 
        'RushingAttempts', 
        'RushingYards', 
        'RushingYardsPerAttempt', 
        'RushingTouchdowns', 
        'RushingLong', 
        'Receptions', 
        'ReceivingYards', 
        'ReceivingYardsPerReception', 
        'ReceivingTouchdowns', 
        'ReceivingLong', 
        'FieldGoalsAttempted', 
        'FieldGoalsMade', 
        'FieldGoalPercentage', 
        'FieldGoalsLongestMade', 
        'ExtraPointsAttempted', 
        'ExtraPointsMade', 
        'Interceptions', 
        'InterceptionReturnYards', 
        'InterceptionReturnTouchdowns', 
        'SoloTackles', 
        'AssistedTackles', 
        'TacklesForLoss', 
        'Sacks', 
        'PassesDefended', 
        'FumblesRecovered', 
        'FumbleReturnTouchdowns', 
        'QuarterbackHurries', 
        'Fumbles', 
        'FumblesLost'
    ])
    
    # Replacing NaN Values to None which is equal to  NULL in postgres
    # the games which haven´t started can be filtered 
    df_teams_season = df_teams_season.fillna(0)

    # Concat
    df_teams_seasons_total = pd.concat([df_teams_seasons_total, df_teams_season], axis=0, ignore_index=True)

    time.sleep(5)


# Save the data local as a CSV file
df_teams_seasons_total.to_csv(f'Projekte/Football_Analytics/data/NCAA_teams_season.csv', index=False)
df_teams_seasons_total.to_excel(f'Projekte/Football_Analytics/data/NCAA_teams_season.xlsx', index=False)

# Loading the data in the Database
db = MyDatabase()

insert_ncaa_teams_season = """INSERT INTO ncaa_teams_season (
statID,
teamID, 
Season_type,
season,
name,
team,
wins,
losses,
points_for,
points_against,
Conference_Wins,
Conference_Losses,
Conference_Points_For,
Conference_Points_Against,
Home_Wins,
Home_Losses,
Road_Wins,
Road_Losses,
Streak,
Score,
Opponent_Score,
First_Downs,
Third_Down_Conversions,
Third_Down_Attempts,
Fourth_Down_Conversions,
Fourth_Down_Attempts,
Penalties,
Penalty_Yards,
Time_Of_Possession_Minutes,
Time_Of_Possession_Seconds,
Global_TeamID,
Conference_Rank,
Division_Rank,
Games,
Passing_Attempts,
Passing_Completions,
Passing_Yards,
Passing_Completion_Percentage,
Passing_Yards_Per_Attempt,
Passing_Yards_Per_Completion,
Passing_Touchdowns,
Passing_Interceptions,
Passing_Rating,
Rushing_Attempts,
Rushing_Yards,
Rushing_Yards_Per_Attempt,
Rushing_Touchdowns,
Rushing_Long,
Receptions,
Receiving_Yards,
Receiving_Yards_Per_Reception,
Receiving_Touchdowns,
Receiving_Long,
FieldGoals_Attempted,
FieldGoals_Made,
FieldGoal_Percentage,
FieldGoals_Longest_Made,
ExtraPoints_Attempted,
ExtraPoints_Made,
Interceptions,
Interception_Return_Yards,
Interception_Return_Touchdowns,
Solo_Tackles,
Assisted_Tackles,
Tackles_For_Loss,
Sacks,
Passes_Defended,
Fumbles_Recovered,
Fumble_Return_Touchdowns,
Quarterback_Hurries,
Fumbles,
Fumbles_Lost)  
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
"""

for i, row in df_teams_seasons_total.iterrows():
    db.query_func(insert_ncaa_teams_season, list(row))