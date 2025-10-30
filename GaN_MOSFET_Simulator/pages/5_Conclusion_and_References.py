# pages/5_Formulas_and_References.py
# Phase 6: Equations, References & Acknowledgements
# University of Hyderabad — Group 4

import streamlit as st

st.set_page_config(page_title="Formulas & References - GaN MOSFET", layout="wide")

# ---------- STYLE ----------
st.markdown("""
<style>
.title {font-size:28px;color:#003366;font-weight:700;text-align:center;}
.section {color:#004c99;font-size:20px;font-weight:600;margin-top:25px;}
.equation {background:#f4f9ff;padding:8px 15px;border-left:4px solid #007bff;border-radius:4px;margin:8px 0;}
.ref-box {background:#f7faff;border-left:4px solid #004c99;padding:10px;margin:5px 0;}
.team-box {background:#f0f8ff;padding:10px;border-radius:8px;margin-top:10px;}
hr {border: 0; height: 1px; background: #cce0ff; margin: 20px 0;}
</style>
""", unsafe_allow_html=True)

st.markdown("<div class='title'>📘 Formulas, References & Acknowledgements</div>", unsafe_allow_html=True)
st.markdown("---")

# ---------- FORMULAS ----------
st.markdown("<div class='section'>📐 Key Formulas Used in the Simulation</div>", unsafe_allow_html=True)

st.markdown("""
<div class='equation'>
<b>1️⃣ Drain Current Equation (MOSFET):</b><br>
\\[
I_D = \\frac{1}{2} \\mu C_{ox} \\frac{W}{L} (V_{GS} - V_{TH})^2 (1 + \\lambda V_{DS})
\\]
Describes how drain current depends on gate voltage, threshold, and channel parameters.
</div>

<div class='equation'>
<b>2️⃣ Mobility vs Temperature:</b><br>
\\[
\\mu(T) = \\mu_0 \\left( \\frac{300}{T + 273} \\right)^{1.5}
\\]
Mobility decreases with temperature due to increased lattice scattering.
</div>

<div class='equation'>
<b>3️⃣ Bandgap vs Temperature (Varshni Equation):</b><br>
\\[
E_g(T) = E_{g0} - \\frac{\\alpha T^2}{T + \\beta}
\\]
Empirical relation showing how bandgap reduces slightly as temperature rises.
</div>

<div class='equation'>
<b>4️⃣ Breakdown Voltage vs Bandgap:</b><br>
\\[
BV \\propto (E_g)^{2.5}
\\]
Higher bandgap materials exhibit exponentially greater breakdown voltage.
</div>

<div class='equation'>
<b>5️⃣ Power Dissipation:</b><br>
\\[
P = I_D \\times V_{DS}
\\]
Represents instantaneous power in the device channel.
</div>
""", unsafe_allow_html=True)

# ---------- REFERENCES ----------
st.markdown("<div class='section'>📚 References</div>", unsafe_allow_html=True)
st.markdown("""
<div class='ref-box'>
[1] S.M. Sze, Kwok K. Ng — *Physics of Semiconductor Devices*, 3rd Ed. Wiley, 2006.  
[2] B. Jayant Baliga — *Fundamentals of Power Semiconductor Devices*, Springer, 2008.  
[3] EPC Corporation — *EPC GaN FET Application Handbook*, 2023.  
[4] IEEE Transactions on Electron Devices — Selected papers on GaN MOSFET modeling.  
[5] Nexperia — *MOSFET Application Notes* (AN90003), 2024.  
[6] Group-4 Research Paper: “Compound Semiconductors — A Comprehensive Theoretical Study”, University of Hyderabad, 2025.
</div>
""", unsafe_allow_html=True)

# ---------- TEAM DETAILS ----------
st.markdown("<div class='section'>👥 Project Team & Acknowledgements</div>", unsafe_allow_html=True)
st.markdown("""
<div class='team-box'>
<b>🎓 University:</b> University of Hyderabad  
<b>📘 Course:</b> Semiconductor Materials  
<b>👨‍🏫 Faculty:</b> <i>Dr. Raj Kishora Dash</i>  
<b>🏗️ Project Title:</b> <i>Analysis and Simulation of GaN MOSFETs for High Power Applications</i>  
<b>💡 Team Name:</b> Group 4  
<b>Team Members:</b><br>
• Maddela Bhargav — 24ETIM18<br>
• Karangula Sai Nikhil — 24ETIM20<br>
• Gourav Kumar Singh — 24ETIM21<br>
• Raj Gupta — 24ETIM22<br>
• Rahul Kumar — 24ETIM23
</div>
""", unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)
st.info("✅ End of Project — All data, simulations, and visuals are original and research-based for educational demonstration.")
