import streamlit as st
import requests
import json

# Page config with Forza-inspired theming
st.set_page_config(
    page_title="Forza Horizon PI Calculator",
    page_icon="🏎️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Forza Horizon theming
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@300;400;600;700&display=swap');
    
    /* Main app styling */
    .stApp {
        background: linear-gradient(135deg, #0d1421 0%, #1a2332 50%, #0d1421 100%);
        color: #ffffff;
    }
    
    /* Header styling */
    .main-header {
        background: linear-gradient(90deg, #ff6b35 0%, #f7931e 50%, #ffaa00 100%);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px rgba(255, 107, 53, 0.3);
        text-align: center;
    }
    
    .main-title {
        font-family: 'Orbitron', monospace;
        font-weight: 900;
        font-size: 3.5rem;
        color: #ffffff;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
        margin-bottom: 0.5rem;
    }
    
    .main-subtitle {
        font-family: 'Rajdhani', sans-serif;
        font-weight: 400;
        font-size: 1.2rem;
        color: #ffffff;
        opacity: 0.9;
    }
    
    /* Input sections */
    .input-section {
        background: rgba(26, 35, 50, 0.8);
        padding: 1.5rem;
        border-radius: 12px;
        border: 2px solid rgba(255, 107, 53, 0.3);
        margin-bottom: 1rem;
        backdrop-filter: blur(10px);
    }
    
    .section-title {
        font-family: 'Orbitron', monospace;
        font-weight: 700;
        font-size: 1.8rem;
        color: #ff6b35;
        margin-bottom: 1rem;
        text-align: center;
    }
    
    /* Results styling */
    .results-container {
        background: linear-gradient(135deg, rgba(255, 107, 53, 0.1) 0%, rgba(247, 147, 30, 0.1) 100%);
        padding: 2rem;
        border-radius: 15px;
        border: 3px solid #ff6b35;
        text-align: center;
        margin: 2rem 0;
        box-shadow: 0 0 30px rgba(255, 107, 53, 0.4);
    }
    
    .pi-score {
        font-family: 'Orbitron', monospace;
        font-weight: 900;
        font-size: 4rem;
        color: #ffaa00;
        text-shadow: 0 0 20px rgba(255, 170, 0, 0.6);
        margin: 0;
    }
    
    .forza-class {
        font-family: 'Orbitron', monospace;
        font-weight: 700;
        font-size: 2.5rem;
        color: #ff6b35;
        text-shadow: 0 0 15px rgba(255, 107, 53, 0.6);
        margin: 0.5rem 0;
    }
    
    /* Class-specific colors */
    .class-d { color: #8B4513 !important; }
    .class-c { color: #4169E1 !important; }
    .class-b { color: #32CD32 !important; }
    .class-a { color: #FFD700 !important; }
    .class-s1 { color: #FF6347 !important; }
    .class-s2 { color: #FF1493 !important; }
    .class-x { color: #9400D3 !important; }
    
    /* VIN section */
    .vin-section {
        background: linear-gradient(45deg, rgba(0, 191, 255, 0.1) 0%, rgba(30, 144, 255, 0.1) 100%);
        border: 2px solid #00bfff;
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 2rem;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(45deg, #ff6b35 0%, #f7931e 100%);
        color: white;
        border: none;
        border-radius: 8px;
        font-family: 'Rajdhani', sans-serif;
        font-weight: 600;
        font-size: 1.1rem;
        padding: 0.7rem 2rem;
        box-shadow: 0 4px 15px rgba(255, 107, 53, 0.4);
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(255, 107, 53, 0.6);
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #1a2332 0%, #0d1421 100%);
    }
    
    /* Input field styling */
    .stNumberInput > div > div > input {
        background-color: rgba(26, 35, 50, 0.8);
        color: #ffffff;
        border: 2px solid rgba(255, 107, 53, 0.5);
        border-radius: 8px;
    }
    
    .stTextInput > div > div > input {
        background-color: rgba(26, 35, 50, 0.8);
        color: #ffffff;
        border: 2px solid rgba(0, 191, 255, 0.5);
        border-radius: 8px;
    }
    
    /* Input labels styling - Fix for dark labels */
    .stNumberInput label, .stTextInput label {
        color: #ffffff !important;
        font-weight: 600 !important;
        font-family: 'Rajdhani', sans-serif !important;
    }
    
    label[data-testid="stNumberInput-label"], 
    label[data-testid="stTextInput-label"] {
        color: #ffffff !important;
        font-weight: 600 !important;
    }
    
    /* Streamlit widget labels */
    .stNumberInput > label, .stTextInput > label {
        color: #ffffff !important;
        font-weight: 600 !important;
    }
    
    /* Progress bars and metrics */
    .metric-container {
        display: flex;
        justify-content: space-around;
        margin: 1rem 0;
    }
    
    .metric-item {
        text-align: center;
        padding: 1rem;
        background: rgba(255, 107, 53, 0.1);
        border-radius: 8px;
        border: 1px solid rgba(255, 107, 53, 0.3);
        flex: 1;
        margin: 0 0.5rem;
    }
    
    .metric-label {
        font-family: 'Rajdhani', sans-serif;
        font-weight: 600;
        color: #ff6b35;
        font-size: 0.9rem;
    }
    
    .metric-value {
        font-family: 'Orbitron', monospace;
        font-weight: 700;
        color: #ffffff;
        font-size: 1.2rem;
    }
    
    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display:none;}
    
    /* Custom animations */
    @keyframes glow {
        0% { box-shadow: 0 0 5px rgba(255, 107, 53, 0.5); }
        50% { box-shadow: 0 0 20px rgba(255, 107, 53, 0.8), 0 0 30px rgba(255, 170, 0, 0.4); }
        100% { box-shadow: 0 0 5px rgba(255, 107, 53, 0.5); }
    }
    
    .pi-score {
        animation: glow 2s ease-in-out infinite alternate;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <h1 class="main-title">🏎️ FORZA HORIZON</h1>
    <h2 class="main-subtitle">Performance Index Calculator</h2>
    <p class="main-subtitle">Estimate your real-world car's Forza PI rating and class</p>
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
    
    if st.button("🚀 Decode VIN", help="This feature is coming in Phase 2!"):
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
    
    **Coming Soon:**
    - 🔍 VIN lookup integration
    - 🎨 Enhanced PI algorithms
    - 📱 Mobile optimization
    - 🚗 Car comparison tools
    """)
    
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center;">
        <p style="color: #ff6b35; font-weight: bold;">Ready for Forza Horizon 6! 🚀</p>
    </div>
    """, unsafe_allow_html=True)