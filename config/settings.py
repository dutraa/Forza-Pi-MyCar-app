# config/settings.py
"""
Application configuration settings for Forza PI Calculator
"""

# Page Configuration
PAGE_CONFIG = {
    "page_title": "Forza Horizon PI Calculator",
    "page_icon": "🏎️",
    "layout": "wide",
    "initial_sidebar_state": "expanded"
}

# PI Calculation Constants
PI_CALCULATION = {
    "power_weight": 200,
    "power_max": 1500,
    "weight_weight": 100,
    "weight_max": 5000,
    "speed_weight": 200,
    "speed_max": 300,
    "acceleration_weight": 200,
    "acceleration_max": 10,
    "handling_weight": 200,
    "handling_max": 1.5,
    "braking_weight": 100,
    "braking_max": 150,
    "pi_min": 100,
    "pi_max": 999
}

# Class Color Mapping
CLASS_COLORS = {
    "D": {"css": "class-d", "color": "#8B4513", "name": "D Class"},
    "C": {"css": "class-c", "color": "#4169E1", "name": "C Class"},
    "B": {"css": "class-b", "color": "#32CD32", "name": "B Class"},
    "A": {"css": "class-a", "color": "#FFD700", "name": "A Class"},
    "S1": {"css": "class-s1", "color": "#FF6347", "name": "S1 Class"},
    "S2": {"css": "class-s2", "color": "#FF1493", "name": "S2 Class"},
    "X": {"css": "class-x", "color": "#9400D3", "name": "X Class"}
}

# Similar Cars Configuration
SIMILAR_CARS_CONFIG = {
    "default_count": 6,
    "nearby_classes": {
        "D": ["D", "C"],
        "C": ["D", "C", "B"], 
        "B": ["C", "B", "A"],
        "A": ["B", "A", "S1"],
        "S1": ["A", "S1", "S2"],
        "S2": ["S1", "S2", "X"],
        "X": ["S2", "X"]
    }
}

# File Paths
DATA_PATHS = {
    "forza_cars": "data/forza_cars.json",
    "real_cars": "data/real_cars.json",
    "car_classes": "data/car_classes.json"
}

# UI Text Content
UI_TEXT = {
    "app_title": "🏎️ FORZA HORIZON",
    "app_subtitle": "Performance Index Calculator",
    "app_description": "Estimate your real-world car's Forza PI rating and find similar cars in-game",
    "phase_status": "Phase 2A Complete: Similar Cars Feature",
    "coming_soon": "Coming Soon: VIN lookup, Enhanced algorithms, Mobile optimization"
}

# Feature Flags
FEATURES = {
    "vin_lookup_enabled": False,
    "car_finder_enabled": False,  # Will be True after Phase 2B
    "similar_cars_enabled": True,
    "performance_breakdown_enabled": True
}