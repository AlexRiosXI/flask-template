from flask import Flask
from dotenv import load_dotenv

from sierra_madre_core.models.abstract_models import db
from flask_cors import CORS
from models.auth import auth_blueprint

import os
import sys

load_dotenv()


app = Flask(__name__)

CORS(
    app,
    supports_credentials=True,  # NECESARIO para cookies
    origins=["https://localhost:5173"],  # el origen de tu React app
    methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"],
)

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_CONNECTION_STRING")
app.register_blueprint(auth_blueprint, url_prefix="/auth")

@app.route("/ping")
def ping():
    return "pong"