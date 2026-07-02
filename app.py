import streamlit as st
import google.generativeai as genai
from supabase import create_client, Client
import os

# ==========================================
# 1. INITIAL CONFIGURATION & DATABASE SETUP
# ==========================================
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    url: str = st.secrets["SUPABASE_URL"]
    key: str = st.secrets["SUPABASE_KEY"]
    supabase: Client = create_client(url, key)
except Exception as e:
    st.error("Please ensure GEMINI_API_KEY, SUPABASE_URL, and SUPABASE_KEY are configured in Streamlit Secrets.")

st.set_page_config(page_title="IvyPilot AI Portal", layout="wide", initial_sidebar_state="expanded")

# Advanced Styling Grid: High-Contrast Corporate Theme
st.markdown("""
    <style>
    /* Main Page Workspace Canvas */
    .stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
        background-color: #F1F5F9 !important;
    }
    
    /* Global Text Enforcement for High Readability */
    label, p, span, h1, h2, h3, .section-title {
        color: #0F172A !important;
        font-family: -apple-system, BlinkMacSystemFont, sans-serif !important;
    }
    
    /* Sidebar Restyling: Dark Slate Minimalist Panel */
    [data-testid="stSidebar"] {
        background-color: #0F172A !important;
        border-right: 1px solid #1E293B !important;
    }
    [data-testid="stSidebar"] * {
        color: #F8FAFC !important;
    }
    [data-testid="stSidebar"] label, [data-testid="stSidebar"] p, [data-testid="stSidebar"] span {
        color: #CBD5E1 !important;
    }
    
    /* Top Header Executive Banner */
    .header-banner {
        background: #0F172A;
        padding: 30px 40px;
        border-radius: 8px;
        margin-bottom: 30px;
        border-left: 6px solid #2563EB;
    }
    .header-banner * { color: #FFFFFF !important; }
    .main-title { font-size: 32px; font-weight: 700; letter-spacing: -0.5px; }
    .sub-title { font-size: 14px; color: #94A3B8 !important; margin-top: 4px; }
    
    /* High-Contrast Section Header Lines */
    .section-container { margin-top: 30px; margin-bottom: 15px; }
    .section-title { font-size: 18px; font-weight: 700; color: #1E3A8A !important; }
    
    /* Content Cards (Stark White Over Light Grey Canvas) */
    .form-card {
        background-color: #FFFFFF !important;
        padding: 24px;
        border-radius: 8px;
        border: 1px solid #E2E8F0 !important;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }
    
    /* Strict Input Field Boundaries */
    div[data-baseweb="select"], div[data-baseweb="input"], textarea, select, input {
        background-color: #FFFFFF !important; 
        color: #0F172A !important; 
        border: 1px solid #94A3B8 !important; 
        border-radius: 6px !important;
    }
    div[data-baseweb="select"] *, div[data-baseweb="input"] * { color: #0F172A !important; }
    
    /* Interactive Tab Adjustments */
    button[data-baseweb="tab"] { color: #64748B !important; font-weight: 600 !important; }
    button[data-baseweb="tab"][aria-selected="true"] { color: #2563EB !important; border-bottom-color: #2563EB !important; }
    
    /* High-Contrast UI Action Buttons */
    button[kind="primary"] { background-color: #2563EB !important; border: none !important; width: 100% !important; padding: 10px !important; }
    button[kind="primary"] p { color: #FFFFFF !important; font-weight: 600 !important; }
    
    /* Strategy Engine Response Safe-Zone */
    .ai-output-box { 
        background-color: #FFFFFF !important; 
        padding: 30px; 
        border-radius: 8px; 
        border: 2px solid #2563EB !important; 
        margin-top: 20px; 
    }
    .ai-output-box * { color: #0F172A !important; }
    </style>
""", unsafe_allow_html=True)

# Initialize Session States
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user_email" not in st.session_state:
    st.session_state.user_email = ""
if "user_id" not in st.session_state:
    st.session_state.user_id = ""

# ==========================================
# 2. STREAMLINED SIDEBAR ARCHITECTURE
# ==========================================
with st.sidebar:
    st.markdown("### Access Portal")
    st.markdown("---")
    
    if not st.session_state.logged_in:
        auth_mode = st.radio("Account Action", ["Sign In", "Create Account"])
        st.markdown("<br>", unsafe_allow_html=True)
        email = st.text_input("Email Address")
        password = st.text_input("Password", type="password")
        st.markdown("<br>", unsafe_allow_html=True)
        
        if auth_mode == "Create Account":
            if st.button("Register Account", type="primary"):
                try:
                    res = supabase.auth.sign_up({"email": email, "password": password})
                    st.success("Registration complete. Verify your email link to proceed.")
                except Exception as e:
                    st.error(f"Error: {e}")
        else:
            if st.button("Sign In", type="primary"):
                try:
                    res = supabase.auth.sign_in_with_password({"email": email, "password": password})
                    st.session_state.logged_in = True
                    st.session_state.user_email = res.user.email
                    st.session_state.user_id = res.user.id
                    st.rerun()
                except Exception as e:
                    st.error("Authentication rejected.")
    else:
        st.markdown(f"Authenticated as:<br>**{st.session_state.user_email}**", unsafe_allow_html=True)
        st.markdown("<br><br>", unsafe_allow_html=True)
        if st.button("Log Out of Session"):
            st.session_state.logged_in = False
            st.session_state.user_email = ""
            st.session_state.user_id = ""
            st.rerun()

# Workspace Header Banner
st.markdown("""
    <div class="header-banner">
        <div class="main-title">IvyPilot AI Workspace</div>
        <div class="sub-title">Personalized Profile Analysis and Academic File Management Portal</div>
    </div>
""", unsafe_allow_html=True)

# ==========================================
# 3. HIGH-CONTRAST WORKSPACE CONTENT
# ==========================================
if not st.session_state.logged_in:
    st.info("Authentication Required. Please deploy your credentials or create a profile via the sidebar panel to unlock dashboard functions.")
else:
    app_tab, vault_tab = st.tabs(["Strategy Engine", "Academic Document Vault"])
    
    with app_tab:
        # Wrap form segments in dedicated white high-contrast container blocks
        st.markdown('<div class="form-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-container"><div class="section-title">Academic Framework Metrics</div></div>', unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        with col1:
            student_grade = st.selectbox("Current Grade Level", ["Grade 8", "Grade 9", "Grade 10", "Grade 11 / IB1", "Grade 12 / IB2", "Other"])
        with col2:
            academic_system = st.selectbox("Curriculum System", ["Cambridge (IGCSE/A-Levels)", "IB Diploma", "US High School Diploma", "CBSE / ICSE", "Other"])
        with col3:
            gpa_metrics = st.text_input("Current Grades / Results Index", placeholder="e.g., Straight A*s, 42/45 IB")

        col4, col5 = st.columns(2)
        with col4:
            subjects_taken = st.text_input("Course Configurations / Chosen Subjects", placeholder="e.g., Math AA HL, Economics HL")
        with col5:
            test_scores = st.text_input("Standardized/External Testing History", placeholder="e.g., SAT benchmarks, Checkpoint outcomes")
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="form-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-container"><div class="section-title">Institutional Targets</div></div>', unsafe_allow_html=True)
        col6, col7 = st.columns(2)
        with col6:
            target_major
