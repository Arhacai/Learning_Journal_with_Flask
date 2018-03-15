import re


def slugify(title):
    return re.sub('[^a-zA-Z0-9_-]+', '-', title)
