from flask import Flask
from server.dreceipt import dreceipt_bp
from celery_client import client

CELERY_BROKER_URL = 'redis://redis:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'

app = Flask(__name__)
app.config["DEBUG"] = True
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['CELERY_BROKER_URL'] = CELERY_BROKER_URL
client.conf.update(app.config)

app.register_blueprint(dreceipt_bp, url_prefix='/dreceipt')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')