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

def render_vin_section() -> Tuple[str, Optional[VehicleInfo], Optional[Any]]:
    """Render VIN lookup section and return VIN input, decoded info, and real-world data"""
    st.markdown("""
    <div class="vin-section">
        <h3 class="section-title" style="color: #00bfff;">🔍 VIN Lookup & Real-World Data</h3>
        <p style="text-align: center; color: #ffffff; opacity: 0.8;">
            Enter your vehicle's VIN to get specifications and enhanced PI calculations
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    vin_input = st.text_input("Vehicle Identification Number (VIN)", 
                             placeholder="1HGCM82633A123456", 
                             help="17-character VIN from your vehicle")
    
    vehicle_info = None
    real_world_vehicle = None
    
    if st.button("🚀 Decode VIN & Find Real-World Data", help="Get complete vehicle information and enhanced PI calculation"):
        if vin_input:
            with st.spinner("Decoding VIN..."):
                vehicle_info = VINDecoder.decode_vin(vin_input)
            
            if vehicle_info.is_valid:
                # Success - show vehicle info
                summary = VINDecoder.get_vehicle_summary(vehicle_info)
                st.success(f"✅ **Vehicle Found:** {summary}")
                
                # Try to find real-world data match
                with st.spinner("Searching real-world database..."):
                    if vehicle_info.year and vehicle_info.make and vehicle_info.model:
                        try:
                            year = int(vehicle_info.year)
                            real_world_vehicle = find_real_world_vehicle(
                                year, vehicle_info.make, vehicle_info.model, vehicle_info.trim
                            )
                        except ValueError:
                            pass
                
                # Show VIN decode results
                with st.expander("📋 VIN Decode Results"):
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
                
                # Show real-world data if found
                if real_world_vehicle:
                    st.success("🎯 **Real-World Performance Data Found!**")
                    
                    with st.expander("🏁 Real-World Performance Specifications"):
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.write(f"**Horsepower:** {real_world_vehicle.horsepower} HP")
                            st.write(f"**Torque:** {real_world_vehicle.torque_lbft} lb-ft")
                            st.write(f"**Weight:** {real_world_vehicle.weight_lbs:,.0f} lbs")
                            st.write(f"**0-60 mph:** {real_world_vehicle.acceleration_0_60} sec")
                        
                        with col2:
                            st.write(f"**Top Speed:** {real_world_vehicle.top_speed_mph} mph")
                            if real_world_vehicle.handling_g_force:
                                st.write(f"**Handling:** {real_world_vehicle.handling_g_force} G")
                            if real_world_vehicle.braking_60_0_ft:
                                st.write(f"**Braking 60-0:** {real_world_vehicle.braking_60_0_ft} ft")
                            st.write(f"**Drivetrain:** {real_world_vehicle.drivetrain}")
                    
                    # Calculate enhanced PI
                    enhanced_pi, confidence = calculate_enhanced_pi(real_world_vehicle)
                    
                    st.markdown(f"""
                    <div style="background: linear-gradient(45deg, rgba(50, 205, 50, 0.1) 0%, rgba(34, 139, 34, 0.1) 100%); 
                                border: 2px solid #32CD32; border-radius: 12px; padding: 1rem; margin: 1rem 0;">
                        <h4 style="color: #32CD32; text-align: center; margin-bottom: 0.5rem;">
                            🎯 Enhanced PI Calculation
                        </h4>
                        <div style="text-align: center;">
                            <div style="font-size: 2rem; color: #ffaa00; font-weight: bold;">
                                {enhanced_pi} PI
                            </div>
                            <div style="color: #ffffff; opacity: 0.9;">
                                Confidence: {confidence:.1%} • Real-world data enhanced
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                else:
                    st.info("💡 **Real-world data not found** for this specific vehicle. Using VIN-based estimates for manual input.")
                
                # Show performance hints
                hints = VINDecoder.extract_performance_hints(vehicle_info)
                if hints and not real_world_vehicle:
                    st.info("💡 **Performance Hints Available:** Use the manual input section below with VIN-based estimates!")
                    
            else:
                # Error - show error message
                st.error(f"❌ **VIN Decode Failed:** {vehicle_info.error_message}")
                st.info("💡 Please use the manual input section below to enter your vehicle specifications.")
        else:
            st.warning("⚠️ Please enter a VIN to decode.")
    
    return vin_input, vehicle_info, real_world_vehicle

def render_manual_input_section(vehicle_info: Optional[VehicleInfo] = None, 
                               real_world_vehicle: Optional[Any] = None) -> Tuple[float, float, float, float, float, float]:
    """Render manual input section and return vehicle specifications"""
    st.markdown("---")
    
    # Determine data source and title
    if real_world_vehicle:
        section_title = "🎯 Real-World Enhanced Specifications"
        section_desc = "Pre-filled with authentic real-world data for your vehicle"
    elif vehicle_info and vehicle_info.is_valid:
        section_title = "💡 VIN-Enhanced Manual Input"
        section_desc = "Pre-filled with VIN-based intelligent estimates"
    else:
        section_title = "⚙️ Manual Vehicle Specifications"
        section_desc = "Enter your vehicle's performance specifications"
    
    st.markdown(f"""
    <div class="input-section">
        <h3 class="section-title">{section_title}</h3>
        <p style="text-align: center; color: #ffffff; opacity: 0.8; margin-bottom: 1rem;">
            {section_desc}
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Widget constraints (min_value, max_value, default)
    HP_MIN, HP_MAX, HP_DEFAULT = 50, 2000, 300
    WEIGHT_MIN, WEIGHT_MAX, WEIGHT_DEFAULT = 1000, 8000, 3500
    SPEED_MIN, SPEED_MAX, SPEED_DEFAULT = 60, 300, 150
    ACCEL_MIN, ACCEL_MAX, ACCEL_DEFAULT = 2.0, 15.0, 5.0
    HANDLING_MIN, HANDLING_MAX, HANDLING_DEFAULT = 0.5, 2.0, 1.0
    BRAKING_MIN, BRAKING_MAX, BRAKING_DEFAULT = 80, 200, 120
    
    # Default values
    default_hp = HP_DEFAULT
    default_weight = WEIGHT_DEFAULT
    default_speed = SPEED_DEFAULT
    default_accel = ACCEL_DEFAULT
    default_handling = HANDLING_DEFAULT
    default_braking = BRAKING_DEFAULT
    
    hp_help = "Engine horsepower (HP)"
    weight_help = "Vehicle curb weight in pounds"
    speed_help = "Maximum speed in miles per hour"
    accel_help = "Time to accelerate from 0 to 60 mph"
    handling_help = "Maximum lateral G-force in cornering"
    braking_help = "Distance to stop from 60 mph to 0"
    
    # Data source indicator
    data_source = "manual"
    clamped_values = []
    
    # Apply real-world data if available (highest priority)
    if real_world_vehicle:
        data_source = "real_world"
        
        if real_world_vehicle.horsepower:
            default_hp = max(HP_MIN, min(HP_MAX, int(real_world_vehicle.horsepower)))
            hp_help = f"Real-world spec: {real_world_vehicle.horsepower} HP"
            if real_world_vehicle.horsepower > HP_MAX:
                clamped_values.append(f"HP: {real_world_vehicle.horsepower} → {HP_MAX}")
        
        if real_world_vehicle.weight_lbs:
            default_weight = max(WEIGHT_MIN, min(WEIGHT_MAX, int(real_world_vehicle.weight_lbs)))
            weight_help = f"Real-world spec: {real_world_vehicle.weight_lbs:,.0f} lbs"
        
        if real_world_vehicle.top_speed_mph:
            default_speed = max(SPEED_MIN, min(SPEED_MAX, int(real_world_vehicle.top_speed_mph)))
            speed_help = f"Real-world spec: {real_world_vehicle.top_speed_mph} mph"
        
        if real_world_vehicle.acceleration_0_60:
            default_accel = max(ACCEL_MIN, min(ACCEL_MAX, real_world_vehicle.acceleration_0_60))
            accel_help = f"Real-world spec: {real_world_vehicle.acceleration_0_60} sec"
        
        if real_world_vehicle.handling_g_force:
            default_handling = max(HANDLING_MIN, min(HANDLING_MAX, real_world_vehicle.handling_g_force))
            handling_help = f"Real-world spec: {real_world_vehicle.handling_g_force} G"
        
        if real_world_vehicle.braking_60_0_ft:
            default_braking = max(BRAKING_MIN, min(BRAKING_MAX, int(real_world_vehicle.braking_60_0_ft)))
            braking_help = f"Real-world spec: {real_world_vehicle.braking_60_0_ft} ft"
        
        st.success("🎯 **Using Real-World Performance Data** - These values are from authentic vehicle specifications!")
    
    # Apply VIN hints if real-world data not available
    elif vehicle_info and vehicle_info.is_valid:
        data_source = "vin_hints"
        hints = VINDecoder.extract_performance_hints(vehicle_info)
        
        if hints:
            if 'estimated_hp_from_displacement' in hints:
                estimated_hp = hints['estimated_hp_from_displacement']
                default_hp = max(HP_MIN, min(HP_MAX, estimated_hp))
                
                if estimated_hp > HP_MAX:
                    hp_help += f" (VIN hint: {estimated_hp} HP - clamped to max {HP_MAX} HP)"
                    clamped_values.append(f"HP: {estimated_hp} → {HP_MAX}")
                else:
                    hp_help += f" (VIN hint: ~{default_hp} HP from engine size)"
            
            if 'estimated_weight_range' in hints:
                min_w, max_w = hints['estimated_weight_range']
                estimated_weight = int((min_w + max_w) / 2)
                default_weight = max(WEIGHT_MIN, min(WEIGHT_MAX, estimated_weight))
                weight_help += f" (VIN hint: {min_w:,}-{max_w:,} lbs range)"
            
            st.info("💡 **Using VIN-Based Estimates** - Adjust these values based on your vehicle's actual performance.")
    
    # Show clamped values warning if any
    if clamped_values:
        st.warning(f"⚠️ **Values Adjusted:** {', '.join(clamped_values)}")
    
    # Create sub-columns for input fields
    input_col1, input_col2 = st.columns(2)
    
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
                                  value=default_speed, 
                                  step=5, 
                                  min_value=SPEED_MIN, 
                                  max_value=SPEED_MAX,
                                  help=speed_help)
    
    with input_col2:
        acceleration = st.number_input("⏱️ 0-60 mph Time (seconds)", 
                                     value=default_accel, 
                                     step=0.1, 
                                     min_value=ACCEL_MIN, 
                                     max_value=ACCEL_MAX,
                                     help=accel_help)
        
        handling = st.number_input("🌀 Handling G-Force", 
                                 value=default_handling, 
                                 step=0.01, 
                                 min_value=HANDLING_MIN, 
                                 max_value=HANDLING_MAX,
                                 help=handling_help)
        
        braking = st.number_input("🛑 Braking Distance 60-0 (feet)", 
                                value=default_braking, 
                                step=5, 
                                min_value=BRAKING_MIN, 
                                max_value=BRAKING_MAX,
                                help=braking_help)
    
    # Show data source info
    if data_source == "real_world":
        confidence_score = getattr(real_world_vehicle, 'confidence_score', 0.9)
        st.markdown(f"""
        <div style="background: rgba(50, 205, 50, 0.1); border-left: 4px solid #32CD32; padding: 0.5rem; margin: 1rem 0;">
            <small style="color: #32CD32;">
                📊 <strong>Data Source:</strong> Real-world specifications 
                | <strong>Confidence:</strong> {confidence_score:.1%}
                | <strong>Last Updated:</strong> {getattr(real_world_vehicle, 'last_updated', 'Unknown')[:10]}
            </small>
        </div>
        """, unsafe_allow_html=True)
    elif data_source == "vin_hints":
        st.markdown(f"""
        <div style="background: rgba(255, 170, 0, 0.1); border-left: 4px solid #ffaa00; padding: 0.5rem; margin: 1rem 0;">
            <small style="color: #ffaa00;">
                🔍 <strong>Data Source:</strong> VIN-based estimates from NHTSA database
            </small>
        </div>
        """, unsafe_allow_html=True)
    
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