# Airflow imports
from airflow.decorators import dag, task
import pendulum

# Import Modules for code
import json
import os
import requests
import datetime
import pandas as pd
import psycopg2


# required Methos and classes
def gameweek():
    gameweek = int(datetime.date.today().isocalendar()[1] - 36)
    return gameweek

def season():
    season = int(datetime.date.today().isocalendar()[0])
    return season

# password for the database from an environment variable
db_pw = os.environ.get('DB_PASS')
conn_str = "host=localhost user=postgres dbname=FootballAnalytics password={}".format(db_pw)

class MyDatabase():
    def __init__(self):
        self.conn = psycopg2.connect(conn_str)
        self.cur = self.conn.cursor()

        self.conn.set_session(autocommit=True)

    def query_func(self, query, params=None):
        try:
            self.cur.execute(query, params)
        except psycopg2.Error as e:
            print(e)



# [START instantiate_dag]
@dag(
    schedule_interval=None,                             # interval how often the dag will run as a cron expression string
    start_date=pendulum.datetime(2021, 1, 1, tz="UTC"), # from what point on the dag will run 
    catchup=False,                                      # no catchup needed, because we are running an api that returns now values                
    tags=['FootballAnalytics']                         # tag for searching in airflow GUI
)
def sd_standings():
    """ETL pipeline for extracting the data from the SPortsData.io API,
    transforming it to the needs of our analysis and saving it to local csv and excel files, 
    as well as saving it into a Postgres daabase.
    """
    # [END instantiate_dag]

         # EXTRACT:
    @task()
    def extract():
        api_key = os.environ.get('SD_API_Key')
        url = "https://api.sportsdata.io/v3/nfl/scores/json/Standings/{2022REG}"

        payload={}
        headers = {
            'Ocp-Apim-Subscription-Key': f'{api_key}'
        }

        response = requests.request("GET", url, headers=headers, data=payload)
        print(response.status_code)

        res_json = response.json()
        return res_json

    
    # TRANSFORM: 
    @task()
    def transform(standings_json: json):
        """
        the transform function filters only the neccessary data of the API result
        and add a column with the actual gameweek
        """
        # Transformation
        df_standings = df_standings.drop(['GlobalTeamID'], axis=1)
        # adding column for the current gameweek of the standings.  
        df_standings['week'] = gameweek()
        standings_transformed_json = pd.DataFrame.to_json(df_standings)

        return standings_transformed_json


    # LOAD: 
    @task()
    def load(standings_transformed_json: json):
        """
        A load task, which takes the result of the transform task and
        writes it to the postgres database and local csv and excel files.
        """
        df_standings = pd.DataFrame(standings_transformed_json)


        df_standings.to_csv(f'Projekte/Football_Analytics/data/SD_standings_{season()}_{gameweek()}.csv', index=False)
        df_standings.to_excel(f'Projekte/Football_Analytics/data/SD_standings_{season()}_{gameweek()}.xlsx', index=False)

        insert_standings_string = """INSERT INTO sd_standings (
            season_type, 
            season, 
            conference, 
            division, 
            team, 
            name, 
            wins, 
            losses, 
            ties, 
            percentage, 
            points_for, 
            points_against, 
            net_points, 
            touchdowns, 
            division_wins, 
            division_losses, 
            conference_wins, 
            conference_losses, 
            teamID, 
            division_ties, 
            conference_ties, 
            division_rank, 
            conference_rank,
            week)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        db = MyDatabase()

        for i, row in df_standings.iterrows():
            db.query_func(insert_standings_string, list(row))


    # Define the flow of the DAG
    standings_data = extract()
    transformed_standings = transform(standings_data)
    load(transformed_standings)