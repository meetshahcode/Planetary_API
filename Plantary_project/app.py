from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


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
"""