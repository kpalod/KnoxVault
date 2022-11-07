import os
from unicodedata import name
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_session import Session
from tempfile import mkdtemp
from flask_bcrypt import Bcrypt
import re
import pymysql
from dotenv import load_dotenv
import boto3
# Configure application
load_dotenv()
app = Flask(__name__)
bcrypt = Bcrypt(app)
s3 = boto3.client('s3',
                    aws_access_key_id=os.getenv("ACCESS_KEY_ID"),
                    aws_secret_access_key= os.getenv("ACCESS_SECRET_KEY")
                     )

app.config["TEMPLATES_AUTO_RELOAD"] = True
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
db = SQLAlchemy(app)
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Custom filter


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
from vault import routes