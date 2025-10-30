# pages/1_Theory_and_Working.py
# Enhanced Theory and Working Page with Professional Design

import streamlit as st
from PIL import Image
import base64

st.set_page_config(page_title="Theory & Working - GaN MOSFET", layout="wide")

# ---------------- ENHANCED STYLES ----------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

* {
    font-family: 'Inter', sans-serif;
}

.page-title {
    font-size: 2.8rem;
    font-weight: 800;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    text-align: center;
    margin-bottom: 20px;
}

.section-header {
    color: #2c3e50;
    font-size: 1.8rem;
    font-weight: 700;
    margin: 40px 0 20px 0;
    padding-bottom: 10px;
    border-bottom: 3px solid #667eea;
}

.sub-section {
    color: #34495e;
    font-size: 1.3rem;
    font-weight: 600;
    margin: 30px 0 15px 0;
}

.highlight-box {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 25px;
    border-radius: 15px;
    margin: 20px 0;
    box-shadow: 0 6px 20px rgba(102, 126, 234, 0.3);
}

.formula-card {
    background: #f8f9fa;
    border-left: 5px solid #667eea;
    padding: 20px;
    border-radius: 10px;
    margin: 15px 0;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
}

.feature-point {
    background: white;
    padding: 15px;
    border-radius: 10px;
    margin: 10px 0;
    border-left: 4px solid #27ae60;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
}

.animation-container {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 30px;
    border-radius: 15px;
    color: white;
    text-align: center;
    margin: 20px 0;
}
</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown("<div class='page-title'>📘 GaN MOSFET Theory & Working Principle</div>", unsafe_allow_html=True)
st.markdown("---")

# ---------------- INTRODUCTION SECTION ----------------
st.markdown("<div class='section-header'>🔬 Introduction to GaN MOSFET Technology</div>", unsafe_allow_html=True)

col1, col2 = st.columns([2, 1])
with col1:
    st.markdown("""
    <div style='text-align: justify; line-height: 1.6;'>
    **Gallium Nitride (GaN) MOSFETs** represent a revolutionary advancement in power semiconductor technology. 
    Unlike traditional silicon-based devices, GaN MOSFETs leverage the unique material properties of 
    compound semiconductors to achieve unprecedented performance in power efficiency, switching speed, 
    and thermal stability.
    
    ### 🎯 Key Advantages:
    - **Wide Bandgap (3.4 eV)** enabling high-temperature operation
    - **High Electron Mobility** for faster switching speeds
    - **Superior Thermal Conductivity** for better heat dissipation
    - **High Breakdown Electric Field** for robust high-voltage operation
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class='highlight-box'>
    <h4 style='margin: 0; color: white;'>🚀 Performance Metrics</h4>
    <p style='margin: 10px 0;'>• Switching Frequency: 10-100x Si</p>
    <p style='margin: 10px 0;'>• Power Density: 3-5x Si</p>
    <p style='margin: 10px 0;'>• Operating Temperature: >200°C</p>
    <p style='margin: 10px 0;'>• Breakdown Voltage: 600V+</p>
    </div>
    """, unsafe_allow_html=True)

# ---------------- STRUCTURE VISUALIZATION ----------------
st.markdown("<div class='section-header'>🏗️ Device Structure & Architecture</div>", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class='sub-section'>🔍 Cross-Sectional View</div>
    
    GaN MOSFETs feature a sophisticated layered structure:
    
    <div class='feature-point'>
    <strong>Gate Terminal</strong><br>
    Controls electron flow through the channel with applied voltage
    </div>
    
    <div class='feature-point'>
    <strong>AlGaN Barrier Layer</strong><br>
    Creates polarization-induced 2D Electron Gas (2DEG)
    </div>
    
    <div class='feature-point'>
    <strong>GaN Channel Layer</strong><br>
    High-mobility electron transport region
    </div>
    
    <div class='feature-point'>
    <strong>Buffer/Substrate</strong><br>
    Typically SiC or Si for thermal management
    </div>
    """, unsafe_allow_html=True)

with col2:
    # Placeholder for MOSFET structure image
    try:
        img = Image.open("assets/mosfet_layers.png")
        st.image(img, caption="Enhanced GaN MOSFET Cross-Section", use_column_width=True)
    except:
        st.info("📷 *MOSFET structure visualization would appear here*")

# ---------------- WORKING PRINCIPLE ----------------
st.markdown("<div class='section-header'>⚡ Working Principle & Operation</div>", unsafe_allow_html=True)

st.markdown("""
<div style='background: linear-gradient(135deg, #74b9ff, #0984e3); padding: 25px; border-radius: 15px; color: white;'>
<h4 style='color: white; margin-top: 0;'>🎯 Operational States</h4>
</div>
""", unsafe_allow_html=True)

# Operation States
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div style='text-align: center; padding: 20px; background: #e8f5e8; border-radius: 10px;'>
    <div style='font-size: 2rem; margin-bottom: 10px;'>🛑</div>
    <h4>Cut-off Region</h4>
    <p><strong>V<sub>GS</sub> < V<sub>TH</sub></strong></p>
    <p>Channel is OFF<br>No current flow<br>High impedance state</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div style='text-align: center; padding: 20px; background: #fff3cd; border-radius: 10px;'>
    <div style='font-size: 2rem; margin-bottom: 10px;'>📈</div>
    <h4>Linear Region</h4>
    <p><strong>V<sub>GS</sub> > V<sub>TH</sub></strong><br><strong>V<sub>DS</sub> small</strong></p>
    <p>Channel acts as resistor<br>Current proportional to V<sub>DS</sub></p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div style='text-align: center; padding: 20px; background: #d4edda; border-radius: 10px;'>
    <div style='font-size: 2rem; margin-bottom: 10px;'>💨</div>
    <h4>Saturation Region</h4>
    <p><strong>V<sub>GS</sub> > V<sub>TH</sub></strong><br><strong>V<sub>DS</sub> > V<sub>GS</sub> - V<sub>TH</sub></strong></p>
    <p>Channel pinches off<br>Constant current flow<br>Amplification region</p>
    </div>
    """, unsafe_allow_html=True)

