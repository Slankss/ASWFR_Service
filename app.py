from flask import Flask
from venv import *

app = Flask(__name__)
if __name__ == "__main__":

    app.run(debug=True)
