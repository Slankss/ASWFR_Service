from Constant import image_base64
import pybase64
import base64


def base64_to_image(base64):
    decodedData = pybase64.b64decode(base64)
    image = open("decodedImage.jpeg", "wb")
    image.write(decodedData)
    image.close()


def image_to_base64():

    image = open("originalImage.jpeg", "rb")
    image_bytes = pybase64.b64encode(image.read())
    base64 = image_bytes.decode()
    print(base64)

