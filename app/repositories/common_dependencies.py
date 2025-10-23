import math

EARTH_RADIUS_KM = 6371.0


def haversine_distance(latitude1, longitude1, latitude2, longitude2):
    lat1, lon1, lat2, lon2 = map(math.radians, [latitude1, longitude1, latitude2, longitude2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    c = 2 * math.asin(math.sqrt(a))
    return EARTH_RADIUS_KM * c
