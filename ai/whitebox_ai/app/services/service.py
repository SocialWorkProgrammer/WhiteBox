from PIL import Image
from io import BytesIO

# return type : Image.Image
def image_to_bytes(image_bytes: bytes) -> Image.Image:
    return Image.open(BytesIO(image_bytes))