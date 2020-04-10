
def kwargs_to_string(**kwargs):
    return ', '.join('%s=%r' % x for x in kwargs.items())
