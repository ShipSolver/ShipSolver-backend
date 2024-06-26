import os
from flask import abort, request
from functools import wraps
import copy
import json


class AlchemyEncoder(json.JSONEncoder):
    def default(self, obj):

        if "enum" in str(type(obj)):
            return str(obj)
        # Let the base class default method raise the TypeError
        return json.JSONEncoder.default(self, obj)

def get_clean_filters_dict(immutable_args):
    sql_filters = dict(immutable_args)
    if "start" in sql_filters:
        del sql_filters["start"]
    if "end" in sql_filters:
        del sql_filters["end"]
    if "limit" in sql_filters:
        del sql_filters["limit"]
    return sql_filters

# DFS function used to convert alchemy objects to JSON
def alchemyConvertUtil(object, res, visited):
    visited.add(str(object.__class__))
    for field in [
        x
        for x in dir(object)
        if not x.startswith("_")
        and x not in set({"metadata", "non_prim_identifying_column_name", "registry"})
    ]:

        cls_name = str(object.__getattribute__(field).__class__)

        if "models.models." in cls_name:
            if cls_name in visited:
                continue
            else:
                visited.add(cls_name)

            res[field] = {}
            alchemyConvertUtil(getattr(object, field), res[field], visited=visited)
            visited.remove(cls_name)
        elif "InstrumentedList" in cls_name:
            res[field] = []

            for i, obj in enumerate(getattr(object, field)):

                res[field].append({})
                alchemyConvertUtil(obj, res[field][i], visited=visited)

        else:
            res[field] = getattr(object, field)

    return res
    
def alchemyConverter(obj):
    if type(obj) == list:
        res = [] 
        for ele in obj:
            json_res = alchemyConvertUtil(ele, {}, visited=set())
            res.append(json_res)
        return res
    else:
        return alchemyConvertUtil(obj, {}, visited=set())


# converts fiters as a dictionary to alchemy interpretable results
#  Function expects input
#
#  data = {
#    model.field1: "value1"
#    model.field1: "value2"
# }
def convert_dict_to_alchemy_filters(model, filters_dict):
    res = []

    for key in filters_dict:
        res.append(getattr(model, key) == filters_dict[key])

    return res


# API authentication route decorator
def require_appkey(view_function):
    @wraps(view_function)
    def decorated_function(*args, **kwargs):

        if "API_KEY" not in os.environ:
            raise Exception("NO API KEY FOUND")

        print(request.args)
        print(request.args.get("key"), os.environ["API_KEY"])
        if request.args.get("key") == os.environ["API_KEY"]:
            return view_function(*args, **kwargs)
        else:
            abort(401)

    return decorated_function
