import pandas as pd
from database_config import MyDatabase


# import the date dimension excel file
df_datedim = pd.read_excel(r'D:/Projekte/Football_Analytics/dimdates.xlsx')
print(df_datedim)
col_count = df_datedim.shape[1]
print(col_count)

for col in df_datedim.columns:
    print(col)


# Loading into Database
db = MyDatabase()

# fresh data must replace the data from the last week for the currant season
# drop all rows where season_type = 1 and season = 2022 

insert_dates = """INSERT INTO dim_date 
    (date_num, 
    date, 
    year_month, 
    quartal, 
    month_num, 
    month_name, 
    month_short, 
    week_num, 
    day_num_year, 
    day_num_month, 
    day_num_week, 
    day_name, 
    day_short, 
    quarter_num, 
    year_quarter, 
    day_num_quarter)  
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
"""

for i, row in df_datedim.iterrows():
     db.query_func(insert_dates, list(row))