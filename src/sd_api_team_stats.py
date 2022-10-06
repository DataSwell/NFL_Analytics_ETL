import datetime
import requests
import os
import pandas as pd
from database_config import MyDatabase
from my_funcs import gameweek, season

# getting the API-Key which is stored in the environment variables 
api_key = os.environ.get('SD_API_Key')


url = "https://api.sportsdata.io/v3/nfl/scores/json/TeamSeasonStats/{2022REG}"

payload={}
headers = {
    'Ocp-Apim-Subscription-Key': f'{api_key}'
}

response = requests.request("GET", url, headers=headers, data=payload)
print(response.text)

res_json = response.json()
df_team_season_stats = pd.DataFrame(res_json)


# Transformation
df_team_season_stats = df_team_season_stats.filter(items=[
'SeasonType', 
'Season',
'Team',
'Score',
'OpponentScore',
'TotalScore',
'ScoreQuarter1',
'ScoreQuarter2',
'ScoreQuarter3',
'ScoreQuarter4',
'ScoreOvertime',
'TimeOfPossession',
'OpponentScoreQuarter1',
'OpponentScoreQuarter2',
'OpponentScoreQuarter3',
'OpponentScoreQuarter4',
'OpponentScoreOvertime',
'OpponentTimeOfPossession',
'TimesSackedPercentage',
'TeamName',
'Games',
'TeamSeasonID',
'TeamID',
'TeamStatID'
])

print(df_team_season_stats.head())
print(df_team_season_stats.tail())


df_team_season_stats.to_csv(f'Projekte/Football_Analytics/data/SD_team_season_stats_{season()}_{gameweek()}.csv', index=False)
df_team_season_stats.to_excel(f'Projekte/Football_Analytics/data/SD_team_season_stats_{season()}_{gameweek()}.xlsx', index=False)

# fresh data must replace the data from the last week for the currant season

# Loading into Database
db = MyDatabase()

insert_team_stats = """INSERT INTO sd_team_stats (
    season_type,
    season,
    team,
    score,
    opponent_score,
    total_score,
    score_q1,
    score_q2,
    score_q3,
    score_q4,
    score_overtime,
    time_of_possession,
    opponent_score_q1,
    opponent_score_q2,
    opponent_score_q3,
    opponent_score_q4,
    opponent_score_Overtime,
    opponent_time_of_possession,
    times_sacked_percentage,
    team_name,
    games,
    team_seasonID,
    teamID,
    team_statID)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
"""

for i, row in df_team_season_stats.iterrows():
    db.query_func(insert_team_stats, list(row))