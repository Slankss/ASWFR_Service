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
    result = FaceRecognition.face_matching(data["image"])
    return str(result)
@app.route("/GetData",methods=["GET"])
def GetData():
    data = request.json
    return str(data["image"])

if __name__ == "__main__":
    app.run(debug=True)



