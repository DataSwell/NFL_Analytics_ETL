import datetime

# isocalender creates a tuple (Year, week, weekday)
# Generating the current Game Week. Because the season started in the 
def gameweek():
    gameweek = int(datetime.date.today().isocalendar()[1] - 36)
    return gameweek

# last Game Week (for archiving)
def last_gameweek():
    last_gameweek = int(datetime.date.today().isocalendar()[1] - 36 - 1)
    return last_gameweek

# Season
def season():
    season = int(datetime.date.today().isocalendar()[0])
    return season


