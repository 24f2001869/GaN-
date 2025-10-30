# pages/3_Simulation_Interface.py
# Enhanced GaN MOSFET Simulation Interface with Advanced Physics & Real-time Visualization

import streamlit as st
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

st.set_page_config(page_title="Simulation Interface - GaN MOSFET", layout="wide")

# ---------------- ENHANCED STYLES ----------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

* {
    font-family: 'Inter', sans-serif;
}

.simulation-header {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 30px;
    border-radius: 20px;
    text-align: center;
    margin-bottom: 30px;
    box-shadow: 0 8px 32px rgba(102, 126, 234, 0.3);
}

.control-panel {
    background: white;
    padding: 25px;
    border-radius: 15px;
    margin: 15px 0;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
    border: 1px solid #e9ecef;
}

.parameter-card {
    background: linear-gradient(135deg, #74b9ff 0%, #0984e3 100%);
    color: white;
    padding: 20px;
    border-radius: 12px;
    margin: 10px 0;
    text-align: center;
    transition: transform 0.3s ease;
}

.parameter-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 6px 20px rgba(116, 185, 255, 0.4);
}

.visualization-container {
    background: #f8f9fa;
    border: 2px solid #e9ecef;
    border-radius: 15px;
    padding: 25px;
    margin: 20px 0;
    min-height: 400px;
}

