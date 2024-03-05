import cv2
import firebase_admin
from firebase_admin import credentials, firestore, storage
from model import User
import Constant
import numpy
import pyrebase

credentialData = credentials.Certificate("key/serviceAccountKey.json")
app = firebase_admin.initialize_app(credentialData,{'storageBucket' : 'gs://acwfrdb.appspot.com'})
bucket = storage.bucket()
storage = firebase_admin.storage
db = firebase_admin.firestore.client()

def downloadImage(imagePath):
    with open("src/image_from_db", "wb") as f:
        blob = bucket.blob("images/okan.jpeg")
        image = storage.
        #imageBytes = blob.download_as_bytes()
        #arr = numpy.frombuffer(blob.download_as_string(),numpy.uint8)
        #image = cv2.imdecode(arr,cv2.COLOR_BGR2BGR555)
        #print(image)
        #f.write(imageData)
    try:
        print("s")
    except:
        print("error")


collection = db.collection("Users")

userList = list()

for doc in collection.stream():
    data = doc.to_dict()
    image_path = data["image_path"]
    #downloadImage(image_path)
downloadImage("")
