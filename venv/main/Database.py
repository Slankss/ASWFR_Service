import cv2
import firebase_admin
from firebase_admin import credentials, firestore, storage
from model import User as model
import Constant
import numpy

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
def uploadImage(image_name):
    try:
        blob = bucket.blob("images/" + image_name + ".jpg")
        blob.upload_from_filename("src/added_image.jpg")
    except Exception as e:
        print(e)
def getUserList():
    collection = db.collection("Users")
    userList = list()
    for doc in collection.stream():
        data = doc.to_dict()

        name = data["name"]
        surname = data["surname"]
        company = data["company"]
        image_path = data["image_path"]
        user = model.User(name, surname, company, image_path)

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

def addUser(username,name,surname):
    managerCollection = db.collection("Manager")
    userCollection = db.collection("Users")

    managerQuery = managerCollection.where("username","==",username).limit(1).get()

    if len(managerQuery) == 0:
        return false

    company = managerQuery[0].to_dict()["company"]
    image_path = "images/"+name +"_"+surname+".jpg"
    user = { "name" : name,"surname":surname,"company":company,"image_path":image_path}
    userCollection.add(user)