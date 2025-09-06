# utils/pi_calculator.py
"""
PI calculation module for Forza PI Calculator
Handles all Performance Index calculations and performance breakdowns
"""

from typing import Dict, Tuple
from config.settings import PI_CALCULATION, CLASS_COLORS

def calculate_pi(hp: float, weight: float, top_speed: float, acceleration: float, 
                handling: float, braking: float) -> int:
    """Calculate Performance Index based on vehicle specifications"""
    
    # Use constants from settings
    calc_config = PI_CALCULATION
    
    pi = (
        (hp / calc_config["power_max"]) * calc_config["power_weight"] +
        ((calc_config["weight_max"] - weight) / calc_config["weight_max"]) * calc_config["weight_weight"] +
        (top_speed / calc_config["speed_max"]) * calc_config["speed_weight"] +
        ((calc_config["acceleration_max"] - acceleration) / calc_config["acceleration_max"]) * calc_config["acceleration_weight"] +
        (handling / calc_config["handling_max"]) * calc_config["handling_weight"] +
        ((calc_config["braking_max"] - braking) / calc_config["braking_max"]) * calc_config["braking_weight"]
    )
    
    # Clamp PI to valid range
    pi = round(min(max(pi, calc_config["pi_min"]), calc_config["pi_max"]))
    
    return pi

def get_performance_breakdown(hp: float, weight: float, top_speed: float, 
                            acceleration: float, handling: float, braking: float) -> Dict[str, int]:
    """Calculate individual performance metric contributions to PI"""
    
    calc_config = PI_CALCULATION
    
    return {
        "power": round((hp / calc_config["power_max"]) * calc_config["power_weight"]),
        "weight": round(((calc_config["weight_max"] - weight) / calc_config["weight_max"]) * calc_config["weight_weight"]),
        "speed": round((top_speed / calc_config["speed_max"]) * calc_config["speed_weight"]),
        "acceleration": round(((calc_config["acceleration_max"] - acceleration) / calc_config["acceleration_max"]) * calc_config["acceleration_weight"]),
        "handling": round((handling / calc_config["handling_max"]) * calc_config["handling_weight"]),
        "braking": round(((calc_config["braking_max"] - braking) / calc_config["braking_max"]) * calc_config["braking_weight"])
    }

def determine_forza_class(pi: int) -> str:
    """Determine Forza class based on PI value"""
    if pi < 300:
        return "D"
    elif pi < 400:
        return "C"
    elif pi < 500:
        return "B"
    elif pi < 600:
        return "A"
    elif pi < 700:
        return "S1"
    elif pi < 800:
        return "S2"
    else:
        return "X"

def get_class_info(forza_class: str) -> Tuple[str, str]:
    """Get CSS class and color for a Forza class"""
    class_info = CLASS_COLORS.get(forza_class, {"css": "", "color": "#ffffff"})
    return class_info["css"], class_info["color"]

def validate_input_ranges(hp: float, weight: float, top_speed: float, 
                         acceleration: float, handling: float, braking: float) -> Dict[str, str]:
    """Validate input values and return any warnings"""
    warnings = {}
    
    if hp < 50 or hp > 2000:
        warnings["hp"] = "Horsepower seems unusual (typical range: 50-2000 HP)"
    
    if weight < 1000 or weight > 8000:
        warnings["weight"] = "Weight seems unusual (typical range: 1000-8000 lbs)"
    
    if top_speed < 60 or top_speed > 300:
        warnings["top_speed"] = "Top speed seems unusual (typical range: 60-300 mph)"
    
    if acceleration < 2.0 or acceleration > 15.0:
        warnings["acceleration"] = "0-60 time seems unusual (typical range: 2.0-15.0 seconds)"
    
    if handling < 0.5 or handling > 2.0:
        warnings["handling"] = "Handling G-force seems unusual (typical range: 0.5-2.0 G)"
    
    if braking < 80 or braking > 200:
        warnings["braking"] = "Braking distance seems unusual (typical range: 80-200 feet)"
    
    return warnings