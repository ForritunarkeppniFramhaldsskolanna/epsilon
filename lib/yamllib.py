import yaml
import re
import os
import sys

DIR = os.path.join(os.path.dirname(__file__), "..")
sys.path.append(DIR)

from config import CONFIG


def insert_env(data):
    k = set()
    locations = [m.start() for m in re.finditer('__EPSILON_', data)]
    for loc in locations:
        i = int(loc)
        while data[i].isalnum() or data[i] == "_":
            i += 1
        k.add(data[loc:i])
    for key in k:
        try:
            data = data.replace(key, CONFIG[key.replace("__", "").replace("EPSILON_", "")])
        except KeyError:
            print("Invalid key in file", key)
    return data


def load(src):
    data = ""
    with open(src, 'r', encoding='utf-8') as f:
        data = f.read()
    data = insert_env(data)
    return yaml.load(data)
