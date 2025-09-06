# components/ui_components.py
"""
UI Components for Forza PI Calculator
Modular Streamlit UI components for the application
"""

import streamlit as st
from typing import Dict, List, Any, Tuple, Optional
from config.settings import CLASS_COLORS, UI_TEXT
from utils.pi_calculator import get_class_info
from utils.vin_decoder import VINDecoder, VehicleInfo
from utils.real_world_data import RealWorldDataManager, find_real_world_vehicle, calculate_enhanced_pi

def render_header():
    """Render the main application header"""
    st.markdown(f"""
    <div class="main-header">
        <h1 class="main-title">{UI_TEXT["app_title"]}</h1>
        <h2 class="main-subtitle">{UI_TEXT["app_subtitle"]}</h2>
        <p class="main-subtitle">{UI_TEXT["app_description"]}</p>
    </div>
    """, unsafe_allow_html=True)

def render_vin_section() -> Tuple[str, Optional[VehicleInfo]]:
    """Render VIN lookup section and return VIN input and decoded info"""
    st.markdown("""
    <div class="vin-section">
        <h3 class="section-title" style="color: #00bfff;">🔍 VIN Lookup</h3>
        <p style="text-align: center; color: #ffffff; opacity: 0.8;">
            Enter your vehicle's VIN to automatically get vehicle specifications
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    vin_input = st.text_input("Vehicle Identification Number (VIN)", 
                             placeholder="1HGCM82633A123456", 
                             help="17-character VIN from your vehicle")
    
    vehicle_info = None
    
    if st.button("🚀 Decode VIN", help="Get vehicle information from VIN"):
        if vin_input:
            with st.spinner("Decoding VIN..."):
                vehicle_info = VINDecoder.decode_vin(vin_input)
            
            if vehicle_info.is_valid:
                # Success - show vehicle info
                summary = VINDecoder.get_vehicle_summary(vehicle_info)
                st.success(f"✅ **Vehicle Found:** {summary}")
                
                # Show detailed info in expandable section
                with st.expander("📋 Detailed Vehicle Information"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        if vehicle_info.year:
                            st.write(f"**Year:** {vehicle_info.year}")
                        if vehicle_info.make:
                            st.write(f"**Make:** {vehicle_info.make}")
                        if vehicle_info.model:
                            st.write(f"**Model:** {vehicle_info.model}")
                        if vehicle_info.trim:
                            st.write(f"**Trim:** {vehicle_info.trim}")
                        if vehicle_info.body_class:
                            st.write(f"**Body:** {vehicle_info.body_class}")
                    
                    with col2:
                        if vehicle_info.engine_displacement_cc:
                            cc = vehicle_info.engine_displacement_cc
                            try:
                                liters = float(cc) / 1000
                                st.write(f"**Engine:** {liters:.1f}L ({cc}cc)")
                            except:
                                st.write(f"**Engine:** {cc}cc")
                        if vehicle_info.engine_cylinders:
                            st.write(f"**Cylinders:** {vehicle_info.engine_cylinders}")
                        if vehicle_info.fuel_type:
                            st.write(f"**Fuel:** {vehicle_info.fuel_type}")
                        if vehicle_info.drive_type:
                            st.write(f"**Drive:** {vehicle_info.drive_type}")
                        if vehicle_info.transmission_style:
                            st.write(f"**Transmission:** {vehicle_info.transmission_style}")
                
                # Show performance hints
                hints = VINDecoder.extract_performance_hints(vehicle_info)
                if hints:
                    st.info("💡 **Performance Hints:** Use the manual input section below. We found some hints that might help with estimates!")
                    
            else:
                # Error - show error message
                st.error(f"❌ **VIN Decode Failed:** {vehicle_info.error_message}")
                st.info("💡 Please use the manual input section below to enter your vehicle specifications.")
        else:
            st.warning("⚠️ Please enter a VIN to decode.")
    
    return vin_input, vehicle_info

def render_manual_input_section(vehicle_info: Optional[VehicleInfo] = None) -> Tuple[float, float, float, float, float, float]:
    """Render manual input section and return vehicle specifications"""
    st.markdown("---")
    
    st.markdown("""
    <div class="input-section">
        <h3 class="section-title">⚙️ Manual Vehicle Specifications</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Get performance hints if VIN was decoded
    hints = {}
    if vehicle_info and vehicle_info.is_valid:
        hints = VINDecoder.extract_performance_hints(vehicle_info)
        if hints:
            st.markdown("""
            <div style="background: linear-gradient(45deg, rgba(255, 170, 0, 0.1) 0%, rgba(255, 107, 53, 0.1) 100%); 
                        border: 2px solid #ffaa00; border-radius: 12px; padding: 1rem; margin-bottom: 1rem;">
                <h4 style="color: #ffaa00; text-align: center; margin-bottom: 0.5rem;">💡 Performance Hints from VIN</h4>
                <p style="color: #ffffff; text-align: center; opacity: 0.9; font-size: 0.9rem;">
                    We've detected some vehicle characteristics that might help with your estimates below.
                </p>
            </div>
            """, unsafe_allow_html=True)
    
    # Create sub-columns for input fields
    input_col1, input_col2 = st.columns(2)
    
    # Widget constraints (min_value, max_value, default)
    HP_MIN, HP_MAX, HP_DEFAULT = 50, 2000, 300
    WEIGHT_MIN, WEIGHT_MAX, WEIGHT_DEFAULT = 1000, 8000, 3500
    SPEED_MIN, SPEED_MAX, SPEED_DEFAULT = 60, 300, 150
    ACCEL_MIN, ACCEL_MAX, ACCEL_DEFAULT = 2.0, 15.0, 5.0
    HANDLING_MIN, HANDLING_MAX, HANDLING_DEFAULT = 0.5, 2.0, 1.0
    BRAKING_MIN, BRAKING_MAX, BRAKING_DEFAULT = 80, 200, 120
    
    # Default values and hints
    default_hp = HP_DEFAULT
    default_weight = WEIGHT_DEFAULT
    hp_help = "Engine horsepower (HP)"
    weight_help = "Vehicle curb weight in pounds"
    
    # Apply hints if available with proper validation
    clamped_values = []
    if hints:
        if 'estimated_hp_from_displacement' in hints:
            estimated_hp = hints['estimated_hp_from_displacement']
            # Clamp to valid range
            default_hp = max(HP_MIN, min(HP_MAX, estimated_hp))
            
            if estimated_hp > HP_MAX:
                hp_help += f" (Hint: Estimated {estimated_hp} HP from engine - clamped to max {HP_MAX} HP)"
                clamped_values.append(f"HP: {estimated_hp} → {HP_MAX}")
            elif estimated_hp < HP_MIN:
                hp_help += f" (Hint: Estimated {estimated_hp} HP from engine - adjusted to min {HP_MIN} HP)"
                clamped_values.append(f"HP: {estimated_hp} → {HP_MIN}")
            else:
                hp_help += f" (Hint: ~{default_hp} HP estimated from engine size)"
        
        if 'estimated_weight_range' in hints:
            min_w, max_w = hints['estimated_weight_range']
            estimated_weight = int((min_w + max_w) / 2)
            
            # Clamp to valid range
            default_weight = max(WEIGHT_MIN, min(WEIGHT_MAX, estimated_weight))
            
            if estimated_weight > WEIGHT_MAX:
                weight_help += f" (Hint: Estimated {estimated_weight:,} lbs - clamped to max {WEIGHT_MAX:,} lbs)"
                clamped_values.append(f"Weight: {estimated_weight:,} → {WEIGHT_MAX:,}")
            elif estimated_weight < WEIGHT_MIN:
                weight_help += f" (Hint: Estimated {estimated_weight:,} lbs - adjusted to min {WEIGHT_MIN:,} lbs)"
                clamped_values.append(f"Weight: {estimated_weight:,} → {WEIGHT_MIN:,}")
            else:
                weight_help += f" (Hint: Typical range {min_w:,}-{max_w:,} lbs for this vehicle type)"
    
    # Show clamped values warning if any
    if clamped_values:
        st.warning(f"⚠️ **Values Adjusted:** Some estimates exceeded limits and were adjusted: {', '.join(clamped_values)}")
    
    with input_col1:
        hp = st.number_input("🔥 Horsepower (HP)", 
                           value=default_hp, 
                           step=10, 
                           min_value=HP_MIN, 
                           max_value=HP_MAX,
                           help=hp_help)
        
        weight = st.number_input("⚖️ Weight (lbs)", 
                               value=default_weight, 
                               step=50, 
                               min_value=WEIGHT_MIN, 
                               max_value=WEIGHT_MAX,
                               help=weight_help)
        
        top_speed = st.number_input("💨 Top Speed (mph)", 
                                  value=SPEED_DEFAULT, 
                                  step=5, 
                                  min_value=SPEED_MIN, 
                                  max_value=SPEED_MAX,
                                  help="Maximum speed in miles per hour")
    
    with input_col2:
        acceleration = st.number_input("⏱️ 0-60 mph Time (seconds)", 
                                     value=ACCEL_DEFAULT, 
                                     step=0.1, 
                                     min_value=ACCEL_MIN, 
                                     max_value=ACCEL_MAX,
                                     help="Time to accelerate from 0 to 60 mph")
        
        handling = st.number_input("🌀 Handling G-Force", 
                                 value=HANDLING_DEFAULT, 
                                 step=0.01, 
                                 min_value=HANDLING_MIN, 
                                 max_value=HANDLING_MAX,
                                 help="Maximum lateral G-force in cornering")
        
        braking = st.number_input("🛑 Braking Distance 60-0 (feet)", 
                                value=BRAKING_DEFAULT, 
                                step=5, 
                                min_value=BRAKING_MIN, 
                                max_value=BRAKING_MAX,
                                help="Distance to stop from 60 mph to 0")
    
    # Show additional VIN info if available
    if vehicle_info and vehicle_info.is_valid and hints:
        with st.expander("🔧 Additional Vehicle Details"):
            if 'engine_cylinders' in hints:
                st.write(f"**Engine Configuration:** {hints['engine_cylinders']} cylinders")
            
            if 'performance_fuel' in hints:
                st.write("**Fuel Type:** Premium/High Octane (Performance oriented)")
            
            if 'electric_vehicle' in hints:
                st.write("**Powertrain:** Electric Vehicle")
            
            if 'all_wheel_drive' in hints:
                st.write("**Drive Type:** All-Wheel Drive (Added weight and traction)")
    
    return hp, weight, top_speed, acceleration, handling, braking

def render_results_section(pi: int, forza_class: str):
    """Render the PI results section"""
    st.markdown("""
    <div class="input-section">
        <h3 class="section-title">📊 Performance Metrics</h3>
    </div>
    """, unsafe_allow_html=True)
    
    class_css, class_color = get_class_info(forza_class)
    
    # Display results
    st.markdown(f"""
    <div class="results-container">
        <p style="font-family: 'Rajdhani', sans-serif; font-size: 1.2rem; margin-bottom: 1rem; color: #ffffff;">Performance Index</p>
        <h1 class="pi-score">{pi}</h1>
        <p style="font-family: 'Rajdhani', sans-serif; font-size: 1.1rem; margin: 1rem 0; color: #ffffff;">Class Rating</p>
        <h2 class="forza-class {class_css}">{forza_class}</h2>
    </div>
    """, unsafe_allow_html=True)

def render_performance_breakdown(breakdown: Dict[str, int]):
    """Render performance breakdown metrics"""
    st.markdown("""
    <div class="input-section">
        <h4 style="color: #ff6b35; text-align: center; margin-bottom: 1rem;">Performance Breakdown</h4>
    </div>
    """, unsafe_allow_html=True)
    
    # Display metrics in a grid
    st.markdown(f"""
    <div class="metric-container">
        <div class="metric-item">
            <div class="metric-label">Power</div>
            <div class="metric-value">{breakdown['power']}</div>
        </div>
        <div class="metric-item">
            <div class="metric-label">Weight</div>
            <div class="metric-value">{breakdown['weight']}</div>
        </div>
        <div class="metric-item">
            <div class="metric-label">Speed</div>
            <div class="metric-value">{breakdown['speed']}</div>
        </div>
    </div>
    <div class="metric-container">
        <div class="metric-item">
            <div class="metric-label">Acceleration</div>
            <div class="metric-value">{breakdown['acceleration']}</div>
        </div>
        <div class="metric-item">
            <div class="metric-label">Handling</div>
            <div class="metric-value">{breakdown['handling']}</div>
        </div>
        <div class="metric-item">
            <div class="metric-label">Braking</div>
            <div class="metric-value">{breakdown['braking']}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_similar_cars_section(similar_cars: List[Dict[str, Any]], pi: int, forza_class: str):
    """Render similar cars section"""
    st.markdown("""
    <div class="similar-cars-section">
        <h3 class="section-title" style="color: #32CD32;">🚗 Similar Cars in Forza Horizon 5</h3>
        <p style="text-align: center; color: #ffffff; opacity: 0.9; margin-bottom: 1.5rem;">
            Cars in your PI class that you can drive in Forza Horizon 5
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Display similar cars in a grid
    if similar_cars:
        # Create two columns for car cards
        car_col1, car_col2 = st.columns(2)
        
        for i, car in enumerate(similar_cars):
            col = car_col1 if i % 2 == 0 else car_col2
            
            with col:
                # Determine PI difference and class color
                pi_diff = abs(car["pi"] - pi)
                car_class_css = CLASS_COLORS.get(car["class"], {"css": "", "color": "#ffffff"})["css"]
                
                st.markdown(f"""
                <div class="car-card">
                    <div class="car-name">{car['year']} {car['make']} {car['model']}</div>
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                        <div class="car-pi {car_class_css}">PI: {car['pi']}</div>
                        <div style="color: #32CD32; font-family: 'Orbitron', monospace; font-weight: 600;">
                            Class {car['class']}
                        </div>
                    </div>
                    <div class="car-details">
                        {car['hp']} HP • {car['weight']:,} lbs • {car['type']}<br>
                        <small style="color: #ffaa00;">±{pi_diff} PI from your car</small>
                    </div>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.info("No similar cars found in the database. Try adjusting your vehicle specifications.")

def render_footer():
    """Render application footer"""
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; padding: 2rem; opacity: 0.8;">
        <p style="font-family: 'Rajdhani', sans-serif; color: #ffffff;">
            🏁 Forza Horizon PI Calculator • Built for FH6 Hype • 
            <a href="https://forza.fandom.com/wiki/Performance_Index" target="_blank" style="color: #ff6b35;">Learn about PI</a>
        </p>
        <p style="font-family: 'Rajdhani', sans-serif; color: #ffffff; font-size: 0.9rem;">
            Performance Index ranges: D (100-299) • C (300-399) • B (400-499) • A (500-599) • S1 (600-699) • S2 (700-799) • X (800-999)
        </p>
        <p style="font-family: 'Rajdhani', sans-serif; color: #32CD32; font-size: 0.9rem;">
            ✨ <strong>NEW:</strong> Similar Cars feature shows real Forza Horizon 5 vehicles you can drive in-game!
        </p>
    </div>
    """, unsafe_allow_html=True)

def render_sidebar(similar_cars_count: int, forza_class: str, vehicle_info: Optional[VehicleInfo] = None):
    """Render sidebar with application information"""
    with st.sidebar:
        st.markdown("""
        <div style="text-align: center; padding: 1rem;">
            <h2 style="color: #ff6b35; font-family: 'Orbitron', monospace;">🏎️ About PI</h2>
        </div>
        """, unsafe_allow_html=True)
        
        # Show VIN vehicle info if available
        if vehicle_info and vehicle_info.is_valid:
            st.markdown("""
            <div style="background: linear-gradient(45deg, rgba(0, 191, 255, 0.1) 0%, rgba(30, 144, 255, 0.1) 100%); 
                        border: 2px solid #00bfff; border-radius: 12px; padding: 1rem; margin-bottom: 1rem;">
                <h4 style="color: #00bfff; text-align: center; margin-bottom: 0.5rem;">🚗 Your Vehicle</h4>
            </div>
            """, unsafe_allow_html=True)
            
            summary = VINDecoder.get_vehicle_summary(vehicle_info)
            st.write(f"**{summary}**")
            
            if vehicle_info.body_class:
                st.write(f"Type: {vehicle_info.body_class}")
            if vehicle_info.drive_type:
                st.write(f"Drive: {vehicle_info.drive_type}")
            
            st.markdown("---")
        
        st.markdown("""
        **Performance Index (PI)** is Forza's way of rating vehicle performance on a scale from 100-999.
        
        **Class Breakdown:**
        - **D Class**: Entry-level vehicles
        - **C Class**: Street cars  
        - **B Class**: Performance cars
        - **A Class**: Sports cars
        - **S1 Class**: Supercars
        - **S2 Class**: Hypercars
        - **X Class**: Extreme builds
        
        **✨ Phase 2B Complete:**
        - 🔍 **VIN decoding** with NHTSA API
        - 🚗 Similar Cars feature
        - 📊 Real FH5 car database
        - 🎯 PI-based matching
        
        **Coming Soon:**
        - 🌐 Real-world performance database
        - 🎨 Enhanced PI algorithms
        - 📱 Mobile optimization
        - 🆚 Car comparison tools
        """)
        
        st.markdown("---")
        st.markdown(f"""
        <div style="text-align: center;">
            <p style="color: #32CD32; font-weight: bold;">🎉 Similar Cars: {similar_cars_count} found in {forza_class} class!</p>
            <p style="color: #ff6b35; font-weight: bold;">Ready for Forza Horizon 6! 🚀</p>
        </div>
        """, unsafe_allow_html=True)