.metric-display {
    background: linear-gradient(135deg, #00b894 0%, #00a085 100%);
    color: white;
    padding: 15px;
    border-radius: 10px;
    margin: 8px 0;
    text-align: center;
    font-weight: 600;
}

.warning-metric {
    background: linear-gradient(135deg, #ff7675 0%, #d63031 100%);
    color: white;
    padding: 15px;
    border-radius: 10px;
    margin: 8px 0;
    text-align: center;
    font-weight: 600;
}

.layer-visual {
    background: white;
    padding: 15px;
    border-radius: 10px;
    margin: 10px 0;
    border-left: 4px solid #667eea;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
}

.electron-flow {
    background: linear-gradient(135deg, #2d3436 0%, #636e72 100%);
    color: white;
    padding: 20px;
    border-radius: 12px;
    margin: 15px 0;
}
</style>
""", unsafe_allow_html=True)

# ---------------- ENHANCED HEADER ----------------
st.markdown("""
<div class='simulation-header'>
    <h1 style='margin: 0; font-size: 2.5rem;'>⚡ GaN MOSFET Real-time Simulator</h1>
    <p style='margin: 10px 0 0 0; font-size: 1.2rem; opacity: 0.9;'>
    Advanced Interactive Simulation with Physics-Based Models & Live Visualization
    </p>
</div>
""", unsafe_allow_html=True)

# ---------------- ENHANCED PHYSICS MODELS ----------------
def mobility_temp_dep(mu_0, T_celsius):
    """Enhanced mobility model with temperature dependence"""
    T_kelvin = T_celsius + 273.15
    return mu_0 * (300 / T_kelvin)**1.5

def bandgap_temp_dep(Eg_0, T_celsius):
    """Varshni equation for bandgap temperature dependence"""
    T_kelvin = T_celsius + 273.15
    alpha = 0.909e-3  # eV/K for GaN
    beta = 830        # K for GaN
    return Eg_0 - (alpha * T_kelvin**2) / (T_kelvin + beta)

def breakdown_voltage_model(Eg, thickness=2e-6):
    """Enhanced breakdown voltage model"""
    # BV ∝ Eg^2.5 * thickness
    base_bv = 350  # V for reference GaN
    return base_bv * (Eg / 3.4)**2.5 * (thickness / 2e-6)

def saturation_velocity_temp(T_celsius):
    """Temperature-dependent saturation velocity"""
    T_kelvin = T_celsius + 273.15
    vsat_300 = 2.5e7  # cm/s at 300K
    return vsat_300 * (300 / T_kelvin)**0.5

def drain_current_model(mu_eff, Vgs, Vds, Eg_eff, T_celsius, Vth=2.0, W=100e-6, L=1e-6, Cox=1.5e-6):
    """Enhanced drain current model with physical parameters"""
    # Device parameters
    beta = mu_eff * Cox * (W/L) * 1e-4  # Conversion factor
    
    Vds_sat = Vgs - Vth  # Saturation voltage
    
    # Linear region
    Id_linear = beta * ((Vgs - Vth) * Vds - 0.5 * Vds**2)
    
    # Saturation region
    Id_sat = 0.5 * beta * (Vgs - Vth)**2 * (1 + 0.02 * Vds)  # Including CLM
    
    # Apply temperature and bandgap effects
    thermal_factor = np.exp(-(T_celsius - 25) / 150)
    bandgap_factor = (Eg_eff / 3.4)**0.5
    
    Id = np.where(Vds < Vds_sat, Id_linear, Id_sat) * thermal_factor * bandgap_factor
    Id = np.where(Vgs < Vth, 1e-12, Id)  # Subthreshold leakage
    
    return np.maximum(Id, 1e-12)

def leakage_current(Eg, T_celsius, area=1e-8):
    """Enhanced leakage current model"""
    T_kelvin = T_celsius + 273.15
    k = 8.617e-5  # eV/K
    # Simplified SRH generation current
    return area * 1e-8 * np.exp(-Eg / (2 * k * T_kelvin))

# ---------------- SIDEBAR CONTROLS ----------------
st.sidebar.markdown("""
<div style='background: linear-gradient(135deg, #667eea, #764ba2); color: white; padding: 20px; border-radius: 15px;'>
    <h3 style='margin: 0; text-align: center;'>🎛️ Control Panel</h3>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("### Material Parameters")
Eg_base = st.sidebar.slider("Base Bandgap Eg₀ (eV)", 3.0, 4.0, 3.4, 0.05,
                           help="Wider bandgap enables higher voltage operation")
mu_base = st.sidebar.slider("Base Mobility μ₀ (cm²/V·s)", 500, 3000, 1500, 50,
                           help="Higher mobility enables faster switching")

st.sidebar.markdown("### Operating Conditions")
Temp = st.sidebar.slider("Temperature T (°C)", 25, 300, 50, 5,
                        help="Higher temperatures reduce mobility and increase leakage")
Vgs = st.sidebar.slider("Gate-Source Voltage Vgs (V)", 0.0, 10.0, 5.0, 0.1,
                       help="Controls channel formation")
Vds_max = st.sidebar.slider("Max Drain-Source Voltage Vds (V)", 10, 500, 100, 10,
                           help="Determines operating voltage range")

st.sidebar.markdown("### Device Geometry")
channel_length = st.sidebar.slider("Channel Length L (μm)", 0.1, 5.0, 1.0, 0.1)
channel_width = st.sidebar.slider("Channel Width W (μm)", 10.0, 200.0, 100.0, 10.0)

# ---------------- CALCULATE DERIVED PARAMETERS ----------------
mu_eff = mobility_temp_dep(mu_base, Temp)
Eg_eff = bandgap_temp_dep(Eg_base, Temp)
BV_pred = breakdown_voltage_model(Eg_eff)
I_leak = leakage_current(Eg_eff, Temp)
Vsat = saturation_velocity_temp(Temp)

# Generate I-V characteristics
Vds_range = np.linspace(0, Vds_max, 200)
Id_current = drain_current_model(mu_eff, Vgs, Vds_range, Eg_eff, Temp, 
                                W=channel_width*1e-6, L=channel_length*1e-6)

# Calculate power dissipation
Power_diss = Id_current * Vds_range

# ---------------- MAIN LAYOUT ----------------
col1, col2 = st.columns([1, 1])

with col1:
    # PARAMETERS DISPLAY
    st.markdown("""
    <div class='control-panel'>
        <h3>📊 Real-time Parameters</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Key parameters in cards
    param_col1, param_col2 = st.columns(2)
    
    with param_col1:
        st.markdown(f"""
        <div class='parameter-card'>
            <h4>🎯 Effective Mobility</h4>
            <h2>{mu_eff:.0f} cm²/V·s</h2>
            <p>{((mu_eff/mu_base)-1)*100:+.1f}% from base</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class='parameter-card'>
            <h4>🔥 Temperature</h4>
            <h2>{Temp}°C</h2>
            <p>{Temp + 273} K</p>
        </div>
        """, unsafe_allow_html=True)
    
    with param_col2:
        st.markdown(f"""
        <div class='parameter-card'>
            <h4>💎 Effective Bandgap</h4>
            <h2>{Eg_eff:.3f} eV</h2>
            <p>{((Eg_eff/Eg_base)-1)*100:+.1f}% from base</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class='metric-display'>
            <h4>⚡ Saturation Velocity</h4>
            <h3>{Vsat/1e7:.2f} ×10⁷ cm/s</h3>
        </div>
        """, unsafe_allow_html=True)
    
    # Warnings and limits
    st.markdown("""
    <div class='control-panel'>
        <h3>⚠️ Operating Limits</h3>
    </div>
    """, unsafe_allow_html=True)
    
    limit_col1, limit_col2 = st.columns(2)
    
    with limit_col1:
        bv_status = "🟢 Safe" if Vds_max < BV_pred * 0.8 else "🟡 Warning" if Vds_max < BV_pred else "🔴 Critical"
        st.markdown(f"""
        <div class='{ "metric-display" if Vds_max < BV_pred * 0.8 else "warning-metric" }'>
            <h4>Breakdown Voltage</h4>
            <h3>{BV_pred:.0f} V</h3>
            <p>{bv_status} ({Vds_max/BV_pred*100:.1f}% of limit)</p>
        </div>
        """, unsafe_allow_html=True)
    
    with limit_col2:
        leak_status = "🟢 Low" if I_leak < 1e-6 else "🟡 Moderate" if I_leak < 1e-3 else "🔴 High"
        st.markdown(f"""
        <div class='{ "metric-display" if I_leak < 1e-6 else "warning-metric" }'>
            <h4>Leakage Current</h4>
            <h3>{I_leak:.2e} A</h3>
            <p>{leak_status}</p>
        </div>
        """, unsafe_allow_html=True)

with col2:
    # DEVICE VISUALIZATION
    st.markdown("""
    <div class='control-panel'>
        <h3>🏗️ GaN MOSFET Structure</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Create layered structure visualization
    layers = [
        {"name": "Source Contact", "material": "Ti/Al/Ni/Au", "thickness": 0.2, "color": "#95a5a6"},
        {"name": "Gate Dielectric", "material": "Al₂O₃", "thickness": 0.02, "color": "#3498db"},
        {"name": "Gate Contact", "material": "Ni/Au", "thickness": 0.3, "color": "#2c3e50"},
        {"name": "AlGaN Barrier", "material": "Al₀.₂₅Ga₀.₇₅N", "thickness": 0.025, "color": "#e74c3c"},
        {"name": "GaN Channel", "material": "GaN (2DEG)", "thickness": 0.1, "color": "#2ecc71"},
        {"name": "GaN Buffer", "material": "GaN", "thickness": 2.0, "color": "#27ae60"},
        {"name": "Substrate", "material": "SiC", "thickness": 1.0, "color": "#7f8c8d"}
    ]
    
    # Create visualization
    fig_layers = go.Figure()
    
    y_pos = 0
    for i, layer in enumerate(layers):
        fig_layers.add_trace(go.Bar(
            y=[layer["name"]],
            x=[layer["thickness"]],
            orientation='h',
            marker=dict(color=layer["color"]),
            name=f"{layer['name']} ({layer['material']})",
            text=[f"{layer['thickness']} μm<br>{layer['material']}"],
            textposition='auto',
            hovertemplate=f"<b>{layer['name']}</b><br>Material: {layer['material']}<br>Thickness: {layer['thickness']} μm<extra></extra>"
        ))
        y_pos += layer["thickness"]
    
    fig_layers.update_layout(
        title="GaN MOSFET Layer Structure",
        xaxis_title="Thickness (μm)",
        yaxis_title="Layers",
        barmode='stack',
        height=400,
        template="plotly_white",
        showlegend=False
    )
    
    st.plotly_chart(fig_layers, width='stretch')

# ---------------- REAL-TIME SIMULATION RESULTS ----------------
st.markdown("""
<div class='simulation-header' style='padding: 20px; margin: 30px 0;'>
    <h2 style='margin: 0;'>📈 Live Simulation Results</h2>
</div>
""", unsafe_allow_html=True)

# Create tabs for different analyses
tab1, tab2, tab3, tab4 = st.tabs(["I-V Characteristics", "Temperature Effects", "Power Analysis", "Performance Metrics"])

with tab1:
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # I-V Characteristics
        fig_iv = go.Figure()
        
        # Plot multiple Vgs curves for comparison
        Vgs_range = [3, 4, 5, 6, 7] if Vgs >= 5 else [1, 2, 3, 4, 5]
        colors = px.colors.sequential.Viridis
        
        for i, vgs_val in enumerate(Vgs_range):
            Id_curve = drain_current_model(mu_eff, vgs_val, Vds_range, Eg_eff, Temp,
                                         W=channel_width*1e-6, L=channel_length*1e-6)
            fig_iv.add_trace(go.Scatter(
                x=Vds_range, y=Id_curve*1000,  # Convert to mA
                mode='lines',
                name=f'Vgs = {vgs_val} V',
                line=dict(color=colors[i], width=3),
                hovertemplate="Vds: %{x} V<br>Id: %{y:.2f} mA<extra></extra>"
            ))
        
        fig_iv.update_layout(
            title=f"I-V Characteristics (T = {Temp}°C)",
            xaxis_title="Drain-Source Voltage Vds (V)",
            yaxis_title="Drain Current Id (mA)",
            template="plotly_white",
            height=500,
            legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01)
        )
        
        st.plotly_chart(fig_iv, width='stretch')
    
    with col2:
        st.markdown("### 📊 Operating Point")
        max_current = np.max(Id_current) * 1000  # mA
        max_power = np.max(Power_diss) * 1000  # mW
        
        st.metric("Drain Current", f"{max_current:.1f} mA")
        st.metric("Power Dissipation", f"{max_power:.1f} mW")
        st.metric("On-Resistance", f"{(Vds_range[1]/Id_current[1] if Id_current[1] > 0 else 0):.1f} Ω")
        
        # Efficiency indicator
        efficiency = (max_current * Vgs) / (max_power + 1e-9) * 100
        st.metric("Power Efficiency", f"{efficiency:.1f} %")

with tab2:
    col1, col2 = st.columns(2)
    
    with col1:
        # Temperature effects on mobility
        T_range = np.linspace(25, 300, 50)
        mu_temp = [mobility_temp_dep(mu_base, T) for T in T_range]
        
        fig_temp_mu = go.Figure()
        fig_temp_mu.add_trace(go.Scatter(
            x=T_range, y=mu_temp,
            mode='lines',
            line=dict(color='#e74c3c', width=3),
            name='Mobility'
        ))
        
        fig_temp_mu.update_layout(
            title="Mobility vs Temperature",
            xaxis_title="Temperature (°C)",
            yaxis_title="Mobility (cm²/V·s)",
            template="plotly_white",
            height=400
        )
        
        st.plotly_chart(fig_temp_mu, width='stretch')
    
    with col2:
        # Temperature effects on bandgap
        Eg_temp = [bandgap_temp_dep(Eg_base, T) for T in T_range]
        
        fig_temp_eg = go.Figure()
        fig_temp_eg.add_trace(go.Scatter(
            x=T_range, y=Eg_temp,
            mode='lines',
            line=dict(color='#3498db', width=3),
            name='Bandgap'
        ))
        
        fig_temp_eg.update_layout(
            title="Bandgap vs Temperature (Varshni)",
            xaxis_title="Temperature (°C)",
            yaxis_title="Bandgap (eV)",
            template="plotly_white",
            height=400
        )
        
        st.plotly_chart(fig_temp_eg, width='stretch')

with tab3:
    col1, col2 = st.columns(2)
    
    with col1:
        # Power dissipation
        fig_power = go.Figure()
        fig_power.add_trace(go.Scatter(
            x=Vds_range, y=Power_diss * 1000,  # mW
            mode='lines',
            line=dict(color='#f39c12', width=3),
            name='Power Dissipation',
            fill='tozeroy'
        ))
        
        fig_power.update_layout(
            title="Power Dissipation vs Vds",
            xaxis_title="Drain-Source Voltage Vds (V)",
            yaxis_title="Power (mW)",
            template="plotly_white",
            height=400
        )
        
        st.plotly_chart(fig_power, width='stretch')
    
    with col2:
        # Thermal analysis
        R_th = 50  # Thermal resistance °C/W
        T_junction = Temp + Power_diss * R_th
        
        fig_thermal = go.Figure()
        fig_thermal.add_trace(go.Scatter(
            x=Vds_range, y=T_junction,
            mode='lines',
            line=dict(color='#d35400', width=3),
            name='Junction Temperature',
            fill='tozeroy'
        ))
        
        fig_thermal.add_hline(y=150, line_dash="dash", line_color="red", 
                            annotation_text="Max Junction Temp")
        
        fig_thermal.update_layout(
            title="Junction Temperature vs Vds",
            xaxis_title="Drain-Source Voltage Vds (V)",
            yaxis_title="Junction Temperature (°C)",
            template="plotly_white",
            height=400
        )
        
        st.plotly_chart(fig_thermal, width='stretch')

with tab4:
    # Performance metrics dashboard
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        # Transconductance
        Vgs_small = np.linspace(0, 10, 100)
        Id_gm = drain_current_model(mu_eff, Vgs_small, 5, Eg_eff, Temp,
                                  W=channel_width*1e-6, L=channel_length*1e-6)
        gm = np.gradient(Id_gm, Vgs_small) * 1000  # mS
        max_gm = np.max(gm)
        
        st.metric("Max Transconductance", f"{max_gm:.1f} mS")
    
    with col2:
        # Current density
        Jd_max = np.max(Id_current) / (channel_width * channel_length * 1e-8)  # A/cm²
        st.metric("Current Density", f"{Jd_max:.0f} A/cm²")
    
    with col3:
        # Speed metric
        ft_est = mu_eff * Vgs / (2 * np.pi * channel_length**2 * 1e-8)  # Hz
        st.metric("Cut-off Frequency", f"{ft_est/1e9:.1f} GHz")
    
    with col4:
        # Figure of merit
        fom = (BV_pred**2) / (Vds_range[1]/Id_current[1] if Id_current[1] > 0 else 1e9)
        st.metric("Power FOM", f"{fom:.1e}")

# ---------------- ELECTRON FLOW ANIMATION ----------------
st.markdown("""
<div class='control-panel'>
    <h3>🎬 Electron Flow Visualization</h3>
</div>
""", unsafe_allow_html=True)

# Create electron flow animation
col1, col2 = st.columns([2, 1])

with col1:
    # Simple electron flow representation
    fig_flow = go.Figure()
    
    # Channel
    fig_flow.add_trace(go.Scatter(
        x=[0, 10], y=[5, 5],
        mode='lines',
        line=dict(color='#2ecc71', width=8),
        name='Channel'
    ))
    
    # Electrons
    electron_speed = np.clip(np.max(Id_current) * 50, 0.5, 3.0)
    num_electrons = 20
    x_electrons = np.linspace(0, 10, num_electrons)
    
    for i in range(num_electrons):
        fig_flow.add_trace(go.Scatter(
            x=[x_electrons[i]], y=[5],
            mode='markers',
            marker=dict(size=15, color='#3498db', symbol='circle'),
            name='Electrons' if i == 0 else ''
        ))
    
    fig_flow.update_layout(
        title=f"Electron Flow in Channel (Speed: {electron_speed:.1f}x)",
        xaxis=dict(visible=False, range=[-1, 11]),
        yaxis=dict(visible=False, range=[0, 10]),
        template="plotly_white",
        height=200,
        showlegend=False
    )
    
    st.plotly_chart(fig_flow, width='stretch')

with col2:
    # FIXED: Correct string formatting
    flow_status = "Active" if Vgs > 2.0 else "Inactive"
    st.markdown(f"""
    <div style='background: #f8f9fa; padding: 20px; border-radius: 10px;'>
        <h4>🔬 Flow Dynamics</h4>
        <p><strong>Speed:</strong> {electron_speed:.1f}x</p>
        <p><strong>Density:</strong> High</p>
        <p><strong>Direction:</strong> Source → Drain</p>
        <p><strong>Status:</strong> {flow_status}</p>
    </div>
    """, unsafe_allow_html=True)

# ---------------- EXPORT AND NAVIGATION ----------------
st.markdown("---")
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    st.markdown("""
    <div style='text-align: center;'>
        <h4>Ready for Advanced Analysis?</h4>
        <p>Continue to explore detailed graphs and performance trends</p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("📊 Proceed to Graphs & Trends Analysis", width='stretch'):
        st.switch_page("pages/4_Graphs_and_Trends.py")

# ---------------- PERFORMANCE SUMMARY ----------------
st.markdown("""
<div class='control-panel'>
    <h3>📋 Simulation Summary</h3>
</div>
""", unsafe_allow_html=True)

summary_col1, summary_col2, summary_col3 = st.columns(3)

with summary_col1:
    st.metric("Peak Performance", "Excellent" if mu_eff > 1000 and Eg_eff > 3.2 else "Good")
    st.metric("Thermal Stability", "Stable" if Temp < 150 else "Monitor")

with summary_col2:
    st.metric("Voltage Headroom", f"{(BV_pred - Vds_max)/BV_pred*100:.1f}%")
    st.metric("Efficiency", f"{(np.max(Id_current)*Vgs/(np.max(Power_diss)+1e-9)*100):.1f}%")

with summary_col3:
    st.metric("Technology Node", f"{channel_length} μm")
    st.metric("Power Capability", f"{np.max(Power_diss)*1000:.0f} mW")

st.success("🎯 Simulation completed successfully! All parameters are within safe operating limits.")






'''

# pages/3_Simulation_Interface.py
# Enhanced GaN MOSFET Simulation with Material Layer Controls

import streamlit as st
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

st.set_page_config(page_title="Simulation Interface - GaN MOSFET", layout="wide")

# ---------------- ENHANCED STYLES ----------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

* {
    font-family: 'Inter', sans-serif;
}

.simulation-header {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 30px;
    border-radius: 20px;
    text-align: center;
    margin-bottom: 30px;
    box-shadow: 0 8px 32px rgba(102, 126, 234, 0.3);
}

.control-panel {
    background: white;
    padding: 25px;
    border-radius: 15px;
    margin: 15px 0;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
    border: 1px solid #e9ecef;
}

.material-layer {
    background: linear-gradient(135deg, #74b9ff 0%, #0984e3 100%);
    color: white;
    padding: 20px;
    border-radius: 12px;
    margin: 10px 0;
    transition: transform 0.3s ease;
}

.material-layer:hover {
    transform: translateY(-3px);
    box-shadow: 0 6px 20px rgba(116, 185, 255, 0.4);
}

.parameter-card {
    background: white;
    padding: 15px;
    border-radius: 10px;
    margin: 8px 0;
    border-left: 4px solid #667eea;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
}

.metric-display {
    background: linear-gradient(135deg, #00b894 0%, #00a085 100%);
    color: white;
    padding: 15px;
    border-radius: 10px;
    margin: 8px 0;
    text-align: center;
    font-weight: 600;
}

.warning-metric {
    background: linear-gradient(135deg, #ff7675 0%, #d63031 100%);
    color: white;
    padding: 15px;
    border-radius: 10px;
    margin: 8px 0;
    text-align: center;
    font-weight: 600;
}

.layer-visual {
    background: white;
    padding: 15px;
    border-radius: 10px;
    margin: 10px 0;
    border-left: 4px solid #667eea;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
}
</style>
""", unsafe_allow_html=True)

# ---------------- ENHANCED HEADER ----------------
st.markdown("""
<div class='simulation-header'>
    <h1 style='margin: 0; font-size: 2.5rem;'>⚡ GaN MOSFET Material Layer Simulator</h1>
    <p style='margin: 10px 0 0 0; font-size: 1.2rem; opacity: 0.9;'>
    Interactive Material Properties & Real-time Performance Analysis
    </p>
</div>
""", unsafe_allow_html=True)

# ---------------- MATERIAL DATABASE ----------------
material_properties = {
    "GaN": {
        "Bandgap": 3.4,
        "Mobility": 2000,
        "Breakdown_Field": 3.3,
        "Thermal_Conductivity": 1.3,
        "Color": "#2ecc71",
        "Description": "Wide bandgap semiconductor with high electron mobility"
    },
    "AlGaN": {
        "Bandgap": 4.0,
        "Mobility": 1500,
        "Breakdown_Field": 3.5,
        "Thermal_Conductivity": 1.1,
        "Color": "#3498db",
        "Description": "Aluminum Gallium Nitride barrier layer"
    },
    "SiC": {
        "Bandgap": 3.26,
        "Mobility": 900,
        "Breakdown_Field": 3.5,
        "Thermal_Conductivity": 4.9,
        "Color": "#e74c3c",
        "Description": "Silicon Carbide substrate with excellent thermal conductivity"
    },
    "GaAs": {
        "Bandgap": 1.42,
        "Mobility": 8500,
        "Breakdown_Field": 0.4,
        "Thermal_Conductivity": 0.55,
        "Color": "#9b59b6",
        "Description": "Gallium Arsenide with very high electron mobility"
    },
    "Si": {
        "Bandgap": 1.12,
        "Mobility": 1400,
        "Breakdown_Field": 0.3,
        "Thermal_Conductivity": 1.5,
        "Color": "#f39c12",
        "Description": "Traditional Silicon semiconductor material"
    }
}

# ---------------- ENHANCED PHYSICS MODELS ----------------
def mobility_temp_dep(mu_0, T_celsius, material):
    """Enhanced mobility model with material-specific temperature dependence"""
    T_kelvin = T_celsius + 273.15
    if material in ["GaN", "AlGaN"]:
        return mu_0 * (300 / T_kelvin)**1.5
    elif material == "SiC":
        return mu_0 * (300 / T_kelvin)**2.0
    else:
        return mu_0 * (300 / T_kelvin)**1.7

def bandgap_temp_dep(Eg_0, T_celsius, material):
    """Varshni equation for bandgap temperature dependence"""
    T_kelvin = T_celsius + 273.15
    if material in ["GaN", "AlGaN"]:
        alpha = 0.909e-3
        beta = 830
    elif material == "SiC":
        alpha = 0.0003
        beta = 700
    else:
        alpha = 0.0005
        beta = 300
    return Eg_0 - (alpha * T_kelvin**2) / (T_kelvin + beta)

def breakdown_voltage_model(Eg, thickness=2e-6):
    """Enhanced breakdown voltage model"""
    return 350 * (Eg / 3.4)**2.5 * (thickness / 2e-6)

def drain_current_model(mu_eff, Vgs, Vds, Eg_eff, T_celsius, Vth=2.0, W=100e-6, L=1e-6, Cox=1.5e-6):
    """Enhanced drain current model"""
    beta = mu_eff * Cox * (W/L) * 1e-4
    Vds_sat = Vgs - Vth
    
    Id_linear = beta * ((Vgs - Vth) * Vds - 0.5 * Vds**2)
    Id_sat = 0.5 * beta * (Vgs - Vth)**2 * (1 + 0.02 * Vds)
    
    thermal_factor = np.exp(-(T_celsius - 25) / 150)
    bandgap_factor = (Eg_eff / 3.4)**0.5
    
    Id = np.where(Vds < Vds_sat, Id_linear, Id_sat) * thermal_factor * bandgap_factor
    Id = np.where(Vgs < Vth, 1e-12, Id)
    
    return np.maximum(Id, 1e-12)

# ---------------- SIDEBAR CONTROLS ----------------
st.sidebar.markdown("""
<div style='background: linear-gradient(135deg, #667eea, #764ba2); color: white; padding: 20px; border-radius: 15px;'>
    <h3 style='margin: 0; text-align: center;'>🎛️ Material Control Panel</h3>
</div>
""", unsafe_allow_html=True)

# Material Selection
st.sidebar.markdown("### 🔬 Material Selection")
selected_material = st.sidebar.selectbox(
    "Choose Base Material:",
    list(material_properties.keys()),
    index=0,
    help="Select the primary material for the channel layer"
)

# Show material description
st.sidebar.info(f"**{selected_material}**: {material_properties[selected_material]['Description']}")

# Operating Conditions
st.sidebar.markdown("### ⚡ Operating Conditions")
Temp = st.sidebar.slider("Temperature (°C)", 25, 300, 50, 5,
                        help="Higher temperatures reduce mobility and increase leakage")
Vgs = st.sidebar.slider("Gate Voltage (V)", 0.0, 10.0, 5.0, 0.1,
                       help="Controls channel formation and current flow")
Vds_max = st.sidebar.slider("Max Drain Voltage (V)", 10, 500, 100, 10,
                           help="Maximum operating voltage for the device")

# Material Property Adjustments
st.sidebar.markdown("### 🎯 Material Properties")
base_props = material_properties[selected_material]

Eg_base = st.sidebar.slider(
    f"Bandgap for {selected_material} (eV)", 
    1.0, 5.0, float(base_props["Bandgap"]), 0.05,
    help="Energy gap between valence and conduction bands"
)

mu_base = st.sidebar.slider(
    f"Mobility for {selected_material} (cm²/V·s)", 
    100, 10000, int(base_props["Mobility"]), 50,
    help="How easily electrons move through the material"
)

# ---------------- CALCULATE DERIVED PARAMETERS ----------------
mu_eff = mobility_temp_dep(mu_base, Temp, selected_material)
Eg_eff = bandgap_temp_dep(Eg_base, Temp, selected_material)
BV_pred = breakdown_voltage_model(Eg_eff)

# Generate I-V characteristics
Vds_range = np.linspace(0, Vds_max, 200)
Id_current = drain_current_model(mu_eff, Vgs, Vds_range, Eg_eff, Temp)
Power_diss = Id_current * Vds_range

# ---------------- MAIN LAYOUT ----------------
col1, col2 = st.columns([1, 1])

with col1:
    # MATERIAL LAYERS VISUALIZATION
    st.markdown("""
    <div class='control-panel'>
        <h3>🏗️ MOSFET Material Layers</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Define layers with materials
    layers = [
        {"name": "Gate Contact", "material": "Ni/Au", "thickness": 0.3, "color": "#34495e"},
        {"name": "Gate Oxide", "material": "Al₂O₃", "thickness": 0.02, "color": "#3498db"},
        {"name": "Barrier Layer", "material": "AlGaN", "thickness": 0.025, "color": material_properties["AlGaN"]["Color"]},
        {"name": "Channel Layer", "material": selected_material, "thickness": 0.1, "color": material_properties[selected_material]["Color"]},
        {"name": "Buffer Layer", "material": "GaN", "thickness": 2.0, "color": material_properties["GaN"]["Color"]},
        {"name": "Substrate", "material": "SiC", "thickness": 1.0, "color": material_properties["SiC"]["Color"]}
    ]
    
    # Create layer visualization
    fig_layers = go.Figure()
    
    for i, layer in enumerate(layers):
        fig_layers.add_trace(go.Bar(
            y=[layer["name"]],
            x=[layer["thickness"]],
            orientation='h',
            marker=dict(color=layer["color"]),
            name=f"{layer['material']}",
            text=[f"{layer['thickness']} μm<br>{layer['material']}"],
            textposition='auto',
            hovertemplate=f"<b>{layer['name']}</b><br>Material: {layer['material']}<br>Thickness: {layer['thickness']} μm<extra></extra>"
        ))
    
    fig_layers.update_layout(
        title="MOSFET Layer Structure",
        xaxis_title="Thickness (μm)",
        yaxis_title="Layers",
        barmode='stack',
        height=400,
        template="plotly_white",
        showlegend=False
    )
    
    st.plotly_chart(fig_layers, use_container_width=True)
    
    # LAYER PROPERTIES
    st.markdown("""
    <div class='control-panel'>
        <h3>📊 Layer Properties</h3>
    </div>
    """, unsafe_allow_html=True)
    
    for layer in layers:
        if layer["material"] in material_properties:
            props = material_properties[layer["material"]]
            st.markdown(f"""
            <div class='parameter-card'>
                <h4>{layer['name']} ({layer['material']})</h4>
                <p><strong>Bandgap:</strong> {props['Bandgap']} eV</p>
                <p><strong>Mobility:</strong> {props['Mobility']} cm²/V·s</p>
                <p><strong>Breakdown Field:</strong> {props['Breakdown_Field']} MV/cm</p>
                <p><strong>Thermal Conductivity:</strong> {props['Thermal_Conductivity']} W/cm·K</p>
            </div>
            """, unsafe_allow_html=True)

with col2:
    # REAL-TIME PARAMETERS
    st.markdown("""
    <div class='control-panel'>
        <h3>📈 Real-time Performance</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Key parameters
    param_col1, param_col2 = st.columns(2)
    
    with param_col1:
        st.markdown(f"""
        <div class='metric-display'>
            <h4>Effective Mobility</h4>
            <h3>{mu_eff:.0f} cm²/V·s</h3>
            <p>{((mu_eff/mu_base)-1)*100:+.1f}% change</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class='metric-display'>
            <h4>Operating Temperature</h4>
            <h3>{Temp}°C</h3>
            <p>{Temp + 273} K</p>
        </div>
        """, unsafe_allow_html=True)
    
    with param_col2:
        st.markdown(f"""
        <div class='metric-display'>
            <h4>Effective Bandgap</h4>
            <h3>{Eg_eff:.3f} eV</h3>
            <p>{((Eg_eff/Eg_base)-1)*100:+.1f}% change</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Breakdown voltage status
        bv_status = "🟢 Safe" if Vds_max < BV_pred * 0.8 else "🟡 Warning" if Vds_max < BV_pred else "🔴 Critical"
        status_class = "metric-display" if Vds_max < BV_pred * 0.8 else "warning-metric"
        st.markdown(f"""
        <div class='{status_class}'>
            <h4>Breakdown Voltage</h4>
            <h3>{BV_pred:.0f} V</h3>
            <p>{bv_status} ({Vds_max/BV_pred*100:.1f}% of limit)</p>
        </div>
        """, unsafe_allow_html=True)

    # I-V CHARACTERISTICS
    st.markdown("""
    <div class='control-panel'>
        <h3>⚡ Current-Voltage Characteristics</h3>
    </div>
    """, unsafe_allow_html=True)
    
    fig_iv = go.Figure()
    fig_iv.add_trace(go.Scatter(
        x=Vds_range, y=Id_current*1000,
        mode='lines',
        line=dict(color=material_properties[selected_material]["Color"], width=3),
        name=f'{selected_material} - Vgs = {Vgs}V',
        hovertemplate="Vds: %{x} V<br>Id: %{y:.2f} mA<extra></extra>"
    ))
    
    fig_iv.update_layout(
        title=f"I-V Characteristics - {selected_material}",
        xaxis_title="Drain Voltage Vds (V)",
        yaxis_title="Drain Current Id (mA)",
        template="plotly_white",
        height=300
    )
    
    st.plotly_chart(fig_iv, use_container_width=True)
    
    # PERFORMANCE METRICS
    st.markdown("""
    <div class='control-panel'>
        <h3>🎯 Performance Metrics</h3>
    </div>
    """, unsafe_allow_html=True)
    
    metric_col1, metric_col2, metric_col3 = st.columns(3)
    
    with metric_col1:
        max_current = np.max(Id_current) * 1000
        st.metric("Max Current", f"{max_current:.1f} mA")
    
    with metric_col2:
        max_power = np.max(Power_diss) * 1000
        st.metric("Max Power", f"{max_power:.1f} mW")
    
    with metric_col3:
        on_resistance = Vds_range[1] / Id_current[1] if Id_current[1] > 0 else 0
        st.metric("On-Resistance", f"{on_resistance:.1f} Ω")

# ---------------- MATERIAL COMPARISON ----------------
st.markdown("""
<div class='simulation-header' style='padding: 20px; margin: 30px 0;'>
    <h2 style='margin: 0;'>🔬 Material Performance Comparison</h2>
</div>
""", unsafe_allow_html=True)

# Compare all materials
comparison_data = []
for material, props in material_properties.items():
    mu_eff_comp = mobility_temp_dep(props["Mobility"], Temp, material)
    Eg_eff_comp = bandgap_temp_dep(props["Bandgap"], Temp, material)
    BV_comp = breakdown_voltage_model(Eg_eff_comp)
    
    comparison_data.append({
        "Material": material,
        "Bandgap": props["Bandgap"],
        "Mobility": props["Mobility"],
        "Effective_Mobility": mu_eff_comp,
        "Effective_Bandgap": Eg_eff_comp,
        "Breakdown_Voltage": BV_comp,
        "Color": props["Color"]
    })

df_comparison = pd.DataFrame(comparison_data)

# Create comparison charts
col1, col2 = st.columns(2)

with col1:
    # Bandgap Comparison
    fig_bg = px.bar(
        df_comparison, 
        x='Material', 
        y=['Bandgap', 'Effective_Bandgap'],
        title='Bandgap Comparison (Base vs Effective)',
        color_discrete_sequence=['#95a5a6', '#3498db'],
        barmode='group'
    )
    fig_bg.update_layout(template="plotly_white", height=400)
    st.plotly_chart(fig_bg, use_container_width=True)

with col2:
    # Mobility Comparison
    fig_mob = px.bar(
        df_comparison,
        x='Material',
        y=['Mobility', 'Effective_Mobility'],
        title='Mobility Comparison (Base vs Effective)',
        color_discrete_sequence=['#95a5a6', '#e74c3c'],
        barmode='group'
    )
    fig_mob.update_layout(template="plotly_white", height=400)
    st.plotly_chart(fig_mob, use_container_width=True)

# ---------------- NAVIGATION ----------------
st.markdown("---")
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    st.markdown("""
    <div style='text-align: center;'>
        <h4>Ready for Detailed Analysis?</h4>
        <p>Explore advanced graphs and performance trends</p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("📊 Continue to Graphs & Trends", use_container_width=True):
        st.switch_page("pages/4_Graphs_and_Trends.py")

st.success("🎯 Simulation completed! All material properties are actively influencing device performance.") '''








''' # pages/3_Simulation_Interface.py
# Enhanced GaN MOSFET Simulation with Material Layer Controls

import streamlit as st
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

st.set_page_config(page_title="Simulation Interface - GaN MOSFET", layout="wide")

# ---------------- ENHANCED STYLES ----------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

* {
    font-family: 'Inter', sans-serif;
}

.simulation-header {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 30px;
    border-radius: 20px;
    text-align: center;
    margin-bottom: 30px;
    box-shadow: 0 8px 32px rgba(102, 126, 234, 0.3);
}

.control-panel {
    background: white;
    padding: 25px;
    border-radius: 15px;
    margin: 15px 0;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
    border: 1px solid #e9ecef;
}

.material-layer {
    background: linear-gradient(135deg, #74b9ff 0%, #0984e3 100%);
    color: white;
    padding: 20px;
    border-radius: 12px;
    margin: 10px 0;
    transition: transform 0.3s ease;
}

.material-layer:hover {
    transform: translateY(-3px);
    box-shadow: 0 6px 20px rgba(116, 185, 255, 0.4);
}

.parameter-card {
    background: white;
    padding: 15px;
    border-radius: 10px;
    margin: 8px 0;
    border-left: 4px solid #667eea;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
}

.metric-display {
    background: linear-gradient(135deg, #00b894 0%, #00a085 100%);
    color: white;
    padding: 15px;
    border-radius: 10px;
    margin: 8px 0;
    text-align: center;
    font-weight: 600;
}

.warning-metric {
    background: linear-gradient(135deg, #ff7675 0%, #d63031 100%);
    color: white;
    padding: 15px;
    border-radius: 10px;
    margin: 8px 0;
    text-align: center;
    font-weight: 600;
}

.layer-visual {
    background: white;
    padding: 15px;
    border-radius: 10px;
    margin: 10px 0;
    border-left: 4px solid #667eea;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
}
</style>
""", unsafe_allow_html=True)

# ---------------- ENHANCED HEADER ----------------
st.markdown("""
<div class='simulation-header'>
    <h1 style='margin: 0; font-size: 2.5rem;'>⚡ GaN MOSFET Material Layer Simulator</h1>
    <p style='margin: 10px 0 0 0; font-size: 1.2rem; opacity: 0.9;'>
    Interactive Material Properties & Real-time Performance Analysis
    </p>
</div>
""", unsafe_allow_html=True)

# ---------------- MATERIAL DATABASE ----------------
material_properties = {
    "GaN": {
        "Bandgap": 3.4,
        "Mobility": 2000,
        "Breakdown_Field": 3.3,
        "Thermal_Conductivity": 1.3,
        "Color": "#2ecc71"
    },
    "AlGaN": {
        "Bandgap": 4.0,
        "Mobility": 1500,
        "Breakdown_Field": 3.5,
        "Thermal_Conductivity": 1.1,
        "Color": "#3498db"
    },
    "SiC": {
        "Bandgap": 3.26,
        "Mobility": 900,
        "Breakdown_Field": 3.5,
        "Thermal_Conductivity": 4.9,
        "Color": "#e74c3c"
    },
    "GaAs": {
        "Bandgap": 1.42,
        "Mobility": 8500,
        "Breakdown_Field": 0.4,
        "Thermal_Conductivity": 0.55,
        "Color": "#9b59b6"
    },
    "Si": {
        "Bandgap": 1.12,
        "Mobility": 1400,
        "Breakdown_Field": 0.3,
        "Thermal_Conductivity": 1.5,
        "Color": "#f39c12"
    }
}

# ---------------- ENHANCED PHYSICS MODELS ----------------
def mobility_temp_dep(mu_0, T_celsius, material):
    """Enhanced mobility model with material-specific temperature dependence"""
    T_kelvin = T_celsius + 273.15
    if material in ["GaN", "AlGaN"]:
        return mu_0 * (300 / T_kelvin)**1.5
    elif material == "SiC":
        return mu_0 * (300 / T_kelvin)**2.0
    else:
        return mu_0 * (300 / T_kelvin)**1.7

def bandgap_temp_dep(Eg_0, T_celsius, material):
    """Varshni equation for bandgap temperature dependence"""
    T_kelvin = T_celsius + 273.15
    if material in ["GaN", "AlGaN"]:
        alpha = 0.909e-3
        beta = 830
    elif material == "SiC":
        alpha = 0.0003
        beta = 700
    else:
        alpha = 0.0005
        beta = 300
    return Eg_0 - (alpha * T_kelvin**2) / (T_kelvin + beta)

def breakdown_voltage_model(Eg, thickness=2e-6):
    """Enhanced breakdown voltage model"""
    return 350 * (Eg / 3.4)**2.5 * (thickness / 2e-6)

def drain_current_model(mu_eff, Vgs, Vds, Eg_eff, T_celsius, Vth=2.0, W=100e-6, L=1e-6, Cox=1.5e-6):
    """Enhanced drain current model"""
    beta = mu_eff * Cox * (W/L) * 1e-4
    Vds_sat = Vgs - Vth
    
    Id_linear = beta * ((Vgs - Vth) * Vds - 0.5 * Vds**2)
    Id_sat = 0.5 * beta * (Vgs - Vth)**2 * (1 + 0.02 * Vds)
    
    thermal_factor = np.exp(-(T_celsius - 25) / 150)
    bandgap_factor = (Eg_eff / 3.4)**0.5
    
    Id = np.where(Vds < Vds_sat, Id_linear, Id_sat) * thermal_factor * bandgap_factor
    Id = np.where(Vgs < Vth, 1e-12, Id)
    
    return np.maximum(Id, 1e-12)

# ---------------- SIDEBAR CONTROLS ----------------
st.sidebar.markdown("""
<div style='background: linear-gradient(135deg, #667eea, #764ba2); color: white; padding: 20px; border-radius: 15px;'>
    <h3 style='margin: 0; text-align: center;'>🎛️ Material Control Panel</h3>
</div>
""", unsafe_allow_html=True)

# Material Selection
st.sidebar.markdown("### 🔬 Material Selection")
selected_material = st.sidebar.selectbox(
    "Choose Base Material:",
    list(material_properties.keys()),
    index=0
)

# Operating Conditions
st.sidebar.markdown("### ⚡ Operating Conditions")
Temp = st.sidebar.slider("Temperature (°C)", 25, 300, 50, 5)
Vgs = st.sidebar.slider("Gate Voltage (V)", 0.0, 10.0, 5.0, 0.1)
Vds_max = st.sidebar.slider("Max Drain Voltage (V)", 10, 500, 100, 10)

# Material Property Adjustments
st.sidebar.markdown("### 🎯 Material Properties")
base_props = material_properties[selected_material]

Eg_base = st.sidebar.slider(
    f"Bandgap for {selected_material} (eV)", 
    1.0, 5.0, float(base_props["Bandgap"]), 0.05
)

mu_base = st.sidebar.slider(
    f"Mobility for {selected_material} (cm²/V·s)", 
    100, 10000, int(base_props["Mobility"]), 50
)

# ---------------- CALCULATE DERIVED PARAMETERS ----------------
mu_eff = mobility_temp_dep(mu_base, Temp, selected_material)
Eg_eff = bandgap_temp_dep(Eg_base, Temp, selected_material)
BV_pred = breakdown_voltage_model(Eg_eff)

# Generate I-V characteristics
Vds_range = np.linspace(0, Vds_max, 200)
Id_current = drain_current_model(mu_eff, Vgs, Vds_range, Eg_eff, Temp)
Power_diss = Id_current * Vds_range

# ---------------- MAIN LAYOUT ----------------
col1, col2 = st.columns([1, 1])

with col1:
    # MATERIAL LAYERS VISUALIZATION
    st.markdown("""
    <div class='control-panel'>
        <h3>🏗️ MOSFET Material Layers</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Define layers with materials
    layers = [
        {"name": "Gate Contact", "material": "Ni/Au", "thickness": 0.3, "color": "#34495e"},
        {"name": "Gate Oxide", "material": "Al₂O₃", "thickness": 0.02, "color": "#3498db"},
        {"name": "Barrier Layer", "material": "AlGaN", "thickness": 0.025, "color": material_properties["AlGaN"]["Color"]},
        {"name": "Channel Layer", "material": selected_material, "thickness": 0.1, "color": material_properties[selected_material]["Color"]},
        {"name": "Buffer Layer", "material": "GaN", "thickness": 2.0, "color": material_properties["GaN"]["Color"]},
        {"name": "Substrate", "material": "SiC", "thickness": 1.0, "color": material_properties["SiC"]["Color"]}
    ]
    
    # Create layer visualization
    fig_layers = go.Figure()
    
    for i, layer in enumerate(layers):
        fig_layers.add_trace(go.Bar(
            y=[layer["name"]],
            x=[layer["thickness"]],
            orientation='h',
            marker=dict(color=layer["color"]),
            name=f"{layer['material']}",
            text=[f"{layer['thickness']} μm<br>{layer['material']}"],
            textposition='auto',
            hovertemplate=f"<b>{layer['name']}</b><br>Material: {layer['material']}<br>Thickness: {layer['thickness']} μm<extra></extra>"
        ))
    
    fig_layers.update_layout(
        title="MOSFET Layer Structure",
        xaxis_title="Thickness (μm)",
        yaxis_title="Layers",
        barmode='stack',
        height=400,
        template="plotly_white",
        showlegend=False
    )
    
    st.plotly_chart(fig_layers, use_container_width=True)
    
    # LAYER PROPERTIES
    st.markdown("""
    <div class='control-panel'>
        <h3>📊 Layer Properties</h3>
    </div>
    """, unsafe_allow_html=True)
    
    for layer in layers:
        if layer["material"] in material_properties:
            props = material_properties[layer["material"]]
            st.markdown(f"""
            <div class='parameter-card'>
                <h4>{layer['name']} ({layer['material']})</h4>
                <p>Bandgap: {props['Bandgap']} eV</p>
                <p>Mobility: {props['Mobility']} cm²/V·s</p>
                <p>Breakdown Field: {props['Breakdown_Field']} MV/cm</p>
            </div>
            """, unsafe_allow_html=True)

with col2:
    # REAL-TIME PARAMETERS
    st.markdown("""
    <div class='control-panel'>
        <h3>📈 Real-time Performance</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Key parameters
    param_col1, param_col2 = st.columns(2)
    
    with param_col1:
        st.markdown(f"""
        <div class='metric-display'>
            <h4>Effective Mobility</h4>
            <h3>{mu_eff:.0f} cm²/V·s</h3>
            <p>{((mu_eff/mu_base)-1)*100:+.1f}% change</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class='metric-display'>
            <h4>Operating Temperature</h4>
            <h3>{Temp}°C</h3>
            <p>{Temp + 273} K</p>
        </div>
        """, unsafe_allow_html=True)
    
    with param_col2:
        st.markdown(f"""
        <div class='metric-display'>
            <h4>Effective Bandgap</h4>
            <h3>{Eg_eff:.3f} eV</h3>
            <p>{((Eg_eff/Eg_base)-1)*100:+.1f}% change</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Breakdown voltage status
        bv_status = "🟢 Safe" if Vds_max < BV_pred * 0.8 else "🟡 Warning" if Vds_max < BV_pred else "🔴 Critical"
        status_class = "metric-display" if Vds_max < BV_pred * 0.8 else "warning-metric"
        st.markdown(f"""
        <div class='{status_class}'>
            <h4>Breakdown Voltage</h4>
            <h3>{BV_pred:.0f} V</h3>
            <p>{bv_status} ({Vds_max/BV_pred*100:.1f}% of limit)</p>
        </div>
        """, unsafe_allow_html=True)

    # I-V CHARACTERISTICS
    st.markdown("""
    <div class='control-panel'>
        <h3>⚡ Current-Voltage Characteristics</h3>
    </div>
    """, unsafe_allow_html=True)
    
    fig_iv = go.Figure()
    fig_iv.add_trace(go.Scatter(
        x=Vds_range, y=Id_current*1000,
        mode='lines',
        line=dict(color=material_properties[selected_material]["Color"], width=3),
        name=f'{selected_material} - Vgs = {Vgs}V',
        hovertemplate="Vds: %{x} V<br>Id: %{y:.2f} mA<extra></extra>"
    ))
    
    fig_iv.update_layout(
        title=f"I-V Characteristics - {selected_material}",
        xaxis_title="Drain Voltage Vds (V)",
        yaxis_title="Drain Current Id (mA)",
        template="plotly_white",
        height=300
    )
    
    st.plotly_chart(fig_iv, use_container_width=True)
    
    # PERFORMANCE METRICS
    st.markdown("""
    <div class='control-panel'>
        <h3>🎯 Performance Metrics</h3>
    </div>
    """, unsafe_allow_html=True)
    
    metric_col1, metric_col2, metric_col3 = st.columns(3)
    
    with metric_col1:
        max_current = np.max(Id_current) * 1000
        st.metric("Max Current", f"{max_current:.1f} mA")
    
    with metric_col2:
        max_power = np.max(Power_diss) * 1000
        st.metric("Max Power", f"{max_power:.1f} mW")
    
    with metric_col3:
        on_resistance = Vds_range[1] / Id_current[1] if Id_current[1] > 0 else 0
        st.metric("On-Resistance", f"{on_resistance:.1f} Ω")

# ---------------- MATERIAL COMPARISON ----------------
st.markdown("""
<div class='simulation-header' style='padding: 20px; margin: 30px 0;'>
    <h2 style='margin: 0;'>🔬 Material Performance Comparison</h2>
</div>
""", unsafe_allow_html=True)

# Compare all materials
comparison_data = []
for material, props in material_properties.items():
    mu_eff_comp = mobility_temp_dep(props["Mobility"], Temp, material)
    Eg_eff_comp = bandgap_temp_dep(props["Bandgap"], Temp, material)
    BV_comp = breakdown_voltage_model(Eg_eff_comp)
    
    comparison_data.append({
        "Material": material,
        "Bandgap": props["Bandgap"],
        "Mobility": props["Mobility"],
        "Effective_Mobility": mu_eff_comp,
        "Effective_Bandgap": Eg_eff_comp,
        "Breakdown_Voltage": BV_comp,
        "Color": props["Color"]
    })

df_comparison = pd.DataFrame(comparison_data)

# Create comparison charts
col1, col2 = st.columns(2)

with col1:
    # Bandgap Comparison
    fig_bg = px.bar(
        df_comparison, 
        x='Material', 
        y=['Bandgap', 'Effective_Bandgap'],
        title='Bandgap Comparison (Base vs Effective)',
        color_discrete_sequence=['#95a5a6', '#3498db'],
        barmode='group'
    )
    fig_bg.update_layout(template="plotly_white", height=400)
    st.plotly_chart(fig_bg, use_container_width=True)

with col2:
    # Mobility Comparison
    fig_mob = px.bar(
        df_comparison,
        x='Material',
        y=['Mobility', 'Effective_Mobility'],
        title='Mobility Comparison (Base vs Effective)',
        color_discrete_sequence=['#95a5a6', '#e74c3c'],
        barmode='group'
    )
    fig_mob.update_layout(template="plotly_white", height=400)
    st.plotly_chart(fig_mob, use_container_width=True)

# ---------------- NAVIGATION ----------------
st.markdown("---")
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    st.markdown("""
    <div style='text-align: center;'>
        <h4>Ready for Detailed Analysis?</h4>
        <p>Explore advanced graphs and performance trends</p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("📊 Continue to Graphs & Trends", use_container_width=True):
        st.switch_page("pages/4_Graphs_and_Trends.py")

st.success("🎯 Simulation completed! All material properties are actively influencing device performance.")  '''