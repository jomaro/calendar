from datetime import datetime, date, timedelta
from random import randint

def main():

    start = date(2021, 3, 1)

    today = date.today()

    days = date_to_datetime(today) - date_to_datetime(start)

    time_series = [start + timedelta(days=x) for x in range(days.days)]

    return [(x, gen_n(x)) for x in time_series]



def date_to_datetime(d: date):
    return datetime(d.year, d.month, d.day)


def gen_n(d: date):
    if d.weekday() in (5, 6):
        return 0

    return randint(200, 2600)


if __name__ == "__main__":
    print(main())
