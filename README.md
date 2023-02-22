# HOW TO START SERVER

```

cd root_directory;
python3 -m venv venv; // if not already exists
source venv/bin/activate;
cd servers/tenant;
pip3 install -r requirements.txt
cd postgres;
docker-compose up -d;
cd ../;
python3 server.py

# start frontend
# login with user

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


