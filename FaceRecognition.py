import queue
import threading
import cv2
import face_recognition
import Database
import ImageJob

def find_face(imagePath):
    image = face_recognition.load_image_file(imagePath)
    face = face_recognition.face_encodings(image)
    if len(face) > 0:
        return face[0]

def base64_decode(base64Image, dest_image):
    ImageJob.base64_to_image(base64Image, dest_image)

def get_user_list_db(q):
    userList = Database.getUserList()
    q.put(userList)

def download_image(image_path):
    Database.downloadImage(image_path)
def access(base64Image):
    try:
        q = queue.Queue()

        base64Decode_thread = threading.Thread(target=base64_decode(base64Image, "decoded_image"))
        get_user_list_thread = threading.Thread(target=get_user_list_db, args=(q,))

        base64Decode_thread.start()
        get_user_list_thread.start()

        base64Decode_thread.join()
        get_user_list_thread.join()

        userList = q.get()
        is_there_in_db = False

        face_from_image = find_face("src/decoded_image.jpg")

        for user in userList:
            result = face_matching(face_from_image,user.image_path)
            if result:
                is_there_in_db = True
                break

        return is_there_in_db
    except:
        return "Error"


def face_matching(face_from_image,image_path):
    download_image_thread = threading.Thread(target=download_image(image_path))
    download_image_thread.start()
    download_image_thread.join()

    face_from_db = find_face("src/image_from_db.jpg")

    if face_from_image is None or face_from_db is None:
        return False
    return face_recognition.compare_faces([face_from_image], face_from_db)[0]
