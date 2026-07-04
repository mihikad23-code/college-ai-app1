import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="IvyPilot Portal", layout="centered", initial_sidebar_state="auto")

# Premium Ultra-Dark High-Contrast Theme (Enforces readability across all dynamic elements)
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
    /* Drop-down selection box values (closed state) */
    div[data-baseweb="select"] div {
        color: #FFFFFF !important;
    }
    /* TARGETED DROPDOWN MENU FIX: Forces dark dropdown boxes with clean white text options */
    div[data-baseweb="popover"] ul, div[role="listbox"], div[role="listbox"] li {
        background-color: #1E293B !important;
        color: #FFFFFF !important;
    }
    /* Ensure hover states inside dropdown list remain clearly visible */
    div[role="listbox"] li:hover {
        background-color: #334155 !important;
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
st.caption("Universal Strategic Admissions Profile Analyzer")
st.markdown("---")

# Section 1: Academic Dataset
st.markdown('<div class="form-card">', unsafe_allow_html=True)
st.subheader("📊 Academic Baseline")
col1, col2 = st.columns(2)
with col1:
    student_grade = st.text_input("Current Grade / Year Level", placeholder="e.g., Grade 8, Year 9, Grade 11 / IB1")
    academic_system = st.text_input("Current Educational Framework", placeholder="e.g., Cambridge, IB, National Curriculum, US High School")
with col2:
    gpa_metrics = st.text_input("Academic Performance / Marks Baseline", placeholder="e.g., Straight A*s, 3.9 GPA, 95%")
    test_scores = st.text_input("Standardized Testing / External Benchmarks", placeholder="e.g., Diagnostic metrics, Checkpoints, SAT, APs")
    
subjects_taken = st.text_area("Current Course Load / Subject Selection", placeholder="List all subjects currently being taken or confirmed for the upcoming term...")
st.markdown('</div>', unsafe_allow_html=True)

# Section 2: Goals
st.markdown('<div class="form-card">', unsafe_allow_html=True)
st.subheader("🎯 Academic & Professional Targets")
col3, col4 = st.columns(2)
with col3:
    target_major = st.text_input("Intended Focus / Major / Career Track", placeholder="e.g., Corporate Finance, Computer Science, Undecided")
with col4:
    target_countries = st.text_input("Geographic Destinations", placeholder="e.g., UK, US, Canada, Domestic, Global")
st.markdown('</div>', unsafe_allow_html=True)

# Section 3: Portfolio
st.markdown('<div class="form-card">', unsafe_allow_html=True)
st.subheader("💡 Qualitative Parameters & Engagement")
activities = st.text_area("Extracurricular Activities & Leadership Profile", placeholder="Detail school clubs, community initiatives, sports, or regular commitments...")
independent_projects = st.text_area("Independent Projects / Developed Media / Platforms", placeholder="Detail any personal sites, research papers, resource tools, or independent creations...")
core_passions = st.text_area("Intellectual Passions & Self-Directed Interests", placeholder="What specific topics or areas do you study, track, or read about purely out of personal curiosity?")
dream_colleges = st.text_area("Target Institutions / Profiles", placeholder="List specific higher-education colleges or general university profiles you are aiming for...")
st.markdown('</div>', unsafe_allow_html=True)

# Run Strategic Analysis
if st.button("Execute Strategic Profile Analysis", type="primary"):
    if not gpa_metrics or not target_major or not dream_colleges:
        st.warning("Data Missing: Please populate the performance metrics, intended focus, and target institution fields to generate an accurate analysis.")
    else:
        with st.spinner("Compiling profile strategy layers..."):
            # A perfectly balanced, objective prompt blueprint that acts purely on input parameters
            analysis_prompt = (
                f"You are an expert, highly objective global admissions consultant evaluating a student's profile baseline.\n\n"
                f"Profile Input Parameters:\n"
                f"- Academic Level: {student_grade}\n"
                f"- Educational System: {academic_system}\n"
                f"- Academic Standings/Grades: {gpa_metrics}\n"
                f"- Subject Portfolio: {subjects_taken}\n"
                f"- Testing Benchmarks: {test_scores}\n"
                f"- Stated Core Focus/Career Intent: {target_major}\n"
                f"- Targeted Geographic Regions: {target_countries}\n"
                f"- Activities Data: {activities}\n"
                f"- Independent Work/Projects: {independent_projects}\n"
                f"- Focus Areas/Passions: {core_passions}\n"
                f"- Institutional Targets: {dream_colleges}\n\n"
                f"Strict Parameters for Response:\n"
                f"1. Evaluate the profile strictly as it stands today based on the precise text provided. Do not extrapolate, assume future high school paths, or guess subsequent graduation systems (e.g., do not predict A-Levels vs IB unless explicit in the text).\n"
                f"2. Keep the advice highly objective, avoiding generic statements. Analyze how well their current course combinations, metrics, and qualitative actions line up with their specified career or academic path.\n"
                f"3. Frame the feedback logically within their regional target context.\n\n"
                f"Structure the final output precisely using these Markdown Headers (#, ##, ###):\n"
                f"- Profile Evaluation & Current Standings\n"
                f"- Curricular Alignment & Choice Assessment\n"
                f"- Institutional Positioning Analysis\n"
                f"- Strategic Milestones & Recommended Interventions\n\n"
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
