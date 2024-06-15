import fitz
import pdfplumber
from typing import List, Tuple
import bibtexparser

from archi import ArticleData

import datetime

def extract_bib_info(bib_file):
    with open(bib_file, 'r', encoding="utf-8") as bibtex_file:
        bib_database = bibtexparser.load(bibtex_file)

    data_list: List[ArticleData] = []
    for entry in bib_database.entries:
        data = ArticleData(**bib_database.entries[0])
        if data.title is None:
            continue
        data_list.append(data)
    for data in data_list:
        for key in data._fields():
            if isinstance(data[key], str):
                data[key] = data[key].strip() if data[key] else ""
                data[key] = data[key].replace("\n", " ")
        data.add_time = datetime.datetime.now().strftime("%Y-%m-%d")
    return data_list

def extract_annotations(pdf_path: str) -> List[Tuple[str, str, int]]:    
    def extract_highlight(page, annot):
        quadpoints = annot.vertices
        if not quadpoints:
            return ""
        
        text = ""
        for i in range(0, len(quadpoints), 4):
            quad = quadpoints[i:i + 4]
            xs = [q[0] for q in quad]
            ys = [q[1] for q in quad]
            xmin, xmax = min(xs), max(xs)
            ymin, ymax = min(ys), max(ys)
            
            line_text = page.within_bbox((xmin - 2, ymin - 2, xmax + 2, ymax + 2)).extract_text(x_tolerance_ratio=0.1)
            if not line_text:
                continue
            if line_text[-1] == "-":
                line_text = line_text[:-1]
                sep = ""
            else:
                sep = " "
            text += line_text + sep
        
        return text.strip()

    annot_pages = fitz.open(pdf_path)
    f_text = pdfplumber.open(pdf_path)
    annotations = []
    
    for i, (pa, pt) in enumerate(zip(annot_pages, f_text.pages)):

        for annot in pa.annots():
            if annot.type[0] != fitz.PDF_ANNOT_HIGHLIGHT:
                continue
            
            refer_text = extract_highlight(pt, annot)
            annot_text = annot.info.get("content", "")
            annotations.append((refer_text, annot_text, i + 1))
    
    return annotations


if __name__ == "__main__":
    pdf_path = "./papers/dou-et-al-2023-machine-learning-methods-for-sm.pdf"
    annotations = extract_annotations(pdf_path)
    for annotation in annotations:
        if annotation[1] != "":
            print(annotation)

