from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import sqlalchemy.orm

from typing import List
from database import Article, Keyword, Note
from sylva import Sylva

engine = create_engine('sqlite:///repository.db')
with engine.connect() as connection:
    result = connection.execute(text("SELECT name FROM sqlite_master WHERE type='table'"))
    exists = result.fetchone() is not None
    print(f"Table exists: {exists}")

Session = sessionmaker(bind=engine)
session = Session()

sylva = Sylva()
sylva.load()

def global_session() -> sqlalchemy.orm.session.Session:
    return session

def global_sylva() -> Sylva:
    return sylva