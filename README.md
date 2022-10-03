# NFL_Analytics
 Test
For this NFL project different types of data are collected. From Kaggle the "NFL scores and betting" dataset, which
include the historic game scores und betting odds since 1966.

https://www.kaggle.com/datasets/tobycrabtree/nfl-scores-and-betting-data?resource=download&select=spreadspoke_scores.csv

Also NFL data from the API (https://sportsdata.io/nfl-api) is used. With the free API Version some data is scramled,
which means, that the data like scores are not the exact results. We want compare them to the real scores from the kaggle data set.
The free API provides 1,000 API calls per month.

Also the API provides additional informtaion like:
- Roster and Depth Chart, Team Depth Chart
- Injurys
- Player details (actual Team, Position, Height, Weight, Age, College, Experience)
- Player Season Stats (Rushing, Passing, Receiving, Tackles, Sacks, ...)
- Team details (Coaches, Offensive- & Defensive Scheme)

## Used Tools
Python Scripts for extracting, transforming and loading the data
The data is stored in a Postgres database
Job Orchestration with Airflow
Deployment with Docker

## Particularities
The sportsdata.io API 


## Update intervalls
The data will be updated weekly during the Football season. Because the last game of a Gameweek is on monday, the updates will occur on thursday.


## Datamodel and Data Dictionary
upcoming...


## switching to Cloud
upcomin ....