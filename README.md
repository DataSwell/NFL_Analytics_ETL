# NFL_Analytics
For this NFL project different types of data are collected. From Kaggle the "NFL scores and betting" dataset, which
include the historic game scores und betting odds since 1966, also the team and staium information.

https://www.kaggle.com/datasets/tobycrabtree/nfl-scores-and-betting-data?resource=download&select=spreadspoke_scores.csv

Also NFL data from the API (https://sportsdata.io/nfl-api) is used. With the free API Version some data is scramled,
which means, that the data like scores are not the exact results. We want compare them to the real scores from the kaggle data set.
The free API provides 1,000 API calls per month. In the data dictionary is listed, which data is scrambled.

Also the API provides additional informtaion like:
- Games (scrambled, but can be compared to the data from kaggle, only playoffs scrambled?)
- Stadiums
- Standings 
- Team Season Stats (scores, scores by quarters, also for the opponents)
- Team details (Coaches, Offensive- & Defensive Scheme)


## Used Tools
Python Scripts for extracting, transforming and loading the data. The download of the kaggle dataset is automized with a websraper based on selenium, because it is a dynamic page (login). For now the data is stored in a relational Postgres database. 


## Particularities / Hints
Data folder is excluded/ignored from git, because the updting and archiving creates a lot of changed files. 
Therefore the data on GitHub can be old or not coomplete.


## Update intervalls and scheduling
The data will be updated weekly during the Football season. Because the last game of a Gameweek is on monday, the updates will occur on tuesday.
Airflow Schedule:
1. archiving.py -> moves the files from last week in the archiv folder
2. 5 files for the data from the SportsData.io API (scores, stadiums, standings, team_stats, teams)
3. kaggle extract and upload


## Datamodel and Data Dictionary

Normally we want the columns season and week as integer, so we can use SQL operator like between/lower/higher. 
In the table kg_scores_bets the data of the column week is mixed with numbers for the regular season games and also with chars for the different kind of playoff games (Division, Superbowl).
The data for the season, the week and the type of season (pre, regular, pre) of the table sd_scores are all integers. Therefor we can use SQL operators for the data from SportsData.
To equal the schmeas and make the data comparable, a transformation of the kaggle dataset is required. This will happen in different data warehouse layers with SQL scripts run by dbt. There is a different project for the data warehousing part:

https://github.com/DataSwell/football_analytics_dbt
