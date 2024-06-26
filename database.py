from sqlalchemy import create_engine, text, \
    Column, Integer, String, ForeignKey, JSON, Table, inspect
from sqlalchemy.orm import relationship, sessionmaker, declarative_base

import os
from typing import List

Base = declarative_base()

article_keyword = Table(
    'article_keyword', Base.metadata,
    Column('article_id', Integer, ForeignKey('articles.id'), primary_key=True),
    Column('keyword_id', Integer, ForeignKey('keywords.id'), primary_key=True),
)

class Article(Base):
    __tablename__ = 'articles'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    author = Column(String)
    journal = Column(String)
    year = Column(String)
    doi = Column(String)
    local_path = Column(String)
    add_time = Column(String)
    keywords = relationship("Keyword",secondary=article_keyword, back_populates="articles")
    notes = relationship("Note", back_populates="article", cascade="all, delete-orphan")
    annotations = relationship("Annotation", back_populates="article", cascade="all, delete-orphan")

class Keyword(Base):
    __tablename__ = 'keywords'

    id = Column(Integer, primary_key=True)
    word = Column(String)
    articles = relationship("Article", secondary=article_keyword, back_populates="keywords")

class Note(Base):
    r""" the structure of related_content
    [{
        "doi": "doi_string",
        "local_path": "~/example.pdf",
        "article_id": 1,
    }]
    """
    __tablename__ = 'notes'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    note = Column(String)
    date = Column(String)
    related_content = Column(JSON, default=[])
    torder = Column(Integer)
    article_id = Column(Integer, ForeignKey('articles.id'))
    article = relationship("Article", back_populates="notes")

class Annotation(Base):
    __tablename__ = 'annotations'

    id = Column(Integer, primary_key=True)
    annot = Column(String)
    date = Column(String)
    page_number = Column(Integer)
    quote_content = Column(String)
    colour = Column(String)
    torder = Column(Integer) # needed?
    article_id = Column(Integer, ForeignKey('articles.id'))
    article = relationship("Article", back_populates="annotations")

def create_database():
    # Create an engine that stores data in the local directory's
    if not os.path.exists("repository.db"):
        engine = create_engine('sqlite:///repository.db')
        Base.metadata.create_all(engine)

def export_articles(db_path: str, output_path: str = 'articles.csv'):
    import csv
    from sqlalchemy import create_engine, MetaData, Table

    engine = create_engine('sqlite:///' + db_path)
    metadata = MetaData()
    articles_table = Table('articles', metadata, autoload_with=engine)

    with engine.connect() as conn:
        result = conn.execute(articles_table.select())
        articles_data = result.fetchall()

    with open(output_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['id', 'title', 'author', 'journal', 'year', 'doi', 'local_path'])
        for row in articles_data:
            writer.writerow(row)
    print("success export articles.csv")

def import_articles(db_path: str, input_path: str = 'articles.csv'):
    import csv
    from sqlalchemy import create_engine, MetaData, Table

    engine = create_engine('sqlite:///' + db_path)
    metadata = MetaData()
    articles_table = Table('articles', metadata, autoload_with=engine)

    columns = [column.name for column in articles_table.columns]

    with open('articles.csv', mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        with engine.connect() as conn:
            for row in reader:
                data = {column: row.get(column, '') for column in columns}
                conn.execute(articles_table.insert().values(data))
    print("success import articles.csv")

create_database()
if __name__=="__main__":
    # import csv

    # engine = create_engine('sqlite:///repository.db')  # 这里使用SQLite数据库作为示例，请根据需要修改为实际的数据库URI
    # Base.metadata.create_all(engine)

    # Session = sessionmaker(bind=engine)
    # session = Session()

    # with open('test utils/articles.csv', 'r', encoding='utf-8') as file:
    #     reader = csv.DictReader(file)
    #     for row in reader:
    #         article = Article(
    #             id=row['id'],
    #             title=row['title'],
    #             author=row['author'],
    #             journal=row['journal'],
    #             year=row['year'] if row['year'] else None,
    #             doi=row['doi'] if row['doi'] else None,
    #             local_path=row['local_path']
    #         )
    #         session.add(article)

    # session.commit()
    # session.close()
    pass