from distutils import filelist
import os
import re
import io
from auxiliary import *
from unicodedata import name
import zlib
from werkzeug.utils import secure_filename
from flask import Response
from cs50 import SQL
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, flash, jsonify, redirect, render_template, request, session ,url_for,send_file
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from flask_bcrypt import Bcrypt
from datetime import datetime
import face_recognition
from io import BytesIO
from PIL import Image
from base64 import b64encode, b64decode
import re
import pymysql
from dotenv import load_dotenv
import boto3
import tempfile
import matplotlib.image as mpimg
from helpers import apology, login_required
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

@app.route("/")
@login_required
def home():

    return redirect("/home")

@app.route("/home")
@login_required
def index():
    files = FileTable.query.filter_by(user_id=session["user_id"]).all()
    return render_template("index.html",files=files)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""


 
    if request.method == "POST":

        # Assign inputs to variables
        input_username = request.form.get("username")
        input_password = request.form.get("password")

 
        if not input_username:
            return render_template("login.html",messager = 1)


        elif not input_password:
             return render_template("login.html",messager = 2)


        user = User.query.filter_by(username=input_username).first() 

        # if user is None or not check_password_hash(user.password, input_password):
       # if user is None:
        if user is None or not bcrypt.check_password_hash(user.password, input_password):
            return render_template("login.html",messager = 3)

        # Remember which user has logged in
        session["user_id"] = user.id
        session['user_name'] = user.username

        return redirect("/")

    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")



@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    if request.method == "POST":

        input_username = request.form.get("username")
        input_email = request.form.get("email")
        input_password = request.form.get("password")
        input_confirmation = request.form.get("confirmation")

        if not input_username:
            return render_template("register.html",messager = 1)

        elif not input_password:
            return render_template("register.html",messager = 2)

        elif not input_confirmation:
            return render_template("register.html",messager = 4)

        elif not input_password == input_confirmation:
            return render_template("register.html",messager = 3)

        user = User.query.filter_by(username=input_username).first()   


        if (user):
            return render_template("register.html",messager = 5)

        else:
            # new_user = db.execute("INSERT INTO users (username, hash) VALUES (:username, :password)",
            #                       username=input_username,
            #                       password=generate_password_hash(input_password, method="pbkdf2:sha256", salt_length=8),)
            
            #hashed_password=(input_password, method="pbkdf2:sha256", salt_length=8)
            hashed_password=bcrypt.generate_password_hash(input_password)
            new_user = User(username=input_username,email=input_email,password=hashed_password)
            db.session.add(new_user)
            db.session.commit()

            if new_user:
                session["user_id"] = new_user.id

            flash(f"Registered as {input_username}")

            # Redirect user to homepage
            return redirect("/")


    else:
        return render_template("register.html")




@app.route("/facereg", methods=["GET", "POST"])
def facereg():
    session.clear()
    if request.method == "POST":


        encoded_image = (request.form.get("pic")+"==").encode('utf-8')
        input_username = request.form.get("name")
        user = User.query.filter_by(username=input_username).first()
              
        if user is None:
            return render_template("camera.html",message = 1)

        id_ = user.id    
        compressed_data = zlib.compress(encoded_image, 9) 
        
        uncompressed_data = zlib.decompress(compressed_data)
        
        decoded_data = b64decode(uncompressed_data)
        
        new_image_handle = open('./static/face/unknown/'+str(id_)+'.jpg', 'wb')
        
        new_image_handle.write(decoded_data)
        new_image_handle.close()
        # s3_read=boto3.resource('s3', region_name="us-east-1")
        # bucket = s3_read.Bucket(os.getenv("BUCKET_NAME"))
        # object = bucket.Object(str(id_)+'.jpg')
        # #image_load = s3.get_object(Bucket=os.getenv("BUCKET_NAME"),Key=str(id_)+'.jpg')
        # temp = tempfile.NamedTemporaryFile(mode='w')
        # object.download_fileobj(temp.name)
        # img = mpimg.imread(temp.name)
        with tempfile.TemporaryFile(mode='w+b') as f:
            s3.download_fileobj(os.getenv("BUCKET_NAME"), str(id_)+'.jpg', f)
                    
            try:
                # image_of_bill = face_recognition.load_image_file(
                # './static/face/'+str(id_)+'.jpg')
                image_of_bill = face_recognition.load_image_file(f)
            except:
                return render_template("camera.html",message = 5)

            bill_face_encoding = face_recognition.face_encodings(image_of_bill)[0]

            unknown_image = face_recognition.load_image_file(
            './static/face/unknown/'+str(id_)+'.jpg')
            try:
                unknown_face_encoding = face_recognition.face_encodings(unknown_image)[0]
            except:
                return render_template("camera.html",message = 2)
            f.close()


