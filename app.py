import streamlit as st
import pandas as pd
import numpy as np
import math

# --- 1. DASHBOARD HEADER ---
st.title("🛡️ Green Shield: SDG 9 Infrastructure Dashboard")
st.write("Predicting the service life of RCC structures using Calotropis Bio-Inhibitor.")

# --- 2. THE USER INPUTS (SIDEBAR) ---
# We put sliders on the side so the judges can interact with your data
st.sidebar.header("Simulation Parameters")
cover_depth = st.sidebar.slider("Concrete Cover Depth (mm)", 20, 75, 40)
inhibition_eff = st.sidebar.slider("Inhibitor Efficiency (%)", 0, 99, 84) # 84% based on typical Calotropis results

# --- 3. THE MATH (FICK'S SECOND LAW) ---
# This calculates how fast chloride (salt) travels through concrete over time
base_Dc = 1.5 # Diffusion rate for standard concrete
protected_Dc = base_Dc * (1 - (inhibition_eff / 100.0)) # Calotropis slows diffusion down

# The "Error Function" (erf) is a complex math formula used in diffusion physics.
def erf_approx(x):
    sign = 1 if x >= 0 else -1
    x = abs(x)
    t = 1.0 / (1.0 + 0.3275911 * x)
    y = 1.0 - (((((1.061405429 * t - 1.453152027) * t) + 1.421413741) * t - 0.284496736) * t + 0.254829592) * t * math.exp(-x * x)
    return sign * y

# --- 4. GENERATING THE DATA FOR 100 YEARS ---
years = np.arange(0, 101, 1) # Simulating from Year 0 to Year 100
Cs = 3.0 # Surface chloride concentration (%)
critical_threshold = 0.4 # The point where steel starts to rust!

standard_conc = []
protected_conc = []

# Loop through every year and calculate the rust level
for t in years:
    if t == 0:
        standard_conc.append(0)
        protected_conc.append(0)
    else:
        # Standard Concrete calculation
        z_std = cover_depth / (2 * math.sqrt(base_Dc * t))
        standard_conc.append(Cs * (1 - erf_approx(z_std)))
        
        # Protected Concrete calculation
        z_prot = cover_depth / (2 * math.sqrt(protected_Dc * t))
        protected_conc.append(Cs * (1 - erf_approx(z_prot)))

# --- 5. DRAWING THE CHART ---
# Pandas organizes the math into a neat table so Streamlit can draw it
df = pd.DataFrame({
    "Year": years,
    "Standard RCC (%)": standard_conc,
    "Protected RCC (%)": protected_conc
})
df.set_index("Year", inplace=True)

st.subheader("Chloride Penetration Over Time")
st.line_chart(df)

st.success("Notice how the 'Protected RCC' line stays much lower for much longer. This gap represents the years of life added to the building, reducing the need to manufacture replacement cement (Saving CO2)!")