from posixpath import basename#, dirname
from urllib.parse import urlparse

def return_num(link):
    parse_object = urlparse(link)
    return basename(parse_object.path)


url = '/tasks/535923'

print(return_num(url))