import os
from multilingual_pdf2text.pdf2text import PDF2Text
from multilingual_pdf2text.models.document_model.document import Document
import pdfplumber
import extraction.extract as e
import json


def read_pdfplumber(file_name):
    with pdfplumber.open(file_name) as pdf:
        page = pdf.pages[0]
        page = page.extract_text()
    return page


def work(folder_path):
    pdf_uuid = folder_path.split("/")[-1]
    pdf_file = f"{folder_path}/{pdf_uuid}.pdf"
    print(f"Working on {pdf_file}...")
    pdf_document = Document(
        document_path=pdf_file,
        language='eng'
    )
    pdf2text = PDF2Text(document=pdf_document)
    content = pdf2text.extract()

    ml_page_text = list(content)[0]["text"]
    pp_text = read_pdfplumber(pdf_file)

    extract_json = e.extract(ml_page_text, plumber_page=pp_text)

    with open(f"{folder_path}/{pdf_uuid}.json", "w") as f:
        json.dump(extract_json, f, indent=2)

if __name__ == '__main__':
    work("uploads/bf0c396f-dcc6-4d3f-8d7c-9180d2f0a322/cedc5b27-2a94-4e17-ac48-65c13e065102")