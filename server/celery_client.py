from celery import Celery
from celery.utils.log import get_logger

CELERY_BROKER_URL = 'redis://redis:6379/0'
client = Celery(__name__, broker=CELERY_BROKER_URL)
logger = get_logger(__name__)
