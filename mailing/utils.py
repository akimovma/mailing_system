import calendar
import datetime


def next_month(date, months=0):
    """
    Calculate next month date
    """
    month_range = calendar.monthrange(date.year, date.month)[1]
    month = datetime.timedelta(days=month_range)
    next_date = date + month
    return next_month(next_date, months - 1) if months else next_date
