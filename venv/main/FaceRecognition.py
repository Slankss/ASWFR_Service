import cv2
import ImageProcess as imgP
import Constant as c
import face_recognition

face_cascade_path = "src/haarcascade_frontalface_default.xml"
face_cascade = cv2.CascadeClassifier(face_cascade_path)

imgP.base64_to_image(c.image_base64)
def find_face_encodings(imagePath):
    image = cv2.imread(imagePath)
    face_enc = face_recognition.face_encodings(image)
    if len(face_enc) > 0:
        return face_enc[0]
def is_same(image):
    face1 = find_face_encodings("src/decodedImage.jpeg")
    face2 = find_face_encodings(image)

    isSame = face_recognition.compare_faces([face1],face2)[0]
    return isSame










