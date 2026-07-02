import streamlit as st
import google.generativeai as genai
from supabase import create_client, Client
import os

# ==========================================
# 1. BULLETPROOF DIRECT DATABASE CONNECTION
# ==========================================
# We are hardcoding the key check to ensure 'supabase' is always defined
try:
    # Attempt to load from secrets first
    GEMINI_KEY = st.secrets.get("AQ.Ab8RN6Lkn3_xuzg-zEM6aZxu4JmrLlAsETSY6a-KqaJ8AIVJSg", "")
    SUPABASE_URL = st.secrets.get("//xeiwkcteindimxbcsoub.supabase.co", "")
    SUPABASE_KEY = st.secrets.get("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InhlaXdrY3RlaW5kaW14YmNzb3ViIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODI5ODk0NTUsImV4cCI6MjA5ODU2NTQ1NX0.KZYU22pRFDVu9MOAncExjozUJiCxqEgawLwMrRwBpbY", "")
    
    # IF SECRETS ARE FAILING, UNCOMMENT THESE LINES AND PASTE YOUR STRINGS DIRECTLY:
    # SUPABASE_URL = "https://your-project-id.supabase.co"
    # SUPABASE_KEY = "your-anon-public-key"
    # GEMINI_KEY = "your-gemini-key"

    if GEMINI_KEY:
        genai.configure(api_key=GEMINI_KEY)
    else:
        genai.configure(api_key="Bypass") # Fallback to prevent startup crash

    # Force create the client connection so it is NEVER undefined
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

except Exception as e:
    st.error(f"Critical Connection Error: {e}")
    # Emergency fallback definition to prevent button crashes
    try:
        supabase = create_client("https://placeholder.supabase.co", "placeholder")
    except Exception:
        pass

st.set_page_config(page_title="IvyPilot Portal", layout="centered", initial_sidebar_state="auto")

# Clean Interface Structure
st.title("IvyPilot AI Portal")
st.caption("Personalized Profile Analysis and Academic File Management Dashboard")
st.markdown("---")

# Initialize Session States
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user_email" not in st.session_state:
    st.session_state.user_email = ""
if "user_id" not in st.session_state:
    st.session_state.user_id = ""

# ==========================================
# 2. LOGIN MANAGER
# ==========================================
if not st.session_state.logged_in:
    st.subheader("🔑 Account Access Gateway")
    
    auth_col1, auth_col2 = st.columns([1, 1])
    
    with auth_col1:
        st.markdown("**OAuth Shortcuts:**")
        if st.button("🌐 Sign in with Google", use_container_width=True):
            st.info("To activate production Google Sign-In, redirect URIs must be assigned inside your Supabase Auth dashboard panel.")
            
    with auth_col2:
        st.markdown("**Direct Email Portal:**")
        auth_mode = st.radio("Choose Action", ["Sign In", "Create Account"])
        email = st.text_input("Email Address", placeholder="name@example.com")
        password = st.text_input("Password", type="password")
        
        if auth_mode == "Create Account":
            if st.button("Register Account", type="primary", use_container_width=True):
                try:
                    res = supabase.auth.sign_up({"email": email, "password": password})
                    st.success("Account registration sent! Check your inbox or Supabase logs to verify.")
                except Exception as e:
                    st.error(f"Registration Interrupted: {e}")
        else:
            if st.button("Log In", type="primary", use_container_width=True):
                try:
                    res = supabase.auth.sign_in_with_password({"email": email, "password": password})
                    st.session_state.logged_in = True
                    st.session_state.user_email = res.user.email
                    st.session_state.user_id = res.user.id
                    st.rerun()
                except Exception as e:
                    st.error("Login verification failed. Check your credentials or confirmation status.")

