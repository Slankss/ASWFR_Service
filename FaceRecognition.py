import queue
import threading
import cv2
import face_recognition
import Database
import ImageJob
def find_face(imagePath):
    with open(imagePath,"rb") as f:
        image = cv2.imread(imagePath)
        #image = face_recognition.load_image_file(f)
        face = face_recognition.face_encodings(image)
        if len(face) > 0:
            return face[0]

def base64_decode(base64Image,dest_image):
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

        for user in userList:
            result = face_matching(user.image_path)
            if result:
                is_there_in_db = True
                break

        return is_there_in_db
    except:
        return "Error"


def face_matching(image_path):
    download_image_thread = threading.Thread(target=download_image(image_path))
    download_image_thread.start()
    download_image_thread.join()

    face1 = find_face("src/decoded_image.jpg")
    face2 = find_face("src/image_from_db.jpg")

    if face1 is None or face2 is None:
        return False

    return face_recognition.compare_faces([face1], face2)[0]
