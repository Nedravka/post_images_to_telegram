import os
import json
from pathlib import Path

import requests


def create_path(path):
    Path(f'{path}').mkdir(parents=True, exist_ok=True)
    os.chdir(path)

