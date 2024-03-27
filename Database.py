import queue
import threading

import firebase_admin
from firebase_admin import credentials, firestore, storage
from model import User
import uuid

credentialData = credentials.Certificate("key/serviceAccountKey.json")
app = firebase_admin.initialize_app(credentialData, {'storageBucket': 'acwfrdb.appspot.com'})
bucket = storage.bucket()
db = firebase_admin.firestore.client()


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
        doc = db.collection("Users").where("id", "==", id).get()[0]
        data = doc.to_dict()
        id = doc.id
        image_path = data["image_path"]

        deleteImageFinish = queue.Queue()
        deleteImageThread = threading.Thread(target=deleteImage(image_path, deleteImageFinish))

        deleteImageThread.start()
        deleteImageThread.join()

        if (deleteImageFinish.get() == False):
            deleteUserFinish.put(False)

        db.collection("Users").document(id).delete()
        deleteUserFinish.put(True)
    except Exception as e:
        deleteUserFinish.put(False)

def getUserList():
    collection = db.collection("Users")
    userList = list()
    for doc in collection.stream():
        data = doc.to_dict()

        name = data["name"]
        surname = data["surname"]
        id = data["id"]
        company = data["company"]
        image_path = data["image_path"]
        user = User.User(name, surname, id, company, image_path)

        userList.append(user)

    return userList


def login(username, password):
    collection = db.collection("Manager")
    result = False
    for doc in collection.stream():
        data = doc.to_dict()
        if data["username"] == username and data["password"] == password:
            result = True
            break
    return result


def addUser(username, name, surname, addUserFinish):
    try:
        managerCollection = db.collection("Manager")
        userCollection = db.collection("Users")

        managerQuery = managerCollection.where("username", "==", username).limit(1).get()

        if len(managerQuery) == 0:
            return False

        company = managerQuery[0].to_dict()["company"]
        id = uuid.uuid4()
        image_path = "images/" + name + "_" + surname + ".jpg"
        user = {"name": name, "surname": surname, "id": id, "company": company, "image_path": image_path}
        userCollection.add(user)
        addUserFinish.put(True)
    except Exception as e:
        addUserFinish.put(False)
