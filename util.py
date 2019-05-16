from datetime import datetime


def unix_date_filter(unix_date):
    return datetime.fromtimestamp(unix_date)


def date_to_unix(date):
    return datetime.timestamp(date)


def unix_date_now():
    now = datetime.now().timestamp()
    return int(now)
