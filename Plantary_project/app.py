import email
from email.mime import base
from enum import unique
import string
from turtle import distance
from flask import Flask,jsonify,request, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String , Float
import os

app = Flask(__name__)
#app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLAlCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir,'planets.db')

db = SQLAlchemy(app)

@app.cli.add_command("db_create")
def db_create():
    db.create_all()
    print("Database Created !!")

@app.cli.add_command("db_drop")
def db_drop():
    db.drop_all()
    print("database Dropped !!")

@app.cli.command("db_seed")
def db_seed():
    Mercury = Planet(
        planet_name = "Mercury",
        Planet_type = "Class D",
        home_star = "Sun",
        mass = 3.258e23,
        redius = 1516,
        distance = 35.98e6
    )
    Venus = Planet(
        planet_name = "Venus",
        Planet_type = "Class K",
        home_star = "Sun",
        mass = 4.867e24,
        redius = 3760,
        distance = 67.24e6
    )
    Earth = Planet(
        planet_name = "Earth",
        Planet_type = "Class M",
        home_star = "Sun",
        mass = 5.972e24,
        redius = 3959,
        distance = 92.96e6
    )
    db.session.add(Mercury)
    db.session.add(Venus)
    db.session.add(Earth)
    test_user = User(
        first_name = "Kalpana",
        last_name = "Chawla",
        email = "kal.cha@nasa.com",
        password = "passworD" 
    )
    db.session.add(test_user)


@app.route("/")
def hello_world():
    return "<p>Hello World!</p>"


@app.route("/Super_simple")
def super_simple():
    return "Hello from the Planetary API."

"""
use below command to run
1. activate project
.\Script\activate

2. set flask parameter 
    set FLASK_APP=app(python file name without .py)
    set FLASK_ENV=development

3.run the application
    flask run 

CTRL+C to stop server.


ny default it is get mrthod. (test with postman)

It will auto restart on change so be aware.
"""

@app.route("/Super_simple2")
def super_simple2():
    return jsonify(message = "Hello from Planetary API",id = 2) ,200
"""
jsonify is helpfull to create json file as shown as above example.
"""


"""
All web apps are based on a request-response mechanism

Requests and responses have headers which is metadata.
headers is characteristics of the request or response.

like Status code which tell you that request was successful or not.

200 -> ok
404 -> not found

"""

@app.route("/not_found")
def not_found():
    return jsonify(message="That resource was not found."),404



"""
URL Parameters
"""
@app.route("/parameters")
def parameters():
    name = request.args.get('name')
    age = int(request.args.get('age'))
    return jsonify(message = f"Name is  {name} and age is {age}."),200
"""
URL Parameters with mordern pattern
and fixed datatype

<Flask_datatype:Name of varible>

on site 
<>/parameter_new/xyz/20
"""
@app.route("/parameter_new/<string:name>/<int:age>")
def parameters2(name : str , age : int):
    if age < 18 :
        return jsonify(message = f"Sorry {name},you are not allow. your age is {age} which is below 18."),401
    else :
        return jsonify(message = f"Name is  {name} and age is {age}."),200



"""
working with Relation Database
SQLLite and SQLAlchemy

install flask-SQLAlchemy
"""


"""
Database model (ORM)
"""

class User(db.Model):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key = True)
    first_name  = Column(String)
    last_name  = Column(String)
    email =  Column(String,unique = True)
    password = Column(string)

class Planet(db.model):
    __tablename__ = 'planets'
    planet_id = Column(Integer, primary_key = True)
    planet_name  = Column(String)
    planet_type = Column(String)
    home_star = Column(String)
    mass = Column(Float)
    redius = Column(Float)
    distance = Column(Float)