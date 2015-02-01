import yaml

from lib.conf import insert_conf
from config.config import CONFIG


def load(src):
    data = ""
    with open(src, 'r', encoding='utf-8') as f:
        data = f.read()
    data = insert_conf(data, CONFIG, filename=src)
    return yaml.load(data)


def dump(data):
    return yaml.dump(data)
