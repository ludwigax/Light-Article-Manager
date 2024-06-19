import os
import re
import bibtexparser
from urllib.parse import unquote
from typing import List, Dict, Tuple

from database import Article, Keyword, Note
from archi import ArticleData

from utils.opn import matches_pattern, to_data
import markdown2

# --------------------------------------------------------------------------------
# predefined html strings
CSS_THEMES = {
    "microsoft_white": """
        body {
            background-color: #ffffff;
            color: #000000;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            font-size: 14px;
        }
        h1 { color: #0a0a0a; }
        h2 { color: #0a0a0a; }
        h3 { color: #114467; }
        h4 { color: #114467; }
        h5 { color: #4472c4; }
        .title-style { font-weight: bold; font-size: 18px; color: #0a0a0a; }
        .author-style { font-size: 12px; color: grey; }
        .journal-style { font-weight: bold; font-size: 16px; color: green; }
        .year-style { font-weight: bold; font-size: 16px; color: #0a0a0a; }
        .doi-style { font-size: 12px; color: #2b6fff; }
        .path-style { font-size: 12px; color: #2b6fff; }
        .time-style { font-size: 12px; color: grey; }
        .highlight { background-color: yellow; }
        .keyword-style { background-color: grey; color: white; }
    """
}

FIELD_STYLES = {
    'title': 'title-style',
    'author': 'author-style',
    'journal': 'journal-style',
    'year': 'year-style',
    'doi': 'doi-style',
    'local_path': 'path-style',
    'add_time': 'time-style'
}

# this is deprecated decorator
RED_BOLD = lambda x: f'<span style="color: red; font-weight: bold;">{x}</span>'
GREEN_BOLD = lambda x: f'<span style="color: green; font-weight: bold;">{x}</span>'
BLUE_BOLD = lambda x: f'<span style="color: blue; font-weight: bold;">{x}</span>'
YELLOW_BKG = lambda x: f'<span style="background-color: yellow;">{x}</span>'
GREY_BKG = lambda x: f'<span style="background-color: grey; color: white;">{x}</span>'
CITE_TEXT = lambda x: f'<span style="font-size: 10pt; color: gray;">{x}</span>'
URL_TEXT = lambda x: f'<span style="font-size: 10pt; color: blue; text-decoration: underline;">{x}</span>'

PDF_FILTER = "pdf files (*.pdf)"
BIB_FILTER = "bibtex files (*.bib)"
SEP = "\n\n---\n\n"

def ANCHOR_TEXT(x, local_path):
    if local_path is None:
        return x
    return f'<a href="{absolute_path(local_path)}">{x}</a>'

ARTICLE_INFO = lambda tl, au, jn, yr, url, local_path: f"""**{tl}**<br>
{CITE_TEXT(au)}<br>
{GREEN_BOLD(jn)} {yr}<br>
{URL_TEXT(url)}<br>
{URL_TEXT(ANCHOR_TEXT(local_path, local_path))}"""

KEYWORD_INFO = lambda word: f"{GREY_BKG(word)} &nbsp;"

NOTE_INFO = lambda note, date, page, quote_content: f"""{BLUE_BOLD(note)}<br>
{CITE_TEXT(date + "  " + str(page))} <br>
{quote_content}"""

# the upper part is deprecated

# --------------------------------------------------------------------------------
# highlevel formatting functions
def highlight_search_results(text: str, search_str: str) -> str:
    matches = matches_pattern(text, search_str)
    return highlight_matches(text, matches)

# --------------------------------------------------------------------------------
# basic formatting functions
# def article_info(article: Article) -> Dict[str, str]:
#     return {
#         'title': article.title,
#         'author': article.author,
#         'journal': article.journal,
#         'year': article.year,
#         'doi': article.doi,
#         'local_path': article.local_path,
#         'keywords': [keyword.word for keyword in article.keywords]
#     }

# def note_info(note: Note) -> Dict[str, str]:
#     return {
#         'note': note.note,
#         'date': note.date,
#         'page_number': note.page_number,
#         'quote_content': note.quote_content,
#         'related_cites': note.related_cites # List[dict]
#     }

def wrap_html(html_content: str, css_content: str) -> str:
    full_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <style>
    {css_content}
    </style>
    </head>
    <body>
    {html_content}
    </body>
    </html>
    """
    return full_html

def anchor_path(path: str) -> str:
    if path is None:
        return None
    return f'<a href="{absolute_path(path)}">{related_path(path)}</a>'

def get_article_html(article: Article, article_only=False) -> str:
    ArticleData = to_data(article)
    raw = ""
    raw_dict: Dict[str, str] = {}
    for key in ArticleData.keys():
        if key == "local_path":
            raw_dict[key] = f"<span class='{FIELD_STYLES[key]}'>{anchor_path(ArticleData[key])}</span><br>\n"
            continue
        raw_dict[key] = f"<span class='{FIELD_STYLES[key]}'>{ArticleData[key]}</span><br>\n"
    raw += raw_dict['title'] + raw_dict['author'] + raw_dict['journal'].replace("<br>\n", " ") +\
        raw_dict['year'] + raw_dict['doi'] + raw_dict['local_path'] + raw_dict['add_time']

    if not article_only:
        if article.keywords:
            raw += "<hr>"
            raw += get_keywords_html(article.keywords)
        if article.notes:
            raw += "<hr>"
            raw += get_notes_html(article.notes)
        annotations = article.annotations
    return raw

def get_keywords_html(keywords: List[Keyword]) -> str:
    raw = ""
    for keyword in keywords:
        raw += f"<span class='keyword-style'>{keyword.word}</span> &nbsp;"
    return raw

def get_notes_html(notes: List[Note]) -> str:
    raw = ""
    for note in notes:
        html = markdown2.markdown(note.note)
        raw += f"{html}<br>"
        raw += f"<span class='time-style'>{note.date}</span><br>"
    return raw

def get_annotations_html(annotations: List[str]) -> str:
    pass # TODO
    return ""

def highlight_matches(text: str, matches: List[Tuple[int, int]]) -> str: # deprecated function
    yellowed_text = ""
    last_end = 0
    for start, end in matches:
        yellowed_text += text[last_end:start]
        yellowed_text += YELLOW_BKG(text[start:end])
        last_end = end
    yellowed_text += text[last_end:]
    return yellowed_text

def progressbar(percentage: int) -> str:
    fullblock = (percentage // 4) * "█"
    restblock = percentage % 4
    if restblock==0:
        partblock = ""
    elif restblock==1:
        partblock = "▏"
    elif restblock==2:
        partblock = "▎"
    elif restblock==3:
        partblock = "▍"
    return f'{fullblock}{partblock}'

def absolute_path(path: str) -> str:
    if path is None:
        return None
    if path.strip():
        path = path.replace("/", "_")
        return os.path.join(os.environ.get("LAM_WORK_DIR"), "papers", f"{path}")
    
def related_path(path: str) -> str:
    if path is None:
        return None
    return os.path.basename(path)

def open_path(path) -> None:
    if path is None:
        return
    path = unquote(path.toString())
    os.startfile(path)
    