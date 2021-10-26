import jsonref
import json
from copy import deepcopy
from enum import IntEnum


def read_schema(fname):
    try:
        with open(fname, 'r') as f:
            schema = deepcopy(jsonref.load(f))
            return schema
    except Exception as e:
        msg = f"Error Reading: {fname} | {str(e)}"
        raise Exception(msg)


def save_json(data: dict, fname):
    with open(fname, "w") as fout:
        json.dump(data, fout, indent=2, ensure_ascii=False)


class Log(IntEnum):
    WARNING = 0
    CRITICAL = 1
