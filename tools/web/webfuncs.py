import requests
import urllib.parse

import json
import time
from typing import List, Dict

import tools.web.configs as cfg

# utils functions ----------------------------------------
def quote(url: str):
    return urllib.parse.quote(url, safe=':/?&=')

def wos_keywords(field: str, text: str, boolean: str=None) -> Dict[str, str]:
    kwd = {
        "rowBoolean": boolean, # "AND" or "OR
        "rowField": cfg.WOS_KW_FIELDS[field],
        "rowText": text
    }
    if boolean is None:
        kwd.pop("rowBoolean")
    return kwd

def tcping(urls):
    if not isinstance(urls, list):
        urls = [urls]

    availability = []
    average_latency = []

    for url in urls:
        latencies = []
        for _ in range(3):
            try:
                start_time = time.time()
                response = requests.get(url, timeout=2)
                if response.status_code == 200:
                    latencies.append((time.time() - start_time) * 1000)
            except Exception as e:
                print(e)
                pass
            
        if latencies:
            avg_latency = sum(latencies) / len(latencies)
            average_latency.append(avg_latency)
            availability.append(1)
        else:
            average_latency.append(-1)
            availability.append(0)
    return availability, average_latency


# scrap functions ----------------------------------------
def google_scholar_get(kwd: str):
    # kwd is a string of keywords
    params = {
        "hl": "en",
        "as_sdt": "0,5",
        "q": kwd,
        "oq": "",
    }
    
    response = requests.get(cfg.GOOGLE_SCHOLAR_URL, headers=cfg.GOOGLE_EXAMPLE_HEADERS, params=params)
    if response.status_code != 200:
        raise Exception(f"Status code: {response.status_code}")
    return response

def crossref_get(title, doi=None):
    params = {"query.title": title, "rows": 20}
    if doi:
        params["query.doi"] = doi

    response = requests.get(cfg.CROSSREF_URL, headers=cfg.CROSSREF_EXAMPLE_HEADERS, params=params)
    if response.status_code != 200:
        raise Exception(f"Status code: {response.status_code}")
    return response

def wos_query_post(query_list: List[Dict[str, str]], sid: str):
    query_body_js = json.loads(cfg.WOS_QUERY_BODY)
    query_body_js["search"]["query"] = query_list
    query_body = json.dumps(query_body_js, separators=(',', ':'))

    query_header = cfg.WOS_EXAMPLE_HEADERS
    query_header["content-length"] = str(len(query_body))
    query_header["content-type"] = "text/plain;charset=UTF-8"
    query_header["referer"] = cfg.WOS_HM_URL

    params = {"SID": sid}
    query_url = urllib.parse.urljoin(cfg.WOS_API_URL, cfg.WOS_API_NAME["query"])
    response = requests.post(query_url, headers=query_header, data=query_body, params=params)
    return response
    
def wos_stream_post(first: int, qid: str, sid: str): # TODO what api keys?
    stream_body_js = json.loads(cfg.WOS_STREAM_BODY)
    stream_body_js["qid"] = qid
    stream_body_js["retrieve"]["first"] = str(first)
    stream_body = json.dumps(stream_body_js, separators=(',', ':'))

    stream_header = cfg.WOS_EXAMPLE_HEADERS
    stream_header["content-length"] = str(len(stream_body))
    stream_header["content-type"] = "text/plain;charset=UTF-8"
    stream_header["referer"] = cfg.WOS_HM_URL

    params = {"SID": sid}
    stream_url = urllib.parse.urljoin(cfg.WOS_API_URL, cfg.WOS_API_NAME["stream"])
    response = requests.post(stream_url, headers=stream_header, data=stream_body, params=params)
    return response

def wos_fullrecord_post(wos_uid: str, qid: str, sid: str):
    fullrec_body_js = json.loads(cfg.WOS_FULLREC_BODY)
    fullrec_body_js["qid"] = qid
    fullrec_body_js["id"]["value"] = wos_uid
    fullrec_body = json.dumps(fullrec_body_js, separators=(',', ':'))

    fullrec_header = cfg.WOS_EXAMPLE_HEADERS
    fullrec_header["content-length"] = str(len(fullrec_body))
    fullrec_header["content-type"] = "text/plain;charset=UTF-8"
    fullrec_header["referer"] = cfg.WOS_HM_URL

    params = {"SID": sid}
    fullrec_url = urllib.parse.urljoin(cfg.WOS_API_URL, cfg.WOS_API_NAME["fullrec"])
    response = requests.post(fullrec_url, headers=fullrec_header, data=fullrec_body, params=params)
    return response

def arxiv_get(query, max_results=15):
    params = {
        'search_query': f'all:{query}',
        'start': 0,
        'max_results': max_results
    }
    
    response = requests.get('http://export.arxiv.org/api/query', params=params)
    if response.status_code != 200:
        raise Exception(f"Status code: {response.status_code}")
    return response
