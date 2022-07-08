# PREREQUISITE THAT SERVER IS RUNNING
import requests

base_url = "localhost:6767"


res = requests.get("http://127.0.0.1:6767/api/ticket/")

print(res.text)


# http://127.0.0.1:6767/api/ticket/?start=2022-01-01T00:00:00&end=2022-04-04T00:00:00&shipperName=Eric%20Shea
# curl http://127.0.0.1:6767/api/ticket/?shipperName
# # curl http://127.0.0.1:6767/api/ticket?key=a
# # curl http://127.0.0.1:6767/api/ticket/?start=2022-01-01T00:00:00Z&end=2022-04-04T00:00:00Z
