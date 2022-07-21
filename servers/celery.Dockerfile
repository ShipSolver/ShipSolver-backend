FROM python:3.9
RUN apt-get update && apt-get -y install qpdf poppler-utils && apt-get install -y build-essential libpoppler-cpp-dev pkg-config python-dev
RUN apt -y install tesseract-ocr && apt -y install libtesseract-dev
COPY requirements.txt .
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt
WORKDIR /opt/metadata-extraction/tenant
ENV PYTHONPATH ..
