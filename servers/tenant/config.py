from flask import Flask, make_response
from celery_client import client
from flask_caching import Cache

CELERY_BROKER_URL = "redis://redis:6379/0"
CELERY_RESULT_BACKEND = "redis://localhost:6379/0"

app = Flask(__name__)
app.config["DEBUG"] = True
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024
app.config["CELERY_BROKER_URL"] = CELERY_BROKER_URL
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['CACHE_TYPE'] = 'SimpleCache'
app.config['CACHE_DEFAULT_TIMEOUT'] = 300
client.conf.update(app.config)

cache = Cache(app)