# Home.py — Professional Landing Page for GaN MOSFET Simulation
# University of Hyderabad — Group 4

import streamlit as st
from PIL import Image

st.set_page_config(
    page_title="GaN MOSFET Simulator - UoH",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---------------- ENHANCED STYLES ----------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

* {
    font-family: 'Inter', sans-serif;
}

@keyframes gradient {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

.main-container {
    background: linear-gradient(-45deg, #667eea, #764ba2, #f093fb, #f5576c);
    background-size: 400% 400%;
    animation: gradient 15s ease infinite;
    min-height: 100vh;
    padding: 20px;
}

.glass-card {
    background: rgba(255, 255, 255, 0.95);
    backdrop-filter: blur(20px);
    border-radius: 20px;
    border: 1px solid rgba(255, 255, 255, 0.2);
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
    padding: 40px;
    margin: 20px 0;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.glass-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 12px 40px rgba(0, 0, 0, 0.15);
}

.header-title {
    font-size: 3.5rem;
    font-weight: 800;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    text-align: center;
    margin-bottom: 10px;
}

.subtitle {
    font-size: 1.3rem;
    color: #6c757d;
    text-align: center;
    margin-bottom: 30px;
    font-weight: 400;
}

.feature-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 25px;
    margin: 40px 0;
}

.feature-card {
    background: white;
    padding: 25px;
    border-radius: 15px;
    text-align: center;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
    transition: all 0.3s ease;
    border: 1px solid #e9ecef;
}

.feature-card:hover {
    transform: translateY(-8px);
    box-shadow: 0 8px 30px rgba(0, 0, 0, 0.12);
}

.feature-icon {
    font-size: 2.5rem;
    margin-bottom: 15px;
}

.team-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 20px;
    margin: 30px 0;
}

.team-card {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 20px;
    border-radius: 15px;
    text-align: center;
    transition: transform 0.3s ease;
}

.team-card:hover {
    transform: scale(1.05);
}

.start-btn {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border: none;
    padding: 15px 40px;
    font-size: 1.2rem;
    font-weight: 600;
    border-radius: 50px;
    cursor: pointer;
    transition: all 0.3s ease;
    box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    width: 100%;
}

.start-btn:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
}

.university-info {
    background: linear-gradient(135deg, #f8f9fa, #e9ecef);
    padding: 20px;
    border-radius: 15px;
    margin: 20px 0;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

# ---------------- HEADER SECTION ----------------
st.markdown("""
<div class="main-container">
    <div class="glass-card">
        <div style="text-align: center; margin-bottom: 40px;">
            <div class="header-title">
                🚀 GaN MOSFET Interactive Simulator
            </div>
            <div class="subtitle">
                Advanced Visualization & Analysis Platform for Semiconductor Materials
            </div>
        </div>
""", unsafe_allow_html=True)

# University Info
st.markdown("""
<div class="university-info">
    <h3 style="color: #2c3e50; margin-bottom: 15px;">🎓 University of Hyderabad</h3>
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 15px;">
        <div>
            <p style="color: #6c757d; margin: 5px 0;"><strong>Course:</strong> Semiconductor Materials</p>
            <p style="color: #6c757d; margin: 5px 0;"><strong>Faculty:</strong> Dr. Raj Kishora Dash</p>
        </div>
        <div>
            <p style="color: #6c757d; margin: 5px 0;"><strong>Team:</strong> Group 4</p>
            <p style="color: #6c757d; margin: 5px 0;"><strong>Project:</strong> GaN MOSFET Analysis</p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ---------------- FEATURE GRID ----------------
st.markdown("""
<div class="feature-grid">
    <div class="feature-card">
        <div class="feature-icon">📊</div>
        <h3>Real-time Simulation</h3>
        <p>Interactive GaN MOSFET simulation with live parameter control and instant visualization</p>
    </div>
    <div class="feature-card">
        <div class="feature-icon">🔬</div>
        <h3>Material Analysis</h3>
        <p>Compare GaN, SiC, GaAs, and Si properties with detailed parameter comparisons</p>
    </div>
    <div class="feature-card">
        <div class="feature-icon">📈</div>
        <h3>Advanced Visualization</h3>
        <p>3D plots, temperature dependencies, and breakdown voltage analysis</p>
    </div>
    <div class="feature-card">
        <div class="feature-icon">🧮</div>
        <h3>Physics-Based Models</h3>
        <p>Accurate semiconductor physics with Varshni equation and mobility models</p>
    </div>
</div>
""", unsafe_allow_html=True)

# ---------------- TEAM SECTION ----------------
st.markdown("### 👥 Project Team - Group 4")
st.markdown("<div class='team-grid'>", unsafe_allow_html=True)

members = [
    ("Maddela Bhargav", "24ETIM18", "Team Lead"),
    ("Karangula Sai Nikhil", "24ETIM20", "Simulation Expert"),
    ("Gourav Kumar Singh", "24ETIM21", "Data Analyst"),
    ("Raj Gupta", "24ETIM22", "UI/UX Developer"),
    ("Rahul Kumar", "24ETIM23", "Documentation")
]

for name, reg, role in members:
    st.markdown(f"""
    <div class='team-card'>
        <h4 style='margin: 0 0 10px 0;'>{name}</h4>
        <p style='margin: 5px 0; font-size: 0.9em;'>{reg}</p>
        <p style='margin: 5px 0; font-size: 0.8em; opacity: 0.9;'>{role}</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# ---------------- START BUTTON ----------------
st.markdown("""
<div style="text-align: center; margin: 50px 0 20px 0;">
    <h3 style="color: #2c3e50; margin-bottom: 20px;">Ready to Explore GaN MOSFET Technology?</h3>
""", unsafe_allow_html=True)

if st.button("🚀 Launch Simulation Dashboard", key="start_btn", use_container_width=True):
    st.switch_page("pages/1_Theory_and_Working.py")

st.markdown("""
</div>
</div>
</div>
""", unsafe_allow_html=True)