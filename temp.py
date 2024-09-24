from tools.web import webfuncs as wbf
from tools.web import webfuncs_selenium as wbfs
from tools.web import parse as prs
import tools.web.configs as cfg

import json
import urllib
from typing import List, Dict
import requests


wbfs.init_driver()
driver = wbfs.driver
driver.get("https://webofscience.clarivate.cn/")

import time
time.sleep(3)

cookies = driver.get_cookies()

_, wossid = wbfs.wos_login()
text = "machine learning"
kwd = [wbf.wos_keywords("topic", text)]
# if wossid is None:
#     print("Login failed")
#     exit()

headers = {
    ':authority': 'webofscience.clarivate.cn',
    ':method': 'POST',
    ':path': f'/api/wosnx/core/runQuerySearch?SID={wossid}',
    ':scheme': 'https',
    'accept': 'application/x-ndjson',
    'accept-encoding': 'gzip, deflate, br, zstd',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'content-length': 'EXAMPLE',
    'content-type': 'text/plain;charset=UTF-8',
    'origin': 'https://webofscience.clarivate.cn',
    'priority': 'u=1, i',
    'referer': 'https://webofscience.clarivate.cn/wos/alldb/basic-search/',
    'sec-ch-ua': '"Microsoft Edge";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.0',
}

def wos_query_post(query_list: List[Dict[str, str]], sid: str):
    query_body_js = json.loads(cfg.WOS_QUERY_BODY)
    query_body_js["search"]["query"] = query_list
    query_body = json.dumps(query_body_js, separators=(',', ':'))

    query_header = headers
    query_header["content-length"] = str(len(query_body))
    query_header["content-type"] = "text/plain;charset=UTF-8"
    # query_header["referer"] = cfg.WOS_HM_URL

    # for key, value in cookies.items():
    #     query_header[key] = value

    params = {"SID": sid}
    query_url = urllib.parse.urljoin(cfg.WOS_API_URL, cfg.WOS_API_NAME["query"])
    response = requests.post(query_url, headers=query_header, data=query_body, params=params, cookies=cookies)
    return response




response = wbf.wos_query_post(kwd, wossid)
with open("temp.json", "w") as f:
    f.write(response.text)
# records, qid, total_records, n_records = prs.wos_query_parse(response)