FROM python:3.9
RUN apt-get update && apt-get -y install qpdf poppler-utils && apt-get install -y build-essential libpoppler-cpp-dev pkg-config python-dev
RUN apt -y install libpq-dev
COPY tenant/requirements.txt .
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt
RUN pip3 install psycopg2
RUN rm -rf flask-cognito-lib || true
RUN git -C /root clone https://github.com/ShipSolver/flask-cognito-lib.git
COPY token_svc.py /root/flask-cognito-lib/src/flask_cognito_lib/services/token_svc.py
RUN pip3 install -e /root/flask-cognito-lib
WORKDIR /opt/metadata-extraction
ENV PYTHONPATH .
EXPOSE 6767
