from datetime import date
from typing import Optional

from pydantic import BaseModel


class NewsDto(BaseModel):
    id: Optional[int]
    date: Optional[date]
    category: Optional[str]
    press: Optional[str]
    title: Optional[str]
    document: Optional[str]  # Maybe content of news.
    link: Optional[str]

    class Config:
        from_attributes = True