# ==========================================
# 3. APPLICATION WORKSPACE
# ==========================================
else:
    status_col1, status_col2 = st.columns([3, 1])
    with status_col1:
        st.success(f"Connected Securely As: **{st.session_state.user_email}**")
    with status_col2:
        if st.button("Log Out", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.user_email = ""
            st.session_state.user_id = ""
            st.rerun()
            
    st.markdown("<br>", unsafe_allow_html=True)
    app_tab, vault_tab = st.tabs(["📊 Profile Strategy Engine", "📁 Document Storage Vault"])
    
    with app_tab:
        st.header("Academic Performance Dataset")
        col1, col2 = st.columns(2)
        with col1:
            student_grade = st.selectbox("Current Grade Level", ["Grade 8", "Grade 9", "Grade 10", "Grade 11 / IB1", "Grade 12 / IB2"])
            academic_system = st.selectbox("Curriculum Framework", ["Cambridge (IGCSE/A-Levels)", "IB Diploma", "US High School Diploma", "CBSE / ICSE", "Other"])
        with col2:
            gpa_metrics = st.text_input("Current Grades / Performance Indices", placeholder="e.g., Straight A*s, 42/45 IB")
            test_scores = st.text_input("External Exam Records / Benchmarks", placeholder="e.g., SAT, Checkpoint results")
            
        subjects_taken = st.text_input("Chosen Subjects / Specific Combinations", placeholder="e.g., Math AA HL, Economics HL")
        
        st.header("Admissions Target Configurations")
        col3, col4 = st.columns(2)
        with col3:
            target_major = st.text_input("Intended Concentration or Career Goal", placeholder="e.g., Corporate Finance, Investment Banking")
        with col4:
            target_countries = st.text_input("Geographic Destinations", placeholder="e.g., US, UK, Singapore")
            
        st.header("Qualitative Parameters Portfolio")
        activities = st.text_area("Extracurricular Engagement Details", placeholder="List school clubs, student leadership roles, internships...")
        independent_projects = st.text_area("Independent Research & Web Platforms Built", placeholder="Detail academic resource sites hosted, digital tools, or charity initiatives launched...")
        core_passions = st.text_area("Intrinsic Passions & Topics You Track Independently", placeholder="What domains do you read about entirely outside of class?")
        dream_colleges = st.text_area("Target Institution Preferences", placeholder="List your high-priority dream universities...")
        
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Execute Strategic Admissions Analysis", type="primary", use_container_width=True):
            if not gpa_metrics or not target_major or not dream_colleges:
                st.warning("Data Missing: Please complete required parameters.")
            else:
                with st.spinner("Processing evaluation parameters..."):
                    analysis_prompt = f"Advisor Mode. User Grade: {student_grade}, Curriculum: {academic_system}, Grades: {gpa_metrics}, Subjects: {subjects_taken}, Tests: {test_scores}, Major: {target_major}, Target Countries: {target_countries}, Activities: {activities}, Projects: {independent_projects}, Passions: {core_passions}, Targets: {dream_colleges}. Structure feedback cleanly into plain markdown headers covering Profile Assessment, Reach/Match/Safety breakdown, and an actionable roadmap timeline. Strict condition: Do not output any emojis."
                    try:
                        model = genai.GenerativeModel("gemini-2.5-flash")
                        response = model.generate_content(analysis_prompt)
                        st.success("Strategy Compiled Successfully.")
                        st.info(response.text)
                    except Exception as e:
                        st.error(f"Analysis engine connection dropped: {e}")

    with vault_tab:
        st.header("Secure Credentials Repository")
        file_category = st.selectbox("Target File Repository Folder", ["Academic Transcripts", "Extracurricular Proofs", "Essay Drafts", "Other Credentials"])
        uploaded_file = st.file_uploader("Upload Document Asset (PDF, PNG, JPG, DOCX)", type=["pdf", "png", "jpg", "jpeg", "docx"])
        
        if uploaded_file is not None:
            if st.button("Commit File Asset to Vault", type="primary", use_container_width=True):
                with st.spinner("Archiving asset layer..."):
                    try:
                        clean_filename = f"{file_category}/{uploaded_file.name}".replace(" ", "_")
                        storage_path = f"{st.session_state.user_id}/{clean_filename}"
                        file_bytes = uploaded_file.getvalue()
                        
                        supabase.storage.from_("student-files").upload(
                            path=storage_path,
                            file=file_bytes,
                            file_options={"content-type": uploaded_file.type, "x-upsert": "true"}
                        )
                        st.success(f"Successfully archived: {uploaded_file.name}")
                    except Exception as e:
                        st.error(f"Repository pipeline error: {e}")
                        
        st.markdown("---")
        st.subheader("Current Document Catalog Inventory")
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
            st.info("No records present in your document catalog index yet.")
