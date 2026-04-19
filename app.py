import streamlit as st
import pandas as pd
import numpy as np
import time
import os
import base64
from model import detect_anomalies, get_risk_level
from rag import analyze_failure
from api import generate_ai_report
from pdf_gen import create_pdf_report
import plotly.express as px

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="Industrial AI Maintenance",
    page_icon="🛠️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- THEME STATE INITIALIZATION ---
if "theme" not in st.session_state:
    st.session_state.theme = "Dark"

# --- THEME SELECTION ---
with st.sidebar:
    st.session_state.theme = st.radio("🎨 Theme Mode", ["Dark", "Light"], horizontal=True, index=0 if st.session_state.theme == "Dark" else 1)
    st.divider()

# --- THEME-AWARE STYLING ---
theme_colors = {
    "Dark": {
        "bg": "#020617",
        "card_bg": "#0f172a",
        "text": "#f8fafc",
        "subtext": "#94a3b8",
        "border": "#1e293b",
        "sidebar": "#020617",
        "header_grad": "linear-gradient(135deg, #1e3a8a, #4338ca)",
        "highlight": "#3b82f6"
    },
    "Light": {
        "bg": "#f8fafc",
        "card_bg": "#ffffff",
        "text": "#0f172a",
        "subtext": "#475569",
        "border": "#e2e8f0",
        "sidebar": "#ffffff",
        "header_grad": "linear-gradient(135deg, #1e40af, #3730a3)",
        "highlight": "#2563eb"
    }
}

colors = theme_colors[st.session_state.theme]

