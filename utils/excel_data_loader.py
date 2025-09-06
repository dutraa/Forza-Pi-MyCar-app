# utils/excel_data_loader.py
"""
Excel data loader for real-world vehicle data
Loads and parses the provided Forza PI Calculator Excel file
"""

import pandas as pd
import os
from typing import List, Optional
from utils.real_world_data import RealWorldVehicle
from datetime import datetime

def load_excel_vehicle_data(file_path: str = "Real_Life_Forza_PI_Calculator.xlsx") -> List[RealWorldVehicle]:
    """Load vehicle data from the provided Excel file"""
    vehicles = []
    
    if not os.path.exists(file_path):
        print(f"Warning: Excel file not found at {file_path}")
        return vehicles
    
    try:
        # Read the Excel file without header first
        df_raw = pd.read_excel(file_path, header=None)
        
        # Find the header row (contains 'Year', 'Make', 'Model')
        header_row = None
        for i, row in df_raw.iterrows():
            if 'Year' in row.values and 'Make' in row.values and 'Model' in row.values:
                header_row = i
                break
        
        if header_row is None:
            print("Warning: Could not find header row in Excel file")
            return vehicles
        
        # Read again with proper header
        df = pd.read_excel(file_path, header=header_row)
        
        # Clean column names (remove extra spaces)
        df.columns = df.columns.str.strip()
        
        print(f"Found {len(df)} rows of data in Excel file")
        print(f"Columns: {list(df.columns)}")
        
        # Process each row
        for _, row in df.iterrows():
            try:
                # Skip rows with missing essential data
                if pd.isna(row.get('Year')) or pd.isna(row.get('Make')) or pd.isna(row.get('Model')):
                    continue
                
                # Convert and validate data
                year = int(row['Year']) if not pd.isna(row['Year']) else None
                make = str(row['Make']).strip() if not pd.isna(row['Make']) else None
                model = str(row['Model']).strip() if not pd.isna(row['Model']) else None
                
                if not year or not make or not model:
                    continue
                
                # Extract performance data
                hp = float(row['Horsepower']) if not pd.isna(row.get('Horsepower')) else None
                torque = float(row['Torque']) if not pd.isna(row.get('Torque')) else None
                weight = float(row['Weight (lbs)']) if not pd.isna(row.get('Weight (lbs)')) else None
                
                # Handle acceleration (0-60 time)
                accel_col = None
                for col in ['0–60 Time(MPH)', '0-60 Time(MPH)', '0-60 Time', '0–60 Time']:
                    if col in row and not pd.isna(row[col]):
                        accel_col = col
                        break
                
                acceleration = float(row[accel_col]) if accel_col and not pd.isna(row[accel_col]) else None
                
                # Handle top speed
                speed_col = None
                for col in ['Top Speed(MPH)', 'Top Speed (MPH)', 'Top Speed']:
                    if col in row and not pd.isna(row[col]):
                        speed_col = col
                        break
                
                top_speed = float(row[speed_col]) if speed_col and not pd.isna(row[speed_col]) else None
                
                # Handle braking distance
                braking_col = None
                for col in ['60-0 Distance(ft)', '60-0 Distance (ft)', 'Braking Distance']:
                    if col in row and not pd.isna(row[col]):
                        braking_col = col
                        break
                
                braking = float(row[braking_col]) if braking_col and not pd.isna(row[braking_col]) else None
                
                # Extract other data
                trim = str(row['Trim']).strip() if not pd.isna(row.get('Trim')) else None
                engine = str(row['Engine']).strip() if not pd.isna(row.get('Engine')) else None
                drivetrain = str(row['Drivetrain']).strip() if not pd.isna(row.get('Drivetrain')) else None
                
                # PI and class from Excel (if calculated)
                excel_pi = int(row['PI']) if not pd.isna(row.get('PI')) and str(row.get('PI')) != '#DIV/0!' else None
                excel_class = str(row['Class']).strip() if not pd.isna(row.get('Class')) else None
                
                # Create RealWorldVehicle object
                vehicle = RealWorldVehicle(
                    year=year,
                    make=make,
                    model=model,
                    trim=trim,
                    horsepower=hp,
                    torque_lbft=torque,
                    weight_lbs=weight,
                    top_speed_mph=top_speed,
                    acceleration_0_60=acceleration,
                    braking_60_0_ft=braking,
                    engine_type=engine,
                    drivetrain=drivetrain,
                    calculated_pi=excel_pi,
                    pi_source="excel_calculator" if excel_pi else None,
                    confidence_score=0.95 if all([hp, weight, top_speed, acceleration]) else 0.8,
                    data_source="excel_file",
                    last_updated=datetime.now().isoformat()
                )
                
                vehicles.append(vehicle)
                print(f"✅ Loaded: {year} {make} {model} - {hp}HP, {weight}lbs, PI: {excel_pi}")
                
            except Exception as e:
                print(f"Warning: Could not process row - {e}")
                continue
        
        print(f"Successfully loaded {len(vehicles)} vehicles from Excel file")
        return vehicles
        
    except Exception as e:
        print(f"Error reading Excel file: {e}")
        return vehicles

def integrate_excel_data_into_manager():
    """Load Excel data and integrate it with the RealWorldDataManager sample data"""
    from utils.real_world_data import RealWorldDataManager
    
    # Load Excel data
    excel_vehicles = load_excel_vehicle_data()
    
    if excel_vehicles:
        # Create manager and combine data
        manager = RealWorldDataManager()
        
        # Add Excel vehicles to the existing sample data
        all_vehicles = manager.vehicles_database + excel_vehicles
        
        # Remove duplicates (keep Excel data as priority)
        unique_vehicles = []
        seen_vehicles = set()
        
        # Process Excel vehicles first (higher priority)
        for vehicle in excel_vehicles:
            vehicle_key = (vehicle.year, vehicle.make.lower(), vehicle.model.lower())
            if vehicle_key not in seen_vehicles:
                unique_vehicles.append(vehicle)
                seen_vehicles.add(vehicle_key)
        
        # Add sample vehicles that don't conflict
        for vehicle in manager.vehicles_database:
            vehicle_key = (vehicle.year, vehicle.make.lower(), vehicle.model.lower())
            if vehicle_key not in seen_vehicles:
                unique_vehicles.append(vehicle)
                seen_vehicles.add(vehicle_key)
        
        # Update the manager's database
        manager.vehicles_database = unique_vehicles
        
        print(f"Integrated data: {len(unique_vehicles)} total vehicles ({len(excel_vehicles)} from Excel)")
        
        return manager
    else:
        print("No Excel data loaded, using default manager")
        return RealWorldDataManager()

if __name__ == "__main__":
    # Test the loader
    vehicles = load_excel_vehicle_data()
    print(f"Test run completed: {len(vehicles)} vehicles loaded")