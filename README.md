# HOW TO START SERVER

```
# in root

export PYTHONPATH=.
# have a venv in /servers
# pip install requirements in tenant

docker-compose up -d # in /servers

# change line in models/__init__.py  postgres_c -> localhost (dont commit this change)

./load_data.sh # load fixtures

python3 tenant/server.py # start server

```



## Docker Environment Setup

Install <a href="https://docs.docker.com/get-docker/">docker</a> and <a href="https://docs.docker.com/compose/install/">docker-compose</a> so you can run the services locally.





# Deprecated
## Starting a Local Celery Cluster
Always pull new changes with 
```
git pull
```
Give the script execution permission initially
```
chmod +x start-cluster.sh
```

Start the cluster as follows:
```
./start-cluster.sh
```

To kill the cluster:
```
./kill-cluster.sh
```
Ensure you run these scripts in the root project directory. 

## Using the API

API calls can be made to localhost:5000


