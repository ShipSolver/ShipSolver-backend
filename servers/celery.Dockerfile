FROM python:3.9
RUN apt-get update && apt-get -y install qpdf poppler-utils && apt-get install -y build-essential libpoppler-cpp-dev pkg-config python-dev
RUN apt -y install tesseract-ocr && apt -y install libtesseract-dev
COPY tenant/requirements.txt .
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt
RUN pip3 install psycopg2-binary
RUN git -C /root clone https://github.com/ShipSolver/flask-cognito-lib.git
RUN pip3 install -e /root/flask-cognito-lib
WORKDIR /opt/metadata-extraction/tenant
ENV PYTHONPATH ..
ENV aws_secret_access_key 0zGUnCc0XNGX5lAfoN88EPnycnuZ0bMOWWKEqine
ENV aws_access_key_id AKIASPMMHOETWM2ETVWJ
ENV AWS_REGION="us-east-1"
ENV AWS_COGNITO_USER_POOL_ID="us-east-1_6AUY6LKPZ"
ENV AWS_COGNITO_USER_POOL_CLIENT_ID="2vukbtukva3u0oh29lf32ghmkp"
ENV AWS_COGNITO_DOMAIN="https://shipsolver-dev.auth.us-east-1.amazoncognito.com/"