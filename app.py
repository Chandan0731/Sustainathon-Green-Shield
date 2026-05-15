import streamlit as st
import pandas as pd
import numpy as np
import math
import plotly.express as px
import plotly.graph_objects as go

# --- 1. PROFESSIONAL UI STYLING ---
st.set_page_config(page_title="Green Shield Intelligence", layout="wide")

st.markdown("""
<style>
    /* Dark theme gradient and custom neon accents */
    .stApp { background: linear-gradient(135deg, #0a1128, #1c2541, #3a506b); color: #ffffff; }
    [data-testid="stSidebar"] { background-color: rgba(10, 17, 40, 0.95) !important; }
    h1, h2, h3 { color: #5bc0be !important; }
    div[data-testid="metric-container"] { background-color: rgba(255, 255, 255, 0.03); border: 1px solid #5bc0be; border-radius: 8px; padding: 15px; }
    
    /* Tab Styling */
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] { background-color: rgba(255,255,255,0.05); border-radius: 4px; padding: 10px 20px; }
    .stTabs [aria-selected="true"] { background-color: #5bc0be; color: #000000 !important; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

st.title("🛡️ Green Shield: Infrastructure Intelligence")

# --- CREATE TABS ---
tab1, tab2, tab3 = st.tabs(["📊 Service Life Simulator", "🧬 3D Molecular Barrier", "📸 Lab Evidence Gallery"])

# ==========================================
# TAB 1: THE SIMULATION (Fick's Second Law)
# ==========================================
with tab1:
    st.sidebar.header("Experimental Parameters")
    
    exposure_type = st.sidebar.selectbox("Environmental Exposure", ["Standard Urban", "Coastal/Marine", "Industrial"])
    Cs = 1.5 if exposure_type == "Standard Urban" else (4.0 if exposure_type == "Coastal/Marine" else 3.0)
    
    cover_depth = st.sidebar.slider("Concrete Cover Depth (mm)", 20, 75, 40)
    inhibition_eff = st.sidebar.slider("Calotropis Inhibition Efficiency (%)", 0.0, 99.9, 84.3) 
    
    base_Dc, critical_threshold = 15.0, 0.4 
    protected_Dc = base_Dc * (1 - (inhibition_eff / 100.0)) 

    def erf_approx(x):
        sign = 1 if x >= 0 else -1
        x = abs(x)
        t = 1.0 / (1.0 + 0.3275911 * x)
        y = 1.0 - (((((1.061405429 * t - 1.453152027) * t) + 1.421413741) * t - 0.284496736) * t + 0.254829592) * t * math.exp(-x * x)
        return sign * y

    years = np.arange(0, 101, 1)
    
    # Calculate concentrations (Ensuring variables are named standard_conc and protected_conc)
    standard_conc = [0 if t==0 else Cs*(1-erf_approx(cover_depth/(2*math.sqrt(base_Dc*t)))) for t in years]
    protected_conc = [0 if t==0 else Cs*(1-erf_approx(cover_depth/(2*math.sqrt(protected_Dc*t)))) for t in years]

    # Calculate exact failure years using the correct standard_conc variable
    std_fail = next((i for i, v in enumerate(standard_conc) if v >= critical_threshold), 100)
    prot_fail = next((i for i, v in enumerate(protected_conc) if v >= critical_threshold), 100)
    years_added = prot_fail - std_fail
    
    st.subheader("Sustainability Impact Assessment")
    col1, col2, col3 = st.columns(3)
    col1.metric("Standard Life", f"{std_fail} Years")
    col2.metric("Green Shield Life", f"{prot_fail} Years", f"+{years_added} Years")
    col3.metric("CO₂ Prevented", f"{round(years_added * 12.5, 1)} Tons", "per 1000 sq.ft")

    # Plotly Graph
    df_plot = pd.DataFrame({"Year": years, "Standard RCC": standard_conc, "Protected RCC": protected_conc}).melt(id_vars=["Year"], var_name="Concrete Type", value_name="Concentration")
    fig = px.line(df_plot, x="Year", y="Concentration", color="Concrete Type", color_discrete_map={"Standard RCC": "#ff4b4b", "Protected RCC": "#5bc0be"})
    fig.add_hline(y=critical_threshold, line_dash="dot", line_color="red", annotation_text="Critical Threshold (Rust Begins)")
    fig.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", font=dict(color="#ffffff"), xaxis_title="Service Life (Years)", yaxis_title="Chloride Concentration (%)")
    st.plotly_chart(fig, use_container_width=True)

# ==========================================
# TAB 2: 3D MOLECULAR BARRIER
# ==========================================
with tab2:
    st.subheader("Conceptual 3D Adsorption Model")
    st.write("This interactive 3D model represents the *Calotropis* metabolites forming a protective chelate layer over the iron surface, repelling incoming Chloride ions.")
    
    cl_x, cl_y, cl_z = np.random.uniform(-10, 10, 100), np.random.uniform(-10, 10, 100), np.random.uniform(2, 10, 100)
    fig3d = go.Figure()
    
    # Steel Surface
    fig3d.add_trace(go.Surface(z=np.zeros((10,10)), colorscale='Greys', opacity=0.5, name="Steel Surface"))
    # Inhibitor Layer
    fig3d.add_trace(go.Surface(z=np.ones((10,10)) * 1.5, colorscale='Greens', opacity=0.8, name="Calotropis Inhibitor"))
    # Chloride Ions
    fig3d.add_trace(go.Scatter3d(x=cl_x, y=cl_y, z=cl_z, mode='markers', marker=dict(size=5, color='red'), name="Chloride Ions"))

    fig3d.update_layout(scene=dict(zaxis=dict(range=[0, 10])), margin=dict(l=0, r=0, b=0, t=0), paper_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig3d, use_container_width=True)

# ==========================================
# TAB 3: MEDIA GALLERY (7 Photos, 2 Videos)
# ==========================================
with tab3:
    st.subheader("📸 Laboratory Evidence & Proof of Concept")
    st.write("Visual documentation of the extraction, material preparation, and testing methodology.")
    
    st.markdown("### 🖼️ Photographic Evidence")
    
    # 3-Column Grid for 7 Photos
    p_col1, p_col2, p_col3 = st.columns(3)
    
    with p_col1:
        st.write("**1. Pre-process**")
        st.image("assets/photo1.jpg", use_container_width=True)
        
        st.write("**4. FTIR Spectral Analysis**")
        st.image("assets/photo4.jpg", use_container_width=True)
        
        st.write("**7. Dried Mould**")
        st.image("assets/photo7.jpg", use_container_width=True)
        
    with p_col2:
        st.write("**2. Soxhlet Extraction Setup**")
        st.image("assets/photo2.jpg", use_container_width=True)
        
        st.write("**5. Final Coated Specimen in 0.1M Hcl solution**")
        st.image("assets/photo5.jpg", use_container_width=True)
        
    with p_col3:
        st.write("**3. Extracted 2' metabolite**")
        st.image("assets/photo3.jpg", use_container_width=True)
        
        st.write("**6. Concrete Mold Casting**")
        st.image("assets/photo6.jpg", use_container_width=True)
        
    st.markdown("---")
    
    st.markdown("### 🎥 Experimental Footage")
    
    # 2-Column Grid for 2 Videos
    v_col1, v_col2 = st.columns(2)
    
    with v_col1:
        st.write("**Process Documentation: Part 1**")
        st.video("assets/video1.mp4")
        
    with v_col2:
        st.write("**Process Documentation: Part 2**")
        st.video("assets/video2.mp4")