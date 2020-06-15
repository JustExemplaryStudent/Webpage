from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.secret_key = "djksfye8794fw,ejvhb314"

db = SQLAlchemy(app)

ROOT_DIR = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///' + os.path.join(ROOT_DIR, 'app.db')

from routes import *
from models import *

if __name__ == "__main__":
    app.run()
