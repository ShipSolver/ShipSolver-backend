FROM python:3.9
RUN apt-get update && apt-get -y install qpdf poppler-utils && apt-get install -y build-essential libpoppler-cpp-dev pkg-config python-dev
RUN apt -y install tesseract-ocr && apt -y install libtesseract-dev
COPY tenant/requirements.txt .
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt
RUN pip3 install psycopg2-binary
RUN pip3 install redis --upgrade
RUN git -C /root clone https://github.com/ShipSolver/flask-cognito-lib.git
RUN pip3 install -e /root/flask-cognito-lib
WORKDIR /opt/metadata-extraction/tenant
ENV PYTHONPATH ..
