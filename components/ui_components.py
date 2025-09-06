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

def render_header():
    """Render the main application header"""
    st.markdown(f"""
    <div class="main-header">
        <h1 class="main-title">{UI_TEXT["app_title"]}</h1>
        <h2 class="main-subtitle">{UI_TEXT["app_subtitle"]}</h2>
        <p class="main-subtitle">{UI_TEXT["app_description"]}</p>
    </div>
    """, unsafe_allow_html=True)

def render_vin_section() -> str:
    """Render VIN lookup section and return VIN input"""
    st.markdown("""
    <div class="vin-section">
        <h3 class="section-title" style="color: #00bfff;">🔍 VIN Lookup (Coming Soon!)</h3>
        <p style="text-align: center; color: #ffffff; opacity: 0.8;">
            Enter your vehicle's VIN to automatically populate specifications
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    vin_input = st.text_input("Vehicle Identification Number (VIN)", 
                             placeholder="1HGCM82633A123456", 
                             help="17-character VIN from your vehicle")
    
    if st.button("🚀 Decode VIN", help="This feature is coming in Phase 2B!"):
        st.info("🚧 VIN decoding functionality will be added in the next update! For now, please use manual input below.")
    
    return vin_input

def render_manual_input_section() -> Tuple[float, float, float, float, float, float]:
    """Render manual input section and return vehicle specifications"""
    st.markdown("---")
    
    st.markdown("""
    <div class="input-section">
        <h3 class="section-title">⚙️ Manual Vehicle Specifications</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Create sub-columns for input fields
    input_col1, input_col2 = st.columns(2)
    
    with input_col1:
        hp = st.number_input("🔥 Horsepower (HP)", value=300, step=10, min_value=50, max_value=2000)
        weight = st.number_input("⚖️ Weight (lbs)", value=3500, step=50, min_value=1000, max_value=8000)
        top_speed = st.number_input("💨 Top Speed (mph)", value=150, step=5, min_value=60, max_value=300)
    
    with input_col2:
        acceleration = st.number_input("⏱️ 0-60 mph Time (seconds)", value=5.0, step=0.1, min_value=2.0, max_value=15.0)
        handling = st.number_input("🌀 Handling G-Force", value=1.0, step=0.01, min_value=0.5, max_value=2.0)
        braking = st.number_input("🛑 Braking Distance 60-0 (feet)", value=120, step=5, min_value=80, max_value=200)
    
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

def render_sidebar(similar_cars_count: int, forza_class: str):
    """Render sidebar with application information"""
    with st.sidebar:
        st.markdown("""
        <div style="text-align: center; padding: 1rem;">
            <h2 style="color: #ff6b35; font-family: 'Orbitron', monospace;">🏎️ About PI</h2>
        </div>
        """, unsafe_allow_html=True)
        
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
        
        **✨ Phase 2A Complete:**
        - 🚗 Similar Cars feature
        - 📊 Real FH5 car database
        - 🎯 PI-based matching
        
        **Coming Soon:**
        - 🔍 VIN lookup integration
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