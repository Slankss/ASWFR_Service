import queue
import threading

import cv2
import face_recognition
import firebase_admin
from firebase_admin import credentials, firestore, storage
from model.User import User
import uuid

credentialData = credentials.Certificate("key/serviceAccountKey.json")
app = firebase_admin.initialize_app(credentialData, {'storageBucket': 'acwfrdb.appspot.com'})
bucket = storage.bucket()
db = firebase_admin.firestore.client()
managerCollection = db.collection("Manager")
userCollection = db.collection("Users")


def downloadImage(imagePath):
    try:
        with open("src/image_from_db.jpg", "wb") as f:
            blob = bucket.blob(imagePath)
            imageBytes = blob.download_as_bytes()
            f.write(imageBytes)
    except Exception as e:
        print(e)


def uploadImage(image_name, uploadImageFinish):
    try:
        image = cv2.imread("src/added_image.jpg")
        face_locations = face_recognition.face_locations(image)

        for face_location in face_locations:
            top, right, bottom, left = face_location

            face_image = image[top:bottom, left:right]

            cv2.imwrite("src/added_image.jpg", face_image)

        blob = bucket.blob("images/" + image_name + ".jpg")
        blob.upload_from_filename("src/added_image.jpg")
        uploadImageFinish.put(True)
    except Exception as e:
        uploadImageFinish.put(False)


def deleteImage(imagePath, deleteImageFinish):
    try:
        blob = bucket.blob(imagePath)
        blob.delete()
        deleteImageFinish.put(True)
    except Exception as e:
        deleteImageFinish.put(False)


def deleteUser(id, deleteUserFinish):
    try:
        doc = userCollection.where("id", "==", id).get()[0]
        data = doc.to_dict()
        id = doc.id
        image_path = data["image_path"]

        deleteImageFinish = queue.Queue()
        deleteImageThread = threading.Thread(target=deleteImage(image_path, deleteImageFinish))

        deleteImageThread.start()
        deleteImageThread.join()

        if (deleteImageFinish.get() == False):
            deleteUserFinish.put(False)

        userCollection.document(id).delete()
        deleteUserFinish.put(True)
    except Exception as e:
        deleteUserFinish.put(False)


def getUserList(company_name):
    userList = list()
    userQuery = userCollection.where("company","==",company_name)
    for doc in userQuery.stream():
        data = doc.to_dict()

        name = data["name"]
        surname = data["surname"]
        id = data["id"]
        company = data["company"]
        image_path = data["image_path"]

        user = { "id": id,"name": name,"surname": surname, "company":company}
        userList.append(user)

    return userList


def login(username, password):
    result = False
    for doc in managerCollection.stream():
        data = doc.to_dict()
        if data["username"] == username and data["password"] == password:
            result = True
            break
    return result

def addUser(username, name, surname, addUserFinish):
    try:
        managerQuery = managerCollection.where("username", "==", username).limit(1).get()
        if len(managerQuery) == 0:
            addUserFinish.put(False)
            return

        company = managerQuery[0].to_dict()["company"]
        id = str(uuid.uuid4())
        image_path = "images/" + name + "_" + surname + ".jpg"
        user = {"name": name, "surname": surname, "id": id, "company": company, "image_path": image_path}
        userCollection.add(user)
        addUserFinish.put(True)
    except Exception as e:
        print("exception : " + str(e))
        addUserFinish.put(False)


def checkUser(name, surname, checkUserFinish):
    try:
        userQuery = userCollection.where("name", "==", name).where("surname", "==", surname).limit(1).get()
        checkUserFinish.put(len(userQuery) == 0)
    except Exception as e:
        checkUserFinish.put(False)
