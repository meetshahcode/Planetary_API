from email import message
from flask import Flask , jsonify

app = Flask(__name__)

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
    return jsonify(message = "Hello from Planetary API",id = 2)
"""
jsonify is helpfull to create json file as shown as above example.
"""


"""
All web apps are based on a request-response mechanism

Requests and responses have headers which is metadata.
headers is characteristics of the request or response.

like Status code which tell you that request was successful or not.


"""