import json
from os.path import join


def get_param(key):
    path = join("parameters.json")
    with open(path, "r", encoding="UTF-8") as file:
        data = json.load(file)
    value = data[key]
    return value