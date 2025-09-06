# utils/data_manager.py
"""
Data management module for Forza PI Calculator
Handles car database loading and similar car search functionality
"""

import json
import os
from typing import List, Dict, Any
from config.settings import SIMILAR_CARS_CONFIG

def load_forza_cars_database() -> List[Dict[str, Any]]:
    """Load the Forza cars database from JSON file"""
    try:
        with open('forza_cars.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
            return data.get('cars', [])
    except FileNotFoundError:
        print("Warning: forza_cars.json not found. Using empty database.")
        return []
    except json.JSONDecodeError:
        print("Warning: Invalid JSON in forza_cars.json. Using empty database.")
        return []

def get_similar_cars(calculated_pi: int, user_class: str, num_cars: int = None) -> List[Dict[str, Any]]:
    """Find similar cars from Forza database based on PI and class"""
    if num_cars is None:
        num_cars = SIMILAR_CARS_CONFIG["default_count"]
    
    # Load the car database
    forza_cars_database = load_forza_cars_database()
    
    if not forza_cars_database:
        return []
    
    # Filter cars by class first, then by PI proximity
    class_cars = [car for car in forza_cars_database if car["class"] == user_class]
    
    if len(class_cars) < num_cars:
        # If not enough cars in exact class, expand to nearby classes
        nearby_classes = SIMILAR_CARS_CONFIG["nearby_classes"]
        expanded_cars = [car for car in forza_cars_database 
                        if car["class"] in nearby_classes.get(user_class, [user_class])]
        class_cars = expanded_cars
    
    # Sort by PI proximity to calculated PI
    class_cars.sort(key=lambda x: abs(x["pi"] - calculated_pi))
    
    return class_cars[:num_cars]

def get_car_database_stats() -> Dict[str, Any]:
    """Get statistics about the car database"""
    forza_cars_database = load_forza_cars_database()
    
    if not forza_cars_database:
        return {"total_cars": 0, "classes": {}}
    
    stats = {
        "total_cars": len(forza_cars_database),
        "classes": {}
    }
    
    # Count cars by class
    for car in forza_cars_database:
        car_class = car.get("class", "Unknown")
        if car_class not in stats["classes"]:
            stats["classes"][car_class] = 0
        stats["classes"][car_class] += 1
    
    return stats