import requests
import urllib.parse
from bs4 import BeautifulSoup

import re
import json

from typing import List, Dict

import tools.web.configs as cfg
from copy import deepcopy

def google_scholar_parse(response, limit=20):
    if isinstance(response, requests.Response):
        response = response.text
    soup = BeautifulSoup(response, 'html.parser')

    search_entry_pattern = re.compile(r"\bgs_r gs_or gs_scl\b")
    title_pattern = "gs_rt"
    author_pattern = "gs_fmaa"
    abstract_pattern = ("gs_fma_abs", re.compile(r"gsh_csp|gs_fma_snp"))

    elements = soup.find_all(class_=search_entry_pattern)

    results = []
    for elem in elements:
        h3_elem = elem.find('h3', class_=title_pattern)
        au_elem = elem.find('div', class_=author_pattern)
        abs_elem = elem.find('div', class_=abstract_pattern[1])
        
        a_elem = h3_elem.find('a', href=True) if h3_elem else None
        
        title = None
        page_url = None
        if a_elem:
            page_url = urllib.parse.unquote(a_elem['href'])
            for b in a_elem.find_all('b'):
                b.unwrap()
            title = a_elem.decode_contents()

        authors = au_elem.decode_contents() if au_elem else None
        abstract = abs_elem.decode_contents() if abs_elem else None
        
        if not title:
            continue

        data = {
            'title': title,
            'authors': authors,
            'abstract': abstract,
            'page_url': page_url
        }
        data = {k: clean_string(v) for k, v in data.items()}
        results.append(data)

        if len(results) >= limit:  # Limit to top 20 results
            break
    return results

def crossref_parse(response):
    if isinstance(response, requests.Response):
        data = response.json()
    else:
        data = response

    results = []
    if not data['message']['items']:
        return []
    
    for item in data['message']['items']:
        article_title = remove_formatting(item.get('title', [''])[0])
        abstract = remove_formatting(item.get('abstract', None))
        authors = "; ".join([author['given'] + ' ' + author['family'] for author in item.get('author', [])])
        journal = item.get('container-title', [None])[0]
        year = str(item.get('published-print', {}).get('date-parts', [[None]])[0][0])
        doi = item.get('DOI', None)
        keywords = item.get('subject', None)
        
        results.append({
            'title': article_title,
            'abstract': abstract,
            'authors': authors,
            'year': year,
            'journal': journal,
            'doi': doi,
            'keywords': keywords
        })
    return results

def wos_query_parse(response, api: str="runQuerySearch"):
    if isinstance(response, requests.Response):
        response = response.text
    nddata = response.strip().split("\n")
    querydata = []
    queryinfo = None
    for data in nddata:
        data = json.loads(data)
        if data["key"] == "searchInfo":
            queryinfo = data

        if "api" in data and data["api"] == api:
            querydata.append(data)

    records = deepcopy(querydata[0])

    for i in range(1, len(querydata)):
        payload = querydata[i].get("payload", None)
        if payload:
            records["payload"].update(payload)

    qid = queryinfo["payload"]["QueryID"]
    total_records = queryinfo["payload"]["RecordsFound"]
    n_records = len(records["payload"])

    return records, qid, total_records, n_records

def wos_stream_parse(response):
    return wos_query_parse(response, cfg.WOS_API_NAME["stream"])

def wos_fullrec_parse(response):
    if isinstance(response, requests.Response):
        response = response.text
    nddata = response.strip().split("\n")
    querydata = []
    queryinfo = None
    for data in nddata:
        data = json.loads(data)
        if data["key"] == "searchInfo":
            queryinfo = data

        if "api" in data and data["api"] == "getFullRecordByQueryId":
            querydata.append(data)

    records = deepcopy(querydata[0])

    for i in range(1, len(querydata)):
        payload = querydata[i].get("payload", None)
        if payload:
            records["payload"].update(payload)

    payload = records.get("payload", None)
    title = payload["titles"]["item"]["en"][0]["title"]
    journal = payload["titles"]["source"]["en"][0]["title"]
    doi = payload["doi"]
    authors = "; ".join([au["display_name"] for au in payload["names"]["author"]["en"]])
    year = payload["pub_info"]["pubyear"]
    abstract = payload.get("abstract", None)

    return {
        "title": title,
        "journal": journal,
        "doi": doi,
        "authors": authors,
        "year": year,
        "abstract": abstract
    }


# utils functions ----------------------------------------
def remove_formatting(text: str):
    if text is None:
        return None
    sup = text.split("\n")
    sup = [s.strip() for s in sup if s.strip()]
    return " ".join(sup)

def clean_string(text: str):
    if text is None:
        return None
    text.replace("\xa0", " ")
    return text