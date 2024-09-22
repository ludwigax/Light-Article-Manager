import os
import re
from typing import List, Dict, Tuple, Union
from urllib.parse import unquote
from PySide6.QtCore import QUrl

from sqlalchemy.orm.session import Session
from sqlalchemy import asc, inspect

from database import Article, Keyword, Note, Annotation
from sylva import ArticleData, NoteData, AnnotationData, Sylva

from func import global_session, global_sylva
import datetime

def create_article(article_data: ArticleData, keywords: List[str] = []) -> Article: # TODO keywords error may cause ?
    article = Article(**article_data.to_dict())
    if keywords:
        keywords = [word.strip() for word in keywords]
        article.keywords = create_keywords(keywords)
    return article

def create_keyword(word: str) -> Keyword:
    word = word.strip().lower()
    keyword = global_session().query(Keyword).filter_by(word=word).first() or Keyword(word=word)
    return keyword

def create_keywords(words = List[str] | str) -> List[Keyword]:
    keywords = []
    if isinstance(words, str):
        words = [words]
    for word in words: # no duplicates
        word = word.strip().lower()
        keyword = global_session().query(Keyword).filter_by(word=word).first() or Keyword(word=word)
        keywords.append(keyword)
    return keywords

def create_note(note_data: NoteData) -> Note:
    note = Note(**note_data.to_dict())
    return note

def create_annotation(annot_data: AnnotationData) -> Annotation:
    annot = Annotation(**annot_data.to_dict())
    return annot

def to_data(table_item) -> ArticleData | NoteData | AnnotationData:
    inspector = inspect(table_item)
    kvpair = {key: getattr(table_item, key) for key in inspector.mapper.attrs.keys()}
    if table_item.__class__.__name__ == 'Article':
        return ArticleData(**kvpair)
    elif table_item.__class__.__name__ == 'Note':
        return NoteData(**kvpair)
    elif table_item.__class__.__name__ == 'Annotation':
        return AnnotationData(**kvpair)
    

# --------------------------------------------------------------------------------
# SQL operations
def search_title_articles(search_pattern) -> List[Article]:
    session = global_session()
    articles = session.query(Article).filter(Article.title.contains(search_pattern)).all()
    return articles

def search_author_articles(search_pattern) -> List[Article]:
    session = global_session()
    articles = session.query(Article).filter(Article.author.contains(search_pattern)).all()
    return articles

def search_journal_articles(search_pattern) -> List[Article]:
    session = global_session()
    articles = session.query(Article).filter(Article.journal.contains(search_pattern)).all()
    return articles

def search_year_articles(search_pattern) -> List[Article]:
    session = global_session()
    articles = session.query(Article).filter_by(Article.year.contains(search_pattern)).all()
    return articles

def search_doi_article(doi: str) -> Article:
    session = global_session()
    article = session.query(Article).filter(Article.doi == doi).first()
    return article

def search_keyword_articles(keyword: str) -> List[Keyword]:
    session = global_session()
    keywords = session.query(Keyword).filter(Keyword.word.contains(keyword)).all()
    return keywords

def get_article(article_id: int) -> Article:
    session = global_session()
    article = session.query(Article).filter(Article.id == article_id).first()
    return article

def get_note_article(note: int | Note) -> Article:
    session = global_session()
    if isinstance(note, int):
        note = session.query(Note).filter(Note.id == note).first()
    return note.article

def get_article_notes(article: Article) -> List[Note]:
    session = global_session()
    notes = session.query(Note).join(Article).filter(Article.id == article.id).order_by(asc(Note.torder)).all()
    return notes

def get_note(note_id: int) -> Note:
    session = global_session()
    note = session.query(Note).filter(Note.id == note_id).first()
    return note

def get_all_articles() -> List[Article]:
    session = global_session()
    articles = session.query(Article).all()
    return articles

def get_all_keywords() -> List[Keyword]:
    session = global_session()
    keywords = session.query(Keyword).all()
    return keywords

def add_article(article: Article):
    session = global_session()
    session.add(article)
    session.commit()
    return article