#       compare faces
        results = face_recognition.compare_faces([bill_face_encoding], unknown_face_encoding,tolerance=0.5)

        if results[0]==True:
            user = User.query.filter_by(username=input_username).first()
            session["user_id"] = user.id
            session['user_name'] = user.username
            os.remove('./static/face/unknown/'+str(id_)+'.jpg')
            return redirect("/")
        else:
            os.remove('./static/face/unknown/'+str(id_)+'.jpg')
            return render_template("camera.html",message=3)


    else:
        return render_template("camera.html")



@app.route("/facesetup", methods=["GET", "POST"])
def facesetup():
    if request.method == "POST":


        encoded_image = (request.form.get("pic")+"==").encode('utf-8')
    

        id_=User.query.filter_by(id=session["user_id"]).first().id
        # id_ = db.execute("SELECT id FROM users WHERE id = :user_id", user_id=session["user_id"])[0]["id"]    
        compressed_data = zlib.compress(encoded_image, 9) 
        
        uncompressed_data = zlib.decompress(compressed_data)
        decoded_data = b64decode(uncompressed_data)
        
        new_image_handle = open('./static/face/'+str(id_)+'.jpg', 'wb')
        
        new_image_handle.write(decoded_data)
        new_image_handle.close()
        image_of_bill = face_recognition.load_image_file(
        './static/face/'+str(id_)+'.jpg')    
        try:
            bill_face_encoding = face_recognition.face_encodings(image_of_bill)[0]
        except:    
            return render_template("face.html",message = 1)
        s3.upload_file('./static/face/'+str(id_)+'.jpg',os.getenv("BUCKET_NAME"),str(id_)+'.jpg')
        os.remove('./static/face/'+str(id_)+'.jpg')
        return redirect("/home")

    else:
        return render_template("face.html")
    
@app.route("/upload",methods=["GET","POST"])
@login_required
def upload():
    if request.method == "POST":
        file = request.files['inputFile']
        data = file.read()   
        newFile = FileTable(name=file.filename, file=data,user_id=session["user_id"])
        db.session.add(newFile)
        db.session.commit()
        return render_template("upload.html",message=1)
    else:
        return render_template("upload.html")
    
@app.route('/retrieve/<id>')
def retrieve(id):
    file = FileTable.query.filter_by(id=id).first()

    if not file:
        return render_template('error.html')

    return send_file(BytesIO(file.file), download_name=f'{file.name}')

@app.route('/delete/<id>')
def delete(id):
    file = FileTable.query.filter_by(id=id).first()

    if not file:
        return render_template('error.html')

    db.session.delete(file)
    db.session.commit()

    return redirect(url_for('index'))    
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    file = db.relationship('FileTable', backref='author', lazy=True)
    
    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"
        

class FileTable(db.Model):
    __tablename__ = 'USER_FILES'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    file = db.Column(db.LargeBinary)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


    def __init__(self, name, file,user_id):
        self.name = name
        # self.tag = tag
        self.file = file
        self.user_id=user_id


    def __repr__(self):
        return f'FILE ID: {self.id} \n FILE NAME: {self.name} \n FILE TAG: {self.tag} \n'
db.drop_all()
db.create_all()

def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return render_template("error.html",e = e)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)

if __name__ == '__main__':
      app.debug = True
      app.run()
