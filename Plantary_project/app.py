from flask import Flask,jsonify,request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String , Float
import os
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager,jwt_manager,jwt_required,create_access_token,create_refresh_token
from flask_mail import Mail,Message

app = Flask(__name__)
#app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir,'planets.db')
app.config["JWT_SECRET_KEY"] = 'unique_key'

app.config['MAIL_SERVER']='smtp.mailtrap.io'
app.config['MAIL_PORT'] = 2525
app.config['MAIL_USERNAME'] = ""
app.config['MAIL_PASSWORD'] = ""
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False


SQLALCHEMY_TRACK_MODIFICATIONS = False
db = SQLAlchemy(app)
ma = Marshmallow(app)
jwt = JWTManager(app)
mail = Mail(app)




"""
use flask db_create command in terminal
"""
@app.cli.command("db_create")
def db_create():
    db.create_all()
    print("Database Created !!")

"""
use flask db_drop command in terminal
"""
@app.cli.command("db_drop")
def db_drop():
    db.drop_all()
    print("database Dropped !!")


"""
use flask db_seed command in terminal
"""
@app.cli.command("db_seed")
def db_seed():
    Mercury = Planet(
        planet_name = "Mercury",
        planet_type = "Class D",
        home_star = "Sun",
        mass = 3.258e23,
        redius = 1516,
        distance = 35.98e6
    )
    Venus = Planet(
        planet_name = "Venus",
        planet_type = "Class K",
        home_star = "Sun",
        mass = 4.867e24,
        redius = 3760,
        distance = 67.24e6
    )
    Earth = Planet(
        planet_name = "Earth",
        planet_type = "Class M",
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
    db.session.commit()
    print("Database seeded!!")


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


@app.route('/planets',methods = ["GET"])
def planets_list():
    planets_li = Planet.query.all()
    re = planets_schema.dump(planets_li)
    return jsonify(re)

@app.route('/users',methods = ["GET"])
def users_list():
    planets_li = User.query.all()
    re = users_schema.dump(planets_li)
    return jsonify(re)

@app.route("/register",methods = ["POST"])
def register():
    email = request.form['email']
    test = User.query.filter_by(email=email).first()
    if test:
        return jsonify(message = "The email is already exists."), 409
    else :
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        password = request.form['password']
        if first_name and last_name and password :
            user = User(first_name = first_name,last_name = last_name, password = password ,email = email)
            db.session.add(user)
            db.session.commit()
            return jsonify(message = "User created Successfully"), 201
        else :
            return jsonify(message = "Please provide all the data"),500

@app.route("/login",methods = ["POST"])
def login():
    if request.is_json:
        email = request.json["email"]
        password = request.json["password"]
    else:
        email = request.form["email"]
        password = request.form["password"]
    login_user = User.query.filter_by(email=email,password=password).first()
    if login_user:
        access_token = create_access_token(identity=email)
        return jsonify(message="Login succeeded !!",access_token = access_token),200
    else:
        return jsonify(message="Bad email id and password"),401

@app.route('/retrieve_password/<string:email>',methods=["GET"])
def retrieve_password(email : str):
    user = User.query.filter_by(email=email).first()
    if user:
        msg = Message("Your planetary API password is "+user.password,
        sender="admin@planetary-noreplay.com",
        recipients=[email])
        mail.send(msg)
        return jsonify(message = "Password is sent to you ragistered id."),201
    else:
        return jsonify(message = "Please enter registered email id."),409


@app.route("/planet_details/<int:planet_id>",methods=["GET","POST"])
def planet_details(planet_id):
    planet = Planet.query.filter_by(planet_id=planet_id).first()
    if planet:
        result = planet_schema.dump(planet)
        return jsonify(result)
    else:
        return jsonify(message = "The planet id does not exist."),404



@app.route("/add_planet",methods=["POST"])
@jwt_required()
def add_planet():
    planet_name = request.form['planet_name']
    test = Planet.query.filter_by(planet_name=planet_name).first()
    if test:
        return jsonify(message = " Planet already exist in database.")
    else :
        planet_type = request.form["planet_type"]
        home_star = request.form["home_star"]
        mass = float(request.form["mass"])
        redius = float(request.form["radius"])
        distance = float(request.form["distance"])

        new_planet = Planet(planet_name = planet_name,
        planet_type=planet_type,
        home_star=home_star,
        mass=mass,
        redius=redius,
        distance=distance) 

        db.session.add(new_planet)
        db.session.commit()
        return jsonify(message= "You added new planet!"),201


@app.route("/update_planet",methods=["PUT","POST"])
@jwt_required()
def update_planet():
    planet_id = int(request.form["planet_id"])
    planet = Planet.query.filter_by(planet_id=planet_id).first()
    if planet:
        planet.planet_name = request.form["planet_name"]
        planet.planet_type = request.form["planet_type"]
        planet.home_star = request.form["home_star"]
        planet.mass = float(request.form["mass"])
        planet.redius = float(request.form["radius"])
        planet.distance = float(request.form["distance"])
        db.session.commit()
        return jsonify(message = "Your planet data is updated !!")
    else:
        return jsonify(message = "There is no such a planet in database.")

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
    password = Column(String)

class Planet(db.Model):
    __tablename__ = 'planets'
    planet_id = Column(Integer, primary_key = True)
    planet_name  = Column(String)
    planet_type = Column(String)
    home_star = Column(String)
    mass = Column(Float)
    redius = Column(Float)
    distance = Column(Float)

class UserSchema(ma.Schema):
    class Meta:
        fields = ("user_id","first_name","last_name","email")
    
class PlanetSchema(ma.Schema):
    class Meta :
        fields  = ("planet_id","planet_name","planet_type","home_star","mass","redius","distance")
    
user_schema = UserSchema()
users_schema = UserSchema(many = True)
planet_schema = PlanetSchema()
planets_schema = PlanetSchema(many = True)