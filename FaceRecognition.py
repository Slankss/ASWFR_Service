import queue
import threading
import face_recognition
import Database
import ImageJob

def find_face(imagePath):
    image = face_recognition.load_image_file(imagePath)
    face = face_recognition.face_encodings(image)
    if len(face) > 0:
        return face[0]
    return None

def base64_decode(base64Image, dest_image):
    ImageJob.base64_to_image(base64Image, dest_image)

def get_user_list_db(q):
    userList = Database.getUserList()
    q.put(userList)

def download_image(image_path):
    Database.downloadImage(image_path)
def access(base64Image,company):
    try:
        userListQueue = queue.Queue()

        base64Decode_thread = threading.Thread(target=base64_decode(base64Image, "decoded_image"))
        base64Decode_thread.start()
        base64Decode_thread.join()

        face_from_image = find_face("src/decoded_image.jpg")
        if face_from_image is None:
            return 0

        get_user_list_thread = threading.Thread(target=Database.getUserList, args=(company,userListQueue))

        get_user_list_thread.start()
        get_user_list_thread.join()

        userList = userListQueue.get()
        is_there_in_db = -1


        for user in userList:
            result = face_matching(face_from_image,user["image_path"])
            if result:
                is_there_in_db = 1
                break
        return is_there_in_db
    except Exception as e:
        print(str(e))
        return -1

def face_matching(face_from_image,image_path):
    download_image_thread = threading.Thread(target=download_image(image_path))
    download_image_thread.start()
    download_image_thread.join()

    face_from_db = find_face("src/image_from_db.jpg")

    if face_from_image is None or face_from_db is None:
        return False
    return face_recognition.compare_faces([face_from_image], face_from_db)[0]
