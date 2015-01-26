import os
import sys
import yaml

sys.path.append(os.path.dirname(__file__))
from conflib import insert_conf

DIR = os.path.join(os.path.dirname(__file__), "..")
sys.path.append(DIR)
sys.path.append(os.path.join(DIR, 'config'))

from config import CONFIG


def load(src):
    data = ""
    with open(src, 'r', encoding='utf-8') as f:
        data = f.read()
    data = insert_conf(data, CONFIG, filename=src)
    return yaml.load(data)
