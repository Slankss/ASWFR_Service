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
def getUserList():
    collection = db.collection("Users")
    userList = list()
    for doc in collection.stream():
        data = doc.to_dict()

        name = data["name"]
        surname = data["surname"]
        company = data["company"]
        image_path = data["image_path"]
        user = model.User(name,surname,company,image_path)

        userList.append(user)

    return userList

