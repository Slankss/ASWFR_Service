import cv2
import Constant
import face_recognition
import threading
import ImageProcess
def find_face(imagePath):
    image = cv2.imread(imagePath)
    face = face_recognition.face_encodings(image)
    if len(face) > 0:
        return face[0]
def face_matching(base64Image):
    try:
        base64Decode = threading.Thread(target=ImageProcess.base64_to_image(base64Image))
        base64Decode.start()
        base64Decode.join()

        face1 = find_face("src/image1.jpeg")
        face2 = find_face("src/decodedImage.jpeg")

        if face1 is None or face2 is None:
            return "there are not faces in images"

        isSame = face_recognition.compare_faces([face1],face2)[0]
        return isSame
    except:
        return "Error"
