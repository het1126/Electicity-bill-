import streamlit as st
import plotly.graph_objects as go

# Set page config
st.set_page_config(
    page_title="Home Energy Calculator",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        text-align: center;
        color: #2E86AB;
        padding: 1rem 0;
        border-bottom: 3px solid #A23B72;
        margin-bottom: 2rem;
    }
    .info-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .energy-result {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        font-size: 24px;
        font-weight: bold;
        margin: 2rem 0;
    }
    .section-header {
        color: #2E86AB;
        border-bottom: 2px solid #F18F01;
        padding-bottom: 0.5rem;
        margin: 1.5rem 0 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Main header
st.markdown('<h1 class="main-header">⚡ Home Energy Calculator</h1>', unsafe_allow_html=True)

# Info box
st.markdown("""
<div class="info-box">
    <h3>🏠 Calculate Your Home's Energy Consumption</h3>
    <p>This calculator helps you estimate your home's energy usage based on your living space and appliances.</p>
</div>
""", unsafe_allow_html=True)

# Create two columns for better layout
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown('<h2 class="section-header">👤 Personal Information</h2>', unsafe_allow_html=True)
    
    # Personal details
    name = st.text_input("📝 Enter your name:", placeholder="e.g., John Doe")
    age = st.number_input("🎂 Enter your age:", min_value=1, max_value=120, value=25)
    city = st.text_input("🏙️ Enter your city:", placeholder="e.g., Mumbai")
    area = st.text_input("📍 Enter your area name:", placeholder="e.g., Bandra West")

with col2:
    st.markdown('<h2 class="section-header">🏠 Housing Details</h2>', unsafe_allow_html=True)
    
    # Housing details
    flat_tenement = st.selectbox(
        "🏢 Are you living in Flat or Tenement?",
        ["Select Option", "Flat", "Tenement"]
    )
    
    facility = st.selectbox(
        "🏘️ What type of accommodation?",
        ["Select Option", "1BHK", "2BHK", "3BHK"]
    )

# Appliances section
st.markdown('<h2 class="section-header">🔌 Appliances</h2>', unsafe_allow_html=True)

col3, col4, col5 = st.columns(3)

with col3:
    st.markdown("### ❄️ Air Conditioner")
    ac = st.radio(
        "Are you using AC?",
        ["No", "Yes"],
        key="ac"
    )

with col4:
    st.markdown("### 🧊 Refrigerator")
    fridge = st.radio(
        "Are you using Fridge?",
        ["No", "Yes"],
        key="fridge"
    )

with col5:
    st.markdown("### 🧺 Washing Machine")
    wm = st.radio(
        "Are you using Washing Machine?",
        ["No", "Yes"],
        key="wm"
    )

# Calculate button
if st.button("🔄 Calculate Energy Consumption", type="primary"):
    if name and city and area and flat_tenement != "Select Option" and facility != "Select Option":
        # Calculate energy
        cal_energy = 0
        
        # Base energy calculation based on facility type
        if facility.lower() == "1bhk":
            cal_energy += 2 * 0.4 + 2 * 0.8  # 2.4 kWh
        elif facility.lower() == "2bhk":
            cal_energy += 3 * 0.4 + 3 * 0.8  # 3.6 kWh
        elif facility.lower() == "3bhk":
            cal_energy += 4 * 0.4 + 4 * 0.8  # 4.8 kWh
        
        # Add appliance energy consumption
        if ac == "Yes":
            cal_energy += 3
        if fridge == "Yes":
            cal_energy += 3
        if wm == "Yes":
            cal_energy += 3
        
        # Display results
        st.markdown(f"""
        <div class="energy-result">
            🎯 Total Energy Consumption: {cal_energy:.1f} kWh/day
        </div>
        """, unsafe_allow_html=True)
        
        # Create energy breakdown
        st.markdown('<h2 class="section-header">📊 Energy Breakdown</h2>', unsafe_allow_html=True)
        
        # Calculate breakdown
        base_energy = cal_energy - (3 if ac == "Yes" else 0) - (3 if fridge == "Yes" else 0) - (3 if wm == "Yes" else 0)
        
        categories = []
        values = []
        
        if base_energy > 0:
            categories.append(f"Base ({facility})")
            values.append(base_energy)
        
        if ac == "Yes":
            categories.append("Air Conditioner")
            values.append(3)
        
        if fridge == "Yes":
            categories.append("Refrigerator")
            values.append(3)
        
        if wm == "Yes":
            categories.append("Washing Machine")
            values.append(3)
        
        # Create pie chart
        fig = go.Figure(data=[go.Pie(
            labels=categories,
            values=values,
            hole=0.3,
            marker_colors=['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4']
        )])
        
        fig.update_layout(
            title="Energy Consumption Breakdown (kWh/day)",
            font=dict(size=14),
            showlegend=True
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Additional information
        col6, col7, col8 = st.columns(3)
        
        with col6:
            st.metric("📅 Daily Consumption", f"{cal_energy:.1f} kWh")
        
        with col7:
            st.metric("📅 Monthly Consumption", f"{cal_energy * 30:.1f} kWh")
        
        with col8:
            st.metric("📅 Yearly Consumption", f"{cal_energy * 365:.1f} kWh")
        
        # User summary
        st.markdown('<h2 class="section-header">📋 Summary</h2>', unsafe_allow_html=True)
        
        st.info(f"""
        **User Details:**
        - Name: {name}
        - Age: {age} years
        - Location: {area}, {city}
        - Housing: {facility} {flat_tenement}
        - Appliances: {', '.join([app for app, status in [('AC', ac), ('Fridge', fridge), ('Washing Machine', wm)] if status == 'Yes']) or 'None'}
        """)
        
        # Energy saving tips
        st.markdown('<h2 class="section-header">💡 Energy Saving Tips</h2>', unsafe_allow_html=True)
        
        tips = [
            "🌡️ Set AC temperature to 24°C or higher",
            "💡 Use LED bulbs instead of incandescent ones",
            "🔌 Unplug electronics when not in use",
            "🚿 Use cold water for washing clothes when possible",
            "🌞 Use natural light during the day",
            "⚡ Regular maintenance of appliances improves efficiency"
        ]
        
        for tip in tips:
            st.write(f"• {tip}")
    
    else:
        st.error("⚠️ Please fill in all required fields before calculating!")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 1rem;">
    <p>🌱 Energy Calculator v1.0 | Built with Streamlit</p>
    <p>💡 Make your home more energy efficient!</p>
</div>
""", unsafe_allow_html=True)