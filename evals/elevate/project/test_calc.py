from calc import average


def test_average():
    assert average([1, 2, 3]) == 2


def test_average_of_nothing():
    assert average([]) == 0
