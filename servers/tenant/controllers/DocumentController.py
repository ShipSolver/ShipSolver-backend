import os
from flask import request, jsonify, Blueprint

from celery import group
import PyPDF2
import io
from uuid import uuid4
import sys

from tenant.controllers.baseController import BaseController

sys.path.insert(0, "..")  # import parent folder

from models.models import DocumentStatus, Documents
from models.__init__ import session
from utils import convert_dict_to_alchemy_filters


class DocumentController(BaseController):
    def __init__(self):
        super().__init__(Documents)


class DocumentStatusController(BaseController):
    def __init__(self):
        super().__init__(DocumentStatus)