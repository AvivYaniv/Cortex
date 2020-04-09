import io

from PIL import Image as PIL

class ColorImageParser:

    field       = 'color_image'

    extension   = '.png'

    def parse(self, snapshot):
        size                = snapshot.color_image.width, snapshot.color_image.height
        image               = PIL.frombytes('RGB', size, bytes(snapshot.color_image.data))
        image_byte_array    = io.BytesIO()
        image.save(image_byte_array, format='PNG')
        return image_byte_array.getvalue()
    