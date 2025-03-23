import streamlit as st

st.set_page_config(page_title="Forza PI Calculator")

st.title("Forza Horizon Performance Index (PI) Calculator")
st.markdown("Estimate your real-life car's Forza PI and class rating.")

# Input fields
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

# Determine Forza class
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

# Output
st.markdown(f"### Estimated PI: **{pi}**")
st.markdown(f"### Forza Class: **{forza_class}**")
