"""Delivery route planner built for Acme Logistics."""


def total_distance(legs: list[float]) -> float:
    """Return the length of a route as the sum of its legs, in kilometres."""
    return sum(legs)
