# Airflow imports
from airflow.decorators import dag, task
import pendulum

# Import Modules for code
import json

# Import custom modules 
from sd_api_scores_funcs import sd_scores_extract, sd_scores_transform, sd_scores_load


# [START instantiate_dag]
@dag(
    schedule_interval=None,                             # interval how often the dag will run as a cron expression string
    start_date=pendulum.datetime(2021, 1, 1, tz="UTC"), # from what point on the dag will run 
    catchup=False,                                      # no catchup needed, because we are running an api that returns now values                
    tags=['FootballAnalytics'],                         # tag for searching in airflow GUI
)
def sd_scores():
    """ETL pipeline for extracting the data from the SPortsData.io API,
    transforming it to the needs of our analysis and saving it to local csv and excel files, 
    as well as saving it into a Postgres daabase.
    """
    # [END instantiate_dag]

     # EXTRACT: using the extract function of the script sd_api_scores.py 
    @task()
    def extract():

        scores_json = sd_scores_extract()
        return scores_json

    
    # TRANSFORM: using the transform function of the script sd_api_scores.py
    @task()
    def transform(scores_json: json):
        """
        the transform function filters only the neccessary data of the API result
        and replace NaN values with None, which is required for the load int Postgres.
        """
        scores_trans_json = sd_scores_transform(scores_json)
        return scores_trans_json


    # LOAD: using the load function of the sd_api_script.py
    @task()
    def load(scores_trans_json: json):
        """
        A load task, which takes the result of the transform task and
        writes it to the postgres database and local csv and excel files.
        """  
        sd_scores_load(scores_trans_json)


    # Define the flow of the DAG
    scores_data = extract()
    transformed_scores = transform(scores_data)
    load(transformed_scores)