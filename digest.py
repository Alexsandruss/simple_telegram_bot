import time


def days_until_summer():
    current_time = time.localtime()
    if current_time[0] % 4 == 0:
        days_in_year = 366
        first_summer_day = 153
    else:
        days_in_year = 365
        first_summer_day = 152
    if current_time[1] > 8:
        result = str(first_summer_day + (days_in_year - current_time[7]) - 1) + " days until summer"
    elif current_time[1] < 6:
        result = str(first_summer_day - current_time[7]) + " days until summer"
    else:
        result = "Summer is here!"
    return result


def days_until_newyear():
    current_time = time.localtime()
    if current_time[0] % 4 == 0:
        days_in_year = 366
    else:
        days_in_year = 365
    return str(days_in_year - current_time[7] + 1) + " days until New Year"
