import FaceRecognition
import time
from flask import Flask, render_template, request
import ImageProcess

app = Flask(__name__)
@app.route("/AccessRequest")
def AccessRequest():
    data = request.json
    imageB64 = data["image"]

    if data is None or len(imageB64) == 0:
        return ""
    result = FaceRecognition.access(data["image"])
    return str(result)

if __name__ == "__main__":
    app.run(debug=True)

