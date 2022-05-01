import os
from flask import request, jsonify, Blueprint
from celery import group
import PyPDF2
import io
from uuid import uuid4
import extraction.app as ex
import traceback
from server.celery_client import client, logger

pdf_bp = Blueprint("pdf_bp", __name__)
ticket_bp = Blueprint("ticket_bp", __name__)