st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    
    html, body, [data-testid="stAppViewContainer"] {{
        background-color: {colors['bg']} !important;
        font-family: 'Inter', sans-serif !important;
        color: {colors['text']} !important;
    }}

    /* Hero Banner Section */
    .header-hero {{
        background: {colors['header_grad']};
        border-radius: 24px;
        padding: 5rem 2rem;
        text-align: center;
        margin-bottom: 2.5rem;
        box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
        position: relative;
    }}

    /* Streamlit Global Overrides */
    header[data-testid="stHeader"], div[data-testid="stToolbar"] {{
        background-color: {colors['bg']} !important;
        color: {colors['text']} !important;
    }}

    /* Hero Banner Redesign */
    .header-hero {{
        background: {colors['header_grad']};
        border-radius: 32px;
        padding: 5rem 3rem;
        margin-bottom: 3rem;
        box-shadow: 0 40px 80px -20px rgba(0, 0, 0, 0.5);
        position: relative;
        overflow: hidden;
    }}

    .hero-content {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        gap: 4rem;
        position: relative;
        z-index: 2;
    }}

    .hero-text-area {{
        flex: 3;
        text-align: left;
        min-width: 0; /* Prevents flex squashing */
    }}

    .hero-badge {{
        display: inline-block;
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(12px);
        padding: 0.6rem 1.4rem;
        border-radius: 100px;
        font-size: 0.9rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.15em;
        color: #ffffff;
        border: 1px solid rgba(255, 255, 255, 0.3);
        margin-bottom: 2rem;
    }}

    .hero-main-title {{
        font-family: 'Inter', sans-serif !important;
        display: flex !important;
        flex-wrap: wrap !important;
        align-items: baseline !important;
        gap: 1.2rem !important;
        font-size: 3.8rem !important;
        font-weight: 800 !important;
        line-height: 1.2 !important;
        color: #ffffff !important;
        margin: 0 !important;
        letter-spacing: normal !important;
        text-shadow: 0 4px 15px rgba(0, 0, 0, 0.25);
        text-align: left;
    }}

    .thin-text {{
        font-weight: 300 !important;
        opacity: 0.95 !important;
        margin-right: 0.5rem !important;
    }}

    .hero-subtitle {{
        font-size: 1.4rem !important;
        color: rgba(255, 255, 255, 0.9) !important;
        margin-top: 1.5rem !important;
        max-width: 800px;
        line-height: 1.5 !important;
        font-weight: 400 !important;
    }}

    .highlight-inline {{
        color: #ffffff !important;
        font-weight: 700 !important;
        border-bottom: 3px solid {colors['highlight']};
        padding-bottom: 2px;
    }}

    .hero-icon-area {{
        flex: 1;
        display: flex;
        justify-content: center;
        align-items: center;
    }}

    .floating-icon {{
        font-size: 8rem;
        filter: drop-shadow(0 20px 30px rgba(0,0,0,0.3));
        animation: floating 3s ease-in-out infinite;
    }}

    @keyframes floating {{
        0% {{ transform: translateY(0px); }}
        50% {{ transform: translateY(-20px); }}
        100% {{ transform: translateY(0px); }}
    }}

    /* Buttons & Uploader Styling */
    .stButton>button {{
        background-color: {colors['highlight']} !important;
        color: white !important;
        border-radius: 12px !important;
        font-weight: 700 !important;
        border: none !important;
        padding: 0.75rem 2rem !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }}
    
    .stButton>button:hover {{
        transform: translateY(-2px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.2);
        opacity: 0.9;
    }}

    .stFileUploader section {{
        background-color: {colors['card_bg']} !important;
        border: 2px dashed {colors['border']} !important;
        border-radius: 16px !important;
        padding: 2rem !important;
    }}
    
    /* Word Readability in Sidebar/Uploader */
    .stFileUploader label [data-testid="stMarkdownContainer"] p {{
        color: {colors['text']} !important;
        font-weight: 600 !important;
    }}
    
    [data-testid="stFileUploaderDropzoneInstructions"] span {{
        color: {colors['subtext']} !important;
    }}

    /* Modern Gallery Style */
    .gallery-card {{
        border-radius: 20px;
        overflow: hidden;
        border: 2px solid {colors['border']};
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        background-color: {colors['card_bg']};
        height: 200px;
    }}
    
    .gallery-card:hover {{
        transform: translateY(-8px);
        box-shadow: 0 12px 20px -5px rgba(0, 0, 0, 0.2);
        border-color: {colors['highlight']};
    }}
    
    .gallery-image {{
        width: 100%;
        height: 100%;
        object-fit: cover;
    }}

    /* Responsive Cards */
    div[data-testid="stMetric"], .stDataFrame, .stPlotlyChart {{
        background-color: {colors['card_bg']} !important;
        border: 1px solid {colors['border']} !important;
        border-radius: 20px !important;
        padding: 1.5rem !important;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
        margin-bottom: 1rem !important;
    }}
    
    /* Metrics Readability */
    [data-testid="stMetricValue"] {{
        color: {colors['text']} !important;
        font-weight: 800 !important;
        font-size: 2.8rem !important;
    }}
    [data-testid="stMetricLabel"] {{
        color: {colors['subtext']} !important;
        font-weight: 600 !important;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }}
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {{
        background-color: {colors['sidebar']} !important;
        border-right: 1px solid {colors['border']} !important;
    }}
    
    /* Highlighting */
    .highlight {{
        color: {colors['highlight']};
        font-weight: 700;
        background-color: rgba(128, 128, 128, 0.1);
        padding: 0.2rem 0.6rem;
        border-radius: 6px;
        border-bottom: 2px solid {colors['highlight']};
    }}

    /* Global Text Readability */
    p, li, span, label {{
        font-size: 1.05rem !important;
        line-height: 1.6 !important;
        font-weight: 500 !important;
    }}
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR CONTENT ---
with st.sidebar:
    st.title("⚙️ Control Panel")
    st.info("Upload your sensor data to begin the analysis.")
    uploaded_file = st.file_uploader("Upload CSV Data", type="csv")
    
    st.divider()
    st.markdown("### 🔑 API Configuration")
    api_key = st.text_input("Google Gemini API Key", type="password", help="Enter your key to enable AI Insight Engine.", key="gemini_api_key_input")
    if api_key:
        os.environ["GOOGLE_GEMINI_KEY"] = api_key

