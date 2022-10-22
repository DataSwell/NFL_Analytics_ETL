import pandas as pd
from database_config import MyDatabase

df_scores_bets = pd.read_csv(r'D:/Projekte/Football_Analytics/data/spreadspoke_scores.csv')

# changing the dateformat from dd/mm/yyyy to yyyy-mm-dd for postgres insert
df_scores_bets['schedule_date'] = pd.to_datetime(df_scores_bets['schedule_date'])

# selecting only the neede columns
df_scores_bets = df_scores_bets.filter(items=[
    'schedule_date',
    'schedule_season',
    'schedule_week',
    'schedule_playoff',
    'team_home',
    'score_home',
    'score_away',
    'team_away',
    'team_favorite_id',
    'spread_favorite',
    'over_under_line',
    'stadium',
    'stadium_neutral',
    'weather_temperature',
    'weather_wind_mph',
    'weather_humidity',
    'weather_detail',
])

# Selecting only row for games which already happend (scores are not NaN)
df_scores_bets = df_scores_bets[df_scores_bets['score_home'].notna()]
print(df_scores_bets['score_home'].tail())


# Deleting the data from last week and loading the new file in the data base
scores_bets_table_insert = """INSERT INTO kg_scores_bets (
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
"""

db = MyDatabase()

db.query_func('DELETE FROM kg_scores_bets')

for i, row in df_scores_bets.iterrows():
    db.query_func(scores_bets_table_insert, list(row))