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

# Premium High-Contrast Executive Theme
st.markdown("""
    <style>
    /* Main Background Canvas */
    .stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
        background-color: #F8FAFC !important;
    }
    
    /* Global Clean Typography */
    label, p, span, h1, h2, h3, h4, .section-title {
        color: #0F172A !important;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif !important;
    }
    
    /* Sidebar Restyling: Premium Dark Midnight Panel */
    [data-testid="stSidebar"] {
        background-color: #090D16 !important;
        border-right: 1px solid #1E293B !important;
    }
    [data-testid="stSidebar"] * {
        color: #F8FAFC !important;
    }
    [data-testid="stSidebar"] label, [data-testid="stSidebar"] p, [data-testid="stSidebar"] span {
        color: #94A3B8 !important;
    }
    
    /* Fix Sidebar Text Input Boxes to be highly readable */
    [data-testid="stSidebar"] input {
        background-color: #111827 !important;
        color: #FFFFFF !important;
        border: 1px solid #374151 !important;
    }
    
    /* Top Header Executive Banner */
    .header-banner {
        background: linear-gradient(135deg, #0F172A 0%, #1E3A8A 100%);
        padding: 35px 40px;
        border-radius: 12px;
        margin-bottom: 30px;
        box-shadow: 0 4px 15px rgba(15, 23, 42, 0.08);
    }
    .header-banner * { color: #FFFFFF !important; }
    .main-title { font-size: 34px; font-weight: 800; letter-spacing: -0.5px; }
    .sub-title { font-size: 15px; color: #CBD5E1 !important; margin-top: 6px; font-weight: 400; }
    
    /* High-Contrast Section Header Lines */
    .section-container { margin-top: 15px; margin-bottom: 15px; }
    .section-title { font-size: 19px; font-weight: 700; color: #1E3A8A !important; border-left: 4px solid #2563EB; padding-left: 12px; }
    
    /* Content Cards (Stark White Over Light Canvas) */
    .form-card {
        background-color: #FFFFFF !important;
        padding: 28px;
        border-radius: 12px;
        border: 1px solid #E2E8F0 !important;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.02), 0 2px 4px -1px rgba(0, 0, 0, 0.01);
        margin-bottom: 25px;
    }
    
    /* Strict Input Field Boundaries for Main Canvas */
    div[data-baseweb="select"], div[data-baseweb="input"], textarea, select, .form-card input {
        background-color: #FFFFFF !important; 
        color: #0F172A !important; 
        border: 1px solid #94A3B8 !important; 
        border-radius: 8px !important;
    }
    div[data-baseweb="select"] *, div[data-baseweb="input"] * { color: #0F172A !important; }
    
    /* Navigation Tab Headers Custom Look */
    button[data-baseweb="tab"] { color: #64748B !important; font-weight: 700 !important; font-size: 16px !important; }
    button[data-baseweb="tab"][aria-selected="true"] { color: #2563EB !important; border-bottom-color: #2563EB !important; }
    
    /* Main Primary Strategy Button */
    button[kind="primary"] { background-color: #2563EB !important; border: none !important; border-radius: 8px !important; padding: 12px 24px !important; }
    button[kind="primary"] p { color: #FFFFFF !important; font-weight: 700 !important; font-size: 16px !important; }
    
    /* Custom Google Sign-In Button Interface */
    .google-btn {
        background-color: #FFFFFF !important;
        color: #374151 !important;
        border: 1px solid #E2E8F0 !important;
        border-radius: 6px;
        padding: 10px;
        text-align: center;
        font-weight: 600;
        font-size: 14px;
        cursor: pointer;
        margin-bottom: 20px;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 1px 2px rgba(0,0,0,0.05);
    }
    .google-btn img { margin-right: 10px; width: 18px; height: 18px; }
    
    /* High-Contrast AI Output Block */
    .ai-output-box { 
        background-color: #FFFFFF !important; 
        padding: 35px; 
        border-radius: 12px; 
        border-left: 6px solid #2563EB !important;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.04);
        margin-top: 25px; 
    }
    .ai-output-box * { color: #0F172A !important; }
    .ai-output-box h1, .ai-output-box h2, .ai-output-box h3 { color: #1E3A8A !important; margin-top: 20px; }
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
    st.markdown("### IvyPilot Account Portal")
    st.markdown("---")
    
    if not st.session_state.logged_in:
        # Custom HTML Google Sign-In Button Component
        st.markdown("""
            <div class="google-btn">
                <img src="https://upload.wikimedia.org/wikipedia/commons/5/53/Google_%22G%22_Logo.svg">
                Sign in with Google
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<p style='text-align:center; color:#64748B; font-size:12px;'>— OR EMAIL SIGN IN —</p>", unsafe_allow_html=True)
        
        auth_mode = st.radio("Account Action", ["Sign In", "Create Account"])
        email = st.text_input("Email Address", key="sidebar_email")
        password = st.text_input("Password", type="password", key="sidebar_password")
        st.markdown("<br>", unsafe_allow_html=True)
        
        if auth_mode == "Create Account":
            if st.button("Register Account", type="primary"):
                try:
                    res = supabase.auth.sign_up({"email": email, "password": password})
                    st.success("Registration complete! Verify your email link to log in.")
                except Exception as e:
                    st.error(f"Error: {e}")
        else:
            if st.button("Sign In with Email", type="primary"):
                try:
                    res = supabase.auth.sign_in_with_password({"email": email, "password": password})
                    st.session_state.logged_in = True
                    st.session_state.user_email = res.user.email
                    st.session_state.user_id = res.user.id
                    st.rerun()
                except Exception as e:
                    st.error("Authentication details incorrect.")
    else:
        st.markdown(f"Active Session:<br><span style='color:#F8FAFC; font-weight:600;'>{st.session_state.user_email}</span>", unsafe_allow_html=True)
        st.markdown("<br><br>", unsafe_allow_html=True)
        if st.button("Log Out of Session"):
            st.session_state.logged_in = False
            st.session_state.user_email = ""
            st.session_state.user_id = ""
            st.rerun()

# Main Workspace Header
st.markdown("""
    <div class="header-banner">
        <div class="main-title">IvyPilot AI Workspace</div>
        <div class="sub-title">Premium Profile Analysis Dashboard & Document Storage Vault</div>
    </div>
""", unsafe_allow_html=True)

# ==========================================
# 3. PREMIUM CONTENT GRIDS
# ==========================================
if not st.session_state.logged_in:
    st.info("Secure Gateway: Please sign in or create an account via the sidebar panel to unlock your strategic dashboard and resource vaults.")
else:
    app_tab, vault_tab = st.tabs(["📊 Profile Strategy Engine", "📁 Academic Document Vault"])
    
    with app_tab:
        st.markdown('<div class="form-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-container"><div class="section-title">Academic Framework Metrics</div></div>', unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        with col1:
            student_grade = st.selectbox("Current Grade Level", ["Grade 8", "Grade 9", "Grade 10", "Grade 11 / IB1", "Grade 12 / IB2", "Other"])
        with col2:
            academic_system = st.selectbox("Curriculum System", ["Cambridge (IGCSE/A-Levels)", "IB Diploma", "US High School Diploma", "CBSE / ICSE", "Other"])
        with col3:
            gpa_metrics = st.text_input("Current Grades / Performance Index", placeholder="e.g., Straight A*s, 42/45 IB")

        col4, col5 = st.columns(2)
        with col4:
            subjects_taken = st.text_input("Course Configurations / Chosen Subjects", placeholder="e.g., Math AA HL, Economics HL")
        with col5:
            test_scores = st.text_input("Standardized/External Testing History", placeholder="e.g., SAT benchmarks, Checkpoint outcomes")
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="form-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-container"><div class="section-title">Admissions Targets</div></div>', unsafe_allow_html=True)
        col6, col7 = st.columns(2)
        with col6:
            target_major = st.text_input("Intended Discipline or Focus Major", placeholder="e.g., Corporate Finance, Investment Banking")
        with col7:
            target_countries = st.text_input("Target Geographic Regions", placeholder="e.g., United States, United Kingdom, Singapore")
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="form-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-container"><div class="section-title">Qualitative Profile Parameters</div></div>', unsafe_allow_html=True)
        activities = st.text_area("Extracurricular Involvements & Leadership Roles", placeholder="List school clubs, debate teams, sports, or internships...", height=80)
        independent_projects = st.text_area("Independent Digital Assets & Web Tools Launched", placeholder="Detail academic resource sites, applications built, or independent tools hosted...", height=80)
        core_passions = st.text_area("Intrinsic Intellectual Passions & Private Research Topics", placeholder="What fields or issues do you study entirely outside standard school constraints?", height=70)
        dream_colleges = st.text_area("Desired Target University Pipeline", placeholder="List specific colleges or priority tiers (e.g., NYU Stern, LSE)...", height=70)
        st.markdown('</div>', unsafe_allow_html=True)

        col_btn, _ = st.columns([1, 2])
        with col_btn:
            execute_analysis = st.button("Generate Comprehensive Strategy", type="primary")

        if execute_analysis:
            if not gpa_metrics or not target_major or not dream_colleges:
                st.warning("Action Deferred: Complete key parameters to run evaluation vectors.")
            else:
                with st.spinner("Processing framework variables..."):
                    analysis_prompt = f"Advisor Mode. User Grade: {student_grade}, Curriculum: {academic_system}, Grades: {gpa_metrics}, Subjects: {subjects_taken}, Tests: {test_scores}, Major: {target_major}, Target Countries: {target_countries}, Activities: {activities}, Projects: {independent_projects}, Passions: {core_passions}, Targets: {dream_colleges}. Structure feedback cleanly into plain markdown headers covering Profile Assessment, Reach/Match/Safety breakdown, and an actionable timeline roadmap. Strict condition: Do not output any emojis."
                    try:
                        model = genai.GenerativeModel("gemini-2.5-flash")
                        response = model.generate_content(analysis_prompt)
                        st.success("Analysis complete.")
                        st.markdown(f'<div class="ai-output-box">{response.text}</div>', unsafe_allow_html=True)
                    except Exception as e:
                        st.error(f"Connection lost: {e}")

    with vault_tab:
        st.markdown('<div class="form-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-container"><div class="section-title">Academic Document Repository</div></div>', unsafe_allow_html=True)
        st.write("Upload and categorize credentials, report cards, or personal statements securely.")
        
        file_category = st.selectbox("Document Category Designation", ["Academic Transcripts", "Extracurricular Proofs", "Essay Drafts", "Other Credentials"])
        uploaded_file = st.file_uploader("Select Target File (PDF, PNG, JPG, DOCX)", type=["pdf", "png", "jpg", "jpeg", "docx"])
        
        if uploaded_file is not None:
            col_up, _ = st.columns([1, 3])
            with col_up:
                upload_trigger = st.button("Commit File to Repository", type="primary")
            if upload_trigger:
                with st.spinner("Writing to secure bucket layer..."):
                    try:
                        clean_filename = f"{file_category}/{uploaded_file.name}".replace(" ", "_")
                        storage_path = f"{st.session_state.user_id}/{clean_filename}"
                        file_bytes = uploaded_file.getvalue()
                        
                        res = supabase.storage.from_("student-files").upload(
                            path=storage_path,
                            file=file_bytes,
                            file_options={"content-type": uploaded_file.type, "x-upsert": "true"}
                        )
                        st.success(f"Archived successfully: {uploaded_file.name}")
                    except Exception as e:
                        st.error(f"Upload failed: {e}")
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="form-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-container"><div class="section-title">Current File Catalog</div></div>', unsafe_allow_html=True)
        try:
            user_folder = f"{st.session_state.user_id}"
            categories = ["Academic Transcripts", "Extracurricular Proofs", "Essay Drafts", "Other Credentials"]
            
            for cat in categories:
                path_to_list = f"{user_folder}/{cat}".replace(" ", "_")
                files = supabase.storage.from_("student-files").list(path_to_list)
                
                if files:
                    st.markdown(f"📁 **{cat}**")
                    for f in files:
                        filename = f.get('name')
                        if filename != '.emptyFolderPlaceholder':
                            st.write(f"  • {filename}")
        except Exception:
            st.info("Repository registry index is empty.")
        st.markdown('</div>', unsafe_allow_html=True)