# ---------------- MATHEMATICAL MODEL ----------------
st.markdown("<div class='section-header'>🧮 Mathematical Foundation</div>", unsafe_allow_html=True)

st.markdown("""
<div class='formula-card'>
<h4>1. Drain Current Equation (Square Law Model)</h4>
$$ I_D = \\frac{1}{2} \\mu_n C_{ox} \\frac{W}{L} (V_{GS} - V_{TH})^2 (1 + \\lambda V_{DS}) $$
<p><strong>Where:</strong> μₙ = Electron mobility, Cₒₓ = Oxide capacitance, W/L = Aspect ratio, λ = Channel-length modulation</p>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class='formula-card'>
    <h4>2. Mobility Temperature Dependence</h4>
    $$ \\mu(T) = \\mu_0 \\left(\\frac{300}{T}\\right)^{1.5} $$
    <p>Electron mobility decreases with temperature due to increased lattice scattering</p>
    </div>
    
    <div class='formula-card'>
    <h4>3. Varshni Equation (Bandgap Temperature Dependence)</h4>
    $$ E_g(T) = E_{g0} - \\frac{\\alpha T^2}{T + \\beta} $$
    <p>Bandgap decreases slightly with increasing temperature</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class='formula-card'>
    <h4>4. Breakdown Voltage Model</h4>
    $$ BV \\propto E_g^{2.5} $$
    <p>Higher bandgap materials exhibit significantly higher breakdown voltages</p>
    </div>
    
    <div class='formula-card'>
    <h4>5. Thermal Power Dissipation</h4>
    $$ P_{diss} = I_D \\times V_{DS} $$
    <p>Power dissipation determines thermal management requirements</p>
    </div>
    """, unsafe_allow_html=True)

# ---------------- APPLICATIONS ----------------
st.markdown("<div class='section-header'>🌍 Real-World Applications</div>", unsafe_allow_html=True)

apps = [
    ("⚡ Power Conversion", "EV chargers, SMPS, inverters with >99% efficiency"),
    ("📡 RF Amplifiers", "5G base stations, radar systems, satellite communication"),
    ("🔋 Automotive", "Electric vehicles, battery management systems"),
    ("💡 Lighting", "High-efficiency LED drivers, industrial lighting"),
    ("🖥️ Computing", "Server power supplies, data center infrastructure")
]

cols = st.columns(3)
for i, (title, desc) in enumerate(apps):
    with cols[i % 3]:
        st.markdown(f"""
        <div style='background: white; padding: 15px; border-radius: 10px; margin: 10px 0; 
                    border-left: 4px solid #667eea; box-shadow: 0 2px 8px rgba(0,0,0,0.1);'>
        <h5 style='margin: 0 0 10px 0; color: #2c3e50;'>{title}</h5>
        <p style='margin: 0; font-size: 0.9em; color: #6c757d;'>{desc}</p>
        </div>
        """, unsafe_allow_html=True)

# ---------------- NAVIGATION ----------------
st.markdown("---")
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown("""
    <div style='text-align: center;'>
    <h4>Ready to explore material properties?</h4>
    """, unsafe_allow_html=True)
    if st.button("➡️ Continue to Material Properties", use_container_width=True):
        st.switch_page("pages/2_Material_Properties.py")