import streamlit as st
import pandas as pd
import numpy as np
import math
import plotly.express as px

# --- 1. PROFESSIONAL UI STYLING ---
st.set_page_config(page_title="Green Shield Intelligence", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #0a1128, #1c2541, #3a506b);
        color: #ffffff;
    }
    [data-testid="stSidebar"] {
        background-color: rgba(10, 17, 40, 0.95) !important;
    }
    h1, h2, h3 {
        color: #5bc0be !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        font-weight: 600;
    }
    div[data-testid="metric-container"] {
        background-color: rgba(255, 255, 255, 0.03);
        border: 1px solid #5bc0be;
        border-radius: 8px;
        padding: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# --- 2. DASHBOARD HEADER (NO EMOJIS) ---
st.title("Green Shield: Infrastructure Intelligence")
st.write("Predictive modeling of reinforced concrete service life utilizing Calotropis secondary metabolites.")

# --- 3. SIDEBAR PARAMETERS ---
st.sidebar.header("Experimental Parameters")

exposure_type = st.sidebar.selectbox("Environmental Exposure", ["Standard Urban", "Coastal/Marine", "Industrial"])

if exposure_type == "Standard Urban":
    Cs = 1.5
elif exposure_type == "Coastal/Marine":
    Cs = 4.0
else:
    Cs = 3.0

cover_depth = st.sidebar.slider("Concrete Cover Depth (mm)", 20, 75, 40)
inhibition_eff = st.sidebar.slider("Calotropis Inhibition Efficiency (%)", 0.0, 99.9, 84.3, step=0.1) 

# --- 4. THE MATH & SIMULATION ---
base_Dc = 15.0 # INCREASED to realistic diffusion rate
protected_Dc = base_Dc * (1 - (inhibition_eff / 100.0)) 
critical_threshold = 0.4 

def erf_approx(x):
    sign = 1 if x >= 0 else -1
    x = abs(x)
    t = 1.0 / (1.0 + 0.3275911 * x)
    y = 1.0 - (((((1.061405429 * t - 1.453152027) * t) + 1.421413741) * t - 0.284496736) * t + 0.254829592) * t * math.exp(-x * x)
    return sign * y

years = np.arange(0, 101, 1)
standard_conc = []
protected_conc = []

for t in years:
    if t == 0:
        standard_conc.append(0)
        protected_conc.append(0)
    else:
        z_std = cover_depth / (2 * math.sqrt(base_Dc * t))
        standard_conc.append(Cs * (1 - erf_approx(z_std)))
        
        z_prot = cover_depth / (2 * math.sqrt(protected_Dc * t))
        protected_conc.append(Cs * (1 - erf_approx(z_prot)))

# --- 5. RESULTS & IMPACT METRICS ---
std_failure_year = next((i for i, v in enumerate(standard_conc) if v >= critical_threshold), 100)
prot_failure_year = next((i for i, v in enumerate(protected_conc) if v >= critical_threshold), 100)
years_added = prot_failure_year - std_failure_year

co2_saved_tons = round(years_added * 12.5, 1) 

st.subheader("Sustainability Impact Assessment")
col1, col2, col3 = st.columns(3)
col1.metric("Standard Service Life", f"{std_failure_year} Years")
col2.metric("Green Shield Service Life", f"{prot_failure_year} Years", f"+{years_added} Years Extended")
col3.metric("CO₂ Emissions Prevented", f"{co2_saved_tons} Tons", "per 1000 sq.ft")

# --- 6. PLOTLY VISUALIZATION (PROFESSIONAL GRAPH) ---
# Data organization for Plotly
df_plot = pd.DataFrame({
    "Year": years,
    "Standard RCC": standard_conc,
    "Protected RCC": protected_conc
})

# Melt the dataframe so Plotly can draw multiple lines easily
df_melted = df_plot.melt(id_vars=["Year"], var_name="Concrete Type", value_name="Concentration")

st.subheader("Chloride Diffusion Trajectory")

# Create the professional Plotly chart
fig = px.line(df_melted, x="Year", y="Concentration", color="Concrete Type",
              color_discrete_map={"Standard RCC": "#ff4b4b", "Protected RCC": "#5bc0be"})

# Add the critical threshold line
fig.add_hline(y=critical_threshold, line_dash="dot", line_color="red", annotation_text="Critical Threshold (Rust Begins)")

# Update Axis Labels and background to fit the dark theme
fig.update_layout(
    xaxis_title="Service Life (Years)",
    yaxis_title="Chloride Concentration (%)",
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    font=dict(color="#ffffff")
)

st.plotly_chart(fig, use_container_width=True)