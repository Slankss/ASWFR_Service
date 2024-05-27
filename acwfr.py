import time
import threading
import FaceRecognition
import Database
import ImageJob
from flask import Flask, jsonify, request
import queue

app = Flask(__name__)


def response(status, message):
    return jsonify({"status": status,"message":message})

@app.route("/")
def SayHello():
    return "test route"


@app.route("/AccessRequest",methods = ["POST"])
def AccessRequest():
    data = request.json
    args = request.args
    company = args.get("company")
    imageB64 = data["image"]

    if data is None or len(imageB64) == 0:
        return jsonify({"status": 0})
    result = FaceRecognition.access(imageB64,company)
    message = ""
    if result == 1:
        message = "Access provided"
    elif result == 0:
        message = "There is no face in the image"
    else:
        message = "Access denied"
    return response(result, message)


@app.route("/Login")
def Login():
    args = request.args
    username = args.get("username")
    password = args.get("password")
    result = Database.login(str(username), str(password))
    message = ""
    if result:
        message = "Login successfully"
    else:
        message = "Login Failed!"
    return response(result, message)


@app.route("/AddUser",methods = ["POST"])
def AddUser():
    data = request.json
    username = data["username"]
    name = data["name"]
    surname = data["surname"]
    image = data["image"]

    checkUserFinish = queue.Queue()
    addUserFinish = queue.Queue()
    uploadImageFinish = queue.Queue()

    checkUserFinishThread = threading.Thread(target=Database.checkUser, args=(name, surname, checkUserFinish))
    base64DecodeThread = threading.Thread(target=ImageJob.base64_to_image, args=(image, "added_image"))

    checkUserFinishThread.start()
    checkUserFinishThread.join()

    if not checkUserFinish.get():
        return response(False, "There is same user with that name and surname!")

    base64DecodeThread.start()
    base64DecodeThread.join()

    addUserThread = threading.Thread(target=Database.addUser, args=(username, name, surname, addUserFinish))
    uploadImageThread = threading.Thread(target=Database.uploadImage, args=(name + "_" + surname, uploadImageFinish))
    face_from_image = FaceRecognition.find_face("src/decoded_image.jpg")

    #if face_from_image is None:
    #    return response(False,"There is no face in the image")
    #else:
    addUserThread.start()
    uploadImageThread.start()


    result = addUserFinish.get() and uploadImageFinish.get()
    message = ""
    if result: message = "User added succesfully"
    return response(result, message)


@app.route("/RemoveUser")
def RemoveUser():
    args = request.args
    id = args.get("id")

    userDeleteFinish = queue.Queue()
    userDeleteThread = threading.Thread(target=Database.deleteUser(id, userDeleteFinish))

    userDeleteThread.start()
    userDeleteThread.join()

    if userDeleteFinish.get() == False:
        return response(False, "User could not deleted")
    return response(True, "User deleted")

@app.route("/GetUserList")
def GetUserList():
    userListQueue = queue.Queue()

    args = request.args
    companyName = args.get("company")
    userList = Database.getUserList(companyName,userListQueue)

    data = jsonify({"userlist": userList})
    return data


if __name__ == "__main__":
    app.run(debug=True)
