import yaml

from lib.conflib import insert_conf
from config.config import CONFIG


def load(src):
    data = ""
    with open(src, 'r', encoding='utf-8') as f:
        data = f.read()
    data = insert_conf(data, CONFIG, filename=src)
    return yaml.load(data)
