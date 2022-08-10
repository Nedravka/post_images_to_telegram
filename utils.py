import os
from urllib.parse import unquote, urlsplit


def get_file_extension(url):
    name_of_file = urlsplit(url).path
    *_, file_extension = os.path.splitext(unquote(name_of_file))
    return file_extension
