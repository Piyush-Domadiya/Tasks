from flask import Flask 
app = Flask(__name__) # type: ignore

@app.route("/")
def hello():
    return "Hello, World!"