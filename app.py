import streamlit as st

from utils.pdf_parser import extract_text_from_pdf
from utils.matcher import calculate_match_score
from utils.skill_extractor import extract_skills
from utils.analytics import (
    create_skill_chart,
    create_score_chart
)


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown(
    """
    <style>

    .main-title {
        font-size: 42px;
        font-weight: 700;
        text-align: center;
        margin-bottom: 5px;
    }

    .subtitle {
        text-align: center;
        color: #777;
        font-size: 18px;
        margin-bottom: 30px;
    }

    .section-title {
        font-size: 25px;
        font-weight: 600;
        margin-top: 20px;
    }

    .skill-box {
        padding: 8px 12px;
        margin: 5px;
        border-radius: 8px;
        display: inline-block;
        background-color: #f1f3f6;
        font-weight: 500;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# HEADER
# =========================================================

st.markdown(
    '<div class="main-title">🤖 AI Resume Analyzer</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Smart Resume & Job Matching System'
    '</div>',
    unsafe_allow_html=True
)

st.divider()


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.header("📌 How It Works")

    st.write(
        """
        **Step 1:** Upload your resume PDF.

        **Step 2:** Paste the job description.

        **Step 3:** Click Analyze Resume.

        **Step 4:** AI analyzes your resume.

        **Step 5:** View your job match score.

        **Step 6:** Check matched and missing skills.
        """
    )

    st.divider()

    st.info(
        "💡 Tip: Use the complete job description "
        "for better results."
    )

    st.divider()

    st.write("### 🛠️ Technologies")

    st.write(
        """
        🐍 Python

        📊 Pandas

        🤖 Scikit-learn

        🧠 NLP

        📄 PDF Processing

        📈 Plotly

        🎨 Streamlit
        """
    )


# =========================================================
# INPUT SECTION
# =========================================================

col1, col2 = st.columns(2)


with col1:

    st.subheader("📄 Upload Resume")

    uploaded_file = st.file_uploader(
        "Upload your resume in PDF format",
        type=["pdf"]
    )

    if uploaded_file:

        st.success(
            f"Uploaded: {uploaded_file.name}"
        )


with col2:

    st.subheader("💼 Job Description")

    job_description = st.text_area(
        "Paste the job description here",
        height=220,
        placeholder=(
            "Example:\n\n"
            "We are looking for a Machine Learning Intern.\n\n"
            "Requirements:\n"
            "Python\n"
            "Machine Learning\n"
            "Pandas\n"
            "NumPy\n"
            "SQL\n"
            "Scikit-learn\n"
            "Git"
        )
    )


st.divider()


# =========================================================
# ANALYZE BUTTON
# =========================================================

analyze_button = st.button(
    "🚀 Analyze Resume",
    use_container_width=True,
    type="primary"
)


# =========================================================
# ANALYSIS
# =========================================================

if analyze_button:

    # -----------------------------------------------------
    # CHECK RESUME
    # -----------------------------------------------------

    if uploaded_file is None:

        st.warning(
            "⚠️ Please upload your resume first."
        )

        st.stop()


    # -----------------------------------------------------
    # CHECK JOB DESCRIPTION
    # -----------------------------------------------------

    if not job_description.strip():

        st.warning(
            "⚠️ Please paste a job description."
        )

        st.stop()


    # -----------------------------------------------------
    # EXTRACT RESUME TEXT
    # -----------------------------------------------------

    with st.spinner(
        "📄 Reading your resume..."
    ):

        try:

            resume_text = extract_text_from_pdf(
                uploaded_file
            )

        except Exception as error:

            st.error(
                f"❌ Error reading PDF: {error}"
            )

            st.stop()


    # -----------------------------------------------------
    # CHECK EXTRACTED TEXT
    # -----------------------------------------------------

    if not resume_text.strip():

        st.error(
            "❌ No readable text was found in the PDF."
        )

        st.info(
            "Try uploading a text-based PDF instead "
            "of a scanned image PDF."
        )

        st.stop()


    # -----------------------------------------------------
    # CALCULATE TEXT SIMILARITY
    # -----------------------------------------------------

    with st.spinner(
        "🧠 Calculating job compatibility..."
    ):

        try:

            similarity_score = calculate_match_score(
                resume_text,
                job_description
            )

        except Exception as error:

            st.error(
                f"❌ Error calculating match score: {error}"
            )

            st.stop()


    # -----------------------------------------------------
    # EXTRACT SKILLS
    # -----------------------------------------------------

    with st.spinner(
        "🔍 Extracting skills..."
    ):

        try:

            resume_skills = extract_skills(
                resume_text
            )

            job_skills = extract_skills(
                job_description
            )

        except Exception as error:

            st.error(
                f"❌ Error extracting skills: {error}"
            )

            st.stop()


    # =====================================================
    # COMPARE SKILLS
    # =====================================================

    resume_skills_lower = {
        skill.lower(): skill
        for skill in resume_skills
    }

    job_skills_lower = {
        skill.lower(): skill
        for skill in job_skills
    }


    matched_skills = []

    missing_skills = []


    for skill in job_skills_lower:

        if skill in resume_skills_lower:

            matched_skills.append(
                job_skills_lower[skill]
            )

        else:

            missing_skills.append(
                job_skills_lower[skill]
            )


    # =====================================================
    # SKILL MATCH PERCENTAGE
    # =====================================================

    if len(job_skills) > 0:

        skill_match_percentage = round(
            (
                len(matched_skills)
                /
                len(job_skills)
            )
            * 100,
            2
        )

    else:

        skill_match_percentage = 0


    # =====================================================
    # ANALYSIS COMPLETED
    # =====================================================

    st.success(
        "✅ Resume analysis completed successfully!"
    )


    st.markdown(
        '<div class="section-title">'
        '🎯 Analysis Results'
        '</div>',
        unsafe_allow_html=True
    )


    # =====================================================
    # TOP METRICS
    # =====================================================

    metric1, metric2, metric3, metric4 = st.columns(4)


    with metric1:

        st.metric(
            "🎯 Job Match",
            f"{similarity_score}%"
        )


    with metric2:

        st.metric(
            "🧠 Skill Match",
            f"{skill_match_percentage}%"
        )


    with metric3:

        st.metric(
            "✅ Matched Skills",
            len(matched_skills)
        )


    with metric4:

        st.metric(
            "❌ Missing Skills",
            len(missing_skills)
        )


    # =====================================================
    # JOB MATCH SCORE
    # =====================================================

    st.divider()

    st.subheader(
        "🎯 Job Compatibility"
    )

    st.progress(
        min(
            max(
                similarity_score / 100,
                0.0
            ),
            1.0
        )
    )


    if similarity_score >= 80:

        st.success(
            "🔥 Excellent match! Your resume is highly "
            "relevant to this job."
        )

    elif similarity_score >= 60:

        st.info(
            "👍 Good match! You have several relevant "
            "skills for this position."
        )

    elif similarity_score >= 40:

        st.warning(
            "⚠️ Moderate match. Consider improving "
            "your resume with relevant skills."
        )

    else:

        st.error(
            "❌ Low match. You may need more skills "
            "relevant to this position."
        )


    # =====================================================
    # SKILL GAP ANALYSIS
    # =====================================================

    st.divider()

    st.subheader(
        "🧠 Skill Gap Analysis"
    )


    skill_col1, skill_col2 = st.columns(2)


    # -----------------------------------------------------
    # MATCHED SKILLS
    # -----------------------------------------------------

    with skill_col1:

        st.success(
            f"✅ Matched Skills ({len(matched_skills)})"
        )

        if matched_skills:

            for skill in matched_skills:

                st.markdown(
                    f"""
                    <div class="skill-box">
                    ✓ {skill}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        else:

            st.write(
                "No matching skills found."
            )


    # -----------------------------------------------------
    # MISSING SKILLS
    # -----------------------------------------------------

    with skill_col2:

        st.error(
            f"❌ Missing Skills ({len(missing_skills)})"
        )

        if missing_skills:

            for skill in missing_skills:

                st.markdown(
                    f"""
                    <div class="skill-box">
                    • {skill}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        else:

            st.write(
                "🎉 Great! No major skills are missing."
            )


    # =====================================================
    # REQUIRED SKILL COVERAGE
    # =====================================================

    st.divider()

    st.subheader(
        "📊 Required Skill Coverage"
    )

    st.progress(
        min(
            max(
                skill_match_percentage / 100,
                0.0
            ),
            1.0
        )
    )

    st.write(
        f"You currently match **{len(matched_skills)} "
        f"out of {len(job_skills)} required skills.**"
    )


    # =====================================================
    # ANALYTICS DASHBOARD
    # =====================================================

    st.divider()

    st.subheader(
        "📈 Resume Analytics Dashboard"
    )


    chart_col1, chart_col2 = st.columns(2)


    # -----------------------------------------------------
    # SKILL CHART
    # -----------------------------------------------------

    with chart_col1:

        try:

            skill_chart = create_skill_chart(
                len(matched_skills),
                len(missing_skills)
            )

            st.plotly_chart(
                skill_chart,
                use_container_width=True
            )

        except Exception as error:

            st.error(
                f"Unable to create skill chart: {error}"
            )


    # -----------------------------------------------------
    # SCORE CHART
    # -----------------------------------------------------

    with chart_col2:

        try:

            score_chart = create_score_chart(
                similarity_score,
                skill_match_percentage
            )

            st.plotly_chart(
                score_chart,
                use_container_width=True
            )

        except Exception as error:

            st.error(
                f"Unable to create score chart: {error}"
            )


    # =====================================================
    # RECOMMENDATIONS
    # =====================================================

    st.divider()

    st.subheader(
        "💡 Personalized Recommendations"
    )


    if missing_skills:

        st.write(
            "Based on the job description, "
            "consider learning or highlighting:"
        )

        for skill in missing_skills:

            st.write(
                f"📚 **{skill}**"
            )

    else:

        st.success(
            "🎉 Your resume contains all the detected "
            "skills required by this job!"
        )


    # =====================================================
    # RESUME SKILLS
    # =====================================================

    with st.expander(
        "🔍 View All Skills Detected in Resume"
    ):

        if resume_skills:

            for skill in resume_skills:

                st.write(
                    f"✓ {skill}"
                )

        else:

            st.write(
                "No skills detected."
            )


    # =====================================================
    # JOB SKILLS
    # =====================================================

    with st.expander(
        "💼 View Skills Detected in Job Description"
    ):

        if job_skills:

            for skill in job_skills:

                st.write(
                    f"• {skill}"
                )

        else:

            st.write(
                "No skills detected."
            )


    # =====================================================
    # EXTRACTED RESUME
    # =====================================================

    with st.expander(
        "📄 View Extracted Resume Text"
    ):

        st.text_area(
            "Resume Content",
            resume_text,
            height=400
        )


    # =====================================================
    # JOB DESCRIPTION
    # =====================================================

    with st.expander(
        "💼 View Job Description"
    ):

        st.write(
            job_description
        )


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "🤖 AI Resume Analyzer | "
    "Python • NLP • Scikit-learn • Plotly • Streamlit"
)