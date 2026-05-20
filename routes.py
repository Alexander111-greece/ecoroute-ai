# Distance matrix for Indian cities (km) - hardcoded for demo
CITY_DISTANCES = {
    ("Mumbai", "Pune"): 150,
    ("Mumbai", "Nashik"): 170,
    ("Mumbai", "Surat"): 280,
    ("Mumbai", "Ahmedabad"): 530,
    ("Mumbai", "Nagpur"): 830,
    ("Pune", "Nashik"): 210,
    ("Pune", "Aurangabad"): 240,
    ("Pune", "Nagpur"): 700,
    ("Delhi", "Jaipur"): 280,
    ("Delhi", "Agra"): 230,
    ("Delhi", "Chandigarh"): 250,
    ("Delhi", "Lucknow"): 550,
    ("Delhi", "Amritsar"): 450,
    ("Chennai", "Bangalore"): 350,
    ("Chennai", "Hyderabad"): 630,
    ("Bangalore", "Hyderabad"): 570,
    ("Bangalore", "Mysore"): 150,
    ("Hyderabad", "Nagpur"): 500,
    ("Kolkata", "Bhubaneswar"): 440,
    ("Kolkata", "Patna"): 580,
}

def get_distance(city_a, city_b):
    """Get distance between two cities."""
    city_a = city_a.strip().title()
    city_b = city_b.strip().title()

    if city_a == city_b:
        return 0

    key1 = (city_a, city_b)
    key2 = (city_b, city_a)

    if key1 in CITY_DISTANCES:
        return CITY_DISTANCES[key1]
    elif key2 in CITY_DISTANCES:
        return CITY_DISTANCES[key2]
    else:
        # Default estimate if city pair not in database
        return 300

def get_route_legs(stops):
    """
    Given a list of stops [warehouse, stop1, stop2, ...],
    return each leg with its distance.
    """
    legs = []
    for i in range(len(stops) - 1):
        from_city = stops[i]
        to_city = stops[i + 1]
        if from_city and to_city:
            distance = get_distance(from_city, to_city)
            legs.append({
                "from": from_city,
                "to": to_city,
                "distance_km": distance
            })
    return legs