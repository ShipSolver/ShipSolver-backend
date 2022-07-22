FROM python:3.9
RUN apt-get update && apt-get -y install qpdf poppler-utils && apt-get install -y build-essential libpoppler-cpp-dev pkg-config python-dev
RUN apt -y install tesseract-ocr && apt -y install libtesseract-dev
COPY requirements.txt .
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt
RUN mkdir /root/.ssh/
# ---------------- Manual Setup Required ------------------ #
#    Must get Deploy Key and drop it into the server dir    #
COPY flask-cognito-lib_deploy /root/.ssh/flask-cognito-lib_deploy
# --------------------------------------------------------- #
RUN touch /root/.ssh/known_hosts
RUN ssh-keyscan github.com >> /root/.ssh/known_hosts
RUN git - C /root clone git@github.com:ShipSolver/flask-cognito-lib.git
RUN pip3 install -e /root/flask-cognito-lib
WORKDIR /opt/metadata-extraction/tenant
ENV PYTHONPATH ..
