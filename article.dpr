from sqlalchemy import create_engine, text, \
    Column, Integer, String, ForeignKey, JSON, Table, Enum
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
    keywords = relationship("Keyword",secondary=article_keyword, back_populates="articles")
    notes = relationship("Note", back_populates="article", cascade="all, delete-orphan")
    tree_nodes = relationship("TreeNode", back_populates="article", cascade="all, delete-orphan")

class Keyword(Base):
    __tablename__ = 'keywords'

    id = Column(Integer, primary_key=True)
    word = Column(String)
    articles = relationship("Article", secondary=article_keyword, back_populates="keywords")

class Note(Base):
    r""" the structure of related_cites
    [{
        "doi": "doi_string",
        "local_path": "c://example.pdf",
        "article_id": 1,
    }]
    """
    __tablename__ = 'notes'

    id = Column(Integer, primary_key=True)
    note = Column(String)
    date = Column(String)
    page_number = Column(Integer)
    quote_content = Column(String)
    related_cites = Column(JSON, nullable=True)
    article_id = Column(Integer, ForeignKey('articles.id'))
    article = relationship("Article", back_populates="notes")

class TreeNode(Base):
    __tablename__ = 'tree_nodes'

    node_id = Column(Integer, primary_key=True, autoincrement=True)
    parent_id = Column(Integer, ForeignKey('tree_nodes.node_id'))
    node_name = Column(String, nullable=True)
    node_type = Column(Enum('folder', 'article', name='node_type_enum'), nullable=False)
    article_id = Column(Integer, ForeignKey('articles.id'), nullable=True)
    
    parent = relationship("TreeNode", back_populates="children", remote_side=[node_id])
    children = relationship("TreeNode", back_populates="parent", remote_side=[parent_id])
    article = relationship("Article", back_populates="tree_nodes")

def create_database():
    # Create an engine that stores data in the local directory's
    if not os.path.exists("repository.db"):
        engine = create_engine('sqlite:///repository.db')
        Base.metadata.create_all(engine)

create_database()
if __name__=="__main__":
    pass
    # try:
    #     engine = create_engine('sqlite:///repository.db')
    # except Exception as e:
    #     print("Error Database Structure")
    #     if input("Delete the database and create a new one? (y/n)") == "y":
    #         os.remove("repository.db")
    #         create_database()

    # with engine.connect() as connection:
    #     result = connection.execute(text("SELECT name FROM sqlite_master WHERE type='table'"))
    #     exists = result.fetchone() is not None
    #     print(f"Table exists: {exists}")

    # Session = sessionmaker(bind=engine)
    # session = Session()

    # new_article = create_article("Example Title", "Example Author", "http://example.com", "example.md")
    # session.add(new_article)
    # session.commit()
    # print("finished")

    # articles = session.query(Article).all()
    # for article in articles:
    #     print(article.title, article.author)

    # # 添加Note到特定的Article
    # article = session.query(Article).filter_by(title="Example Title").first()
    # new_note = create_note("Example Note", "2021-01-01", "Example Quote Content", create_cite([("cite1", 1), ("cite2", 2)]))
    # article.notes.append(new_note)
    # session.commit()

    # article = session.query(Article).filter_by(title="Example Title").first()
    # print(article.title, article.notes[0].note)

    # session.close()

