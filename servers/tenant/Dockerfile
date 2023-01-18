FROM python:3.8-slim-buster
WORKDIR /core-app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

EXPOSE 6767
COPY . .

CMD [ "python3", "server.py"]