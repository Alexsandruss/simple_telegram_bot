import time
from jsondb import JsonDB


def days_until_summer():
    current_time = time.localtime()
    if current_time[0] % 4 == 0:
        days_in_year = 366
        first_summer_day = 153
        last_summer_day = 244
    else:
        days_in_year = 365
        first_summer_day = 152
        last_summer_day = 243
    if current_time[1] > 8:
        result = "{} days until summer".format(first_summer_day + (days_in_year - current_time[7]) - 1)
    elif current_time[1] < 6:
        result = "{} days until summer".format(first_summer_day - current_time[7])
    else:
        result = "{} days until the end of summer".format(last_summer_day-current_time[7])
    return result


def days_until_newyear():
    current_time = time.localtime()
    if current_time[0] % 4 == 0:
        days_in_year = 366
    else:
        days_in_year = 365
    return "{} days until New Year".format(days_in_year - current_time[7] + 1)


def check_holiday():
    holidays = JsonDB("holidays.json").dictionary
    current_local_time = time.localtime()
    result = "Today there is no holiday("
    for date in holidays.keys():
        if date.split(".") == [str(current_local_time[1]), str(current_local_time[2])]:
            result = holidays[date]
            break
    return result
