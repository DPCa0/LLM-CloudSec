import os
import traceback

import yaml


def read_yaml_config(file_path: str):
    print("load_cfg", os.getcwd())
    with open(file_path, 'r') as stream:
        try:
            cfg = yaml.safe_load(stream)
        except yaml.YAMLError:
            print("load_cfg error")
            traceback.print_exc()
            cfg = None
    return cfg


config = read_yaml_config('config/config.yaml')
