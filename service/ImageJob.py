import pybase64
import base64

def base64_to_image(base64, dest_image):
    try:
        decodedData = pybase64.b64decode(base64)
        image = open("service/src/" + dest_image + ".jpg", "wb")
        image.write(decodedData)
        image.close()
    except:
        return None

def image_to_base64():
    image = open("originalImage.jpg", "rb")
    image_bytes = pybase64.b64encode(image.read())
    base64 = image_bytes.decode()
