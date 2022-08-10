import re
from collections import OrderedDict


def is_not_empty(d):
    if isinstance(d, list):
        return any([is_not_empty(x) for x in d])
    if isinstance(d, dict) or isinstance(d, OrderedDict):
        return any([is_not_empty(x) for x in d.values()])
    else:
        return bool(d)


def none_to_blank(s: str) -> str:
    if s is None:
        return ''
    s = s.strip()
    s = re.sub(r'\s+', ' ', s)
    return s


def dict_none_to_blank(d: dict) -> dict:
    for key, value in d.items():
        if isinstance(value, str) or value is None:
            d[key] = none_to_blank(value)
    return d