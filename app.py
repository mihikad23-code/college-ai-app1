import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="IvyPilot Portal", layout="centered", initial_sidebar_state="auto")

# Premium Ultra-Dark High-Contrast Theme (Enforcing 100% White Text Everywhere)
st.markdown("""
    <style>
    /* Global background setup */
    .stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
        background-color: #0F172A !important;
    }
    /* Enforce crisp white text rendering across all standard text elements */
    label, p, span, h1, h2, h3, h4, .stMarkdown, [data-testid="stHeader"] * {
        color: #FFFFFF !important;
    }
    /* Interactive form field element restyling */
    div[data-baseweb="input"] input, textarea, select {
        background-color: #1E293B !important;
        color: #FFFFFF !important;
        border: 1px solid #475569 !important;
    }
    /* FORCE drop-down selection box values and placeholder elements to be white */
    div[data-baseweb="select"] * {
        color: #FFFFFF !important;
    }
    div[data-baseweb="popover"] *, div[role="listbox"] * {
        color: #0F172A !important; /* Kept dark purely inside the expanded click-menu so options are visible against white dropdown paper */
    }
    /* Primary action button styling */
    button[kind="primary"] {
        background-color: #2563EB !important;
        border: none !important;
        width: 100% !important;
    }
    button[kind="primary"] p {
        color: #FFFFFF !important;
        font-weight: 700 !important;
    }
    /* Structural card modules */
    .form-card {
        background-color: #1E293B !important;
        padding: 24px;
        border-radius: 12px;
        border: 1px solid #334155 !important;
        margin-bottom: 24px;
    }
    </style>
""", unsafe_allow_html=True)

# Global Client Configuration
try:
    GEMINI_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=GEMINI_KEY)
except Exception as e:
    st.error("Configuration Key Missing: Please update your GEMINI_API_KEY inside the Streamlit Advanced Secrets panel.")

st.title("IvyPilot AI Portal")
st.caption("Personalized Strategy Engine and Profile Performance Analytics Workspace")
st.markdown("---")

# Section 1: Academic Dataset
st.markdown('<div class="form-card">', unsafe_allow_html=True)
st.subheader("📊 Academic Metrics Dataset")
col1, col2 = col1, col2 = st.columns(2)
with col1:
    student_grade = st.selectbox("Current Grade Level", ["Grade 8", "Grade 9", "Grade 10", "Grade 11 / IB1", "Grade 12 / IB2"])
    academic_system = st.selectbox("Current Curriculum Framework", ["Cambridge (IGCSE/Checkpoint)", "IB Diploma", "US High School Diploma", "CBSE / ICSE", "Other"])
with col2:
    gpa_metrics = st.text_input("Current School Grades / Performance Indices", placeholder="e.g., Straight A*s, 90%+")
    test_scores = st.text_input("External Standardized Benchmarks", placeholder="e.g., Checkpoint results, SAT diagnostics")
    
subjects_taken = st.text_input("Subjects Currently Taken or Planned", placeholder="e.g., Math, Economics, Coordinated Sciences")
st.markdown('</div>', unsafe_allow_html=True)

# Section 2: Goals
st.markdown('<div class="form-card">', unsafe_allow_html=True)
st.subheader("🎯 Target Configurations")
col3, col4 = st.columns(2)
with col3:
    target_major = st.text_input("Intended Career Track / Area of Focus", placeholder="e.g., Corporate Finance / Global Banking")
with col4:
    target_countries = st.text_input("Geographic Target Destinations", placeholder="e.g., UK, US, Singapore")
st.markdown('</div>', unsafe_allow_html=True)

# Section 3: Portfolio
st.markdown('<div class="form-card">', unsafe_allow_html=True)
st.subheader("💡 Qualitative Parameters Portfolio")
activities = st.text_area("Extracurricular Activities & Initiatives", placeholder="List school clubs, competitions, leadership dynamics...")
independent_projects = st.text_area("Independent Research & Web Platforms Launched", placeholder="Detail resource tools, databases, or web apps you host independently...")
core_passions = st.text_area("Intrinsic Passions & Outside Interests", placeholder="What specialized areas do you track outside of school constraints?")
dream_colleges = st.text_area("Target Institution Preferences", placeholder="List specific higher-education profiles or colleges...")
st.markdown('</div>', unsafe_allow_html=True)

# Run Strategic Analysis
if st.button("Execute Strategic Admissions Analysis", type="primary"):
    if not gpa_metrics or not target_major or not dream_colleges:
        st.warning("Incomplete Data: Please complete your Grade Metrics, Target Major, and Target Colleges to continue.")
    else:
        with st.spinner("Compiling profile strategy layers..."):
            # Rigorous prompt constraint to stop assumptions regarding future high school tracks
            analysis_prompt = (
                f"You are a premium, highly objective global admissions consultant evaluating a profile context.\n\n"
                f"Core Profile Parameters:\n"
                f"- Current Student Grade: {student_grade}\n"
                f"- Current Curriculum Framework: {academic_system}\n"
                f"- Academic Marks: {gpa_metrics}\n"
                f"- Current Course Subjects: {subjects_taken}\n"
                f"- Benchmark/Test History: {test_scores}\n"
                f"- Target Concentration/Career Track: {target_major}\n"
                f"- Geographic Focus: {target_countries}\n"
                f"- Activities Data: {activities}\n"
                f"- Web Projects/Platforms Launched: {independent_projects}\n"
                f"- Core Interests/Passions: {core_passions}\n"
                f"- Listed Target Universities: {dream_colleges}\n\n"
                f"Strict Directives for Analysis:\n"
                f"1. DO NOT assume the user will transition to Cambridge A-Levels for high school simply because they are doing IGCSE or Checkpoint now. They may switch to IB DP or other systems. Evaluate ONLY the current status.\n"
                f"2. Avoid making qualitative assumptions or extrapolations about missing details. Stick exactly to the stated inputs to ensure high analytical accuracy.\n"
                f"3. Frame the entire analysis around how their current baseline sets them up for their stated career track ({target_major}).\n\n"
                f"Structure your response with clear Markdown Headers (#, ##, ###):\n"
                f"- Profile Competitive Position Analysis\n"
                f"- Curriculum Subject Alignment Evaluation\n"
                f"- Initial Institutional Competitive Mapping (Reach / Match / Safety perspective based strictly on current metrics)\n"
                f"- Tactical Recommendations & Clear Milestones\n\n"
                f"Formatting Constraint: Output raw, clean markdown text. Absolutely zero emojis or icons are permitted anywhere."
            )
            
            try:
                model = genai.GenerativeModel("gemini-2.5-flash")
                response = model.generate_content(analysis_prompt)
                
                st.success("Analysis Generation Complete.")
                st.markdown("---")
                st.markdown(response.text)
            except Exception as e:
                st.error(f"Strategy Engine dropped connection: {e}")
