from json import JSONEncoder

__author__ = 'drake'


class ObjectJSONEncoder(JSONEncoder):
    def default(self, reject):
        return reject.__json__()