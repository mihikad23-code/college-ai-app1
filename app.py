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
    page_title="IvyPilot AI", 
    layout="wide", 
    initial_sidebar_state="collapsed"
)

# Deep CSS Override to Fix Universal Contrast Issues
st.markdown("""
    <style>
    /* Force main app structural background to light grey */
    .stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
        background-color: #F8FAFC !important;
    }
    
    /* UNIVERSAL FORCE COLOR: Turns absolutely all standard text blocks to dark slate */
    * {
        color: #0F172A !important;
    }
    
    /* Top Header Banner Custom Style Container */
    .header-banner {
        background: linear-gradient(135deg, #0F172A 0%, #1E40AF 100%);
        padding: 40px;
        border-radius: 12px;
        margin-bottom: 35px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
    }
    
    /* ISOLATE BANNER TEXT: Force header text elements to stay stark white */
    .header-banner *, .main-title, .sub-title {
        color: #FFFFFF !important;
    }
    .main-title {
        font-size: 36px;
        font-weight: 700;
        margin-bottom: 6px;
    }
    .sub-title {
        font-size: 15px;
        font-weight: 400;
        letter-spacing: 0.5px;
    }
    
    /* Section Separation Containers */
    .section-container {
        margin-top: 35px;
        margin-bottom: 15px;
    }
    .section-title {
        font-size: 20px;
        font-weight: 600;
        color: #0F172A !important;
        border-left: 4px solid #2563EB;
        padding-left: 12px;
    }
    
    /* Input Fields and Select Dropdowns Framework Setup */
    div[data-baseweb="select"], div[data-baseweb="input"], textarea, select, input {
        border-radius: 8px !important;
        background-color: #FFFFFF !important;
        border: 1px solid #CBD5E1 !important;
    }
    
    /* Ensure typing text color inside text areas and input boxes stays dark slate */
    input, textarea, div[data-baseweb="select"] span, div[data-baseweb="input"] input {
        color: #0F172A !important;
    }
    
    /* Submit Action Button Text Color Alignment */
    button[kind="primary"] p {
        color: #FFFFFF !important;
    }
    
    /* AI Strategy Output Block Formatting */
    div.stMarkdown blockquote {
        background-color: #FFFFFF !important;
        border-left: 4px solid #2563EB !important;
        padding: 24px;
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.03);
    }
    div.stMarkdown blockquote * {
        color: #1E293B !important;
    }
    </style>
""", unsafe_allow_html=True)

# Application Header HTML
st.markdown("""
    <div class="header-banner">
        <div class="main-title">IvyPilot AI</div>
        <div class="sub-title">Personalized Profile Analysis and College Admissions Strategy</div>
    </div>
""", unsafe_allow_html=True)

# ==========================================
# 2. STRATEGY FRAMEWORK INPUT FIELDS
# ==========================================

