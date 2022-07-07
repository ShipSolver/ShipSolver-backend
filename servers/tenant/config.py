from flask import Flask
from celery_client import client

CELERY_BROKER_URL = "redis://redis:6379/0"
CELERY_RESULT_BACKEND = "redis://localhost:6379/0"

app = Flask(__name__)
app.config["DEBUG"] = True
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024
app.config["CELERY_BROKER_URL"] = CELERY_BROKER_URL
app.config['CORS_HEADERS'] = 'Content-Type'
client.conf.update(app.config)
