from planner import total_distance


def test_a_route_is_as_long_as_its_legs_together() -> None:
    assert total_distance([1.5, 2.0, 3.5]) == 7.0


def test_a_route_with_no_legs_has_no_length() -> None:
    assert total_distance([]) == 0
