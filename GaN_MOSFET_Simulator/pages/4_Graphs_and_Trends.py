# pages/4_Graphs_and_Trends.py
# Enhanced Graphs & Trends with Fixed PDF Generation

import streamlit as st
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from io import BytesIO
from fpdf import FPDF
import re

st.set_page_config(page_title="Graphs & Trends - GaN MOSFET", layout="wide")

# ---------------- ENHANCED STYLES ----------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

* {
    font-family: 'Inter', sans-serif;
}

.title {
    font-size: 2.8rem;
    font-weight: 800;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    text-align: center;
    margin-bottom: 20px;
}

.section {
    color: #2c3e50;
    font-size: 1.5rem;
    font-weight: 700;
    margin: 40px 0 20px 0;
    padding-bottom: 10px;
    border-bottom: 3px solid #667eea;
}

.sub {
    font-size: 1.1rem;
    color: #5d6d7e;
    margin-top: 8px;
}

.graph-container {
    background: white;
    padding: 20px;
    border-radius: 15px;
    margin: 15px 0;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
    border: 1px solid #e9ecef;
}
</style>
""", unsafe_allow_html=True)

st.markdown("<div class='title'>📊 Advanced Graphs & Trends Analysis</div>", unsafe_allow_html=True)
st.markdown("---")

# ---------------- INPUT CONTROLS ----------------
st.sidebar.header("🎛️ Simulation Parameters")
mu_base = st.sidebar.slider("Base Mobility μ₀ (cm²/V·s)", 500, 3000, 1500, 50)
Eg_base = st.sidebar.slider("Base Bandgap Eg₀ (eV)", 3.0, 4.0, 3.4, 0.05)
Vgs_sim = st.sidebar.slider("Gate Voltage Vgs (V)", 0.0, 10.0, 5.0, 0.1)

# ---------------- ENHANCED COMPUTATION FUNCTIONS ----------------
def mobility_temp_dep(mu_0, T_celsius):
    T_kelvin = T_celsius + 273.15
    return mu_0 * (300 / T_kelvin)**1.5

def bandgap_temp_dep(Eg_0, T_celsius):
    T_kelvin = T_celsius + 273.15
    alpha = 0.909e-3
    beta = 830
    return Eg_0 - (alpha * T_kelvin**2) / (T_kelvin + beta)

def breakdown_voltage_model(Eg):
    return 350 * (Eg / 3.4)**2.5

def drain_current_model(mu_eff, Vgs, Vds, Vth=2.0, W=100e-6, L=1e-6, Cox=1.5e-6):
    beta = mu_eff * Cox * (W/L) * 1e-4
    Vds_sat = Vgs - Vth
    
    Id_linear = beta * ((Vgs - Vth) * Vds - 0.5 * Vds**2)
    Id_sat = 0.5 * beta * (Vgs - Vth)**2 * (1 + 0.02 * Vds)
    
    Id = np.where(Vds < Vds_sat, Id_linear, Id_sat)
    Id = np.where(Vgs < Vth, 1e-12, Id)
    
    return np.maximum(Id, 1e-12)

# ---------------- DATA GENERATION ----------------
# Temperature range data
T_range = np.linspace(25, 300, 80)
mu_T = [mobility_temp_dep(mu_base, T) for T in T_range]
Eg_T = [bandgap_temp_dep(Eg_base, T) for T in T_range]
BV_Eg_T = [breakdown_voltage_model(Eg) for Eg in Eg_T]

# 3D Surface data
VGS_range = np.linspace(0, 10, 40)
VDS_range = np.linspace(0, 200, 40)
VGS_grid, VDS_grid = np.meshgrid(VGS_range, VDS_range)
ID_grid = drain_current_model(mu_base, VGS_grid, VDS_grid)

# ---------------- ENHANCED PLOTS ----------------
st.markdown("<div class='section'>🎯 3D Performance Surface Analysis</div>", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    # 3D I-V surface
    st.markdown("<div class='graph-container'>", unsafe_allow_html=True)
    fig_3d = go.Figure(data=[go.Surface(
        x=VGS_grid, y=VDS_grid, z=ID_grid*1000,
        colorscale="Viridis",
        showscale=True,
        hovertemplate="Vgs: %{x:.1f} V<br>Vds: %{y:.1f} V<br>Id: %{z:.2f} mA<extra></extra>"
    )])
    
    fig_3d.update_layout(
        scene=dict(
            xaxis_title="Vgs (V)",
            yaxis_title="Vds (V)", 
            zaxis_title="Id (mA)",
            camera=dict(eye=dict(x=1.5, y=1.5, z=1.2))
        ),
        title="3D I-V Characteristics Surface",
        height=500,
        template="plotly_white"
    )
    st.plotly_chart(fig_3d, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    # Mobility vs Temperature
    st.markdown("<div class='graph-container'>", unsafe_allow_html=True)
    fig_mobility = go.Figure()
    fig_mobility.add_trace(go.Scatter(
        x=T_range, y=mu_T, 
        mode="lines", 
        line=dict(color="#e74c3c", width=4),
        name="Mobility",
        hovertemplate="Temp: %{x}°C<br>Mobility: %{y:.0f} cm²/V·s<extra></extra>"
    ))
    
    fig_mobility.update_layout(
        title="Electron Mobility vs Temperature",
        xaxis_title="Temperature (°C)",
        yaxis_title="Mobility (cm²/V·s)",
        template="plotly_white",
        height=500,
        showlegend=True
    )
    st.plotly_chart(fig_mobility, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# Second row of plots
st.markdown("<div class='section'>📈 Temperature & Material Dependencies</div>", unsafe_allow_html=True)

col3, col4 = st.columns(2)

with col3:
    # Bandgap vs Temperature
    st.markdown("<div class='graph-container'>", unsafe_allow_html=True)
    fig_bandgap = go.Figure()
    fig_bandgap.add_trace(go.Scatter(
        x=T_range, y=Eg_T,
        mode="lines",
        line=dict(color="#2ecc71", width=4),
        name="Bandgap",
        hovertemplate="Temp: %{x}°C<br>Bandgap: %{y:.3f} eV<extra></extra>"
    ))
    
    fig_bandgap.update_layout(
        title="Bandgap vs Temperature",
        xaxis_title="Temperature (°C)",
        yaxis_title="Bandgap (eV)",
        template="plotly_white",
        height=450,
        showlegend=True
    )
    st.plotly_chart(fig_bandgap, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

with col4:
    # Breakdown Voltage vs Bandgap & Quick Id @ selected Vgs
    st.markdown("<div class='graph-container'>", unsafe_allow_html=True)
    fig_bv = go.Figure()
    fig_bv.add_trace(go.Scatter(
        x=Eg_T, y=BV_Eg_T,
        mode="lines+markers",
        line=dict(color="#34495e", width=3),
        marker=dict(size=6, color="#34495e"),
        name="Breakdown Voltage",
        hovertemplate="Bandgap: %{x:.3f} eV<br>BV: %{y:.1f} V<extra></extra>"
    ))
    fig_bv.update_layout(
        title="Estimated Breakdown Voltage vs Bandgap (GaN)",
        xaxis_title="Bandgap (eV)",
        yaxis_title="Estimated BV (V)",
        template="plotly_white",
        height=300,
        showlegend=True
    )
    st.plotly_chart(fig_bv, use_container_width=True)

    st.markdown("---")

    # Small table / quick calculation for Id vs Vds at selected Vgs
    st.subheader("Quick I-V at selected Vgs")
    Vgs_val = float(Vgs_sim)
    Vds_sample = np.linspace(0, 100, 201)
    Id_sample = drain_current_model(mu_base, Vgs_val, Vds_sample)
    fig_iv = go.Figure()
    fig_iv.add_trace(go.Scatter(
        x=Vds_sample, y=Id_sample * 1000,
        mode="lines",
        line=dict(color="#9b59b6", width=3),
        name=f"Id @ Vgs={Vgs_val:.1f} V",
        hovertemplate="Vds: %{x:.1f} V<br>Id: %{y:.3f} mA<extra></extra>"
    ))
    fig_iv.update_layout(
        title=f"I-V Curve (Vgs={Vgs_val:.1f} V)",
        xaxis_title="Vds (V)",
        yaxis_title="Id (mA)",
        template="plotly_white",
        height=300,
        showlegend=True
    )
    st.plotly_chart(fig_iv, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ---------------- FIXED PDF GENERATION ----------------
st.markdown("<div class='section'>🧾 Export Summary Report</div>", unsafe_allow_html=True)

# Prepare summary metrics
max_mu = float(np.max(mu_T))
min_Eg = float(np.min(Eg_T))
max_BV = float(np.max(BV_Eg_T))

st.write("Summary metrics computed from the current simulation parameters:")
st.metric("Max Mobility (cm²/V·s)", f"{max_mu:.1f}")
st.metric("Min Bandgap (eV)", f"{min_Eg:.3f}")
st.metric("Max Estimated BV (V)", f"{max_BV:.1f}")

# FIXED: Create PDF with proper encoding
class SafePDF(FPDF):
    def safe_text(self, text):
        """Clean text to avoid encoding issues"""
        # Replace problematic characters
        replacements = {
            '•': '-', '–': '-', '—': '-', '“': '"', '”': '"', 
            '‘': "'", '’': "'", '°': ' deg', '×': 'x', '÷': '/',
            'μ': 'u', '²': '2', '₀': '0', '₁': '1', '₂': '2',
            '₃': '3', '₄': '4', '₅': '5', '₆': '6', '₇': '7',
            '₈': '8', '₉': '9'
        }
        for old, new in replacements.items():
            text = text.replace(old, new)
        return text

def create_safe_pdf(mu_max, eg_min, bv_max, Vgs_val, mu_base, Eg_base):
    pdf = SafePDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    
    # Header
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, pdf.safe_text("GaN MOSFET Simulation Summary"), ln=True, align='C')
    pdf.ln(6)

    # Parameters
    pdf.set_font("Arial", size=12)
    pdf.cell(0, 8, pdf.safe_text(f"Base mobility μ₀: {mu_base} cm²/V·s"), ln=True)
    pdf.cell(0, 8, pdf.safe_text(f"Base bandgap Eg₀: {Eg_base:.3f} eV"), ln=True)
    pdf.cell(0, 8, pdf.safe_text(f"Selected Vgs for quick I-V: {Vgs_val:.2f} V"), ln=True)
    pdf.ln(4)

    # Computed Metrics
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 8, pdf.safe_text("Computed Metrics:"), ln=True)
    pdf.set_font("Arial", size=12)
    pdf.cell(0, 8, pdf.safe_text(f"- Maximum mobility (over T): {mu_max:.2f} cm²/V·s"), ln=True)
    pdf.cell(0, 8, pdf.safe_text(f"- Minimum bandgap (over T): {eg_min:.4f} eV"), ln=True)
    pdf.cell(0, 8, pdf.safe_text(f"- Maximum estimated breakdown voltage: {bv_max:.2f} V"), ln=True)
    pdf.ln(6)

    # Notes
    pdf.set_font("Arial", size=10)
    notes = pdf.safe_text(
        "Notes: This report contains a brief summary of the current simulation run. "
        "For reproducible high-fidelity reports with embedded plots, ensure image-generation "
        "dependencies (kaleido / orca) are installed and adjust the exporter to embed PNGs."
    )
    pdf.multi_cell(0, 6, notes)
    
    return pdf.output(dest='S').encode('latin-1', 'ignore')

# Generate and download PDF
try:
    pdf_bytes = create_safe_pdf(max_mu, min_Eg, max_BV, Vgs_val, mu_base, Eg_base)
    
    st.download_button(
        label="📄 Download Summary PDF",
        data=pdf_bytes,
        file_name="GaN_MOSFET_Summary.pdf",
        mime="application/pdf"
    )
    st.success("✅ PDF generation successful! Click to download.")
    
except Exception as e:
    st.error(f"❌ PDF generation failed: {str(e)}")
    st.info("💡 Try installing required dependencies: pip install fpdf")

# ---------------- NAVIGATION ----------------
st.markdown("---")
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown("""
    <div style='text-align: center;'>
        <h4>Continue Exploring</h4>
    </div>
    """, unsafe_allow_html=True)
    
    col_left, col_right = st.columns(2)
    with col_left:
        if st.button("⬅️ Back to Simulation", use_container_width=True):
            st.switch_page("pages/3_Simulation_Interface.py")
    with col_right:
        if st.button("References ➡️", use_container_width=True):
            st.switch_page("pages/5_Formulas_and_References.py")

st.info("💡 Tip: Adjust simulation parameters in the sidebar and re-download the summary report.")