import time
import threading
import FaceRecognition
import Database
import ImageJob
from flask import Flask, jsonify, request
import queue

app = Flask(__name__)


def response(status, message):
    if len(message) == 0:
        return jsonify({"status": status})
    else:
        return jsonify({"status": status, "message": message})


@app.route("/")
def SayHello():
    return "test route"


@app.route("/AccessRequest")
def AccessRequest():
    data = request.json
    imageB64 = data["image"]

    if data is None or len(imageB64) == 0:
        return jsonify({"status": False})
    result = FaceRecognition.access(imageB64)
    message = ""
    if (result):
        message = "Access provided"
    else:
        message = "Access denied"
    return response(result, message)


@app.route("/Login")
def Login():
    args = request.args
    username = args.get("username")
    password = args.get("password")
    result = Database.login(username, password)
    message = ""
    if (result): message = "Login succesfully"
    return response(result, message)


@app.route("/AddUser")
def AddUser():
    data = request.json
    username = data["username"]
    name = data["name"]
    surname = data["surname"]
    image = data["image"]

    addUserFinish = queue.Queue()
    uploadImageFinish = queue.Queue()

    base64DecodeThread = threading.Thread(target=ImageJob.base64_to_image(image, "added_image"))
    addUserThread = threading.Thread(target=Database.addUser(username, name, surname, addUserFinish))
    uploadImageThread = threading.Thread(target=Database.uploadImage(name + "_" + surname, uploadImageFinish))

    base64DecodeThread.start()
    base64DecodeThread.join()
    addUserThread.start()
    uploadImageThread.start()

    result = addUserFinish.get() and uploadImageFinish.get()
    message = ""
    if result: message = "User added succesfully"
    return response(result, message)


@app.route("/RemoveUser")
def RemoveUser():
    data = request.json
    id = data["id"]

    userDeleteFinish = queue.Queue()
    userDeleteThread = threading.Thread(target=Database.deleteUser(id, userDeleteFinish))

    userDeleteThread.start()
    userDeleteThread.join()

    if userDeleteFinish.get() == False:
        return response(False, "User could not deleted")
    return response(True, "User deleted")


if __name__ == "__main__":
    app.run(debug=True)
