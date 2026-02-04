import sys
import os
# Prevent local file named `flask.py` from shadowing the installed Flask package
script_dir = os.path.dirname(__file__)
if script_dir in sys.path:
    sys.path.remove(script_dir)

from flask import Flask
app = Flask(__name__)  # type: ignore

@app.route("/")
def hello():
    return "Hello, World!"

if __name__ == '__main__':
    app.run(debug=True)
