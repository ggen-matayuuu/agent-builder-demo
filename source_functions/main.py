"""Retail recommendations and search"""

import json
import os
import random
import string

import firebase_admin
from firebase_functions import https_fn
import flask
import google.auth
import google.auth.transport.requests
from google.cloud import firestore
from google.cloud.firestore_v1.base_query import FieldFilter

firebase_admin.initialize_app()
app = flask.Flask(__name__)

creds, project = google.auth.default()
project_id = os.environ.get("project_id", "Specified environment variable is not set.")
db = firestore.Client(project=project_id, database="agent-database")