def add_keywords(keywords: List[Keyword], article: Article):
    session = global_session()
    article.keywords.extend(keywords)
    session.commit()
    return keywords

def add_note(note: Note, article: Article):
    session = global_session()
    article.notes.append(note)
    session.commit()
    return note

def reset_article(data: ArticleData, article: Article):
    session = global_session()
    article.title = data.title
    article.author = data.author
    article.journal = data.journal
    article.year = data.year
    article.doi = data.doi
    article.local_path = data.local_path
    article.abstract = data.abstract
    if article.add_time is None:
        article.add_time = data.add_time
    session.commit()

def reset_keywords(keywords: List[Keyword], article: Article):
    session = global_session()
    article.keywords = keywords
    session.commit()

def reset_note(data: NoteData, note: Note):
    session = global_session()
    note.title = data.title
    note.note = data.note
    note.add_time = data.add_time
    note.changed_time = data.changed_time
    note.quote = data.quote
    note.torder = data.torder
    session.commit()

def remove_keywords(keywords: List[Keyword], article: Article):
    session = global_session()
    pass # TODO i think reset_keywords([]) could substitute this

def delete_article(article_id):
    session = global_session()
    session.query(Article).filter(Article.id == article_id).delete()
    session.commit()

def cascade_delete_article(article_id):
    session = global_session()
    article = session.query(Article).filter(Article.id == article_id).one_or_none()
    if not article:
        return
    session.delete(article)
    session.commit()

def delete_note(note_id):
    session = global_session()
    session.query(Note).filter(Note.id == note_id).delete()
    session.commit()

# --------------------------------------------------------------------------------
# tree operations

def add_folder(idx1: int, folder_name: str):
    sylva = global_sylva()
    if sylva.find(folder_name):
        folder_name = folder_name + ' (1)'

    if idx1 == -1:
        item = sylva.newitem(folder_name, [])
    else:
        item = sylva.newitem_at(idx1, folder_name, [])
    sylva.save()
    return item

def add_folder_article(id: int, article_id: int):
    sylva = global_sylva()
    assert(sylva.index(id) is not None)
    sylva.index(id)['data'].append(article_id)
    sylva.save()

def rename_folder(id: int, new_name: str):
    sylva = global_sylva()
    assert(sylva.index(id) is not None)
    sylva.setitem(id, new_name)
    sylva.save()

def delete_folder(id: int):
    sylva = global_sylva()
    assert(sylva.index(id) is not None)
    sylva.delitem(id)
    sylva.save()

def delete_folder_article(id: int, idx2: int):
    sylva = global_sylva()
    assert(sylva.index(id) is not None)
    sylva.index(id)['data'].pop(idx2)
    sylva.save()

def delete_folder_article_by_id(article_id: int):
    sylva = global_sylva()
    for item in sylva.data:
        if article_id in item['data']:
            item['data'] = [x for x in item['data'] if x != article_id]
    sylva.save()

def get_time():
    return datetime.datetime.now().strftime('%Y-%m-%d')

def open_file(path: str | QUrl) -> bool:
    if path is None:
        return False
    if isinstance(path, QUrl):
        path = path.toString()
    path = unquote(path)
    try:
        os.startfile(path)
        return True
    except:
        return False
    
def check_path(path: str) -> bool:
    if os.path.exists(str(path)):
        return True
    return False
    
def get_absolute_path(path: str) -> str:
    if path is None or not path.strip():
        return None
    path = path.strip().replace("/", "_")
    return os.path.join(os.environ.get("LAM_WORK_DIR"), "papers", f"{path}")

def get_related_path(path: str) -> str:
    if path is None or not path.strip():
        return None
    return os.path.basename(path)
    

# --------------------------------------------------------------------------------
# re operations
def matches_pattern(text: str, pattern: str) -> List[Tuple[int, int]]:
    matches = []
    for mat in re.finditer(pattern, text, re.IGNORECASE):
        start, end = mat.span()
        matches.append((start, end))
    return matches
