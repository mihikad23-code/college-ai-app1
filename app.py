import streamlit as st
import google.generativeai as genai
from supabase import create_client, Client
import os

# ==========================================
# 1. INITIAL CONFIGURATION & DATABASE SETUP
# ==========================================
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    
    # Initialize Supabase Client
    url: str = st.secrets["SUPABASE_URL"]
    key: str = st.secrets["SUPABASE_KEY"]
    supabase: Client = create_client(url, key)
except Exception as e:
    st.error("Please ensure GEMINI_API_KEY, SUPABASE_URL, and SUPABASE_KEY are configured in Streamlit Secrets.")

st.set_page_config(page_title="IvyPilot AI Portal", layout="wide", initial_sidebar_state="expanded")

# Universal Layout and Styling Text Fixes
st.markdown("""
    <style>
    .stApp { background-color: #F8FAFC !important; }
    * { color: #0F172A !important; }
    .header-banner {
        background: linear-gradient(135deg, #0F172A 0%, #1E40AF 100%);
        padding: 30px;
        border-radius: 12px;
        margin-bottom: 25px;
    }
    .header-banner * { color: #FFFFFF !important; }
    .main-title { font-size: 32px; font-weight: 700; margin-bottom: 4px; }
    .sub-title { font-size: 14px; font-weight: 400; }
    .section-container { margin-top: 25px; margin-bottom: 10px; }
    .section-title { font-size: 18px; font-weight: 600; border-left: 4px solid #2563EB; padding-left: 10px; }
    div[data-baseweb="select"], div[data-baseweb="input"], textarea, select, input {
        background-color: #FFFFFF !important; color: #0F172A !important; border: 1px solid #CBD5E1 !important; border-radius: 8px !important;
    }
    div[data-baseweb="select"] *, div[data-baseweb="input"] * { color: #0F172A !important; }
    button[kind="primary"] { background-color: #2563EB !important; border: none !important; }
    button[kind="primary"] p { color: #FFFFFF !important; }
    .ai-output-box { background-color: #FFFFFF !important; padding: 25px; border-radius: 8px; border: 1px solid #E2E8F0 !important; margin-top: 15px; }
    .ai-output-box * { color: #0F172A !important; }
    </style>
""", unsafe_allow_html=True)

# Initialize Session States for Authentication Tracking
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user_email" not in st.session_state:
    st.session_state.user_email = ""
if "user_id" not in st.session_state:
    st.session_state.user_id = ""

# ==========================================
# 2. USER AUTHENTICATION SYSTEM (SIDEBAR)
# ==========================================
with st.sidebar:
    st.title("Account Portal")
    
    if not st.session_state.logged_in:
        auth_mode = st.radio("Choose Action", ["Sign In", "Create Account"])
        email = st.text_input("Account Email Address")
        password = st.text_input("Password", type="password")
        
        if auth_mode == "Create Account":
            if st.button("Register New Account", type="primary"):
                try:
                    res = supabase.auth.sign_up({"email": email, "password": password})
                    st.success("Account created! Please check your email for a confirmation link, then Sign In.")
                except Exception as e:
                    st.error(f"Registration failed: {e}")
        else:
            if st.button("Sign In to Portal", type="primary"):
                try:
                    res = supabase.auth.sign_in_with_password({"email": email, "password": password})
                    st.session_state.logged_in = True
                    st.session_state.user_email = res.user.email
                    st.session_state.user_id = res.user.id
                    st.rerun()
                except Exception as e:
                    st.error("Invalid credentials. Please try again.")
    else:
        st.write(f"Active Account: **{st.session_state.user_email}**")
        if st.button("Log Out of Portal"):
            st.session_state.logged_in = False
            st.session_state.user_email = ""
            st.session_state.user_id = ""
            st.rerun()

# Header Display
st.markdown("""
    <div class="header-banner">
        <div class="main-title">IvyPilot AI Workspace</div>
        <div class="sub-title">Secure Student Academic Vault & Strategic Profile Analyzer</div>
    </div>
""", unsafe_allow_html=True)

# ==========================================
# 3. CORE CORE APP LAYER (IF LOGGED IN)
# ==========================================
if not st.session_state.logged_in:
    st.info("Please sign in or create an account using the sidebar to unlock your personalized application workspace and file organizers.")
