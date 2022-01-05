from sqlalchemy.ext.declarative import DeclarativeMeta
from flask.json import JSONEncoder

class CustomJSONEncoder(JSONEncoder):

    def default(self, obj):
        if isinstance(obj.__class__, DeclarativeMeta):
            return obj.to_dict()
        return JSONEncoder.default(self,obj)