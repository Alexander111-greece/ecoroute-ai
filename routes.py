# Distance matrix for Indian cities (km) - expanded database
CITY_DISTANCES = {
    # Maharashtra
    ("Mumbai", "Pune"): 150,
    ("Mumbai", "Nashik"): 170,
    ("Mumbai", "Surat"): 280,
    ("Mumbai", "Ahmedabad"): 530,
    ("Mumbai", "Nagpur"): 830,
    ("Mumbai", "Aurangabad"): 340,
    ("Mumbai", "Kolhapur"): 380,
    ("Mumbai", "Solapur"): 450,
    ("Pune", "Nashik"): 210,
    ("Pune", "Aurangabad"): 240,
    ("Pune", "Nagpur"): 700,
    ("Pune", "Kolhapur"): 230,
    ("Pune", "Solapur"): 250,
    ("Nagpur", "Aurangabad"): 490,

    # Delhi NCR & North
    ("Delhi", "Jaipur"): 280,
    ("Delhi", "Agra"): 230,
    ("Delhi", "Chandigarh"): 250,
    ("Delhi", "Lucknow"): 550,
    ("Delhi", "Amritsar"): 450,
    ("Delhi", "Dehradun"): 300,
    ("Delhi", "Haridwar"): 220,
    ("Delhi", "Meerut"): 70,
    ("Delhi", "Kanpur"): 480,
    ("Delhi", "Varanasi"): 820,
    ("Delhi", "Patna"): 1000,
    ("Jaipur", "Agra"): 240,
    ("Jaipur", "Ahmedabad"): 670,
    ("Lucknow", "Kanpur"): 80,
    ("Lucknow", "Varanasi"): 320,
    ("Lucknow", "Patna"): 530,

    # South India
    ("Chennai", "Bangalore"): 350,
    ("Chennai", "Hyderabad"): 630,
    ("Chennai", "Coimbatore"): 500,
    ("Chennai", "Madurai"): 460,
    ("Chennai", "Kochi"): 680,
    ("Bangalore", "Hyderabad"): 570,
    ("Bangalore", "Mysore"): 150,
    ("Bangalore", "Coimbatore"): 360,
    ("Bangalore", "Kochi"): 560,
    ("Bangalore", "Mangalore"): 350,
    ("Hyderabad", "Nagpur"): 500,
    ("Hyderabad", "Pune"): 560,
    ("Hyderabad", "Vijayawada"): 270,
    ("Kochi", "Coimbatore"): 200,
    ("Kochi", "Madurai"): 240,

    # East India
    ("Kolkata", "Bhubaneswar"): 440,
    ("Kolkata", "Patna"): 580,
    ("Kolkata", "Guwahati"): 1000,
    ("Kolkata", "Ranchi"): 400,
    ("Kolkata", "Varanasi"): 680,
    ("Bhubaneswar", "Visakhapatnam"): 440,
    ("Patna", "Varanasi"): 280,

    # Gujarat
    ("Ahmedabad", "Surat"): 270,
    ("Ahmedabad", "Rajkot"): 220,
    ("Ahmedabad", "Vadodara"): 110,
    ("Surat", "Vadodara"): 160,
    ("Vadodara", "Rajkot"): 230,

    # Central India
    ("Bhopal", "Indore"): 200,
    ("Bhopal", "Nagpur"): 350,
    ("Bhopal", "Jabalpur"): 290,
    ("Indore", "Ahmedabad"): 400,
    ("Indore", "Mumbai"): 590,
    ("Indore", "Nagpur"): 470,
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
