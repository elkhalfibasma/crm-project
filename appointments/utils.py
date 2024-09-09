import calendar
from datetime import datetime

def get_calendar_weeks(year, month):
    cal = calendar.Calendar(firstweekday=0)  # Monday as the first day of the week
    month_days = cal.monthdayscalendar(year, month)

    # Add leading and trailing empty weeks if needed
    weeks = []
    for week in month_days:
        weeks.append(week)
    return weeks