st.markdown('<div class="section-container"><div class="section-title">1. Academic Framework Details</div></div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
with col1:
    student_grade = st.selectbox(
        "Current Grade Level",
        ["Grade 8", "Grade 9", "Grade 10", "Grade 11 / IB1", "Grade 12 / IB2", "Other"]
    )
with col2:
    academic_system = st.selectbox(
        "Curriculum System",
        ["Cambridge (IGCSE/A-Levels)", "IB Diploma", "US High School Diploma", "CBSE / ICSE", "Other"]
    )
with col3:
    gpa_metrics = st.text_input(
        "Current Grades / GPA / Percentages", 
        placeholder="e.g., Straight A*s, 42/45 IB, 95% aggregate"
    )

col4, col5 = st.columns(2)
with col4:
    subjects_taken = st.text_input(
        "Specific Subjects Chosen / Higher Levels (HL)",
        placeholder="e.g., Math AA HL, Economics HL, Physics SL, or specific IGCSE subjects"
    )
with col5:
    test_scores = st.text_input(
        "Standardized Tests & External Exams", 
        placeholder="e.g., SAT, ACT, AP exams, or Checkpoint results"
    )

st.markdown('<div class="section-container"><div class="section-title">2. Target College & Major Goals</div></div>', unsafe_allow_html=True)

col6, col7 = st.columns(2)
with col6:
    target_major = st.text_input(
        "Intended Major or Career Path", 
        placeholder="e.g., Corporate Finance, Investment Banking, Computer Science"
    )
with col7:
    target_countries = st.text_input(
        "Target Countries or Locations", 
        placeholder="e.g., United States, United Kingdom, Singapore, Europe"
    )

st.markdown('<div class="section-container"><div class="section-title">3. Extracurricular & Independent Projects Portfolio</div></div>', unsafe_allow_html=True)

activities = st.text_area(
    "Key Activities and Leadership Positions",
    placeholder="List school clubs, debate, sports, internships, or student leadership roles...",
    height=100
)

independent_projects = st.text_area(
    "Independent Projects and Digital Tools Developed",
    placeholder="Detail any academic resource tools, websites hosted, research papers, apps built, or charity initiatives launched...",
    height=100
)

core_passions = st.text_area(
    "Personal Interests and Favorite Research Topics",
    placeholder="What fields, subjects, or books do you read and research entirely on your own outside of class assignments?",
    height=80
)

dream_colleges = st.text_area(
    "Target Universities or College Lists",
    placeholder="List the dream institutions you want to evaluate (e.g., NYU Stern, London School of Economics, NUS, Ivy League)...",
    height=80
)

# ==========================================
# 3. AI STRATEGY ENGINE
# ==========================================
st.markdown("<br>", unsafe_allow_html=True)

if st.button("Analyze Profile & Generate Admissions Strategy", type="primary"):
    if not gpa_metrics or not target_major or not dream_colleges:
        st.warning("Please fill out your Grades, Intended Major, and Target Universities to run the analysis.")
    else:
        with st.spinner("Analyzing profile datasets and creating roadmap..."):
            
            analysis_prompt = f"""
            You are an elite, practical, and highly strategic College Admissions Advisor. 
            Analyze this student profile and provide a realistic, deeply tailored plan. 
            Keep the language direct, clear, and highly encouraging, without any fluff.

            STUDENT PROFILE:
            - Current Grade: {student_grade}
            - Curriculum Framework: {academic_system}
            - Current Grades: {gpa_metrics}
            - Specific Subjects/Levels: {subjects_taken}
            - Test Scores/External Exams: {test_scores}
            - Intended Major/Career Path: {target_major}
            - Target Countries: {target_countries}
            - Core Activities: {activities}
            - Independent Projects/Tools: {independent_projects}
            - Personal Interests/Research: {core_passions}
            - Target Universities: {dream_colleges}

            STRICT CONSTRAINT: DO NOT USE ANY EMOJIS IN YOUR RESPONSE. Use clear, plain markdown headers for your output.

            ### 1. Profile Strength Assessment
            Evaluate how competitive this profile is right now for their target major and locations. Highlight their unique strengths (such as building resource tools, independent web projects, or specific subject mastery).

            ### 2. College Categorization (Reach, Match, Safety)
            Break down the student's target universities into:
            - Reach Options (Highly competitive, requiring extra profile building)
            - Match Options (Realistic targets that align well with their current track)
            - Safety Options (High probability choices)
            If the list is unbalanced, suggest alternative choices that fit their major and location goals.

            ### 3. Step-by-Step Roadmap for {student_grade}
            Provide concrete, actionable goals tailored exactly for a student in {student_grade} to build their profile over the coming years:
            - Academic and Subject Strategy: Advice on subject choices, advanced tracks, specific subject packages, or useful academic competitions.
            - Scaling Projects & Impact: Clear ideas on how to grow their independent digital platforms, scale their web resource tools, find unique internships, or turn personal research into formal profile standouts.
            - Immediate Action Plan: Top 3 focus areas to work on right now during this academic year.
            """

            try:
                model = genai.GenerativeModel("gemini-2.5-flash")
                response = model.generate_content(analysis_prompt)
                
                st.success("Analysis complete.")
                st.markdown("---")
                st.markdown(response.text)
                st.markdown("---")
                
            except Exception as e:
                st.error(f"Could not connect to the analysis engine. Error details: {e}")
