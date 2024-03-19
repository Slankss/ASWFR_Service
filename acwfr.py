import threading

import time
from flask import Flask, render_template, request,jsonify

#from service import FaceRecognition, Database, ImageJob

app = Flask(__name__)
@app.route("/")
def SayHello():
    return "Hello World"

def SayFenerAglama():
    return "Fener Ağlama"

"""
@app.route("/AccessRequest")
def AccessRequest():
    data = request.json
    imageB64 = data["image"]

    if data is None or len(imageB64) == 0:
        return ""
    result = FaceRecognition.access(data["image"])
    return str(result)

@app.route("/Login")
def Login():
    args = request.args
    username = args.get("username")
    password = args.get("password")
    result = Database.login(username,password)
    response_data = { "responsee" : result}
    return jsonify(response_data)

@app.route("/AddUser")
def AddUser():
    data = request.json
    username = data["username"]
    name = data["name"]
    surname = data["surname"]
    image = data["image"]

    base64DecodeThread = threading.Thread(target=ImageProcess.base64_to_image(image,"added_image"))
    addUserThread = threading.Thread(target=Database.addUser(username, name, surname))
    uploadImageThread = threading.Thread(target=Database.uploadImage(name + "_" + surname))

    base64DecodeThread.start()
    base64DecodeThread.join()
    addUserThread.start()
    uploadImageThread.start()

    return ""
"""

if __name__ == "__main__":
    app.run(debug=True)

