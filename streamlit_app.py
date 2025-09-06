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

# Main Application
def main():
    """Main application function"""
    # Render header
    render_header()
    
    # Create two columns for layout
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # VIN lookup section - now returns vehicle info and real-world data
        vin_input, vehicle_info, real_world_vehicle = render_vin_section()
        
        # Manual input section - now can use both VIN hints and real-world data
        hp, weight, top_speed, acceleration, handling, braking = render_manual_input_section(vehicle_info, real_world_vehicle)
    
    with col2:
        # Calculate PI and class
        pi = calculate_pi(hp, weight, top_speed, acceleration, handling, braking)
        forza_class = determine_forza_class(pi)
        
        # Render results
        render_results_section(pi, forza_class)
        
        # Performance breakdown
        breakdown = get_performance_breakdown(hp, weight, top_speed, acceleration, handling, braking)
        render_performance_breakdown(breakdown)
    
    # Similar cars section
    similar_cars = get_similar_cars(pi, forza_class, 6)
    render_similar_cars_section(similar_cars, pi, forza_class)
    
    # Footer
    render_footer()
    
    # Sidebar - now shows both VIN info and real-world data
    render_sidebar(len(similar_cars), forza_class, vehicle_info, real_world_vehicle)

if __name__ == "__main__":
    main()