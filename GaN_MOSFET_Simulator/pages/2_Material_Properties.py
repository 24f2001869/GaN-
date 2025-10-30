# pages/2_Material_Properties.py
# Enhanced Material Properties Comparison

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

st.set_page_config(page_title="Material Properties - GaN MOSFET", layout="wide")

# ---------------- ENHANCED STYLES ----------------
st.markdown("""
<style>
.material-card {
    background: white;
    padding: 20px;
    border-radius: 15px;
    margin: 15px 0;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
    border: 1px solid #e9ecef;
    transition: transform 0.3s ease;
}

.material-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 8px 30px rgba(0, 0, 0, 0.12);
}

.property-bar {
    background: linear-gradient(90deg, #667eea, #764ba2);
    color: white;
    padding: 8px 15px;
    border-radius: 25px;
    margin: 5px 0;
    font-weight: 500;
}

.radar-container {
    background: white;
    padding: 20px;
    border-radius: 15px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
}
</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown("<div class='page-title'>🔬 Advanced Material Properties Analysis</div>", unsafe_allow_html=True)
st.markdown("---")

# ---------------- COMPREHENSIVE MATERIAL DATA ----------------
material_data = {
    "Property": [
        "Bandgap (eV)", "Electron Mobility (cm²/V·s)", "Breakdown Field (MV/cm)",
        "Thermal Conductivity (W/cm·K)", "Saturation Velocity (×10⁷ cm/s)", 
        "Relative Permittivity", "Melting Point (°C)", "Density (g/cm³)"
    ],
    "GaN": [3.4, 2000, 3.3, 1.3, 2.5, 9.0, 2500, 6.15],
    "SiC": [3.26, 900, 3.5, 4.9, 2.0, 9.7, 2830, 3.21],
    "GaAs": [1.42, 8500, 0.4, 0.55, 2.0, 12.9, 1238, 5.32],
    "Si": [1.12, 1400, 0.3, 1.5, 1.0, 11.8, 1414, 2.33]
}

df = pd.DataFrame(material_data)

# ---------------- PROPERTY EXPLANATIONS ----------------
property_explanations = {
    "Bandgap (eV)": "Energy required for electron excitation. Wider bandgap enables higher temperature and voltage operation.",
    "Electron Mobility (cm²/V·s)": "Measure of how quickly electrons can move through material. Higher mobility means faster switching.",
    "Breakdown Field (MV/cm)": "Maximum electric field before material breakdown. Critical for high-voltage applications.",
    "Thermal Conductivity (W/cm·K)": "Ability to conduct heat. Higher values enable better thermal management.",
    "Saturation Velocity (×10⁷ cm/s)": "Maximum electron velocity under high fields. Affects high-frequency performance.",
    "Relative Permittivity": "Measure of material's ability to store electrical energy in an electric field.",
    "Melting Point (°C)": "Temperature at which material changes from solid to liquid phase.",
    "Density (g/cm³)": "Mass per unit volume of the material."
}

# ---------------- SIDEBAR CONTROLS ----------------
st.sidebar.header("🎛️ Visualization Controls")
selected_property = st.sidebar.selectbox(
    "Select Property to Highlight:",
    df["Property"].tolist(),
    index=0
)

chart_type = st.sidebar.radio(
    "Chart Type:",
    ["Bar Chart", "Radar Chart", "Comparison Matrix"],
    index=0
)

# ---------------- MAIN CONTENT ----------------
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("### 📊 Material Properties Dashboard")
    
    # Interactive Data Table
    st.dataframe(df, use_container_width=True, hide_index=True)

with col2:
    st.markdown("### 🎯 Property Insight")
    if selected_property in property_explanations:
        st.info(f"**{selected_property}**\n\n{property_explanations[selected_property]}")

# ---------------- VISUALIZATIONS ----------------
if chart_type == "Bar Chart":
    st.markdown("### 📈 Comparative Analysis")
    
    # Filter data for selected property
    prop_data = df[df["Property"] == selected_property].iloc[0, 1:]
    
    fig = px.bar(
        x=prop_data.index,
        y=prop_data.values,
        color=prop_data.index,
        color_discrete_sequence=px.colors.qualitative.Set3,
        title=f"{selected_property} - Material Comparison",
        labels={"x": "Material", "y": selected_property}
    )
    
    fig.update_layout(
        template="plotly_white",
        height=500,
        showlegend=False,
        font=dict(size=12)
    )
    
    st.plotly_chart(fig, use_container_width=True)

elif chart_type == "Radar Chart":
    st.markdown("### 🎯 Performance Radar Chart")
    
    # Normalize data for radar chart
    radar_df = df.set_index("Property").T
    normalized_df = radar_df.copy()
    
    for col in normalized_df.columns:
        max_val = normalized_df[col].max()
        if max_val > 0:
            normalized_df[col] = normalized_df[col] / max_val
    
    categories = normalized_df.columns.tolist()
    
    fig = go.Figure()
    
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4']
    
    for i, (material, row) in enumerate(normalized_df.iterrows()):
        fig.add_trace(go.Scatterpolar(
            r=row.values.tolist() + [row.values[0]],  # Close the circle
            theta=categories + [categories[0]],
            fill='toself',
            name=material,
            line=dict(color=colors[i % len(colors)]),
            opacity=0.8
        ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 1]
            )),
        showlegend=True,
        template="plotly_white",
        height=600,
        title="Normalized Material Properties Comparison"
    )
    
    st.plotly_chart(fig, use_container_width=True)

else:
    st.markdown("### 🔄 Property Comparison Matrix")
    
    # Create heatmap-style comparison
    comparison_data = df.set_index("Property").T
    
    fig = px.imshow(
        comparison_data.values,
        x=comparison_data.columns,
        y=comparison_data.index,
        color_continuous_scale="Viridis",
        aspect="auto"
    )
    
    fig.update_layout(
        title="Material Properties Heatmap",
        xaxis_title="Properties",
        yaxis_title="Materials",
        height=500
    )
    
    st.plotly_chart(fig, use_container_width=True)

# ---------------- MATERIAL CARDS ----------------
st.markdown("### 💎 Detailed Material Profiles")

materials = [
    {
        "name": "Gallium Nitride (GaN)",
        "color": "#FF6B6B",
        "advantages": ["Wide bandgap", "High electron mobility", "Excellent thermal stability", "High breakdown field"],
        "applications": ["Power electronics", "RF amplifiers", "LED technology", "5G infrastructure"]
    },
    {
        "name": "Silicon Carbide (SiC)",
        "color": "#4ECDC4", 
        "advantages": ["Very high thermal conductivity", "Excellent mechanical strength", "High temperature operation", "Radiation hardness"],
        "applications": ["High-power devices", "Electric vehicles", "Industrial motors", "Aerospace systems"]
    },
    {
        "name": "Gallium Arsenide (GaAs)",
        "color": "#45B7D1",
        "advantages": ["Extremely high electron mobility", "Direct bandgap", "Excellent RF performance", "Low noise characteristics"],
        "applications": ["Microwave circuits", "Optoelectronics", "Solar cells", "High-frequency devices"]
    },
    {
        "name": "Silicon (Si)",
        "color": "#96CEB4",
        "advantages": ["Mature technology", "Low cost", "Excellent oxide quality", "Abundant raw material"],
        "applications": ["Digital circuits", "Microprocessors", "Memory chips", "Consumer electronics"]
    }
]

cols = st.columns(2)
for i, material in enumerate(materials):
    with cols[i % 2]:
        st.markdown(f"""
        <div class='material-card'>
            <h4 style='color: {material["color"]}; border-bottom: 2px solid {material["color"]}; 
                       padding-bottom: 10px;'>{material['name']}</h4>
            
            <div style='margin: 15px 0;'>
                <h5>🎯 Key Advantages</h5>
                {''.join([f'<div class="property-bar" style="background: {material["color"]};">• {adv}</div>' for adv in material['advantages']])}
            </div>
            
            <div style='margin: 15px 0;'>
                <h5>🚀 Applications</h5>
                {''.join([f'<div style="background: #f8f9fa; padding: 5px 10px; border-radius: 10px; margin: 3px 0; font-size: 0.9em;">• {app}</div>' for app in material['applications']])}
            </div>
        </div>
        """, unsafe_allow_html=True)

# ---------------- PERFORMANCE METRICS ----------------
st.markdown("### 🏆 Performance Scorecard")

# Calculate performance scores (normalized)
performance_metrics = [
    "High Frequency Capability",
    "Power Handling", 
    "Thermal Performance",
    "Voltage Capability",
    "Cost Effectiveness"
]

scores = {
    "GaN": [9, 8, 7, 8, 6],
    "SiC": [7, 9, 9, 9, 5], 
    "GaAs": [10, 5, 4, 4, 4],
    "Si": [5, 6, 6, 5, 10]
}

score_df = pd.DataFrame(scores, index=performance_metrics)

fig = px.bar(
    score_df.T,
    barmode="group",
    title="Material Performance Scorecard (1-10 Scale)",
    color_discrete_sequence=px.colors.qualitative.Set3
)

fig.update_layout(
    xaxis_title="Material",
    yaxis_title="Performance Score",
    template="plotly_white",
    height=500
)

st.plotly_chart(fig, use_container_width=True)

# ---------------- NAVIGATION ----------------
st.markdown("---")
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown("""
    <div style='text-align: center;'>
    <h4>Ready to simulate GaN MOSFET behavior?</h4>
    """, unsafe_allow_html=True)
    if st.button("➡️ Proceed to Simulation Interface", use_container_width=True):
        st.switch_page("pages/3_Simulation_Interface.py")