else:
    # Split layout into Workspace Form and Document Storage Vault
    app_tab, vault_tab = st.tabs(["Profile Analytics Dashboard", "Document Storage Vault"])
    
    with app_tab:
        st.markdown('<div class="section-container"><div class="section-title">Academic Architecture Framework</div></div>', unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        with col1:
            student_grade = st.selectbox("Current Grade Level", ["Grade 8", "Grade 9", "Grade 10", "Grade 11 / IB1", "Grade 12 / IB2", "Other"])
        with col2:
            academic_system = st.selectbox("Curriculum System", ["Cambridge (IGCSE/A-Levels)", "IB Diploma", "US High School Diploma", "CBSE / ICSE", "Other"])
        with col3:
            gpa_metrics = st.text_input("Current Grades / GPA / Percentages", placeholder="e.g., Straight A*s, 42/45 IB")

        col4, col5 = st.columns(2)
        with col4:
            subjects_taken = st.text_input("Specific Subjects Chosen / Higher Levels (HL)", placeholder="e.g., Math AA HL, Economics HL")
        with col5:
            test_scores = st.text_input("Standardized Tests & External Exams", placeholder="e.g., SAT, ACT, Checkpoint results")

        st.markdown('<div class="section-container"><div class="section-title">Target Preferences</div></div>', unsafe_allow_html=True)
        col6, col7 = st.columns(2)
        with col6:
            target_major = st.text_input("Intended Major or Career Path", placeholder="e.g., Corporate Finance, Computer Science")
        with col7:
            target_countries = st.text_input("Target Countries or Locations", placeholder="e.g., US, UK, Singapore")

        st.markdown('<div class="section-container"><div class="section-title">Portfolio Strategy Data Blocks</div></div>', unsafe_allow_html=True)
        activities = st.text_area("Key Activities and Leadership Positions", placeholder="List school clubs, debate, sports, internships...", height=80)
        independent_projects = st.text_area("Independent Projects and Digital Tools Developed", placeholder="Detail any academic resource tools, websites hosted, apps built...", height=80)
        core_passions = st.text_area("Personal Interests and Favorite Research Topics", placeholder="What domains do you research entirely on your own outside of class?", height=70)
        dream_colleges = st.text_area("Target Universities or College Lists", placeholder="List your dream target universities...", height=70)

        if st.button("Analyze Profile & Generate Admissions Strategy", type="primary"):
            if not gpa_metrics or not target_major or not dream_colleges:
                st.warning("Please complete all academic parameters to proceed.")
            else:
                with st.spinner("Compiling analysis vectors..."):
                    analysis_prompt = f"Advisor Mode. User Grade: {student_grade}, Curriculum: {academic_system}, Grades: {gpa_metrics}, Subjects: {subjects_taken}, Tests: {test_scores}, Major: {target_major}, Target Countries: {target_countries}, Activities: {activities}, Projects: {independent_projects}, Passions: {core_passions}, Targets: {dream_colleges}. Structure your feedback into plain text markdown headers for Profile Assessment, Reach/Match/Safety breakdown, and an actionable roadmap. Avoid all emojis."
                    try:
                        model = genai.GenerativeModel("gemini-2.5-flash")
                        response = model.generate_content(analysis_prompt)
                        st.success("Analysis finalized.")
                        st.markdown(f'<div class="ai-output-box">{response.text}</div>', unsafe_allow_html=True)
                    except Exception as e:
                        st.error(f"Engine connection interrupted: {e}")

    with vault_tab:
        st.markdown('<div class="section-container"><div class="section-title">Student File Storage System</div></div>', unsafe_allow_html=True)
        st.write("Upload, organize, and track your credentials, report sheets, transcripts, or essay drafts securely.")
        
        # File Organization Category Selector
        file_category = st.selectbox("File Destination Category", ["Academic Transcripts", "Extracurricular Proofs", "Essay Drafts", "Other Credentials"])
        uploaded_file = st.file_uploader("Choose a document file to archive (PDF, PNG, JPG, DOCX)", type=["pdf", "png", "jpg", "jpeg", "docx"])
        
        if uploaded_file is not None:
            if st.button("Upload Document to Vault", type="primary"):
                with st.spinner("Uploading and organizing document layer..."):
                    try:
                        # Construct a clean nested folder path specific to this unique user ID
                        file_extension = os.path.splitext(uploaded_file.name)[1]
                        clean_filename = f"{file_category}/{uploaded_file.name}".replace(" ", "_")
                        storage_path = f"{st.session_state.user_id}/{clean_filename}"
                        
                        file_bytes = uploaded_file.getvalue()
                        
                        # Upload byte data straight to Supabase Storage Bucket
                        res = supabase.storage.from_("student-files").upload(
                            path=storage_path,
                            file=file_bytes,
                            file_options={"content-type": uploaded_file.type, "x-upsert": "true"}
                        )
                        st.success(f"Success! '{uploaded_file.name}' has been securely saved and organized under your user profile.")
                    except Exception as e:
                        st.error(f"Storage system upload failed: {e}")
        
        # Display Saved Files List
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="section-container"><div class="section-title">Your Current Document Inventory</div></div>', unsafe_allow_html=True)
        try:
            # List contents inside the user's personal storage folder layout
            user_folder = f"{st.session_state.user_id}"
            categories = ["Academic Transcripts", "Extracurricular Proofs", "Essay Drafts", "Other Credentials"]
            
            for cat in categories:
                path_to_list = f"{user_folder}/{cat}".replace(" ", "_")
                files = supabase.storage.from_("student-files").list(path_to_list)
                
                if files:
                    st.write(f"📁 **{cat}**")
                    for f in files:
                        if f.get('name') != '.emptyFolderPlaceholder':
                            st.write(f"  • {f.get('name')}")
        except Exception:
            st.info("No documents have been logged to your repository file index yet.")
