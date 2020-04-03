import json

def translation_parser(context, snapshot):
    x, y, z = snapshot.translation
    context.save('translation.json', json.dumps(dict(
        x = x,
        y = y,
        z = z,
    )))
translation_parser.field = 'translation'
