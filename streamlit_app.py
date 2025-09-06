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

# Forza Horizon 5 Car Database (Real data from ManteoMax's spreadsheet)
FORZA_CARS_DATABASE = [
    # D Class (100-299)
    {"name": "1968 Abarth 595 esseesse", "year": 1968, "make": "Abarth", "model": "595 esseesse", "pi": 100, "class": "D", "type": "Cult Cars", "hp": 28, "weight": 1257},
    {"name": "1958 Austin-Healey Sprite MkI", "year": 1958, "make": "Austin-Healey", "model": "Sprite MkI", "pi": 131, "class": "D", "type": "Classic Sports Cars", "hp": 45, "weight": 1463},
    {"name": "1930 Bentley Blower 4-1/2 Litre", "year": 1930, "make": "Bentley", "model": "Blower 4-1/2 Litre", "pi": 207, "class": "D", "type": "Vintage Racers", "hp": 175, "weight": 4395},
    {"name": "1973 AMC Gremlin X", "year": 1973, "make": "AMC", "model": "Gremlin X", "pi": 403, "class": "D", "type": "Cult Cars", "hp": 150, "weight": 2840},
    {"name": "2016 Abarth 695 Biposto", "year": 2016, "make": "Abarth", "model": "695 Biposto", "pi": 657, "class": "B", "type": "Hot Hatch", "hp": 186, "weight": 2198},
    {"name": "1993 Autozam AZ-1", "year": 1993, "make": "Autozam", "model": "AZ-1", "pi": 450, "class": "D", "type": "Retro Hot Hatch", "hp": 63, "weight": 1587},
    {"name": "1971 AMC Javelin AMX", "year": 1971, "make": "AMC", "model": "Javelin AMX", "pi": 493, "class": "D", "type": "Classic Muscle", "hp": 330, "weight": 3445},
    
    # C Class (300-399) 
    {"name": "1980 Abarth Fiat 131", "year": 1980, "make": "Abarth", "model": "Fiat 131", "pi": 510, "class": "C", "type": "Classic Rally", "hp": 140, "weight": 2161},
    {"name": "1970 AMC Rebel 'The Machine'", "year": 1970, "make": "AMC", "model": "Rebel 'The Machine'", "pi": 531, "class": "C", "type": "Classic Muscle", "hp": 340, "weight": 3650},
    {"name": "1991 Bentley Turbo R", "year": 1991, "make": "Bentley", "model": "Turbo R", "pi": 543, "class": "C", "type": "Retro Saloons", "hp": 328, "weight": 5313},
    {"name": "1964 Aston Martin DB5", "year": 1964, "make": "Aston Martin", "model": "DB5", "pi": 548, "class": "C", "type": "Rare Classics", "hp": 325, "weight": 3230},
    {"name": "1973 Alpine A110 1600s", "year": 1973, "make": "Alpine", "model": "A110 1600s", "pi": 550, "class": "C", "type": "Classic Rally", "hp": 123, "weight": 1576},
    {"name": "1992 Alfa Romeo 155 Q4", "year": 1992, "make": "Alfa Romeo", "model": "155 Q4", "pi": 561, "class": "C", "type": "Retro Saloons", "hp": 187, "weight": 3064},
    {"name": "2017 Abarth 124 Spider", "year": 2017, "make": "Abarth", "model": "124 Spider", "pi": 562, "class": "C", "type": "Modern Sports Cars", "hp": 186, "weight": 2477},
    {"name": "2002 Acura RSX Type-S", "year": 2002, "make": "Acura", "model": "RSX Type-S", "pi": 585, "class": "C", "type": "Retro Hot Hatch", "hp": 200, "weight": 2820},
    {"name": "2001 Acura Integra Type-R", "year": 2001, "make": "Acura", "model": "Integra Type-R", "pi": 596, "class": "C", "type": "Retro Hot Hatch", "hp": 195, "weight": 2639},
    
    # B Class (400-499)
    {"name": "1995 Audi Avant RS 2", "year": 1995, "make": "Audi", "model": "Avant RS 2", "pi": 601, "class": "B", "type": "Retro Saloons", "hp": 311, "weight": 3517},
    {"name": "1983 Audi Sport quattro", "year": 1983, "make": "Audi", "model": "Sport quattro", "pi": 638, "class": "B", "type": "Retro Rally", "hp": 306, "weight": 2807},
    {"name": "1965 Alfa Romeo Giulia TZ2", "year": 1965, "make": "Alfa Romeo", "model": "Giulia TZ2", "pi": 641, "class": "B", "type": "Classic Racers", "hp": 170, "weight": 1367},
    {"name": "2015 Alumicraft Class 10 Race Car", "year": 2015, "make": "Alumicraft", "model": "Class 10 Race Car", "pi": 642, "class": "B", "type": "Unlimited Buggies", "hp": 196, "weight": 2200},
    {"name": "2015 Audi S1", "year": 2015, "make": "Audi", "model": "S1", "pi": 644, "class": "B", "type": "Hot Hatch", "hp": 228, "weight": 2899},
    {"name": "2001 Audi RS 4 Avant", "year": 2001, "make": "Audi", "model": "RS 4 Avant", "pi": 663, "class": "B", "type": "Retro Saloons", "hp": 375, "weight": 3571},
    {"name": "2003 Audi RS 6", "year": 2003, "make": "Audi", "model": "RS 6", "pi": 677, "class": "B", "type": "Retro Saloons", "hp": 450, "weight": 4024},
    {"name": "1958 Aston Martin DBR1", "year": 1958, "make": "Aston Martin", "model": "DBR1", "pi": 678, "class": "B", "type": "Classic Racers", "hp": 254, "weight": 1930},
    {"name": "2011 Audi RS 3 Sportback", "year": 2011, "make": "Audi", "model": "RS 3 Sportback", "pi": 682, "class": "B", "type": "Super Hot Hatch", "hp": 335, "weight": 3472},
    {"name": "2021 Alumicraft #122 Class 1 Buggy", "year": 2021, "make": "Alumicraft", "model": "#122 Class 1 Buggy", "pi": 689, "class": "B", "type": "Unlimited Buggies", "hp": 495, "weight": 3750},
    {"name": "2017 Alpine A110", "year": 2017, "make": "Alpine", "model": "A110", "pi": 694, "class": "B", "type": "Modern Sports Cars", "hp": 248, "weight": 2432},
    
    # A Class (500-599)
    {"name": "1968 Alfa Romeo 33 Stradale", "year": 1968, "make": "Alfa Romeo", "model": "33 Stradale", "pi": 707, "class": "A", "type": "Classic Racers", "hp": 245, "weight": 1543},
    {"name": "2006 Audi RS 4", "year": 2006, "make": "Audi", "model": "RS 4", "pi": 710, "class": "A", "type": "Super Saloons", "hp": 420, "weight": 3638},
    {"name": "2016 Ariel Nomad", "year": 2016, "make": "Ariel", "model": "Nomad", "pi": 711, "class": "A", "type": "Unlimited Buggies", "hp": 236, "weight": 1477},
    {"name": "2016 BMW M2 Coupé", "year": 2016, "make": "BMW", "model": "M2 Coupé", "pi": 718, "class": "A", "type": "Super Saloons", "hp": 365, "weight": 3450},
    {"name": "2554 AMG Transport Dynamics M12S Warthog CST", "year": 2554, "make": "AMG Transport Dynamics", "model": "M12S Warthog CST", "pi": 719, "class": "A", "type": "Unlimited Offroad", "hp": 720, "weight": 5071},
    {"name": "2009 Audi RS 6", "year": 2009, "make": "Audi", "model": "RS 6", "pi": 722, "class": "A", "type": "Super Saloons", "hp": 570, "weight": 4376},
    {"name": "2015 Audi TTS Coupe", "year": 2015, "make": "Audi", "model": "TTS Coupe", "pi": 724, "class": "A", "type": "Modern Sports Cars", "hp": 310, "weight": 3053},
    {"name": "2016 Bentley Bentayga", "year": 2016, "make": "Bentley", "model": "Bentayga", "pi": 727, "class": "A", "type": "Sports Utility Heroes", "hp": 599, "weight": 5340},
    {"name": "2011 Audi RS 5 Coupe", "year": 2011, "make": "Audi", "model": "RS 5 Coupe", "pi": 733, "class": "A", "type": "Super Saloons", "hp": 442, "weight": 3830},
    {"name": "2020 Audi RS 3 Sedan", "year": 2020, "make": "Audi", "model": "RS 3 Sedan", "pi": 734, "class": "A", "type": "Super Saloons", "hp": 394, "weight": 3593},
    {"name": "2013 Audi RS 7 Sportback", "year": 2013, "make": "Audi", "model": "RS 7 Sportback", "pi": 739, "class": "A", "type": "Super Saloons", "hp": 552, "weight": 4310},
    {"name": "2008 Aston Martin DBS", "year": 2008, "make": "Aston Martin", "model": "DBS", "pi": 746, "class": "A", "type": "GT Cars", "hp": 510, "weight": 3737},
    {"name": "2018 Audi TT RS", "year": 2018, "make": "Audi", "model": "TT RS", "pi": 748, "class": "A", "type": "Modern Sports Cars", "hp": 400, "weight": 3306},
    {"name": "2018 Audi RS 5 Coupé", "year": 2018, "make": "Audi", "model": "RS 5 Coupé", "pi": 750, "class": "A", "type": "Super Saloons", "hp": 444, "weight": 3990},
    {"name": "2018 Audi RS 4 Avant", "year": 2018, "make": "Audi", "model": "RS 4 Avant", "pi": 751, "class": "A", "type": "Super Saloons", "hp": 444, "weight": 3946},
    {"name": "2019 BMW Z4 Roadster", "year": 2019, "make": "BMW", "model": "Z4 Roadster", "pi": 751, "class": "A", "type": "Modern Sports Cars", "hp": 382, "weight": 3252},
    {"name": "2015 Audi RS 6 Avant", "year": 2015, "make": "Audi", "model": "RS 6 Avant", "pi": 754, "class": "A", "type": "Super Saloons", "hp": 552, "weight": 4266},
    {"name": "2014 Alfa Romeo 4C", "year": 2014, "make": "Alfa Romeo", "model": "4C", "pi": 755, "class": "A", "type": "Modern Sports Cars", "hp": 240, "weight": 2077},
    {"name": "2007 Alfa Romeo 8C Competizione", "year": 2007, "make": "Alfa Romeo", "model": "8C Competizione", "pi": 755, "class": "A", "type": "GT Cars", "hp": 450, "weight": 3495},
    {"name": "2021 Bentley Continental GT Convertible", "year": 2021, "make": "Bentley", "model": "Continental GT Convertible", "pi": 759, "class": "A", "type": "GT Cars", "hp": 626, "weight": 5322},
    {"name": "2023 BMW M2", "year": 2023, "make": "BMW", "model": "M2", "pi": 762, "class": "A", "type": "Super Saloons", "hp": 453, "weight": 3748},
    {"name": "2021 Audi RS 6 Avant", "year": 2021, "make": "Audi", "model": "RS 6 Avant", "pi": 763, "class": "A", "type": "Super Saloons", "hp": 591, "weight": 4575},
    {"name": "2015 BMW i8", "year": 2015, "make": "BMW", "model": "i8", "pi": 764, "class": "A", "type": "Modern Supercars", "hp": 357, "weight": 3380},
    {"name": "2020 Audi TT RS Coupe", "year": 2020, "make": "Audi", "model": "TT RS Coupe", "pi": 765, "class": "A", "type": "Modern Sports Cars", "hp": 394, "weight": 3306},
    {"name": "2021 Audi RS 7 Sportback", "year": 2021, "make": "Audi", "model": "RS 7 Sportback", "pi": 768, "class": "A", "type": "Super Saloons", "hp": 591, "weight": 4553},
    {"name": "2017 Bentley Continental Supersports", "year": 2017, "make": "Bentley", "model": "Continental Supersports", "pi": 769, "class": "A", "type": "GT Cars", "hp": 700, "weight": 5029},
    {"name": "2021 Audi RS e-tron GT", "year": 2021, "make": "Audi", "model": "RS e-tron GT", "pi": 770, "class": "A", "type": "Super Saloons", "hp": 637, "weight": 5174},
    {"name": "2021 BMW M3 Competition Sedan", "year": 2021, "make": "BMW", "model": "M3 Competition Sedan", "pi": 772, "class": "A", "type": "Super Saloons", "hp": 503, "weight": 3814},
    {"name": "2017 Alfa Romeo Giulia Quadrifoglio", "year": 2017, "make": "Alfa Romeo", "model": "Giulia Quadrifoglio", "pi": 775, "class": "A", "type": "Super Saloons", "hp": 506, "weight": 3822},
    {"name": "2021 BMW M4 Competition Coupé", "year": 2021, "make": "BMW", "model": "M4 Competition Coupé", "pi": 778, "class": "A", "type": "Super Saloons", "hp": 503, "weight": 3803},
    {"name": "2018 BMW M5", "year": 2018, "make": "BMW", "model": "M5", "pi": 784, "class": "A", "type": "Super Saloons", "hp": 600, "weight": 4370},
    {"name": "2017 Aston Martin DB11", "year": 2017, "make": "Aston Martin", "model": "DB11", "pi": 787, "class": "A", "type": "Super GT", "hp": 608, "weight": 4134},
    {"name": "2020 BMW M8 Competition Coupe", "year": 2020, "make": "BMW", "model": "M8 Competition Coupe", "pi": 791, "class": "A", "type": "GT Cars", "hp": 617, "weight": 4354},
    {"name": "2013 Aston Martin V12 Vantage S", "year": 2013, "make": "Aston Martin", "model": "V12 Vantage S", "pi": 796, "class": "A", "type": "Super GT", "hp": 565, "weight": 3671},
    
    # S1 Class (600-699)
    {"name": "2019 Aston Martin Vantage", "year": 2019, "make": "Aston Martin", "model": "Vantage", "pi": 801, "class": "S1", "type": "GT Cars", "hp": 503, "weight": 3497},
    {"name": "2013 Audi R8 Coupe V10 plus", "year": 2013, "make": "Audi", "model": "R8 Coupe V10 plus", "pi": 802, "class": "S1", "type": "Modern Supercars", "hp": 542, "weight": 3682},
    {"name": "2017 Aston Martin Vanquish Zagato", "year": 2017, "make": "Aston Martin", "model": "Vanquish Zagato Coupe", "pi": 803, "class": "S1", "type": "Super GT", "hp": 595, "weight": 3891},
    {"name": "2016 BMW M4 GTS", "year": 2016, "make": "BMW", "model": "M4 GTS", "pi": 814, "class": "S1", "type": "Track Toys", "hp": 493, "weight": 3329},
    {"name": "1986 Audi #2 Audi Sport quattro S1", "year": 1986, "make": "Audi", "model": "#2 Audi Sport quattro S1", "pi": 827, "class": "S1", "type": "Rally Monsters", "hp": 469, "weight": 2403},
    {"name": "2022 BMW M5 CS", "year": 2022, "make": "BMW", "model": "M5 CS", "pi": 827, "class": "S1", "type": "Super Saloons", "hp": 626, "weight": 4023},
    {"name": "2012 Ascari KZ1R", "year": 2012, "make": "Ascari", "model": "KZ1R", "pi": 829, "class": "S1", "type": "Modern Supercars", "hp": 520, "weight": 2976},
    {"name": "2016 Aston Martin Vantage GT12", "year": 2016, "make": "Aston Martin", "model": "Vantage GT12", "pi": 829, "class": "S1", "type": "Track Toys", "hp": 593, "weight": 3450},
    {"name": "2017 Acura NSX", "year": 2017, "make": "Acura", "model": "NSX", "pi": 831, "class": "S1", "type": "Modern Supercars", "hp": 573, "weight": 3803},
    {"name": "2016 Audi R8 V10 plus", "year": 2016, "make": "Audi", "model": "R8 V10 plus", "pi": 834, "class": "S1", "type": "Modern Supercars", "hp": 610, "weight": 3428},
    {"name": "2019 Aston Martin DBS Superleggera", "year": 2019, "make": "Aston Martin", "model": "DBS Superleggera", "pi": 835, "class": "S1", "type": "Super GT", "hp": 715, "weight": 3966},
    {"name": "2010 Aston Martin One-77", "year": 2010, "make": "Aston Martin", "model": "One-77", "pi": 843, "class": "S1", "type": "Super GT", "hp": 750, "weight": 3307},
    {"name": "2014 BAC Mono", "year": 2014, "make": "BAC", "model": "Mono", "pi": 868, "class": "S1", "type": "Track Toys", "hp": 280, "weight": 1354},
    {"name": "2018 ATS GT", "year": 2018, "make": "ATS", "model": "GT", "pi": 877, "class": "S1", "type": "Modern Supercars", "hp": 720, "weight": 2985},
    
    # S2 Class (700-799)
    {"name": "2018 BMW #1 BMW M Motorsport M8 GTE", "year": 2018, "make": "BMW", "model": "#1 BMW M Motorsport M8 GTE", "pi": 910, "class": "S2", "type": "Extreme Track Toys", "hp": 600, "weight": 2910},
    {"name": "2013 Ariel Atom 500 V8", "year": 2013, "make": "Ariel", "model": "Atom 500 V8", "pi": 924, "class": "S2", "type": "Extreme Track Toys", "hp": 475, "weight": 1433},
    {"name": "2020 Automobili Pininfarina Battista", "year": 2020, "make": "Automobili Pininfarina", "model": "Battista", "pi": 928, "class": "S2", "type": "Hypercars", "hp": 1845, "weight": 4409},
    {"name": "2017 Aston Martin Vulcan AMR Pro", "year": 2017, "make": "Aston Martin", "model": "Vulcan AMR Pro", "pi": 953, "class": "S2", "type": "Extreme Track Toys", "hp": 820, "weight": 2998},
    {"name": "2019 Aston Martin Valhalla Concept", "year": 2019, "make": "Aston Martin", "model": "Valhalla Concept Car", "pi": 959, "class": "S2", "type": "Hypercars", "hp": 1042, "weight": 3097},
    {"name": "2018 Apollo Intensa Emozione", "year": 2018, "make": "Apollo", "model": "Intensa Emozione", "pi": 963, "class": "S2", "type": "Extreme Track Toys", "hp": 780, "weight": 2756},
    {"name": "2023 Aston Martin Valkyrie", "year": 2023, "make": "Aston Martin", "model": "Valkyrie", "pi": 978, "class": "S2", "type": "Hypercars", "hp": 1140, "weight": 2976},
    
    # X Class (800-999)
    {"name": "2018 Apollo Intensa Emozione 'Welcome Pack'", "year": 2018, "make": "Apollo", "model": "Intensa Emozione 'Welcome Pack'", "pi": 998, "class": "X", "type": "Extreme Track Toys", "hp": 930, "weight": 2480},
    {"name": "2022 Aston Martin Valkyrie AMR Pro", "year": 2022, "make": "Aston Martin", "model": "Valkyrie AMR Pro", "pi": 998, "class": "X", "type": "Extreme Track Toys", "hp": 800, "weight": 2370}
]

def get_similar_cars(calculated_pi, user_class, num_cars=5):
    """Find similar cars from Forza database based on PI and class"""
    # Filter cars by class first, then by PI proximity
    class_cars = [car for car in FORZA_CARS_DATABASE if car["class"] == user_class]
    
    if len(class_cars) < num_cars:
        # If not enough cars in exact class, expand to nearby classes
        nearby_classes = {
            "D": ["D", "C"],
            "C": ["D", "C", "B"], 
            "B": ["C", "B", "A"],
            "A": ["B", "A", "S1"],
            "S1": ["A", "S1", "S2"],
            "S2": ["S1", "S2", "X"],
            "X": ["S2", "X"]
        }
        expanded_cars = [car for car in FORZA_CARS_DATABASE 
                        if car["class"] in nearby_classes.get(user_class, [user_class])]
        class_cars = expanded_cars
    
    # Sort by PI proximity to calculated PI
    class_cars.sort(key=lambda x: abs(x["pi"] - calculated_pi))
    
    return class_cars[:num_cars]

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