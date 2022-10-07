# NFL_Analytics

For this NFL project different types of data are collected. From Kaggle the "NFL scores and betting" dataset, which
include the historic game scores und betting odds since 1966, also the team and staium information.

https://www.kaggle.com/datasets/tobycrabtree/nfl-scores-and-betting-data?resource=download&select=spreadspoke_scores.csv

Also NFL data from the API (https://sportsdata.io/nfl-api) is used. With the free API Version some data is scramled,
which means, that the data like scores are not the exact results. We want compare them to the real scores from the kaggle data set.
The free API provides 1,000 API calls per month. In the data dictionary is listed, which data is scrambled.

Also the API provides additional informtaion like:
- Scores_bets (scrambled, but can be compared to the data from kaggle)
- Stadiums
- Standings 
- Team Season Stats (scores, scores by quarters, also for the opponents)
- Team details (Coaches, Offensive- & Defensive Scheme)
Upcoming:
- Injuries
- Player Season Stats by Teams
Not possible:
 - Player Season STats details, because  there are to much player for the amount of API calls per month with the free version.

## Used Tools
Python Scripts for extracting, transforming and loading the data
The data is stored in a Postgres database
Job Orchestration with Airflow
Deployment with Docker

## Particularities
The sportsdata.io API 

## Hints
data folder is excluded/ignored from git, because the updting and archiving creates a lot of changed files. 
Therefore the data on GitHub can be old or not coomplete.

## Update intervalls
The data will be updated weekly during the Football season. Because the last game of a Gameweek is on monday, the updates will occur on thursday.


## Datamodel and Data Dictionary
upcoming...


## switching to Cloud
upcomin ....