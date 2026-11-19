import json


def load_settings(path):
    try:
        with open(path) as file:
            return json.load(file)
    except Exception:
        return {}


def total(prices):
    result = 0
    for price in prices:
        result = result + price
    return result
