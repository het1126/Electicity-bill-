import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import pandas as pd

# Page configuration
st.set_page_config(
    page_title="Energy Consumption Calculator",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        color: #2E86AB;
        font-size: 2.5rem;
        font-weight: bold;
        margin-bottom: 1rem;
    }
    
    .sub-header {
        text-align: center;
        color: #A23B72;
        font-size: 1.2rem;
        margin-bottom: 2rem;
    }
    
    .metric-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin: 10px 0;
    }
    
    .info-box {
        background: #f8f9fa;
        border-left: 4px solid #2E86AB;
        padding: 15px;
        margin: 10px 0;
        border-radius: 5px;
    }
    
    .stSelectbox > div > div {
        background-color: #f0f2f6;
    }
    
    .stTextInput > div > div > input {
        background-color: #f0f2f6;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<h1 class="main-header">⚡ Energy Consumption Calculator</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Calculate your household energy consumption and get insights</p>', unsafe_allow_html=True)

# Sidebar for user inputs
st.sidebar.header("📋 Personal Information")
name = st.sidebar.text_input("Your Name", placeholder="Enter your full name")
age = st.sidebar.number_input("Your Age", min_value=1, max_value=100, value=25)
city = st.sidebar.text_input("City", placeholder="Enter your city")
area = st.sidebar.text_input("Area/Locality", placeholder="Enter your area name")

st.sidebar.header("🏠 Housing Details")
flat_tenament = st.sidebar.selectbox(
    "Housing Type",
    ["Flat", "Tenement", "Independent House", "Villa"]
)

facility = st.sidebar.selectbox(
    "House Configuration",
    ["1BHK", "2BHK", "3BHK", "4BHK+"]
)

st.sidebar.header("🔌 Appliances")
ac = st.sidebar.radio("Air Conditioning", ["Yes", "No"])
fridge = st.sidebar.radio("Refrigerator", ["Yes", "No"])
washing_machine = st.sidebar.radio("Washing Machine", ["Yes", "No"])
tv = st.sidebar.radio("Television", ["Yes", "No"])
microwave = st.sidebar.radio("Microwave", ["Yes", "No"])

# Calculate energy consumption
def calculate_energy():
    cal_energy = 0
    
    # Base consumption based on BHK
    if facility == "1BHK":
        cal_energy += 2 * 0.4 + 2 * 0.8  # 2.4 kWh
    elif facility == "2BHK":
        cal_energy += 3 * 0.4 + 3 * 0.8  # 3.6 kWh
    elif facility == "3BHK":
        cal_energy += 4 * 0.4 + 4 * 0.8  # 4.8 kWh
    elif facility == "4BHK+":
        cal_energy += 5 * 0.4 + 5 * 0.8  # 6.0 kWh
    
    # Appliance consumption
    appliances = {
        'Air Conditioning': 3.0 if ac == "Yes" else 0,
        'Refrigerator': 1.5 if fridge == "Yes" else 0,
        'Washing Machine': 2.0 if washing_machine == "Yes" else 0,
        'Television': 0.8 if tv == "Yes" else 0,
        'Microwave': 1.2 if microwave == "Yes" else 0
    }
    
    for appliance, consumption in appliances.items():
        cal_energy += consumption
    
    return cal_energy, appliances

# Main content area
if name and city and area:
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📊 Energy Consumption Analysis")
        
        total_energy, appliances = calculate_energy()
        
        # Create breakdown data
        breakdown_data = {
            'Category': ['Base Consumption', 'Air Conditioning', 'Refrigerator', 
                        'Washing Machine', 'Television', 'Microwave'],
            'Consumption (kWh)': [
                2.4 if facility == "1BHK" else 3.6 if facility == "2BHK" else 4.8 if facility == "3BHK" else 6.0,
                appliances['Air Conditioning'],
                appliances['Refrigerator'],
                appliances['Washing Machine'],
                appliances['Television'],
                appliances['Microwave']
            ]
        }
        
        # Filter out zero consumption items
        df = pd.DataFrame(breakdown_data)
        df = df[df['Consumption (kWh)'] > 0]
        
        # Create pie chart
        fig_pie = px.pie(
            df, 
            values='Consumption (kWh)', 
            names='Category',
            title="Energy Consumption Breakdown",
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        fig_pie.update_layout(
            font=dict(size=12),
            title_font_size=16,
            showlegend=True
        )
        st.plotly_chart(fig_pie, use_container_width=True)
        
        # Create bar chart
        fig_bar = px.bar(
            df,
            x='Category',
            y='Consumption (kWh)',
            title="Daily Energy Consumption by Category",
            color='Consumption (kWh)',
            color_continuous_scale='viridis'
        )
        fig_bar.update_layout(
            xaxis_title="Category",
            yaxis_title="Consumption (kWh)",
            title_font_size=16
        )
        st.plotly_chart(fig_bar, use_container_width=True)
        
        # Monthly projection
        monthly_consumption = total_energy * 30
        monthly_cost = monthly_consumption * 5  # Assuming ₹5 per kWh
        
        st.subheader("📅 Monthly Projections")
        
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        
        # Simulate seasonal variation
        seasonal_multiplier = [0.8, 0.9, 1.0, 1.2, 1.4, 1.5, 1.6, 1.5, 1.3, 1.1, 0.9, 0.8]
        monthly_data = [monthly_consumption * mult for mult in seasonal_multiplier]
        
        fig_line = go.Figure()
        fig_line.add_trace(go.Scatter(
            x=months,
            y=monthly_data,
            mode='lines+markers',
            name='Monthly Consumption',
            line=dict(color='#2E86AB', width=3),
            marker=dict(size=8)
        ))
        
        fig_line.update_layout(
            title="Projected Monthly Energy Consumption",
            xaxis_title="Month",
            yaxis_title="Consumption (kWh)",
            title_font_size=16,
            hovermode='x unified'
        )
        st.plotly_chart(fig_line, use_container_width=True)
    
    with col2:
        st.subheader("📈 Summary")
        
        # Display metrics
        st.markdown(f"""
        <div class="metric-container">
            <h3>Daily Consumption</h3>
            <h2>{total_energy:.1f} kWh</h2>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="metric-container">
            <h3>Monthly Consumption</h3>
            <h2>{monthly_consumption:.0f} kWh</h2>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="metric-container">
            <h3>Estimated Monthly Cost</h3>
            <h2>₹{monthly_cost:.0f}</h2>
        </div>
        """, unsafe_allow_html=True)
        
        # User profile
        st.subheader("👤 Your Profile")
        st.markdown(f"""
        <div class="info-box">
            <strong>Name:</strong> {name}<br>
            <strong>Age:</strong> {age}<br>
            <strong>Location:</strong> {area}, {city}<br>
            <strong>Housing:</strong> {facility} {flat_tenament}<br>
            <strong>Appliances:</strong> {sum(1 for app in [ac, fridge, washing_machine, tv, microwave] if app == "Yes")} active
        </div>
        """, unsafe_allow_html=True)
        
        # Energy efficiency tips
        st.subheader("💡 Energy Saving Tips")
        
        tips = [
            "Use LED bulbs instead of incandescent",
            "Set AC temperature to 24°C for optimal efficiency",
            "Unplug devices when not in use",
            "Use natural light during daytime",
            "Regular maintenance of appliances",
            "Use timer for water heater"
        ]
        
        for tip in tips:
            st.markdown(f"• {tip}")
        
        # Environmental impact
        st.subheader("🌱 Environmental Impact")
        co2_emission = monthly_consumption * 0.82  # kg CO2 per kWh
        st.markdown(f"""
        <div class="info-box">
            <strong>Monthly CO₂ Emission:</strong><br>
            {co2_emission:.1f} kg CO₂
        </div>
        """, unsafe_allow_html=True)

else:
    st.warning("👆 Please fill in your personal information in the sidebar to see your energy consumption analysis.")
    
    # Show sample visualization
    st.subheader("📊 Sample Energy Consumption Dashboard")
    
    # Sample data
    sample_data = {
        'Category': ['Base Consumption', 'Air Conditioning', 'Refrigerator', 'Washing Machine'],
        'Consumption (kWh)': [3.6, 3.0, 1.5, 2.0]
    }
    
    df_sample = pd.DataFrame(sample_data)
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig_sample_pie = px.pie(
            df_sample, 
            values='Consumption (kWh)', 
            names='Category',
            title="Sample Energy Breakdown"
        )
        st.plotly_chart(fig_sample_pie, use_container_width=True)
    
    with col2:
        fig_sample_bar = px.bar(
            df_sample,
            x='Category',
            y='Consumption (kWh)',
            title="Sample Daily Consumption"
        )
        st.plotly_chart(fig_sample_bar, use_container_width=True)

# Footer
st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: #666;'>Energy Consumption Calculator | "
    f"Generated on {datetime.now().strftime('%B %d, %Y')}</p>",
    unsafe_allow_html=True
)