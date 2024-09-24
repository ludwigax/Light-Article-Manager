GOOGLE_SCHOLAR_HM_URL = "https://scholar.google.com"
GOOGLE_SCHOLAR_URL = "https://scholar.google.com/scholar"

CROSSREF_HM_URL = "https://www.crossref.org"
CROSSREF_URL = "https://api.crossref.org/works"

WOS_HM_URL = "https://webofscience.clarivate.cn/wos/alldb/basic-search"
WOS_API_URL = "https://webofscience.clarivate.cn/api/wosnx/core"

ARXIV_URL = "https://arxiv.org"
ARXIV_API_URL = "https://export.arxiv.org/api/query"

WOS_API_NAME = {
    "query": "runQuerySearch",
    "stream": "runQueryGetRecordsStream",
    "fullrec": "getFullRecordByQueryId",
}

ADDRESSINFO = [
    GOOGLE_SCHOLAR_HM_URL, CROSSREF_HM_URL, WOS_HM_URL, ARXIV_URL
]

GOOGLE_EXAMPLE_HEADERS = {
    "sec-ch-ua-full-version-list": '"Not/A)Brand";v="8.0.0.0", "Chromium";v="126.0.6478.57", "Google Chrome";v="126.0.6478.57"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "Windows",
    "sec-ch-ua-platform-version": "10.0.0",
    "sec-ch-ua-wow64": "?0",
    "sec-ch-ua": '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
    "sec-ch-ua-arch": "x86",
    "sec-ch-ua-bitness": "64",
    "sec-ch-ua-model": "",
    "sec-fetch-user": "?1",
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "upgrade-insecure-requests": "1",
    "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    "priority": "u=0, i",
    "referer": "https://scholar.google.com/?hl=en&as_sdt=0,5",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
}

CROSSREF_EXAMPLE_HEADERS = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-encoding': 'gzip, deflate, br, zstd',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'connection': 'keep-alive',
    'host': 'api.crossref.org',
    'referer': 'https://search.crossref.org/',
    'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Microsoft Edge";v="128"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-site',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.0'
}

WOS_EXAMPLE_HEADERS = {
    "priority": "u=1, i",
    "referer": "EXAMPLE",
    "sec-ch-ua": '"Not/A)Brand";v="8", "Chromium";v="126", "Microsoft Edge";v="126"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "Windows",
    "accept": "application/x-ndjson",
    "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    "content-length": "EXAMPLE",
    "content-type": "EXAMPLE",
    "origin": "https://webofscience.clarivate.cn",
}

WOS_QUERY_BODY = (
    '{"product":"ALLDB","searchMode":"general","viewType":"search","serviceMode":"summary",'
    '"search":{"mode":"general","database":"ALLDB","query":[{"rowField":"TS","rowText":"Machine learning chemistry"}],'
    '"refines":[{"index":"SILOID","value":["PPRN"],"exclude":true}]},"retrieve":{"count":50,"history":true,"jcr":true,"sort":"relevance",'
    '"analyzes":["TP.Value.6","DR.Value.6","REVIEW.Value.6","OA.Value.6","PY.Field_D.6","DT.Value.6","AU.Value.6","PEERREVIEW.Value.6"],'
    '"locale":"en_US"},"eventMode":null,"isPreprintReview":false}'
)

WOS_STREAM_BODY = (
    '{"qid":"EXAMPLE",'
    '"retrieve":{"first":"EXAMPLE","sort":"relevance","count":50,"jcr":true,"highlight":false,"analyzes":[]},'
    '"product":"ALLDB","searchMode":"general","viewType":"records"}'
)

WOS_FULLREC_BODY = (
    '{"qid":"EXAMPLE",'
    '"id":{"value":"EXAMPLE","type":"colluid"},'
    '"retrieve":{"first":1,"links":"retrieve","sort":"relevance","count":1,"view":"super","coll":"",'
    '"activity":true,"analyzes":null,"jcr":true,"reviews":true,"highlight":true,'
    '"secondaryRetrieve":{"associated_data":{"sort":"relevance","count":10},'
    '"cited_references":{"sort":"author-ascending","count":30},"citing_article":{"sort":"date","count":2,'
    '"links":null,"view":"mini"},"cited_references_with_context":{"sort":"date","count":135,"view":"mini"},'
    '"recommendation_articles":{"sort":"recommendation-relevance","count":5,"links":null,"view":"mini"},'
    '"grants_to_wos_records":{"sort":"date-descending","count":30,"links":null,"view":"mini"}},"locale":"en_US"},'
    '"product":"ALLDB","searchMode":"general","serviceMode":"summary","viewType":"records","isPreprintReview":false}'
)

WOS_KW_FIELDS = {
    "topic": "TS",
    "author": "AU",
    "year": "PY",
    "address": "AD",
    "title": "TI",
}