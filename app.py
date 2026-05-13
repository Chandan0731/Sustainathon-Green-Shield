import streamlit as st
import pandas as pd
import numpy as np
import math

# --- 1. CUSTOM UI STYLING (THE UPGRADE) ---
# This forces the app into 'wide' mode and injects custom CSS for a premium look
st.set_page_config(page_title="Green Shield Dashboard", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
    /* Premium Dark Gradient Background */
    .stApp {
        background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
        color: #ffffff;
    }
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: rgba(15, 32, 39, 0.9) !important;
    }
    /* Neon Green Accents for Headers */
    h1, h2, h3 {
        color: #00ffcc !important;
        font-family: 'Helvetica Neue', sans-serif;
    }
    /* Metric Card Styling */
    div[data-testid="metric-container"] {
        background-color: rgba(255, 255, 255, 0.05);
        border: 1px solid #00ffcc;
        border-radius: 10px;
        padding: 15px;
    }
</style>
""", unsafe_allow_html=True)

# --- 2. DASHBOARD HEADER ---
st.title("🛡️ Green Shield: SDG 9 Infrastructure Intelligence")
st.write("Predictive modeling of reinforced concrete service life utilizing Calotropis secondary metabolites.")

# --- 3. SIDEBAR PARAMETERS (INCLUDING YOUR NEW FINDINGS) ---
st.sidebar.header("🔬 Experimental Parameters")
st.sidebar.write("Input your lab findings here:")

# Adding a new attribute for environmental exposure
exposure_type = st.sidebar.selectbox("Environmental Exposure", ["Standard City", "Coastal/Marine (High Chloride)", "Industrial (Acidic)"])

# Adjusting base chloride levels based on exposure
if exposure_type == "Standard City":
    Cs = 1.5
elif exposure_type == "Coastal/Marine (High Chloride)":
    Cs = 4.0
else:
    Cs = 3.0

cover_depth = st.sidebar.slider("Concrete Cover Depth (mm)", 20, 75, 40)

# This is where your 24hr HCl test results shine!
inhibition_eff = st.sidebar.slider("Calotropis Inhibition Efficiency (%)", 0.0, 99.9, 84.3, step=0.1) 

# --- 4. THE MATH & SIMULATION ---
base_Dc = 1.5 
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

# Calculate penetration
for t in years:
    if t == 0:
        standard_conc.append(0)
        protected_conc.append(0)
    else:
        z_std = cover_depth / (2 * math.sqrt(base_Dc * t))
        standard_conc.append(Cs * (1 - erf_approx(z_std)))
        
        z_prot = cover_depth / (2 * math.sqrt(protected_Dc * t))
        protected_conc.append(Cs * (1 - erf_approx(z_prot)))

# --- 5. RESULTS & IMPACT METRICS (NEW SECTION) ---
# Calculate the exact year they cross the 0.4 threshold
std_failure_year = next((i for i, v in enumerate(standard_conc) if v >= critical_threshold), 100)
prot_failure_year = next((i for i, v in enumerate(protected_conc) if v >= critical_threshold), 100)
years_added = prot_failure_year - std_failure_year

# Assuming 0.9kg of CO2 per 1kg of cement saved by not rebuilding
co2_saved_tons = years_added * 12.5 # Estimated tons of CO2 saved per 1000 sq ft over the added lifespan

st.subheader("🌍 Sustainability Impact (SDG 9 & 13)")
col1, col2, col3 = st.columns(3)
col1.metric("Standard Life", f"{std_failure_year} Years")
col2.metric("Green Shield Life", f"{prot_failure_year} Years", f"+{years_added} Years Added")
col3.metric("CO₂ Emissions Prevented", f"{co2_saved_tons} Tons", "per 1000 sq.ft")

# --- 6. THE VISUALIZATION ---
df = pd.DataFrame({
    "Year": years,
    "Standard RCC (%)": standard_conc,
    "Protected RCC (%)": protected_conc
})
df.set_index("Year", inplace=True)

st.subheader("📊 Chloride Diffusion Trajectory")
st.line_chart(df, color=["#ff4b4b", "#00ffcc"]) # Red for failure, Neon Green for your inhibitor