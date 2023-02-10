import pandas as pd
from database_config import MyDatabase


# import the date dimension excel file
df_dim_regions = pd.read_excel(r'D:/Projekte/Football_Analytics/dim_regions.xlsx')
print(df_dim_regions)
col_count = df_dim_regions.shape[1]
print(col_count)

for col in df_dim_regions.columns:
    print(col)


# Loading into Database
db = MyDatabase()

# fresh data must replace the data from the last week for the currant season
# drop all rows where season_type = 1 and season = 2022 

insert_regions = """INSERT INTO dim_regions
    (state_id,
    state_name,
    capital,
    region) 
    VALUES (%s, %s, %s, %s)
"""

for i, row in df_dim_regions.iterrows():
     db.query_func(insert_regions, list(row))