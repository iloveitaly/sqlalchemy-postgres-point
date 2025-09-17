import math


def haversine_miles(lat1: float, lng1: float, lat2: float, lng2: float) -> float:
    """
    Compute the straight-line distance between two locations on Earth, measured in miles.

    This uses the Haversine formula, which treats the Earth as a sphere and returns the
    great‑circle distance (the shortest path over the planet's surface). It is ideal for
    proximity checks (e.g., “within 10 miles?”) and for sorting by closeness. The result
    is “as‑the‑crow‑flies” distance: it does not reflect driving routes, traffic, terrain,
    or elevation. For most application use cases up to a few hundred miles, the spherical
    assumption provides a sufficiently accurate answer (typically within well under 1%).

    Inputs are latitude and longitude in degrees for both points, and the output is a
    floating‑point number in miles. The function is symmetric in its two points and does
    not require any external services or API calls.
    """
    R = 3958.8

    lat1_rad = math.radians(lat1)
    lat2_rad = math.radians(lat2)
    dlat = math.radians(lat2 - lat1)
    dlng = math.radians(lng2 - lng1)

    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlng / 2) ** 2
    )
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c
