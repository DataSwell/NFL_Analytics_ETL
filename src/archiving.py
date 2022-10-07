import shutil
from my_funcs import last_gameweek, season


# absolute paths
src_folder = 'D:/Projekte/Football_Analytics/data/'
dst_folder_csv = 'D:/Projekte/Football_Analytics/data/archiv/csv/'
dst_folder_xlsx = 'D:/Projekte/Football_Analytics/data/archiv/xlsx/'

# files to move
csv_files = [
    f'SD_scores_{season()}_{last_gameweek()}.csv',
    f'SD_stadiums_{season()}_{last_gameweek()}.csv',
    f'SD_standings_{season()}_{last_gameweek()}.csv',
    f'SD_team_season_stats_{season()}_{last_gameweek()}.csv',
    f'SD_teams_{season()}_{last_gameweek()}.csv',
    'spreadspoke_scores.csv',
]

xlsx_files = [
    f'SD_scores_{season()}_{last_gameweek()}.xlsx',
    f'SD_stadiums_{season()}_{last_gameweek()}.xlsx',
    f'SD_standings_{season()}_{last_gameweek()}.xlsx',
    f'SD_team_season_stats_{season()}_{last_gameweek()}.xlsx',
    f'SD_teams_{season()}_{last_gameweek()}.xlsx'
]


for file in csv_files:
    # creating file path
    source = src_folder + file
    destination = dst_folder_csv + file
    # move file
    try:
        shutil.move(source, destination)
    except shutil.Error as err:
        print(err)


for file in xlsx_files:
    # creating file path
    source = src_folder + file
    destination = dst_folder_xlsx + file
    # move file
    try:
        shutil.move(source, destination)
    except shutil.Error as err:
        print(err)