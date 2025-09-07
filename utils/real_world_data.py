# utils/real_world_data.py
"""
Real-world vehicle data integration module for enhanced PI calculations
Integrates with external data sources for authentic vehicle specifications
"""

import csv
import json
import requests
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
from datetime import datetime, timedelta
import os

@dataclass
class RealWorldVehicle:
    """Data class for real-world vehicle specifications"""
    year: int
    make: str
    model: str
    trim: Optional[str] = None
    
    # Performance specs
    horsepower: Optional[float] = None
    torque_lbft: Optional[float] = None
    weight_lbs: Optional[float] = None
    top_speed_mph: Optional[float] = None
    acceleration_0_60: Optional[float] = None
    handling_g_force: Optional[float] = None
    braking_60_0_ft: Optional[float] = None
    
    # Additional specs
    engine_displacement_cc: Optional[float] = None
    engine_cylinders: Optional[int] = None
    drivetrain: Optional[str] = None
    transmission: Optional[str] = None
    fuel_type: Optional[str] = None
    body_style: Optional[str] = None
    
    # Calculated/derived values
    calculated_pi: Optional[int] = None
    pi_source: Optional[str] = None
    confidence_score: Optional[float] = None
    
    # Metadata
    data_source: Optional[str] = None
    last_updated: Optional[str] = None

