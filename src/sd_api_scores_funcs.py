import datetime
import requests
import os
import pandas as pd
from database_config import MyDatabase
from my_funcs import gameweek, season

# getting the API-Key which is stored in the environment variables 
def sd_scores_extract():
    api_key = os.environ.get('SD_API_Key')

    url = "https://api.sportsdata.io/v3/nfl/scores/json/Scores/{2022REG}"

    payload={}
    headers = {
        'Ocp-Apim-Subscription-Key': f'{api_key}'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    res_json = response.json()
    return res_json


# Transform
def sd_scores_transform(res_json):
    df_scores = pd.DataFrame(res_json)

    df_scores = df_scores.filter(items=[
    'GameKey',
    'SeasonType',
    'Season',
    'Week',
    'Date',
    'AwayTeam',
    'HomeTeam',
    'AwayScore',
    'HomeScore',
    'PointSpread',
    'OverUnder',
    'StadiumID',
    'Day',
    'AwayTeamID',
    'HomeTeamID',
    'ScoreID',
    'Status'
    ])

    # Replacing NaN Values to None which is equal to  NULL in postgres
    # the games which haven´t started can be filtered 
    df_scores = df_scores.fillna(0)
    scores_trans_json = pd.DataFrame.to_json(df_scores)
    print(type(scores_trans_json))
    return scores_trans_json


def sd_scores_load(scores_trans_json):
    df_scores_trans = pd.DataFrame(scores_trans_json)

    # saving local files
    df_scores_trans.to_csv(f'Projekte/Football_Analytics/data/SD_scores_{season()}_{gameweek()}.csv', index=False)
    df_scores_trans.to_excel(f'Projekte/Football_Analytics/data/SD_scores_{season()}_{gameweek()}.xlsx', index=False)

    # Loading into Database
    db = MyDatabase()

    # fresh data must replace the data from the last week for the currant season
    # drop all rows where season_type = 1 and season = 2022 
    insert_scores = """INSERT INTO sd_scores (
        game_key,
        season_type,
        season,
        week,
        date,
        away_team,
        home_team,
        away_score,
        home_score,
        point_spread,
        over_under,
        stadiumID,
        day,
        away_teamID,
        home_teamID,
        scoreID,
        status) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    for i, row in df_scores_trans.iterrows():
        db.query_func(insert_scores, list(row))