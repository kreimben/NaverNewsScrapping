from datetime import datetime, timedelta
from typing import List

from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from scrapping.api import model
from scrapping.api.crud import get_all_news_pagination, swap_db, get_all_news
from scrapping.api.database import engine, SessionLocal
from scrapping.api.dto import NewsDto

model.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Scrapping API",
)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/all")
def index(db: Session = Depends(get_db)) -> List[NewsDto]:
    """
    Get all the news without pagination and filtering.
    """
    return get_all_news(db)


@app.get('/filter')
def filter(
        start_date: datetime = datetime.now() - timedelta(days=7),
        end_date: datetime = datetime.now(),
        press: str = None,
        page_number: int = 1,
        limit: int = 20,
        db: Session = Depends(get_db)
) -> List[NewsDto]:
    """
    Get the news with pagination and filtering.
    If you don't give a `press` field, Automatically get you all press. 
    To get a list of press kind, use `/press_kind`.
    """
    return get_all_news_pagination(db, page_number, limit, start_date=start_date, end_date=end_date, press=press)


@app.get('/press_kind')
def press_kind(db: Session = Depends(get_db)) -> List[str]:
    """
    Get all the list of press kind.
    """
    res = db.query(model.News.press).distinct().all()
    return [r[0] for r in res]


@app.get('/reload_db')
def reload_db(db: Session = Depends(get_db)) -> List[NewsDto]:
    """
    Reload the database with the latest data from the saved csv file.
    """
    res = swap_db(db)
    return res
