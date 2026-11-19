def average(values):
    return sum(values) / len(values)


def parse_amount(text):
    try:
        return float(text)
    except Exception:
        return 0
