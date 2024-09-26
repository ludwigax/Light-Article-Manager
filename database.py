from sqlalchemy import create_engine, text, MetaData, \
    Column, Integer, String, ForeignKey, JSON, Table, inspect
from sqlalchemy.orm import relationship, sessionmaker, declarative_base

import os
import csv
from typing import List
    

Base = declarative_base()

article_keyword = Table(
    'article_keyword', Base.metadata,
    Column('article_id', Integer, ForeignKey('articles.id'), primary_key=True),
    Column('keyword_id', Integer, ForeignKey('keywords.id'), primary_key=True),
)
article_tag = Table(
    'article_tag', Base.metadata,
    Column('article_id', Integer, ForeignKey('articles.id'), primary_key=True),
    Column('tag_id', Integer, ForeignKey('tags.id'), primary_key=True),
)

class Article(Base):
    r"""
    Article Structure:
    
    - `title`: Title of the article
    - `author`: Author(s) of the article
    - `journal`: Journal where the article was published
    - `year`: Publication year
    - `doi`: DOI of the article
    - `local_path`: Local file path of the article
    - `add_time`: Date the article was added
    """
    __tablename__ = 'articles'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    author = Column(String)
    journal = Column(String)
    year = Column(String)
    doi = Column(String)
    local_path = Column(String)
    add_time = Column(String)
    abstract = Column(String) # TODO
    keywords = relationship("Keyword",secondary=article_keyword, back_populates="articles")
    tags = relationship("Tag", secondary=article_tag, back_populates="articles")
    notes = relationship("Note", back_populates="article", cascade="all, delete-orphan")
    annotations = relationship("Annotation", back_populates="article", cascade="all, delete-orphan")

# class ArticleData(Base): # Now use a JSON file to store the data TODO
#     __tablename__ = 'article_data'

#     id = Column(Integer, primary_key=True)
#     article_id = Column(Integer)
#     type = Column(String)
#     data = Column(String)  # Store JSON encoded float array

#     # Define relationship for ORM usage, though not strictly needed
#     # You are not establishing a direct ForeignKey constraint, 
#     # but you can add a relationship for ease of querying if desired
#     article = relationship("Article", backref="article_data", cascade="all, delete-orphan")

class Keyword(Base):
    r"""
    Keyword Structure:

    - `word`: The keyword
    - `count`: Number of articles containing this keyword
    """

    __tablename__ = 'keywords'

    id = Column(Integer, primary_key=True)
    word = Column(String)
    count = Column(Integer, default=0)
    articles = relationship("Article", secondary=article_keyword, back_populates="keywords")

class Tag(Base):
    r"""
    Tag Structure:

    - `tag`: The tag
    - `count`: Number of articles containing this tag
    """

    __tablename__ = 'tags'

    id = Column(Integer, primary_key=True)
    tag = Column(String)
    color = Column(String)
    articles = relationship("Article", secondary=article_tag, back_populates="tags")

class Note(Base):
    r"""
    Note Structure:
    - `title`: Title of the note
    - `note`: Content of the note
    - `add_time`: Time when the note was added
    - `changed_time`: Time when the note was last modified
    - `quote`: Related article quotes (list of dictionaries with `doi`, `local_path`, `article_id`)
    - `torder`: Order of the note
    """

    __tablename__ = 'notes'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    note = Column(String)
    add_time = Column(String)
    changed_time = Column(String)
    quote = Column(JSON, default=[])
    torder = Column(Integer)
    article_id = Column(Integer, ForeignKey('articles.id'))
    article = relationship("Article", back_populates="notes")

class Annotation(Base):
    r"""
    Annotation Structure:

    - `annot`: Content of the annotation.
    - `refer`: Reference information related to the annotation.
    - `page_number`: Page number where the annotation appears.
    - `add_time`: Time when the annotation was added.
    - `changed_time`: Time when the annotation was last modified.
    - `colour`: Highlight color for the annotation.
    - `torder`: Order of the annotation
    """
    
    __tablename__ = 'annotations'

    id = Column(Integer, primary_key=True)
    annot = Column(String)
    refer = Column(String)
    color = Column(String)
    page_number = Column(Integer)
    add_time = Column(String)
    changed_time = Column(String)
    torder = Column(Integer) # needed?
    article_id = Column(Integer, ForeignKey('articles.id'))
    article = relationship("Article", back_populates="annotations")

def create_database():
    # Create an engine that stores data in the local directory's
    if not os.path.exists("repository.db"):
        engine = create_engine('sqlite:///repository.db')
        Base.metadata.create_all(engine)

def export_articles(db_path: str): # TODO
    engine = create_engine('sqlite:///' + db_path)
    metadata = MetaData()
    articles_table = Table('articles', metadata, autoload_with=engine)

    with engine.connect() as conn:
        result = conn.execute(articles_table.select())
        articles_data = result.fetchall()
        columns_name = result.keys()

    def row_to_dict(table_name, columns, data):
        with open(f"{table_name}.csv", mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(columns)
            for row in data:
                writer.writerow(row)

    for table_name in ["articles", "notes"]:
        table = Table(table_name, metadata, autoload_with=engine)
        with engine.connect() as conn:
            result = conn.execute(table.select())
            data = result.fetchall()
            columns = result.keys()
            row_to_dict(table_name, columns, data)

    print("success export articles.csv")

def import_articles(db_path: str):
    engine = create_engine('sqlite:///' + db_path)

    session = sessionmaker(bind=engine)()
    with open('articles.csv', mode='r', newline='', encoding='utf-8') as file: 
        reader = csv.DictReader(file)
        for row in reader:
            for k, v in row.items():
                if not v:
                    row[k] = None
            row['id'] = int(row['id'])
            article = Article(**row)
            session.add(article)
        session.commit()

    with open('notes.csv', mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            for k, v in row.items():
                if not v:
                    row[k] = None
            row['id'] = int(row['id'])
            note = Note(**row)
            session.add(note)
        session.commit()
    print("success import articles.csv")

create_database()
if __name__=="__main__":
    import csv

    engine = create_engine('sqlite:///repository.db')  # 这里使用SQLite数据库作为示例，请根据需要修改为实际的数据库URI
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    with open('articles.csv', 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            article = Article(
                id=row['id'],
                title=row['title'],
                author=row['author'],
                journal=row['journal'],
                year=row['year'] if row['year'] else None,
                doi=row['doi'] if row['doi'] else None,
                local_path=row['local_path'],
                add_time=row['add_time']
            )
            session.add(article)

    session.commit()
    session.close()
    pass