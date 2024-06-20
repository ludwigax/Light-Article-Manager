import fitz
import pdfplumber
from typing import List, Tuple

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

