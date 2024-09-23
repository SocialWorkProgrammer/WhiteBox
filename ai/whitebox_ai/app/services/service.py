from PIL import Image
from io import BytesIO
import requests
import cv2
import numpy as np

# return type : Image.Image
def url_to_img(img_path):
    response = requests.get(img_path)
    img_array = np.asarray(bytearray(response.content), dtype=np.uint8)
    img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
    print(img)
    return img

def byte_to_img(img_bytes):
    np_array = np.frombuffer(img_bytes, np.uint8)
    img = cv2.imdecode(np_array, cv2.IMREAD_COLOR)
    return img