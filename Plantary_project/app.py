from flask import Flask,jsonify,request, url_for

app = Flask(__name__)
#app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False

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
