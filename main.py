from typing import Optional
from datetime import datetime, date, timedelta
import calendar
from pprint import pformat
from dataclasses import dataclass


from more_itertools import chunked, flatten

from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates

from data import get_data

app = FastAPI()

@dataclass
class ScaleParams:
    orig_min: int
    orig_max: int

    res_min: int
    res_max: int


@dataclass(order=True)
class Cell:
    date: date
    value: int
    is_placeholder: bool

    @staticmethod
    def from_tuple(t):
        return Cell(
            date=t[0],
            value=t[1],
            is_placeholder=False,
        )

    @staticmethod
    def placeholder_for_date(d: date):
        return Cell(
            date=d,
            value=0,
            is_placeholder=True,
        )


def get_scaling_factors(series, res_min, res_max, orig_min=None) -> ScaleParams:
    return ScaleParams(
        orig_min=orig_min or min(series),
        orig_max=max(series),
        res_min=res_min,
        res_max=res_max,
    )

def map_weekday(day: int) -> int:
    if day == 6:
        return 0

    return day+1
    

def scale(number: int, params: ScaleParams):
    normalize_from_origin = (number-params.orig_min) / (params.orig_max - params.orig_min)

    scale_to_result = normalize_from_origin * (params.res_max - params.res_min) + params.res_min

    return scale_to_result


def fill_series(series):
    first = series[0][0]
    last = series[-1][0]

    first_weekday = map_weekday(first.weekday())
    last_weekday = map_weekday(last.weekday())

    result = []

    if first_weekday != 0:
        result.extend(reversed([Cell.placeholder_for_date(first-timedelta(days=d))
                                for d in range(1, first_weekday+1)]))

    result.extend([Cell.from_tuple(x) for x in series])

    if last_weekday != 6:
        result.extend([Cell.placeholder_for_date(last+timedelta(days=d))
                       for d in range(1, 7-last_weekday)])


    return result


def transpose(series):
    return list(zip(*chunked(fill_series(series), 7)))


def get_value(t: tuple):
    return t[1]


def get_values(series: list):
    return [get_value(x) for x in series]


templates = Jinja2Templates(directory="templates")

templates.env.globals.update(pformat=pformat,
                             transpose=transpose,
                             get_scaling_factors=get_scaling_factors,
                             scale=scale,
                             get_values=get_values)



@app.get("/")
def read_root(request: Request):
    calendar = get_data()

    return templates.TemplateResponse("index.html", {"request": request, "calendar": calendar})


