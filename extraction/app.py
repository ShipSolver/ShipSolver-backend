import os
from multilingual_pdf2text.pdf2text import PDF2Text
from multilingual_pdf2text.models.document_model.document import Document
import pdfplumber
import extraction.extract as e
import json
import traceback

def read_pdfplumber(file_name):
    with pdfplumber.open(file_name) as pdf:
        page = pdf.pages[0]
        page = page.extract_text()
    return page

def fan_out(folder):
    pdf_folders = os.listdir(folder)
    for pdf_folder in pdf_folders:
        pdf_file = f"{pdf_folder}.pdf"
        try:
            work(f"{folder}/{pdf_folder}")
        except Exception as e:
            print(f"file {pdf_folder}/{pdf_file} error. msg: {str(e)}")
            print(traceback.format_exc())

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