# --- MAIN HEADER ---
st.markdown(f"""
<div class="header-hero">
    <div class="hero-content">
        <div class="hero-text-area">
            <div class="hero-badge">Industrial Intelligence 4.0</div>
            <h1 class="hero-main-title">
                <span class="thin-text">AI</span>
                <span><b>Predictive</b></span>
                <span>Maintenance</span>
            </h1>
            <p class="hero-subtitle">
                Harnessing high-frequency sensor fusion and Deep Learning to ensure 
                <span class="highlight-inline">zero-downtime</span> manufacturing environments.
            </p>
        </div>
        <div class="hero-icon-area">
            <div class="floating-icon">🛠️</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# --- HEADER IMAGES GALLERY ---
images = [
    "industrial_maintenance_1_1776582343099.png",
    "industrial_maintenance_2_1776582354854.png",
    "industrial_maintenance_3_1776582367550.png",
    "industrial_maintenance_4_1776582538791.png"
]

with st.container():
    cols = st.columns(4)
    for i, col in enumerate(cols):
        if i < len(images) and os.path.exists(images[i]):
            with col:
                st.markdown(f"""
                <div class="gallery-card">
                    <img src="data:image/png;base64,{base64.b64encode(open(images[i], "rb").read()).decode()}" class="gallery-image">
                </div>
                """, unsafe_allow_html=True)

st.divider()

# --- DATA PROCESSING ---
if uploaded_file is not None or st.button("🚀 Load Sample Data"):
    if uploaded_file is not None:
        raw_df = pd.read_csv(uploaded_file)
        st.success("File uploaded successfully!")
    else:
        raw_df = pd.read_csv("sample_data.csv")
        st.warning("Using sample data for demonstration.")

    # 1. User Input & Preview
    st.markdown("### 📄 Data Preview")
    st.dataframe(raw_df.head(10), use_container_width=True)

    # 2. Sensor Data Processing (Simulation if needed)
    df = raw_df.copy()
    required_cols = ['vibration', 'temperature', 'rpm']
    missing_cols = [c for c in required_cols if c not in df.columns]
    
    if missing_cols:
        st.info(f"Simulating missing columns: {', '.join(missing_cols)}")
        for col in missing_cols:
            if col == 'vibration':
                df['vibration'] = np.random.uniform(0, 1, len(df))
            elif col == 'temperature':
                df['temperature'] = np.random.uniform(0, 1, len(df))
            elif col == 'rpm':
                df['rpm'] = np.random.randint(800, 2001, len(df))

    # 3. Machine Learning (Anomaly Detection)
    st.divider()
    st.markdown("### 🤖 Anomaly Detection (ML)")
    
    with st.spinner("Analyzing sensor patterns..."):
        time.sleep(1) # Visual effect
        processed_df, anomaly_ratio = detect_anomalies(df)
        risk_level, emoji = get_risk_level(anomaly_ratio)
    
    c1, c2, c3 = st.columns(3)
    c1.metric("Anomaly Ratio", f"{anomaly_ratio:.2%}", delta=f"{anomaly_ratio*100:.1f}%", delta_color="inverse")
    color_map = {"HIGH": "error", "MEDIUM": "warning", "LOW": "success"}
    c2.markdown(f"**System Risk Level:**")
    if risk_level == "HIGH":
        c2.error(f"{emoji} {risk_level} RISK")
    elif risk_level == "MEDIUM":
        c2.warning(f"{emoji} {risk_level} RISK")
    else:
        c2.success(f"{emoji} {risk_level} RISK")
    
    # Visualization
    fig = px.scatter(processed_df, x='vibration', y='temperature', color='status', 
                     title="Vibration vs Temperature (Anomalies Highlighted)",
                     color_discrete_map={'Normal': '#38bdf8', 'Anomaly': '#f43f5e'},
                     height=500)
    st.plotly_chart(fig, width="stretch")

    # 4. RAG Result
    st.divider()
    st.markdown("### 🧠 Knowledge Base (RAG)")
    rag_result = analyze_failure(processed_df, anomaly_ratio)
    
    with st.container():
        st.markdown(f"**Detected Issue:** <span class='highlight'>{rag_result['type']}</span>", unsafe_allow_html=True)
        st.write(f"**Probable Cause:** {rag_result['cause']}")
        st.info(f"**Recommended Solution:** {rag_result['solution']}")

    # 5. AI Insight Engine
    st.divider()
    st.markdown("### ✨ AI Insight Engine")
    
    summary_data = f"Avg Vibration: {df['vibration'].mean():.2f}, Avg Temp: {df['temperature'].mean():.2f}, Max RPM: {df['rpm'].max()}"
    
    with st.spinner("Generating AI Analysis..."):
        ai_output = generate_ai_report(
            risk_level, 
            rag_result['type'], 
            rag_result['solution'], 
            summary_data
        )
    
    st.markdown(ai_output)

    # 9. PDF Export
    st.divider()
    pdf_bytes = create_pdf_report(ai_output, risk_level, rag_result['type'])
    st.download_button(
        label="📥 Download Maintenance Report (PDF)",
        data=pdf_bytes,
        file_name=f"maintenance_report_{time.strftime('%Y%m%d_%H%M%S')}.pdf",
        mime="application/pdf"
    )

else:
    st.markdown("""
    ### 👋 Welcome to the AI Predictive Maintenance System
    Please upload a CSV file with sensor data (vibration, temperature, rpm) or click the button below to use sample data.
    
    **Features:**
    - 🔍 Real-time Anomaly Detection with Isolation Forest
    - 🧠 Automated Diagnosis using RAG rules
    - ✨ AI-Generated Technical Insights
    - 📊 Interactive Data Visualizations
    - 📥 Professional PDF Report Generation
    """)
    st.image(images[0], caption="Advanced Industrial Monitoring", use_container_width=True)
