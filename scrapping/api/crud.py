from datetime import date, datetime
from typing import List

import pandas as pd
from sqlalchemy import and_
from sqlalchemy.orm import Session

from . import model
from .dto import NewsDto
from .model import News


def __converter(news: List[News]) -> List[NewsDto]:
    return [NewsDto(id=n.id, press=n.press, title=n.title, link=n.link, category=n.category, date=n.date,
                    document=n.document) for n in news]


def __convert_to_datetime(date_str) -> date:
    # Replace Korean AM/PM with their English equivalents
    date_str = date_str.replace("오전", "AM").replace("오후", "PM")

    # Define the format string corresponding to the date string
    format_str = "%Y.%m.%d. %p %I:%M"

    return datetime.strptime(date_str, format_str).date()


def swap_db(db: Session) -> List[NewsDto]:
    # load data from csv
    df = pd.read_csv('./result_from_20240115_end_20240117.csv')
    # df to pydantic
    news = [News(**row) for index, row in df.iterrows()]
    for n in news:
        n.date = __convert_to_datetime(n.date)
    db.add_all(news)
    db.commit()
    return get_all_news(db)


def get_all_news(db: Session) -> List[NewsDto]:
    news = db.query(model.News).all()
    return __converter(news)


def get_all_news_pagination(db: Session, offset: int = 0, limit: int = 20, **kwargs) -> List[NewsDto]:
    """
    Function about getting all news with pagination.
    :param db: SqlAlchemy Session
    :param offset: Page number
    :param limit: limit of news per page
    :param kwargs: start_date, end_date, press / if press is None or empty, it will return all press
    :return:
    """
    if offset < 1:
        offset = 1

    press = kwargs.get('press')
    start_date = kwargs.get('start_date')
    end_date = kwargs.get('end_date')

    query = db.query(model.News)

    if press:
        query = query.filter_by(press=press)

    if start_date and end_date:
        query = query.filter(
            and_(
                News.date >= start_date,
                News.date <= end_date
            )
        )

    query = query.limit(limit).offset((offset - 1) * limit)

    news = query.all()
    return __converter(news)
