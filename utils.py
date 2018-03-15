import re


def slugify(title):
	"""Generates a slug for the title introduced"""
    return re.sub('[^a-zA-Z0-9_-]+', '-', title)
