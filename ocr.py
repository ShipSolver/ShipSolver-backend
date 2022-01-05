

from multilingual_pdf2text.pdf2text import PDF2Text
from multilingual_pdf2text.models.document_model.document import Document
import logging
import time

if __name__ == "__main__":
    stat = time.time()
    pdf_document = Document(
        document_path="data/NORTH_AMERICAN.pdf",
        language='eng'
    )
    pdf2text = PDF2Text(document=pdf_document)
    content = pdf2text.extract()
    print(time.time()-stat)

    for page in content:
        with open(f"text/NORTH_AMERICAN/{page['page_number']}.txt", "w") as f:
            f.write(page["text"])


