import os
import pandas
from database_config import MyDatabase


test_query = '''SELECT * from teams;'''
create_test = '''CREATE TABLE test (ID int, name varchar)'''
insert_test = """INSERT INTO teams (team_name, team_id) VALUES ('TestTeam', 'TT')"""
delete_test = """DELETE FROM teams WHERE team_id = 'TT';"""
drop_test = """DROP TABLE IF EXISTS test"""

db = MyDatabase()
# teams = db.fetchall(test_query)
# print(teams)
db.query_func(drop_test)
db.close()

