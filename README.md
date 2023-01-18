HOW TO RUN: 

cd /servers/tenant/postgres

docker compose-up -d # start postgres database 


pipenv shell #install this or load env file Vars and use pip3 
pipenv install -r requiremnets.txt # or pip3 install


python3 server.py
