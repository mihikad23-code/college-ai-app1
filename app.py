import streamlit as st
import google.generativeai as genai

# ==========================================
# 1. INITIAL CONFIGURATION & API SETUP
# ==========================================
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
except Exception:
    st.error("Please set up your GEMINI_API_KEY in your Streamlit secrets.")

st.set_page_config(
    page_title="IvyPilot Corporate", 
    layout="wide", 
    initial_sidebar_state="collapsed"
)

# Premium Enterprise Theme Injection
st.markdown("""
    <style>
    /* Global App Background and Font Override */
    .stApp {
        background-color: #FAFAFA;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }
    
    /* Executive Header Banner */
    .header-banner {
        background: linear-gradient(135deg, #0F172A 0%, #1E3A8A 100%);
        padding: 40px;
        border-radius: 12px;
        margin-bottom: 35px;
        color: #FFFFFF;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    .main-title {
        font-size: 38px;
        font-weight: 700;
        letter-spacing: -0.5px;
        margin-bottom: 8px;
    }
    .sub-title {
        font-size: 16px;
        font-weight: 300;
        color: #93C5FD;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* Clean Section Dividers */
    .section-container {
        margin-top: 30px;
        margin-bottom: 20px;
    }
    .section-title {
        font-size: 20px;
        font-weight: 600;
        color: #0F172A;
        border-left: 4px solid #2563EB;
        padding-left: 12px;
        margin-bottom: 20px;
    }
    
    /* Minimalist Form Field Borders */
    div[data-baseweb="select"], div[data-baseweb="input"], textarea {
        border-radius: 6px !important;
        border-color: #E2E8F0 !important;
        background-color: #FFFFFF !important;
    }
    
    /* Premium Blockquote / AI Card Styling */
    div.stMarkdown blockquote {
        background-color: #FFFFFF;
        border-left: 4px solid #10B981;
        padding: 20px;
        border-radius: 0px 8px 8px 0px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    </style>
""", unsafe_allow_html=True)

# Executive Header Section
st.markdown("""
    <div class="header-banner">
        <div class="sub-title">Predictive Admissions Analytics</div>
        <div class="main-title">IvyPilot Intelligence</div>
    </div>
""", unsafe_allow_html=True)

# ==========================================
# 2. APPLICATION MATRIX (STRUCTURED ROWS)
# ==========================================

