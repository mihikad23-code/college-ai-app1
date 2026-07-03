import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="IvyPilot Portal", layout="centered", initial_sidebar_state="auto")

# Premium Ultra-Dark High-Contrast Theme
st.markdown("""
    <style>
    /* Global background setup */
    .stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
        background-color: #0F172A !important;
    }
    /* Enforce crisp high-contrast text rendering */
    label, p, span, h1, h2, h3, h4, .stMarkdown, [data-testid="stHeader"] * {
        color: #FFFFFF !important;
    }
    /* Interactive form field element restyling */
    div[data-baseweb="input"] input, textarea, select, div[data-baseweb="select"] {
        background-color: #1E293B !important;
        color: #FFFFFF !important;
        border: 1px solid #475569 !important;
    }
    /* Fix drop-down selection options contrast */
    div[data-baseweb="select"] * {
        color: #0F172A !important;
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

# ==========================================
# 1. GENERATIVE AI ENGINE LIFTLINE
# ==========================================
try:
    # Looks directly inside your Streamlit Cloud Dashboard secrets panel for your key
    GEMINI_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=GEMINI_KEY)
except Exception as e:
    st.error(f"Configuration Missing: Ensure GEMINI_API_KEY is defined inside your Streamlit Secrets panel. Error: {e}")

# ==========================================
# 2. APP HEADER & LAYOUT INTERFACE
# ==========================================
st.title("IvyPilot AI Portal")
st.caption("Personalized Strategy Engine and Profile Performance Analytics Workspace")
st.markdown("---")

# Main Input Framework Card
st.markdown('<div class="form-card">', unsafe_allow_html=True)
st.subheader("📊 Academic Metrics Dataset")
col1, col2 = st.columns(2)
with col1:
    student_grade = st.selectbox("Current Grade Level", ["Grade 8", "Grade 9", "Grade 10", "Grade 11 / IB1", "Grade 12 / IB2"])
    academic_system = st.selectbox("Curriculum Framework", ["Cambridge (IGCSE/A-Levels)", "IB Diploma", "US High School Diploma", "CBSE / ICSE", "Other"])
with col2:
    gpa_metrics = st.text_input("Current Grades / Performance Indices", placeholder="e.g., Straight A*s, 3.97 UW GPA")
    test_scores = st.text_input("External Exam Records / Benchmarks", placeholder="e.g., Checkpoint results, SAT practice metrics")
    
subjects_taken = st.text_input("Chosen Subjects / Specific Branch Combinations", placeholder="e.g., Extended Mathematics, Economics, Business Studies")
st.markdown('</div>', unsafe_allow_html=True)

# Target Setting Framework Card
st.markdown('<div class="form-card">', unsafe_allow_html=True)
st.subheader("🎯 Target Configurations")
col3, col4 = st.columns(2)
with col3:
    target_major = st.text_input("Intended Concentration or Career Track", placeholder="e.g., Corporate Finance / Investment Banking")
with col4:
    target_countries = st.text_input("Geographic Target Destinations", placeholder="e.g., UK, US, Singapore")
st.markdown('</div>', unsafe_allow_html=True)

# Qualitative Portfolio Card
st.markdown('<div class="form-card">', unsafe_allow_html=True)
st.subheader("💡 Qualitative Parameters Portfolio")
activities = st.text_area("Extracurricular Engagement Details", placeholder="School clubs, leadership dynamics, competitions, or active initiatives...")
independent_projects = st.text_area("Independent Research & Digital Platforms Launched", placeholder="Detail tools, databases, resources, or web platforms you host independently...")
core_passions = st.text_area("Intrinsic Passions & Outside Interests", placeholder="What domains, market sectors, or specialized areas do you track outside structural assignments?")
dream_colleges = st.text_area("Target Institution Preferences", placeholder="List specific higher-education colleges or dream global university profiles...")
st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# 3. STRATEGY DISPATCH PROCESSOR
# ==========================================
if st.button("Execute Strategic Admissions Analysis", type="primary"):
    if not gpa_metrics or not target_major or not dream_colleges:
        st.warning("Incomplete Data Layer: Please populate your Grade Metrics, Target Major, and Dream Colleges to activate the analytical core.")
    else:
        with st.spinner("Compiling academic framework parameters..."):
            
            analysis_prompt = (
                f"You are a premium, highly strategic global admissions consultant evaluating a profile. "
                f"User Profile Details:\n"
                f"- Grade: {student_grade}\n"
                f"- Curriculum: {academic_system}\n"
                f"- Performance Marks: {gpa_metrics}\n"
                f"- Selected Subjects: {subjects_taken}\n"
                f"- Benchmarks/Tests: {test_scores}\n"
                f"- Concentration/Career Path: {target_major}\n"
                f"- Geographic Targets: {target_countries}\n"
                f"- Activities: {activities}\n"
                f"- Projects: {independent_projects}\n"
                f"- Core Passions: {core_passions}\n"
                f"- Institutional Targets: {dream_colleges}\n\n"
                f"Provide a highly clear, professional, macro-level strategic evaluation. "
                f"Structure your feedback using clear Markdown Headers (#, ##, ###) covering:\n"
                f"1. Profile Strengths and Competitive Position\n"
                f"2. Curriculum Context and Competitive Alignment (evaluating their subject choices for their target path)\n"
                f"3. Reach / Match / Safety Breakdown for their listed target destinations\n"
                f"4. Actionable Multi-Year Milestones and Strategic Recommendations\n\n"
                f"Strict Formatting Condition: Output pure, crisp text and headings. Do not output any emojis or icons anywhere in your text."
            )
            
            try:
                model = genai.GenerativeModel("gemini-2.5-flash")
                response = model.generate_content(analysis_prompt)
                
                st.success("Analysis Generation Complete.")
                st.markdown("---")
                st.markdown(response.text)
                
            except Exception as e:
                st.error(f"Strategy Engine dropped connection: {e}")
