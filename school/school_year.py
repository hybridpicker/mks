import datetime

def get_current_school_year():
    from datetime import date
    old_year = [1,2,3,4,5,6,7,8]
    current_year = date.today().year
    current_month = date.today().month
    if current_month in old_year:
        school_year = str(current_year) + "/" + str(current_year-1)
    else:
        school_year = str(current_year) + "/" + str(current_year+1)[-2:]
    return school_year