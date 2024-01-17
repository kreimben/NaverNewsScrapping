from sqlalchemy import Column, Integer, String, Date

from scrapping.api.database import Base


class News(Base):
    __tablename__ = "news"
    # title,date,document,link,press,category

    id = Column(Integer, primary_key=True)
    date = Column(Date)
    category = Column(String)
    press = Column(String)
    title = Column(String)
    document = Column(String)
    link = Column(String)
