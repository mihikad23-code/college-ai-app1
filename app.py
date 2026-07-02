import streamlit as st
import google.generativeai as genai

# ==========================================
# 1. INITIAL CONFIGURATION & API SETUP
# ==========================================
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
except Exception:
    st.error("Please set up your GEMINI_API_KEY in your Streamlit secrets.")

st.set_page_config(page_title="IvyPilot AI", page_icon="🎓", layout="centered")

st.title("🎓 IvyPilot AI")
st.subheader("Your Personalized, Data-Driven College Admissions Counselor")
st.write("Input your profile details below to receive a custom admissions analysis and strategy plan.")

# ==========================================
# 2. USER PROFILE INPUT FORM
# ==========================================
st.header("📋 Student Profile Details")

col1, col2 = st.columns(2)

with col1:
    # Added Grade Level selection
    student_grade = st.selectbox(
        "Current Grade / Year Level",
        ["Grade 8", "Grade 9", "Grade 10", "Grade 11 / IB1", "Grade 12 / IB2", "Other"]
    )
    academic_system = st.selectbox(
        "Academic Curriculum",
        ["Cambridge (IGCSE/A-Levels)", "IB Diploma", "US High School Diploma", "CBSE / ICSE", "Other"]
    )

with col2:
    gpa_metrics = st.text_input("Current Grades / Results (e.g., Straight A*s, 42/45 IB, 95%)")
    target_major = st.text_input("Intended Major / Field (e.g., Finance, Computer Science)")

target_countries = st.text_input("Target Countries / Regions (e.g., US, UK, Singapore)")

st.subheader("🌟 Extracurriculars & Leadership")
activities = st.text_area(
    "List your activities, web projects, or leadership positions:",
    placeholder="e.g., Built an academic resource website, school debate team..."
)

st.subheader("🎯 Target Institutions")
dream_colleges = st.text_area(
    "List the colleges or types of universities you want to target:",
    placeholder="e.g., NYU Stern, London School of Economics, NUS"
)

# ==========================================
# 3. AI PROCESSING LOGIC
# ==========================================
if st.button("🚀 Analyze My Profile & Generate Strategy"):
    if not gpa_metrics or not target_major or not dream_colleges:
        st.warning("Please fill out your Grades, Major, and Target Colleges to get an accurate analysis.")
    else:
        with st.spinner("Analyzing data vectors, historic admission rates, and profile strengths..."):
            
            analysis_prompt = f"""
            You are an elite, highly insightful, and encouraging AI College Admissions Counselor. 
            Analyze the following student profile details and provide a comprehensive, tailored strategy.
            Make the target roadmap highly custom for their exact current grade level.

            STUDENT PROFILE:
            - Current Grade Level: {student_grade}
            - Curriculum: {academic_system}
            - Grades/GPA: {gpa_metrics}
            - Intended Major: {target_major}
            - Target Regions: {target_countries}
            - Extracurriculars/Projects: {activities}
            - Student's Desired Colleges: {dream_colleges}

            PLEASE PROVIDE YOUR RESPONSE IN THE FOLLOWING FORMAT USING CLEAR MARKDOWN:

            ### 📊 1. Profile Strength Assessment
            Evaluate the current strength of the profile for the intended major based on their grade level. Highlight key unique selling points.

            ### 🎯 2. College List Categorization
            Analyze the student's desired colleges based on their profile. Categorize them into Reach, Match, and Safety schools.

            ### 🛠️ 3. Strategic Roadmap for {student_grade}
            Provide clear, actionable steps tailored to a student currently in {student_grade} to build their profile over the coming years:
            - **Academic Strategy:** (Subject choices, track recommendations, or academic competitions)
            - **Profile Building & Extracurriculars:** (How to scale current resource tools, build a narrative around their major, or build impact projects)
            - **Timeline Milestones:** (What they should focus on doing right now this year)
            """

            try:
                # Updated to the fully live current production model to fix 404 errors
                model = genai.GenerativeModel("gemini-2.5-flash")
                response = model.generate_content(analysis_prompt)
                
                st.success("Analysis Complete!")
                st.markdown("---")
                st.markdown(response.text)
                st.markdown("---")
                
            except Exception as e:
                st.error(f"An error occurred while connecting to the AI engine: {e}")
