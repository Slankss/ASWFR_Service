import FaceRecognition as fa
import time
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/AccessRequest")
def AccessRequest():

    result = fa.is_same("src/icardi2.jpg")
    return str(result)

if __name__ == "__main__":
    app.run(debug=True)



