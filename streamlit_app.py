import streamlit as st

# App config
st.set_page_config(page_title="Forza Horizon PI Calculator", layout="centered")

# Custom styling
st.markdown("""
    <style>
    body {
        background-color: #f9f9f9;
    }
    .forza-title {
        font-size: 2.5em;
        font-weight: bold;
        color: #0E1117;
        text-align: center;
        margin-bottom: 20px;
    }
    .forza-box {
        padding: 20px;
        border-radius: 10px;
        margin-top: 20px;
        font-size: 1.2em;
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

# Title
st.markdown('<div class="forza-title">Forza Horizon Performance Index (PI) Calculator</div>', unsafe_allow_html=True)
st.markdown("Estimate your real-life car's PI and class in Forza Horizon.")

# Input form
hp = st.number_input("Horsepower (HP)", value=300, step=10)
weight = st.number_input("Weight (lbs)", value=3500, step=50)
top_speed = st.number_input("Top Speed (mph)", value=150, step=5)
acceleration = st.number_input("0-60 mph Time (seconds)", value=5.0, step=0.1)
handling = st.number_input("Handling (G-force)", value=1.0, step=0.01)
braking = st.number_input("Braking Distance (60-0 mph in feet)", value=120, step=5)

# Calculate PI
pi = (
    (hp / 1500) * 200 +
    ((5000 - weight) / 5000) * 100 +
    (top_speed / 300) * 200 +
    ((10 - acceleration) / 10) * 200 +
    (handling / 1.5) * 200 +
    ((150 - braking) / 150) * 100
)
pi = round(min(max(pi, 100), 999))

# Forza class determination and color
if pi < 300:
    forza_class, color = "D", "#7e7e7e"
elif pi < 400:
    forza_class, color = "C", "#4caf50"
elif pi < 500:
    forza_class, color = "B", "#2196f3"
elif pi < 600:
    forza_class, color = "A", "#9c27b0"
elif pi < 700:
    forza_class, color = "S1", "#ff9800"
elif pi < 800:
    forza_class, color = "S2", "#f44336"
else:
    forza_class, color = "X", "#ffd700"

# Display result with style
st.markdown(f"""
    <div class="forza-box" style="background-color: {color}; color: white;">
        <strong>Estimated PI:</strong> {pi}<br>
        <strong>Forza Class:</strong> {forza_class}
    </div>
""", unsafe_allow_html=True)
