import streamlit as st
import google.generativeai as genai

# ==========================================
# 1. INITIAL CONFIGURATION & API SETUP
# ==========================================
# Securely fetch the API key from Streamlit's secrets manager
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
except Exception:
    st.error("Please set up your GEMINI_API_KEY in your Streamlit secrets.")

# Set up the app page layout
st.set_page_config(page_title="IvyPilot AI", page_icon="🎓", layout="centered")

# App Header
st.title("🎓 IvyPilot AI")
st.subheader("Your Personalized, Data-Driven College Admissions Counselor")
st.write("Input your profile details below to receive a custom admissions analysis and strategy plan.")

# ==========================================
# 2. USER PROFILE INPUT FORM
# ==========================================
st.header("📋 Student Profile Details")

col1, col2 = st.columns(2)

with col1:
    academic_system = st.selectbox(
        "Academic Curriculum",
        ["IB Diploma", "Cambridge (A-Levels/IGCSE)", "US High School Diploma", "CBSE / ICSE", "Other"]
    )
    gpa_metrics = st.text_input("Current Grades / GPA (e.g., 3.9/4.0, 42/45 IB, 95%)")

with col2:
    target_major = st.text_input("Intended Major / Field of Study (e.g., Finance, Computer Science)")
    target_countries = st.text_input("Target Countries / Regions (e.g., US, UK, Singapore)")

# Extracurriculars & Achievements
st.subheader("🌟 Extracurriculars & Leadership")
activities = st.text_area(
    "List your top activities, projects, internships, or leadership positions:",
    placeholder="e.g., Founded a student resource website, Captain of debate team, Completed a finance research report..."
)

# Dream Colleges
st.subheader("🎯 Target Institutions")
dream_colleges = st.text_area(
    "List the colleges or types of universities you want to target:",
    placeholder="e.g., NYU Stern, London School of Economics, NUS, University of Toronto"
)

# ==========================================
# 3. AI PROCESSING LOGIC
# ==========================================
if st.button("🚀 Analyze My Profile & Generate Strategy"):
    if not gpa_metrics or not target_major or not dream_colleges:
        st.warning("Please fill out your Grades, Major, and Target Colleges to get an accurate analysis.")
    else:
        with st.spinner("Analyzing data vectors, historic admission rates, and profile strengths..."):
            
            # Construct a structured prompt to guide the AI's behavior
            analysis_prompt = f"""
            You are an elite, highly insightful, and encouraging AI College Admissions Counselor. 
            Analyze the following student profile details and provide a comprehensive, tailored strategy.

            STUDENT PROFILE:
            - Curriculum: {academic_system}
            - Grades/GPA: {gpa_metrics}
            - Intended Major: {target_major}
            - Target Regions: {target_countries}
            - Extracurriculars/Projects: {activities}
            - Student's Desired Colleges: {dream_colleges}

            PLEASE PROVIDE YOUR RESPONSE IN THE FOLLOWING FORMAT USING CLEAR MARKDOWN:

            ### 📊 1. Profile Strength Assessment
            Evaluate the current strength of the profile for the intended major. Highlight key unique selling points (e.g., unique web projects, specific research papers).

            ### 🎯 2. College List Categorization
            Analyze the student's desired colleges based on their profile. Categorize them into:
            - **Reach Schools:** (High stretch but possible)
            - **Match Schools:** (Good fit with competitive chance)
            - **Safety Schools:** (High probability of admission)
            If the listed schools are unrealistic, recommend alternative target options.

            ### 🛠️ 3. Strategic Gap Analysis & Roadmap
            Provide clear, actionable steps to improve admissions chances over the next 1-3 years:
            - **Academic Strategy:** (Subject choices, test score targets like SAT/ACT, or academic competitions)
            - **Profile Building & Extracurriculars:** (How to scale current projects, build a narrative around their major, or find internships)
            - **Essays & Recommendations:** (Key themes they should focus on highlighting)
            """

            try:
                # Initialize the Gemini Flash model
                model = genai.GenerativeModel("gemini-1.5-flash")
                response = model.generate_content(analysis_prompt)
                
                # Render the AI's response beautifully on the screen
                st.success("Analysis Complete!")
                st.markdown("---")
                st.markdown(response.text)
                st.markdown("---")
                
            except Exception as e:
                st.error(f"An error occurred while connecting to the AI engine: {e}")