# SECTION 1: ACADEMIC PROFILE
st.markdown('<div class="section-container"><div class="section-title">Academic Architecture</div></div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
with col1:
    student_grade = st.selectbox(
        "Cohort Placement / Current Grade",
        ["Grade 8", "Grade 9", "Grade 10", "Grade 11 / IB1", "Grade 12 / IB2", "Other"]
    )
with col2:
    academic_system = st.selectbox(
        "Curriculum Framework",
        ["Cambridge (IGCSE/A-Levels)", "IB Diploma", "US High School Diploma", "CBSE / ICSE", "Other"]
    )
with col3:
    gpa_metrics = st.text_input(
        "Cumulative Performance Metric (GPA / Percentage)", 
        placeholder="e.g., 3.92/4.0, 42/45 IB, 95%"
    )

col4, col5 = st.columns(2)
with col4:
    test_scores = st.text_input(
        "Standardized Testing Benchmarks (SAT / ACT / AP / Core Exams)", 
        placeholder="e.g., SAT: 1540, AP Calculus: 5"
    )
with col5:
    academic_interests = st.text_input(
        "Primary Academic Strengths", 
        placeholder="e.g., Quantitative Methods, Macroeconomics"
    )

# SECTION 2: TARGET PARAMETERS
st.markdown('<div class="section-container"><div class="section-title">Institutional Strategy Parameters</div></div>', unsafe_allow_html=True)

col6, col7 = st.columns(2)
with col6:
    target_major = st.text_input(
        "Intended Discipline / Major Focus", 
        placeholder="e.g., Computer Science & Operational Research"
    )
with col7:
    target_countries = st.text_input(
        "Target Jurisdictions / Global Regions", 
        placeholder="e.g., United States, United Kingdom, Singapore"
    )

# SECTION 3: QUALITATIVE PROFILE DATA
st.markdown('<div class="section-container"><div class="section-title">Qualitative Profile Data Vectors</div></div>', unsafe_allow_html=True)

activities = st.text_area(
    "Extracurricular Portfolio & Leadership Engagements",
    placeholder="Detail strategic engagements, independent technical projects, research initiatives, or founding operations...",
    height=120
)

core_passions = st.text_area(
    "Independent Intellectual Pursuits & Personal Disciplines",
    placeholder="Identify intrinsic motivations, technical proficiencies, or specific domains researched independently outside mandatory settings...",
    height=100
)

dream_colleges = st.text_area(
    "Target Institutional Pipeline",
    placeholder="List primary target universities or competitive tiers tiering preference (e.g., Stanford University, LSE, NUS)...",
    height=100
)

# ==========================================
# 3. ANALYTICS EXECUTION
# ==========================================
st.markdown("<br>", unsafe_allow_html=True)

# Custom stylized action button
if st.button("Execute Strategic Profile Evaluation", type="primary"):
    if not gpa_metrics or not target_major or not dream_colleges:
        st.warning("Action Deferred: Please fill out Academic Metrics, Intended Discipline, and Target Pipeline to proceed.")
    else:
        with st.spinner("Executing analytical assessment matrices..."):
            
            analysis_prompt = f"""
            You are a senior executive-level College Admissions Strategist. 
            Analyze the following operational profile parameters and provide a formal, highly corporate, objective strategic advisory report.

            PROFILE CONSTANTS:
            - Cohort Placement: {student_grade}
            - Framework: {academic_system}
            - Quantitative Metrics: {gpa_metrics}
            - Standardized Testing: {test_scores}
            - Focus Domains: {academic_interests}
            - Intended Discipline: {target_major}
            - Jurisdictions: {target_countries}
            - Portfolio Engagements: {activities}
            - Intellectual Pursuits: {core_passions}
            - Target Institutions: {dream_colleges}

            CRITICAL CONSTANTS: CRITICAL: AVOID ALL EMOJIS, TRITE PHRASES, OR CONGRATULATORY LANGUAGE. CHOOSE AN EXECUTIVE, DATA-DRIVEN, SYSTEMATIC TONALITY.

            FORMAT COMPLIANCE REQUIREMENT:

            ### 1. Quantitative and Portfolio Assessment
            Evaluate applicant matrix relative to baseline competitive parameters for top-tier international standard models in the target discipline.

            ### 2. Institutional Target Optimization Matrix
            Synthesize applicant viability. Categorize institutional options precisely into:
            - Tier 1: Aggressive Stretch Targets (Low probability / Amplification mandatory)
            - Tier 2: Aligned Viable Targets (Competitive index matching target metrics)
            - Tier 3: High-Probability Core Anchors (High statistical security)

            ### 3. Tactical Development Roadmap: Milestone Horizon
            Provide targeted, measurable optimizations for a candidate positioned in {student_grade}:
            - Curriculum and Academic Optimizations: Recommended rigorous pathways, advanced track considerations, or institutional contests.
            - Portfolio Scaling and Narrative Leverage: Operational blueprints to scale current technical/resource tools and build deep vertical expertise.
            - Near-Term Strategic Focus Items: Objectives demanding execution within the current active financial/academic calendar year.
            """

            try:
                model = genai.GenerativeModel("gemini-2.5-flash")
                response = model.generate_content(analysis_prompt)
                
                st.success("Analysis finalized successfully.")
                st.markdown("---")
                st.markdown(response.text)
                st.markdown("---")
                
            except Exception as e:
                st.error(f"System Link Interrupted: Unable to reach analysis core engine. Error details: {e}")
