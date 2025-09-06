import streamlit as st

# Import our modular components
from config.settings import PAGE_CONFIG
from utils.styling import get_forza_css
from utils.pi_calculator import calculate_pi, get_performance_breakdown, determine_forza_class
from utils.data_manager import get_similar_cars
from components.ui_components import (
    render_header, render_vin_section, render_manual_input_section,
    render_results_section, render_performance_breakdown, 
    render_similar_cars_section, render_footer, render_sidebar
)

# Page config using settings
st.set_page_config(**PAGE_CONFIG)

# Apply custom CSS styling
st.markdown(get_forza_css(), unsafe_allow_html=True)

# Main Application Logic

# Header
st.markdown("""
<div class="main-header">
    <h1 class="main-title">🏎️ FORZA HORIZON</h1>
    <h2 class="main-subtitle">Performance Index Calculator</h2>
    <p class="main-subtitle">Estimate your real-world car's Forza PI rating and find similar cars in-game</p>
</div>
""", unsafe_allow_html=True)

# Create two columns for layout
col1, col2 = st.columns([2, 1])

with col1:
    # VIN Lookup Section
    st.markdown("""
    <div class="vin-section">
        <h3 class="section-title" style="color: #00bfff;">🔍 VIN Lookup (Coming Soon!)</h3>
        <p style="text-align: center; color: #ffffff; opacity: 0.8;">
            Enter your vehicle's VIN to automatically populate specifications
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    vin_input = st.text_input("Vehicle Identification Number (VIN)", placeholder="1HGCM82633A123456", help="17-character VIN from your vehicle")
    
    if st.button("🚀 Decode VIN", help="This feature is coming in Phase 2B!"):
        st.info("🚧 VIN decoding functionality will be added in the next update! For now, please use manual input below.")
    
    st.markdown("---")
    
    # Manual Input Section
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

with col2:
    # Results Section
    st.markdown("""
    <div class="input-section">
        <h3 class="section-title">📊 Performance Metrics</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Calculate PI using the existing formula
    pi = (
        (hp / 1500) * 200 +
        ((5000 - weight) / 5000) * 100 +
        (top_speed / 300) * 200 +
        ((10 - acceleration) / 10) * 200 +
        (handling / 1.5) * 200 +
        ((150 - braking) / 150) * 100
    )
    pi = round(min(max(pi, 100), 999))
    
    # Determine Forza class and color
    class_colors = {
        "D": ("class-d", "#8B4513"),
        "C": ("class-c", "#4169E1"), 
        "B": ("class-b", "#32CD32"),
        "A": ("class-a", "#FFD700"),
        "S1": ("class-s1", "#FF6347"),
        "S2": ("class-s2", "#FF1493"),
        "X": ("class-x", "#9400D3")
    }
    
    if pi < 300:
        forza_class = "D"
    elif pi < 400:
        forza_class = "C"
    elif pi < 500:
        forza_class = "B"
    elif pi < 600:
        forza_class = "A"
    elif pi < 700:
        forza_class = "S1"
    elif pi < 800:
        forza_class = "S2"
    else:
        forza_class = "X"
    
    class_css, class_color = class_colors[forza_class]
    
    # Display results
    st.markdown(f"""
    <div class="results-container">
        <p style="font-family: 'Rajdhani', sans-serif; font-size: 1.2rem; margin-bottom: 1rem; color: #ffffff;">Performance Index</p>
        <h1 class="pi-score">{pi}</h1>
        <p style="font-family: 'Rajdhani', sans-serif; font-size: 1.1rem; margin: 1rem 0; color: #ffffff;">Class Rating</p>
        <h2 class="forza-class {class_css}">{forza_class}</h2>
    </div>
    """, unsafe_allow_html=True)
    
    # Performance breakdown
    st.markdown("""
    <div class="input-section">
        <h4 style="color: #ff6b35; text-align: center; margin-bottom: 1rem;">Performance Breakdown</h4>
    </div>
    """, unsafe_allow_html=True)
    
    # Calculate individual contributions
    power_score = round((hp / 1500) * 200)
    weight_score = round(((5000 - weight) / 5000) * 100)
    speed_score = round((top_speed / 300) * 200)
    accel_score = round(((10 - acceleration) / 10) * 200)
    handling_score = round((handling / 1.5) * 200)
    braking_score = round(((150 - braking) / 150) * 100)
    
    # Display metrics in a grid
    st.markdown(f"""
    <div class="metric-container">
        <div class="metric-item">
            <div class="metric-label">Power</div>
            <div class="metric-value">{power_score}</div>
        </div>
        <div class="metric-item">
            <div class="metric-label">Weight</div>
            <div class="metric-value">{weight_score}</div>
        </div>
        <div class="metric-item">
            <div class="metric-label">Speed</div>
            <div class="metric-value">{speed_score}</div>
        </div>
    </div>
    <div class="metric-container">
        <div class="metric-item">
            <div class="metric-label">Acceleration</div>
            <div class="metric-value">{accel_score}</div>
        </div>
        <div class="metric-item">
            <div class="metric-label">Handling</div>
            <div class="metric-value">{handling_score}</div>
        </div>
        <div class="metric-item">
            <div class="metric-label">Braking</div>
            <div class="metric-value">{braking_score}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Similar Cars Section - This is the new Phase 2A feature!
st.markdown("""
<div class="similar-cars-section">
    <h3 class="section-title" style="color: #32CD32;">🚗 Similar Cars in Forza Horizon 5</h3>
    <p style="text-align: center; color: #ffffff; opacity: 0.9; margin-bottom: 1.5rem;">
        Cars in your PI class that you can drive in Forza Horizon 5
    </p>
</div>
""", unsafe_allow_html=True)

# Get similar cars based on calculated PI
similar_cars = get_similar_cars(pi, forza_class, 6)

# Display similar cars in a grid
if similar_cars:
    # Create two columns for car cards
    car_col1, car_col2 = st.columns(2)
    
    for i, car in enumerate(similar_cars):
        col = car_col1 if i % 2 == 0 else car_col2
        
        with col:
            # Determine PI difference and class color
            pi_diff = abs(car["pi"] - pi)
            car_class_css = class_colors.get(car["class"], ("", "#ffffff"))[0]
            
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

# Footer information
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

# Sidebar with additional info
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
        <p style="color: #32CD32; font-weight: bold;">🎉 Similar Cars: {len(similar_cars)} found in {forza_class} class!</p>
        <p style="color: #ff6b35; font-weight: bold;">Ready for Forza Horizon 6! 🚀</p>
    </div>
    """, unsafe_allow_html=True)