import json

def user_feeling_parser(context, snapshot):
    hunger, thirst, exhaustion, happiness = \
            snapshot.user_feeling
    context.save('user_feeling.json', json.dumps(dict(
        hunger = hunger,
        thirst = thirst,
        exhaustion = exhaustion,
        happiness = happiness,
    )))
user_feeling_parser.field = 'user_feeling'