class RealWorldDataManager:
    """Manages real-world vehicle data from various sources"""
    
    def __init__(self, cache_dir: str = None):
        # Use a proper cache directory with fallback options
        if cache_dir is None:
            # Try multiple cache directory options
            possible_dirs = [
                os.path.expanduser("~/.forza_pi_cache"),  # User home directory
                "/tmp/forza_pi_cache",                     # System temp directory
                "./cache",                                 # Current directory cache
            ]
            
            cache_dir = None
            for dir_path in possible_dirs:
                try:
                    os.makedirs(dir_path, exist_ok=True)
                    # Test write permission
                    test_file = os.path.join(dir_path, "test_write.tmp")
                    with open(test_file, 'w') as f:
                        f.write("test")
                    os.remove(test_file)
                    cache_dir = dir_path
                    break
                except (OSError, PermissionError):
                    continue
            
            # If all attempts fail, disable caching
            if cache_dir is None:
                print("Warning: Could not create cache directory. Caching disabled.")
                self.cache_enabled = False
                self.cache_dir = None
                self.cache_file = None
            else:
                self.cache_enabled = True
                self.cache_dir = cache_dir
                self.cache_file = os.path.join(cache_dir, "real_world_data.json")
        else:
            try:
                os.makedirs(cache_dir, exist_ok=True)
                self.cache_enabled = True
                self.cache_dir = cache_dir
                self.cache_file = os.path.join(cache_dir, "real_world_data.json")
            except (OSError, PermissionError):
                print(f"Warning: Could not create cache directory {cache_dir}. Caching disabled.")
                self.cache_enabled = False
                self.cache_dir = None
                self.cache_file = None
        
        self.google_sheets_id = "1IStNOtVWi8DLEUXqPLAWMPDiIvQzX_msrmFfd4dOfI4"
        self.cache_duration = timedelta(hours=24)  # Cache for 24 hours
        
        # Initialize with sample data
        self.vehicles_database = self._load_cached_data()
    
    def _load_cached_data(self) -> List[RealWorldVehicle]:
        """Load cached real-world vehicle data"""
        if not self.cache_enabled or not os.path.exists(self.cache_file):
            return self._get_sample_data()
            
        try:
            with open(self.cache_file, 'r') as f:
                data = json.load(f)
                
            # Check if cache is still valid
            cache_time = datetime.fromisoformat(data.get('timestamp', '2000-01-01'))
            if datetime.now() - cache_time < self.cache_duration:
                vehicles = []
                for vehicle_data in data.get('vehicles', []):
                    vehicles.append(RealWorldVehicle(**vehicle_data))
                return vehicles
        except (json.JSONDecodeError, TypeError, ValueError, OSError):
            pass
        
        # Return sample data if cache is invalid or doesn't exist
        return self._get_sample_data()
    
    def _save_cached_data(self, vehicles: List[RealWorldVehicle]):
        """Save vehicle data to cache"""
        if not self.cache_enabled:
            return
            
        try:
            data = {
                'timestamp': datetime.now().isoformat(),
                'vehicles': [vehicle.__dict__ for vehicle in vehicles],
                'source': 'mixed'
            }
            
            with open(self.cache_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Warning: Could not save cache: {e}")
    
    def _get_sample_data(self) -> List[RealWorldVehicle]:
        """Get sample real-world vehicle data for demonstration"""
        sample_vehicles = [
            # Sports Cars
            RealWorldVehicle(
                year=2022, make="Chevrolet", model="Corvette Stingray", trim="3LT",
                horsepower=495, torque_lbft=470, weight_lbs=3366, top_speed_mph=194,
                acceleration_0_60=2.9, handling_g_force=1.05, braking_60_0_ft=107,
                engine_displacement_cc=6162, engine_cylinders=8, drivetrain="RWD",
                transmission="8-Speed Automatic", fuel_type="Premium", body_style="Coupe",
                calculated_pi=823, pi_source="real_world_enhanced", confidence_score=0.95,
                data_source="sample_data", last_updated=datetime.now().isoformat()
            ),
            
            RealWorldVehicle(
                year=2023, make="Porsche", model="911", trim="Carrera S",
                horsepower=443, torque_lbft=390, weight_lbs=3354, top_speed_mph=191,
                acceleration_0_60=3.5, handling_g_force=1.10, braking_60_0_ft=104,
                engine_displacement_cc=2981, engine_cylinders=6, drivetrain="RWD",
                transmission="8-Speed PDK", fuel_type="Premium", body_style="Coupe",
                calculated_pi=798, pi_source="real_world_enhanced", confidence_score=0.92,
                data_source="sample_data", last_updated=datetime.now().isoformat()
            ),
            
            # Luxury Sedans
            RealWorldVehicle(
                year=2023, make="BMW", model="M5", trim="Competition",
                horsepower=617, torque_lbft=553, weight_lbs=4370, top_speed_mph=190,
                acceleration_0_60=3.1, handling_g_force=0.98, braking_60_0_ft=103,
                engine_displacement_cc=4395, engine_cylinders=8, drivetrain="AWD",
                transmission="8-Speed Automatic", fuel_type="Premium", body_style="Sedan",
                calculated_pi=765, pi_source="real_world_enhanced", confidence_score=0.94,
                data_source="sample_data", last_updated=datetime.now().isoformat()
            ),
            
            RealWorldVehicle(
                year=2023, make="Mercedes-AMG", model="E63 S", trim="4MATIC+",
                horsepower=603, torque_lbft=627, weight_lbs=4400, top_speed_mph=186,
                acceleration_0_60=3.4, handling_g_force=0.95, braking_60_0_ft=105,
                engine_displacement_cc=3982, engine_cylinders=8, drivetrain="AWD",
                transmission="9-Speed Automatic", fuel_type="Premium", body_style="Sedan",
                calculated_pi=742, pi_source="real_world_enhanced", confidence_score=0.91,
                data_source="sample_data", last_updated=datetime.now().isoformat()
            ),
            
            # Hot Hatches
            RealWorldVehicle(
                year=2023, make="Honda", model="Civic Type R", trim="FL5",
                horsepower=315, torque_lbft=310, weight_lbs=3125, top_speed_mph=169,
                acceleration_0_60=5.0, handling_g_force=1.02, braking_60_0_ft=100,
                engine_displacement_cc=1996, engine_cylinders=4, drivetrain="FWD",
                transmission="6-Speed Manual", fuel_type="Premium", body_style="Hatchback",
                calculated_pi=658, pi_source="real_world_enhanced", confidence_score=0.89,
                data_source="sample_data", last_updated=datetime.now().isoformat()
            ),
            
            RealWorldVehicle(
                year=2023, make="Volkswagen", model="Golf R", trim="DSG",
                horsepower=315, torque_lbft=295, weight_lbs=3300, top_speed_mph=155,
                acceleration_0_60=4.7, handling_g_force=0.97, braking_60_0_ft=108,
                engine_displacement_cc=1984, engine_cylinders=4, drivetrain="AWD",
                transmission="7-Speed DSG", fuel_type="Premium", body_style="Hatchback",
                calculated_pi=672, pi_source="real_world_enhanced", confidence_score=0.87,
                data_source="sample_data", last_updated=datetime.now().isoformat()
            ),
            
            # SUVs
            RealWorldVehicle(
                year=2023, make="BMW", model="X3 M", trim="Competition",
                horsepower=503, torque_lbft=442, weight_lbs=4350, top_speed_mph=177,
                acceleration_0_60=3.8, handling_g_force=0.89, braking_60_0_ft=110,
                engine_displacement_cc=2993, engine_cylinders=6, drivetrain="AWD",
                transmission="8-Speed Automatic", fuel_type="Premium", body_style="SUV",
                calculated_pi=692, pi_source="real_world_enhanced", confidence_score=0.88,
                data_source="sample_data", last_updated=datetime.now().isoformat()
            ),
        ]
        
        return sample_vehicles
    
    def find_vehicle_match(self, year: int, make: str, model: str, 
                          trim: Optional[str] = None) -> Optional[RealWorldVehicle]:
        """Find exact or close match for a vehicle in real-world database"""
        make_clean = make.lower().strip()
        model_clean = model.lower().strip()
        
        # Try exact match first
        for vehicle in self.vehicles_database:
            if (vehicle.year == year and 
                vehicle.make.lower() == make_clean and 
                vehicle.model.lower() == model_clean):
                
                # If trim specified, try to match it too
                if trim:
                    trim_clean = trim.lower().strip()
                    if vehicle.trim and trim_clean in vehicle.trim.lower():
                        return vehicle
                else:
                    return vehicle
        
        # Try fuzzy match (same make/model, different year within 2 years)
        for vehicle in self.vehicles_database:
            if (abs(vehicle.year - year) <= 2 and 
                vehicle.make.lower() == make_clean and 
                vehicle.model.lower() == model_clean):
                return vehicle
        
        return None
    
    def get_enhanced_pi_calculation(self, vehicle: RealWorldVehicle) -> Tuple[int, float]:
        """Calculate enhanced PI using real-world data and improved formulas"""
        if not all([vehicle.horsepower, vehicle.weight_lbs, vehicle.top_speed_mph, 
                   vehicle.acceleration_0_60]):
            # Fallback to basic calculation if missing data
            return self._basic_pi_calculation(vehicle), 0.5
        
        # Enhanced PI calculation with real-world weighting
        pi_components = {}
        
        # Power component (35% weight) - includes torque consideration
        base_power = (vehicle.horsepower / 1500) * 350
        if vehicle.torque_lbft:
            torque_bonus = (vehicle.torque_lbft / 800) * 50  # Torque adds up to 50 PI
            pi_components['power'] = min(base_power + torque_bonus, 400)
        else:
            pi_components['power'] = min(base_power, 350)
        
        # Weight component (15% weight) - improved scaling
        pi_components['weight'] = ((5500 - vehicle.weight_lbs) / 5500) * 150
        
        # Speed component (20% weight)
        pi_components['speed'] = (vehicle.top_speed_mph / 300) * 200
        
        # Acceleration component (20% weight) - more realistic scaling
        accel_score = ((12 - vehicle.acceleration_0_60) / 12) * 200
        pi_components['acceleration'] = max(0, min(accel_score, 200))
        
        # Handling component (7% weight) - if available
        if vehicle.handling_g_force:
            pi_components['handling'] = (vehicle.handling_g_force / 1.5) * 70
        else:
            # Estimate based on vehicle type and weight
            estimated_g = self._estimate_handling(vehicle)
            pi_components['handling'] = (estimated_g / 1.5) * 70
        
        # Braking component (3% weight) - if available
        if vehicle.braking_60_0_ft:
            braking_score = ((160 - vehicle.braking_60_0_ft) / 160) * 30
            pi_components['braking'] = max(0, min(braking_score, 30))
        else:
            # Estimate based on vehicle type
            estimated_braking = self._estimate_braking(vehicle)
            pi_components['braking'] = ((160 - estimated_braking) / 160) * 30
        
        # Calculate total PI
        total_pi = sum(pi_components.values())
        
        # Apply drivetrain and vehicle type modifiers
        total_pi = self._apply_modifiers(total_pi, vehicle)
        
        # Clamp to valid range
        final_pi = max(100, min(999, int(total_pi)))
        
        # Calculate confidence based on available data
        confidence = self._calculate_confidence(vehicle)
        
        return final_pi, confidence
    
    def _basic_pi_calculation(self, vehicle: RealWorldVehicle) -> int:
        """Fallback to basic PI calculation if missing real-world data"""
        hp = vehicle.horsepower or 300
        weight = vehicle.weight_lbs or 3500
        speed = vehicle.top_speed_mph or 150
        accel = vehicle.acceleration_0_60 or 5.0
        
        pi = (
            (hp / 1500) * 200 +
            ((5000 - weight) / 5000) * 100 +
            (speed / 300) * 200 +
            ((10 - accel) / 10) * 200 +
            (1.0 / 1.5) * 200 +  # Default handling
            ((150 - 120) / 150) * 100  # Default braking
        )
        
        return max(100, min(999, int(pi)))
    
    def _estimate_handling(self, vehicle: RealWorldVehicle) -> float:
        """Estimate handling G-force based on vehicle characteristics"""
        base_g = 0.85  # Base handling
        
        if vehicle.body_style:
            body = vehicle.body_style.lower()
            if 'coupe' in body or 'roadster' in body:
                base_g = 1.0
            elif 'sedan' in body:
                base_g = 0.9
            elif 'suv' in body or 'truck' in body:
                base_g = 0.8
            elif 'hatch' in body:
                base_g = 0.95
        
        # Weight penalty
        if vehicle.weight_lbs:
            if vehicle.weight_lbs > 4000:
                base_g -= 0.1
            elif vehicle.weight_lbs < 3000:
                base_g += 0.1
        
        # AWD bonus for handling
        if vehicle.drivetrain and 'awd' in vehicle.drivetrain.lower():
            base_g += 0.05
        
        return max(0.7, min(1.3, base_g))
    
    def _estimate_braking(self, vehicle: RealWorldVehicle) -> float:
        """Estimate braking distance based on vehicle characteristics"""
        base_braking = 115  # Base braking distance
        
        # Weight penalty
        if vehicle.weight_lbs:
            weight_factor = (vehicle.weight_lbs - 3000) / 1000 * 10
            base_braking += weight_factor
        
        # Performance vehicle bonus
        if vehicle.horsepower and vehicle.horsepower > 400:
            base_braking -= 10  # Better brakes on performance cars
        
        return max(90, min(150, base_braking))
    
    def _apply_modifiers(self, pi: float, vehicle: RealWorldVehicle) -> float:
        """Apply vehicle-specific modifiers to PI"""
        modified_pi = pi
        
        # AWD modifier (better traction but more weight)
        if vehicle.drivetrain and 'awd' in vehicle.drivetrain.lower():
            modified_pi *= 1.02  # Slight bonus for AWD
        
        # Manual transmission modifier (enthusiast bonus)
        if vehicle.transmission and 'manual' in vehicle.transmission.lower():
            modified_pi *= 1.01
        
        # Premium fuel modifier
        if vehicle.fuel_type and 'premium' in vehicle.fuel_type.lower():
            modified_pi *= 1.005
        
        return modified_pi
    
    def _calculate_confidence(self, vehicle: RealWorldVehicle) -> float:
        """Calculate confidence score based on available data completeness"""
        required_fields = ['horsepower', 'weight_lbs', 'top_speed_mph', 'acceleration_0_60']
        optional_fields = ['torque_lbft', 'handling_g_force', 'braking_60_0_ft', 
                          'engine_displacement_cc', 'drivetrain']
        
        required_score = sum(1 for field in required_fields 
                           if getattr(vehicle, field) is not None) / len(required_fields)
        
        optional_score = sum(1 for field in optional_fields 
                           if getattr(vehicle, field) is not None) / len(optional_fields)
        
        # Weight required fields more heavily
        confidence = (required_score * 0.8) + (optional_score * 0.2)
        
        return min(1.0, confidence)
    
    def update_from_google_sheets(self) -> bool:
        """Update real-world data from Google Sheets (when available)"""
        try:
            csv_url = f"https://docs.google.com/spreadsheets/d/{self.google_sheets_id}/export?format=csv"
            response = requests.get(csv_url, timeout=10)
            
            if response.status_code == 200:
                # Parse CSV data
                vehicles = self._parse_csv_data(response.text)
                if vehicles:
                    self.vehicles_database = vehicles
                    if self.cache_enabled:
                        self._save_cached_data(vehicles)
                    return True
                    
        except Exception as e:
            print(f"Could not update from Google Sheets: {e}")
        
        return False
    
    def _parse_csv_data(self, csv_data: str) -> List[RealWorldVehicle]:
        """Parse CSV data into RealWorldVehicle objects"""
        vehicles = []
        reader = csv.DictReader(csv_data.splitlines())
        
        for row in reader:
            try:
                # Map CSV columns to vehicle attributes
                # This would need to be adjusted based on actual sheet structure
                vehicle = RealWorldVehicle(
                    year=int(row.get('Year', 0)),
                    make=row.get('Make', ''),
                    model=row.get('Model', ''),
                    trim=row.get('Trim'),
                    horsepower=float(row.get('HP', 0)) if row.get('HP') else None,
                    weight_lbs=float(row.get('Weight', 0)) if row.get('Weight') else None,
                    # Add more mappings as needed
                    data_source="google_sheets",
                    last_updated=datetime.now().isoformat()
                )
                
                if vehicle.year > 0 and vehicle.make and vehicle.model:
                    vehicles.append(vehicle)
                    
            except (ValueError, TypeError):
                continue  # Skip invalid rows
        
        return vehicles

# Convenience functions
def find_real_world_vehicle(year: int, make: str, model: str, 
                           trim: Optional[str] = None) -> Optional[RealWorldVehicle]:
    """Find a real-world vehicle match"""
    manager = RealWorldDataManager()
    return manager.find_vehicle_match(year, make, model, trim)

def calculate_enhanced_pi(vehicle: RealWorldVehicle) -> Tuple[int, float]:
    """Calculate enhanced PI for a real-world vehicle"""
    manager = RealWorldDataManager()
    return manager.get_enhanced_pi_calculation(vehicle)