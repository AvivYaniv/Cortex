
from PIL import Image

def get_image_metadata(pil_image):
    return pil_image.size

def get_image_metadata_by_uri(uri):
    pil_image = Image.open(uri)
    return get_image_metadata(pil_image)

