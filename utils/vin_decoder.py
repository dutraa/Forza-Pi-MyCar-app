# utils/vin_decoder.py
"""
VIN decoder module for Forza PI Calculator
Interfaces with NHTSA API to decode Vehicle Identification Numbers
"""

import requests
import re
from typing import Dict, Optional, Tuple, Any
from dataclasses import dataclass

@dataclass
class VehicleInfo:
    """Data class to hold decoded vehicle information"""
    year: Optional[str] = None
    make: Optional[str] = None
    model: Optional[str] = None
    trim: Optional[str] = None
    engine_type: Optional[str] = None
    engine_cylinders: Optional[str] = None
    engine_displacement_cc: Optional[str] = None
    engine_displacement_ci: Optional[str] = None
    engine_power_kw: Optional[str] = None
    fuel_type: Optional[str] = None
    body_class: Optional[str] = None
    drive_type: Optional[str] = None
    transmission_speeds: Optional[str] = None
    transmission_style: Optional[str] = None
    vehicle_type: Optional[str] = None
    is_valid: bool = False
    error_message: Optional[str] = None
    raw_data: Optional[Dict] = None

class VINDecoder:
    """VIN decoder using NHTSA API"""
    
    NHTSA_API_BASE = "https://vpic.nhtsa.dot.gov/api/vehicles"
    
    # Mapping of NHTSA API field names to our VehicleInfo attributes
    FIELD_MAPPING = {
        'Model Year': 'year',
        'Make': 'make',
        'Model': 'model',
        'Trim': 'trim',
        'Engine Model': 'engine_type',
        'Engine Number of Cylinders': 'engine_cylinders', 
        'Displacement (CC)': 'engine_displacement_cc',
        'Displacement (CI)': 'engine_displacement_ci',
        'Engine Power (kW)': 'engine_power_kw',
        'Fuel Type - Primary': 'fuel_type',
        'Body Class': 'body_class',
        'Drive Type': 'drive_type',
        'Number of Speeds': 'transmission_speeds',
        'Transmission Style': 'transmission_style',
        'Vehicle Type': 'vehicle_type'
    }
    
    @staticmethod
    def validate_vin(vin: str) -> Tuple[bool, str]:
        """
        Validate VIN format
        
        Args:
            vin: Vehicle Identification Number
            
        Returns:
            Tuple of (is_valid: bool, error_message: str)
        """
        if not vin:
            return False, "VIN cannot be empty"
        
        # Remove spaces and convert to uppercase
        vin = vin.replace(" ", "").upper()
        
        # Check length
        if len(vin) != 17:
            return False, "VIN must be exactly 17 characters long"
        
        # Check characters (letters and numbers, no I, O, Q)
        if not re.match(r'^[ABCDEFGHJKLMNPRSTUVWXYZ0-9]{17}$', vin):
            return False, "VIN contains invalid characters (I, O, Q not allowed)"
        
        return True, ""
    
    @staticmethod
    def decode_vin(vin: str, timeout: int = 10) -> VehicleInfo:
        """
        Decode VIN using NHTSA API
        
        Args:
            vin: Vehicle Identification Number
            timeout: Request timeout in seconds
            
        Returns:
            VehicleInfo object with decoded information
        """
        # Validate VIN first
        is_valid, error_msg = VINDecoder.validate_vin(vin)
        if not is_valid:
            return VehicleInfo(error_message=error_msg)
        
        # Clean VIN
        clean_vin = vin.replace(" ", "").upper()
        
        try:
            # Make API request
            url = f"{VINDecoder.NHTSA_API_BASE}/decodevin/{clean_vin}?format=json"
            response = requests.get(url, timeout=timeout)
            response.raise_for_status()
            
            data = response.json()
            
            # Check if API returned valid results
            if 'Results' not in data or not data['Results']:
                return VehicleInfo(error_message="No vehicle data found for this VIN")
            
            # Parse results
            vehicle_info = VehicleInfo(is_valid=True, raw_data=data)
            
            # Extract relevant fields
            for result in data['Results']:
                variable_name = result.get('Variable', '')
                value = result.get('Value', '')
                
                # Skip null or empty values
                if not value or value.lower() in ['null', 'not applicable', '']:
                    continue
                
                # Map to our VehicleInfo fields
                if variable_name in VINDecoder.FIELD_MAPPING:
                    field_name = VINDecoder.FIELD_MAPPING[variable_name]
                    setattr(vehicle_info, field_name, value)
            
            # Validate that we got essential information
            if not vehicle_info.year or not vehicle_info.make or not vehicle_info.model:
                vehicle_info.error_message = "Incomplete vehicle information from VIN"
                vehicle_info.is_valid = False
            
            return vehicle_info
            
        except requests.exceptions.Timeout:
            return VehicleInfo(error_message="Request timeout - NHTSA API is slow to respond")
        except requests.exceptions.ConnectionError:
            return VehicleInfo(error_message="Connection error - Check internet connection")
        except requests.exceptions.HTTPError as e:
            return VehicleInfo(error_message=f"API error: {e}")
        except requests.exceptions.RequestException as e:
            return VehicleInfo(error_message=f"Request failed: {e}")
        except Exception as e:
            return VehicleInfo(error_message=f"Unexpected error: {e}")

    @staticmethod
    def extract_performance_hints(vehicle_info: VehicleInfo) -> Dict[str, Any]:
        """
        Extract performance-related hints from decoded vehicle info
        
        Args:
            vehicle_info: Decoded vehicle information
            
        Returns:
            Dictionary with performance hints for PI calculation
        """
        hints = {}
        
        if not vehicle_info.is_valid:
            return hints
        
        # Engine displacement hints
        if vehicle_info.engine_displacement_cc:
            try:
                cc = float(vehicle_info.engine_displacement_cc)
                # Rough HP estimation from displacement (very rough!)
                estimated_hp = cc * 0.5  # This is a very rough estimation
                hints['estimated_hp_from_displacement'] = int(estimated_hp)
            except (ValueError, TypeError):
                pass
        
        # Cylinder count hints
        if vehicle_info.engine_cylinders:
            try:
                cylinders = int(vehicle_info.engine_cylinders)
                hints['engine_cylinders'] = cylinders
                
                # Weight hints based on vehicle type and cylinders
                if vehicle_info.body_class:
                    body_class = vehicle_info.body_class.lower()
                    if 'coupe' in body_class or 'convertible' in body_class:
                        hints['estimated_weight_range'] = (2800, 4000)
                    elif 'sedan' in body_class:
                        hints['estimated_weight_range'] = (3000, 4200)
                    elif 'suv' in body_class or 'truck' in body_class:
                        hints['estimated_weight_range'] = (4000, 6000)
                    elif 'hatch' in body_class:
                        hints['estimated_weight_range'] = (2500, 3500)
                        
            except (ValueError, TypeError):
                pass
        
        # Fuel type hints
        if vehicle_info.fuel_type:
            fuel_type = vehicle_info.fuel_type.lower()
            if 'premium' in fuel_type or 'high octane' in fuel_type:
                hints['performance_fuel'] = True
            elif 'electric' in fuel_type:
                hints['electric_vehicle'] = True
        
        # Drive type hints
        if vehicle_info.drive_type:
            drive_type = vehicle_info.drive_type.lower()
            if 'awd' in drive_type or '4wd' in drive_type:
                hints['all_wheel_drive'] = True
                # AWD cars typically heavier
                if 'estimated_weight_range' in hints:
                    min_w, max_w = hints['estimated_weight_range']
                    hints['estimated_weight_range'] = (min_w + 200, max_w + 300)
        
        return hints

    @staticmethod
    def get_vehicle_summary(vehicle_info: VehicleInfo) -> str:
        """
        Get a human-readable summary of the vehicle
        
        Args:
            vehicle_info: Decoded vehicle information
            
        Returns:
            String summary of the vehicle
        """
        if not vehicle_info.is_valid:
            return f"Invalid VIN: {vehicle_info.error_message}"
        
        summary_parts = []
        
        if vehicle_info.year:
            summary_parts.append(vehicle_info.year)
        if vehicle_info.make:
            summary_parts.append(vehicle_info.make)
        if vehicle_info.model:
            summary_parts.append(vehicle_info.model)
        if vehicle_info.trim:
            summary_parts.append(vehicle_info.trim)
        
        summary = " ".join(summary_parts)
        
        # Add engine info if available
        engine_parts = []
        if vehicle_info.engine_displacement_cc:
            try:
                cc = float(vehicle_info.engine_displacement_cc)
                liters = cc / 1000
                engine_parts.append(f"{liters:.1f}L")
            except (ValueError, TypeError):
                pass
        
        if vehicle_info.engine_cylinders:
            engine_parts.append(f"V{vehicle_info.engine_cylinders}")
        
        if engine_parts:
            summary += f" ({' '.join(engine_parts)})"
        
        return summary

# Convenience function for easy imports
def decode_vin(vin: str) -> VehicleInfo:
    """Convenience function to decode a VIN"""
    return VINDecoder.decode_vin(vin)