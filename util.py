from datetime import datetime


def date_now():
    dt = datetime.now()
    return dt.replace(microsecond=0)

