from datetime import date, timedelta

REVIEW_DAYS = [3, 7, 10, 21, 30, 40]


def get_review_dates(start_date=None):
    if start_date is None:
        start_date = date.today()

    return [
        start_date + timedelta(days=days)
        for days in REVIEW_DAYS
    ]