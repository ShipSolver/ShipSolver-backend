import os
from flask import abort, request
from functools import wraps

import json


class AlchemyEncoder(json.JSONEncoder):
    def default(self, obj):

        if "enum" in str(type(obj)):
            return str(obj)
        # Let the base class default method raise the TypeError
        return json.JSONEncoder.default(self, obj)


def alchemyConverter(object, res={}, visited=set({})):
    for field in [
        x
        for x in dir(object)
        if not x.startswith("_")
        and x not in set({"metadata", "non_prim_identifying_column_name", "registry"})
    ]:

        cls_name = str(object.__getattribute__(field).__class__)

        visited.add(cls_name)

        if "models.models." in cls_name:
            if cls_name not in visited:
                res[field] = {}
                print(visited)
                alchemyConverter(getattr(object, field), res[field], visited=visited)
        elif "InstrumentedList" in cls_name:
            res[field] = []

            for i, obj in enumerate(getattr(object, field)):

                res[field].append({})
                alchemyConverter(obj, res[field][i], visited=visited)

        else:
            res[field] = getattr(object, field)

    return res


def require_appkey(view_function):

    # API authentication route decorator
    @wraps(view_function)
    def decorated_function(*args, **kwargs):
        if request.args.get("key") and request.args.get("key") == os.environ["API_KEY"]:
            return view_function(*args, **kwargs)
        else:
            abort(401)

    return decorated_function
