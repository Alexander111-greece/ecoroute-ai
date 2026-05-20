# Emission factors (kg CO2 per km)
EMISSION_FACTORS = {
    "Diesel Truck (Heavy)": 1.1,
    "Diesel Truck (Light)": 0.6,
    "CNG Truck": 0.65,
    "Electric Vehicle": 0.15
}

# Average fuel cost per km (INR)
FUEL_COST_PER_KM = {
    "Diesel Truck (Heavy)": 18,
    "Diesel Truck (Light)": 12,
    "CNG Truck": 9,
    "Electric Vehicle": 3
}

def calculate_carbon(distance_km, vehicle_type, load_weight_tons):
    """Calculate CO2 emitted for a given route."""
    base_factor = EMISSION_FACTORS[vehicle_type]
    
    # Heavier load = slightly more emissions
    load_multiplier = 1 + (load_weight_tons / 100)
    
    co2_kg = distance_km * base_factor * load_multiplier
    return round(co2_kg, 2)

def calculate_fuel_cost(distance_km, vehicle_type):
    """Estimate fuel cost in INR."""
    cost = distance_km * FUEL_COST_PER_KM[vehicle_type]
    return round(cost, 2)

def calculate_carbon_saved(distance_km, chosen_vehicle, load_weight_tons):
    """Compare chosen vehicle vs worst option (Diesel Heavy)."""
    worst = calculate_carbon(distance_km, "Diesel Truck (Heavy)", load_weight_tons)
    chosen = calculate_carbon(distance_km, chosen_vehicle, load_weight_tons)
    saved = worst - chosen
    return round(saved, 2)

def get_carbon_score(co2_kg, distance_km):
    """Rate the route from 1-5 stars based on CO2 per km."""
    co2_per_km = co2_kg / distance_km
    if co2_per_km < 0.2:
        return 5
    elif co2_per_km < 0.5:
        return 4
    elif co2_per_km < 0.8:
        return 3
    elif co2_per_km < 1.0:
        return 2
    else:
        return 1