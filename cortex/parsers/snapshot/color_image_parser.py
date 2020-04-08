from PIL import Image as PIL

class ColorImageParser:

    field       = 'color_image'

    extension   =   '.jpg'

    def parse(self, parser_saver, context, snapshot):
        path = parser_saver.get_path(context, ColorImageParser.extension)
        parser_saver.create_path(path)
        size = snapshot.color_image.width, snapshot.color_image.height
        image = PIL.frombytes('RGB', size, bytes(snapshot.color_image.data))
        image.save(path)
        return path