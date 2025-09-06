# utils/styling.py
"""
CSS styling and UI theming for Forza PI Calculator
"""

def get_forza_css():
    """Return the main CSS styling for the Forza-themed UI"""
    return """
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
            animation: glow 2s ease-in-out infinite alternate;
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
        
        /* Similar cars section */
        .similar-cars-section {
            background: linear-gradient(45deg, rgba(50, 205, 50, 0.1) 0%, rgba(34, 139, 34, 0.1) 100%);
            border: 2px solid #32CD32;
            border-radius: 12px;
            padding: 1.5rem;
            margin-top: 2rem;
        }
        
        .car-card {
            background: rgba(26, 35, 50, 0.9);
            border: 2px solid rgba(255, 107, 53, 0.5);
            border-radius: 12px;
            padding: 1rem;
            margin: 0.5rem 0;
            transition: all 0.3s ease;
        }
        
        .car-card:hover {
            border-color: #ff6b35;
            box-shadow: 0 4px 20px rgba(255, 107, 53, 0.3);
            transform: translateY(-2px);
        }
        
        .car-name {
            font-family: 'Orbitron', monospace;
            font-weight: 700;
            color: #ff6b35;
            font-size: 1.1rem;
            margin-bottom: 0.5rem;
        }
        
        .car-details {
            font-family: 'Rajdhani', sans-serif;
            color: #ffffff;
            font-size: 0.9rem;
            opacity: 0.8;
        }
        
        .car-pi {
            font-family: 'Orbitron', monospace;
            font-weight: 700;
            font-size: 1.2rem;
            color: #ffaa00;
        }
        
        /* Button styling - Fixed for better visibility */
        .stButton > button {
            background: linear-gradient(45deg, #ff6b35 0%, #f7931e 100%) !important;
            color: #ffffff !important;
            border: 2px solid #ff6b35 !important;
            border-radius: 8px !important;
            font-family: 'Rajdhani', sans-serif !important;
            font-weight: 700 !important;
            font-size: 1.1rem !important;
            padding: 0.7rem 2rem !important;
            box-shadow: 0 4px 15px rgba(255, 107, 53, 0.4) !important;
            transition: all 0.3s ease !important;
            opacity: 1 !important;
            text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.5) !important;
            min-height: 3rem !important;
            cursor: pointer !important;
        }
        
        .stButton > button:hover {
            background: linear-gradient(45deg, #e55a2e 0%, #e6841a 100%) !important;
            color: #ffffff !important;
            transform: translateY(-2px) !important;
            box-shadow: 0 8px 25px rgba(255, 107, 53, 0.6) !important;
            border-color: #e55a2e !important;
        }
        
        .stButton > button:focus {
            background: linear-gradient(45deg, #ff6b35 0%, #f7931e 100%) !important;
            color: #ffffff !important;
            outline: 2px solid #ffaa00 !important;
            outline-offset: 2px !important;
        }
        
        .stButton > button:active {
            background: linear-gradient(45deg, #d14b20 0%, #d1751a 100%) !important;
            color: #ffffff !important;
            transform: translateY(0px) !important;
        }
        
        .stButton > button:disabled {
            background: #666666 !important;
            color: #cccccc !important;
            border-color: #666666 !important;
            cursor: not-allowed !important;
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
        
        /* Input labels styling */
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
    </style>
    """