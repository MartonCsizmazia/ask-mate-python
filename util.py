from datetime import datetime


def unix_date_filter(unix_date):
    return datetime.fromtimestamp(unix_date)