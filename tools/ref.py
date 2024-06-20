import datetime
from typing import List

from archi import ArticleData

class BIB_EXTRACTOR:
    keymap = {
        'Title': 'title',
        'Author': 'author',
        'Journal': 'journal',
        'Year': 'year',
        'DOI': 'doi',
    }

    def parse(raw_text: str):
        entry = {}
        lines = raw_text.split('\n')
        key = None
        for line in lines:
            if '=' in line:
                key, value = line.split('=', 1)
                key = key.strip()
                value = value.strip().strip('{},"')
                entry[key] = value
            elif key is not None:
                value = line.strip().strip('{},"')
                entry[key] += " " + value
        return entry
    
    def extract(bib_file: str):
        with open(bib_file, 'r', encoding="utf-8") as file:
            content = file.read()

        entries_text = content.split('@')[1:]
        data_list: List[ArticleData] = []
        for entry_text in entries_text:
            entry = BIB_EXTRACTOR.parse(entry_text)
            if entry.get('Title') is None:
                continue
            article_entry = {}
            for key in entry.keys():
                if key in BIB_EXTRACTOR.keymap:
                    article_entry[BIB_EXTRACTOR.keymap[key]] = entry[key]
            data = ArticleData(**article_entry)
            data.add_time = datetime.datetime.now().strftime("%Y-%m-%d")
            data_list.append(data)
        return data_list

class RIS_EXTRACTOR:
    keymap = {
        'TI': 'title',
        'AU': 'author',
        'T2': 'journal',
        'PY': 'year',
        'DO': 'doi',
    }

    def parse(raw_text: str):
        entry = {}
        lines = raw_text.strip().split('\n')
        for line in lines:
            if line.strip() == 'ER  -':
                break
            key, value = line[:2], line[6:].strip()
            if key == 'AU':
                if 'AU' in entry:
                    entry['AU'] += ' and ' + value
                else:
                    entry['AU'] = value
            else:
                entry[key] = value
        return entry

    def extract(ris_file: str):
        with open(ris_file, 'r', encoding="utf-8") as file:
            content = file.read()

        entries_text = content.strip().split('\n\n')
        data_list: List[ArticleData] = []
        for entry_text in entries_text:
            entry = RIS_EXTRACTOR.parse(entry_text)
            if entry.get('TI') is None:
                continue
            article_entry = {}
            for key in entry.keys():
                if key in RIS_EXTRACTOR.keymap:
                    article_entry[RIS_EXTRACTOR.keymap[key]] = entry[key]
            data = ArticleData(**article_entry)
            data.add_time = datetime.datetime.now().strftime("%Y-%m-%d")
            data_list.append(data)
        return data_list
    
class CIW_EXTRACTOR:
    keymap = {
        'TI': 'title',
        'AF': 'author',
        'SO': 'journal',
        'PY': 'year',
        'DI': 'doi',
    }

    def parse(raw_text: str):
        entry = {}
        lines = raw_text.strip().split('\n')
        key = None
        for line in lines:
            if line.startswith('ER'):
                break
            if line[:2] == "  " and key is not None:
                entry[key] += ' ' + line.strip()
                continue
            key, value = line[:2], line[3:].strip()
            if (key == 'AU' or key == 'AF') and key in entry:
                entry[key] += ' and ' + value
            else:
                entry[key] = value
        return entry
    
    def extract(ciw_file: str):
        with open(ciw_file, 'r', encoding="utf-8") as file:
            content = file.read()

        entries_text = content.strip().split('\n\n')
        data_list: List[ArticleData] = []
        for entry_text in entries_text:
            entry = CIW_EXTRACTOR.parse(entry_text)
            if entry.get('TI') is None:
                continue
            article_entry = {}
            for key in entry.keys():
                if key in CIW_EXTRACTOR.keymap:
                    article_entry[CIW_EXTRACTOR.keymap[key]] = entry[key]
            data = ArticleData(**article_entry)
            data.add_time = datetime.datetime.now().strftime("%Y-%m-%d")
            data_list.append(data)
        return data_list
    

class REF_PARSER:
    supported_formats = ['.bib', '.ris', '.ciw']

    def extract(file_path: str):
        if file_path.endswith('.bib'):
            return BIB_EXTRACTOR.extract(file_path)
        if file_path.endswith('.ris'):
            return RIS_EXTRACTOR.extract(file_path)
        if file_path.endswith('.ciw'):
            return CIW_EXTRACTOR.extract(file_path)
        return None