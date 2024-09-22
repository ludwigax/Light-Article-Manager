import requests
import re
from bs4 import BeautifulSoup
import urllib.parse

INITIAL_URL = "https://scholar.google.com/scholar"
QUERY = {
    "hl": "en",
    "as_sdt": "0,5",
    "q": "EXAMPLE",
    "oq": "",
}
EXAMPEL_HEADERS = {
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
}

def google_scholar_get(kwd: str):
    headers = EXAMPEL_HEADERS
    query = QUERY
    query["q"] = kwd
    response = requests.get(INITIAL_URL, headers=headers, params=query)
    
    if response.status_code != 200:
        raise Exception(f"Status code: {response.status_code}")
    return response

def parse_google_scholar_results(response):
    soup = BeautifulSoup(response.text, 'html.parser')
    pattern = re.compile(r"\bgs_r gs_or gs_scl\b")
    elements = soup.find_all(class_=pattern)

    results = []
    for elem in elements:
        title = None
        doi = None
        h3_element = elem.find('h3', class_='gs_rt')
        
        if h3_element:
            a_element = h3_element.find('a', href=True)
            if a_element:
                href = a_element['href']
                decoded_url = urllib.parse.unquote(href)
                doi = decoded_url
                for b in a_element.find_all('b'):
                    b.unwrap()
                title = a_element.decode_contents()

            if title:
                results.append({
                    'title': title,
                    'doi': doi or "DOI not available"
                })
                
        if len(results) >= 20:  # Limit to top 20 results
            break
    return results

def crossref_get(title, doi=None):
    api_url = "https://api.crossref.org/works"
    params = {"query.title": title, "rows": 1}
    
    if doi:
        params['query'] = doi
    
    response = requests.get(api_url, params=params)
    if response.status_code != 200:
        raise Exception(f"Status code: {response.status_code}")
    return response

def parse_crossref_results(response):
    data = response.json()
    if data['message']['items']:
        item = data['message']['items'][0]
        article_title = item.get('title', [''])[0]
        abstract = item.get('abstract', 'No abstract available')
        authors = [author['given'] + ' ' + author['family'] for author in item.get('author', [])]
        published_year = str(item.get('published-print', {}).get('date-parts', [[None]])[0][0])
        journal = item.get('container-title', [''])[0]
        article_doi = item.get('DOI', 'No DOI available')
        keywords = item.get('subject', 'No keywords available')
        
        return {
            'title': article_title,
            'abstract': abstract,
            'authors': authors,
            'published_year': published_year,
            'journal': journal,
            'doi': article_doi,
            'keywords': keywords
        }
    return "No metadata found or error occurred."

def remove_formatting(text: str):
    sup = text.split("\n")
    sup = [s.strip() for s in sup if s.strip()]
    return " ".join(sup)


if __name__ == "__main__":
    pass
