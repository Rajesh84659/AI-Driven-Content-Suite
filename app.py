import streamlit as st
import pandas as pd
from datetime import datetime

from modules.prompt_manager import PromptManager
from modules.generator import generate_content
from modules.evaluator import evaluate_content
from modules.storage import (
    save_prompt,
    save_output,
    save_refine_prompt,
    save_refine_output,
    save_evaluation
)


# -----------------------------------------------------
# PAGE CONFIG
# -----------------------------------------------------

st.set_page_config(
    page_title="AI Content Suite",
    page_icon="",
    layout="wide"
)


# -----------------------------------------------------
# CUSTOM CSS
# -----------------------------------------------------

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600&family=DM+Mono:wght@400;500&display=swap');

    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif;
    }

    /* Hide default Streamlit header padding */
    .block-container {
        padding-top: 3.5rem;
        padding-bottom: 2rem;
        max-width: 1400px;
    }

    /* App background */
    .stApp {
        background-color: #f7f8fa;
    }

    /* Main title */
    .app-title {
        font-size: 1.75rem;
        font-weight: 600;
        color: #111827;
        letter-spacing: -0.02em;
        margin-bottom: 0.15rem;
    }

    .app-subtitle {
        font-size: 0.9rem;
        color: #6b7280;
        margin-bottom: 1.5rem;
        font-weight: 400;
    }

    /* Section cards */
    .section-card {
        background: #ffffff;
        border: 1px solid #e5e7eb;
        border-radius: 10px;
        padding: 1.25rem 1.5rem;
        margin-bottom: 1.25rem;
    }

    .section-label {
        font-size: 0.7rem;
        font-weight: 600;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        color: #9ca3af;
        margin-bottom: 0.5rem;
    }

    .section-title {
        font-size: 1rem;
        font-weight: 600;
        color: #111827;
        margin-bottom: 0.75rem;
    }

    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background-color: #ffffff;
        border-right: 1px solid #e5e7eb;
    }

    [data-testid="stSidebar"] .block-container {
        padding-top: 1.5rem;
    }

    .sidebar-section-title {
        font-size: 0.7rem;
        font-weight: 600;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        color: #9ca3af;
        margin-bottom: 0.75rem;
        margin-top: 0.5rem;
    }

    /* Input labels */
    label {
        font-size: 0.82rem !important;
        font-weight: 500 !important;
        color: #374151 !important;
    }

    /* Select boxes and inputs */
    .stSelectbox > div > div,
    .stTextInput > div > div {
        border-radius: 7px !important;
        border-color: #d1d5db !important;
        font-size: 0.875rem !important;
    }

    /* Buttons */
    .stButton > button {
        width: 100%;
        border-radius: 7px;
        font-family: 'DM Sans', sans-serif;
        font-size: 0.85rem;
        font-weight: 500;
        height: 2.5rem;
        transition: all 0.15s ease;
    }

    .stButton > button[kind="primary"] {
        background-color: #111827;
        border: none;
        color: #ffffff;
    }

    .stButton > button[kind="primary"]:hover {
        background-color: #1f2937;
        box-shadow: 0 2px 8px rgba(17,24,39,0.18);
    }

    .stButton > button[kind="secondary"] {
        background-color: #f3f4f6;
        border: 1px solid #e5e7eb;
        color: #374151;
    }

    .stButton > button[kind="secondary"]:hover {
        background-color: #e5e7eb;
    }

    /* Text area */
    .stTextArea > div > div > textarea {
        font-family: 'DM Mono', monospace !important;
        font-size: 0.82rem !important;
        border-radius: 7px !important;
        border-color: #d1d5db !important;
        background-color: #fafafa !important;
        color: #111827 !important;
        line-height: 1.65 !important;
    }

    /* Code block */
    .stCode {
        border-radius: 7px !important;
        font-size: 0.8rem !important;
    }

    /* Expander */
    .streamlit-expanderHeader {
        font-size: 0.85rem !important;
        font-weight: 500 !important;
        color: #374151 !important;
        background-color: #f9fafb !important;
        border-radius: 7px !important;
        border: 1px solid #e5e7eb !important;
    }

    /* Tables */
    .stTable table {
        font-size: 0.82rem;
        border-collapse: separate;
        border-spacing: 0;
        width: 100%;
        border-radius: 8px;
        overflow: hidden;
        border: 1px solid #e5e7eb;
    }

    .stTable table thead tr th {
        background-color: #f3f4f6;
        color: #374151;
        font-weight: 600;
        font-size: 0.75rem;
        letter-spacing: 0.04em;
        text-transform: uppercase;
        padding: 0.6rem 1rem;
        border-bottom: 1px solid #e5e7eb;
    }

    .stTable table tbody tr td {
        padding: 0.55rem 1rem;
        color: #111827;
        border-bottom: 1px solid #f3f4f6;
        vertical-align: middle;
    }

    .stTable table tbody tr:last-child td {
        border-bottom: none;
    }

    .stTable table tbody tr:hover td {
        background-color: #f9fafb;
    }

    /* Divider */
    hr {
        border: none;
        border-top: 1px solid #e5e7eb;
        margin: 1rem 0;
    }

    /* Info box */
    .stInfo {
        border-radius: 7px;
        font-size: 0.85rem;
    }

    /* Warning */
    .stAlert {
        border-radius: 7px;
        font-size: 0.85rem;
    }

    /* Footer caption */
    .stCaption {
        font-size: 0.75rem;
        color: #9ca3af;
    }

    /* Subheader override */
    h3 {
        font-size: 1rem !important;
        font-weight: 600 !important;
        color: #111827 !important;
        letter-spacing: -0.01em !important;
    }

    /* Spinner text */
    .stSpinner > div {
        font-size: 0.85rem;
        color: #6b7280;
    }
</style>
""", unsafe_allow_html=True)


# -----------------------------------------------------
# SESSION STATE
# -----------------------------------------------------

if "outline" not in st.session_state:
    st.session_state.outline = ""

if "draft" not in st.session_state:
    st.session_state.draft = ""

if "refined_content" not in st.session_state:
    st.session_state.refined_content = ""

if "evaluation_report" not in st.session_state:
    st.session_state.evaluation_report = {}

if "outline_prompt" not in st.session_state:
    st.session_state.outline_prompt = ""

if "draft_prompt" not in st.session_state:
    st.session_state.draft_prompt = ""

if "refine_prompt" not in st.session_state:
    st.session_state.refine_prompt = ""

if "output_id" not in st.session_state:
    st.session_state.output_id = ""

if "output_version" not in st.session_state:
    st.session_state.output_version = ""


# -----------------------------------------------------
# TITLE
# -----------------------------------------------------

st.markdown('<p class="app-title">AI-Driven Content Suite</p>', unsafe_allow_html=True)
st.markdown(
    '<p class="app-subtitle">Generate blogs, emails, and LinkedIn posts using an outline, draft, and refinement workflow.</p>',
    unsafe_allow_html=True
)


# -----------------------------------------------------
# SIDEBAR
# -----------------------------------------------------

st.sidebar.markdown('<p class="sidebar-section-title">Content Configuration</p>', unsafe_allow_html=True)

content_type = st.sidebar.selectbox(
    "Content Type",
    ["blog", "email", "linkedin_post"]
)

topic = st.sidebar.text_input(
    "Topic",
    placeholder="e.g. AI in Healthcare"
)

tone = st.sidebar.selectbox(
    "Tone",
    ["professional", "casual", "friendly"]
)

target_audience = st.sidebar.selectbox(
    "Target Audience",
    ["beginners", "developers", "business owners"]
)

refinement_type = st.sidebar.selectbox(
    "Refinement Style",
    ["professional", "casual", "friendly"]
)

st.sidebar.markdown("---")

st.sidebar.markdown('<p class="sidebar-section-title">Actions</p>', unsafe_allow_html=True)


# -----------------------------------------------------
# INITIALIZE PROMPT MANAGER
# -----------------------------------------------------

pm = PromptManager()


# -----------------------------------------------------
# GENERATE OUTLINE
# -----------------------------------------------------

if st.sidebar.button("Generate Outline", type="primary"):

    if topic.strip() == "":
        st.warning("Please enter a topic.")

    else:

        with st.spinner("Generating outline..."):

            outline_prompt = pm.build_outline_prompt(
                content_type=content_type,
                topic=topic,
                tone=tone,
                target_audience=target_audience
            )

            outline = generate_content(outline_prompt)

            st.session_state.outline_prompt = outline_prompt
            st.session_state.outline = outline

            prompt_id = save_prompt(
                action="outline",
                content_type=content_type,
                topic=topic,
                tone=tone,
                target_audience=target_audience,
                prompt=outline_prompt
            )
            save_output(
                action="outline",
                parent_prompt_id=prompt_id,
                topic=topic,
                content=outline
            )


# -----------------------------------------------------
# GENERATE DRAFT
# -----------------------------------------------------

if st.sidebar.button("Generate Draft", type="primary"):

    if st.session_state.outline == "":
        st.warning("Please generate outline first.")

    else:

        with st.spinner("Generating draft..."):

            draft_prompt = pm.build_draft_prompt(
                content_type=content_type,
                topic=topic,
                tone=tone,
                target_audience=target_audience,
                outline=st.session_state.outline
            )

            draft = generate_content(draft_prompt)

            st.session_state.draft_prompt = draft_prompt
            st.session_state.draft = draft

            report = evaluate_content(draft)
            st.session_state.evaluation_report = report

            prompt_id = save_prompt(
                action="draft",
                content_type=content_type,
                topic=topic,
                tone=tone,
                target_audience=target_audience,
                prompt=draft_prompt
            )
            output_id, output_version = save_output(
                action="draft",
                parent_prompt_id=prompt_id,
                topic=topic,
                content=draft
            )

            evaluation_id = save_evaluation(
                related_output_id=st.session_state.output_id,
                evaluation_data=report
            )

            st.session_state.output_id = output_id
            st.session_state.output_version = output_version


# -----------------------------------------------------
# REFINE CONTENT
# -----------------------------------------------------

if st.sidebar.button("Refine Content", type="primary"):

    if st.session_state.draft == "":
        st.warning("Please generate draft first.")

    else:

        with st.spinner("Refining content..."):

            refine_prompt = pm.build_refinement_prompt(
                refinement_type=refinement_type,
                content=st.session_state.draft,
                target_audience=target_audience
            )

            refined_content = generate_content(refine_prompt)

            st.session_state.refine_prompt = refine_prompt
            st.session_state.refined_content = refined_content

            refined_report = evaluate_content(refined_content)
            st.session_state.evaluation_report = refined_report

            refine_prompt_id, refine_prompt_version = save_refine_prompt(
                action="refinement",
                output_draft_id=st.session_state.output_id,
                refinement_type=refinement_type,
                prompt=refine_prompt,
                output_draft_version=st.session_state.output_version
            )

            save_refine_output(
                action="refinement",
                parent_prompt_id=refine_prompt_id,
                topic=topic,
                refinement_type=refinement_type,
                content=refined_content,
                refine_prompt_version=refine_prompt_version
            )

            evaluation_id = save_evaluation(
                related_output_id=st.session_state.output_id,
                evaluation_data=refined_report
            )


# -----------------------------------------------------
# MAIN LAYOUT
# -----------------------------------------------------

col1, col2 = st.columns([2, 1])


# -----------------------------------------------------
# LEFT SECTION
# -----------------------------------------------------

with col1:

    # OUTLINE PROMPT
    if st.session_state.outline_prompt:
        with st.expander("Outline Prompt", expanded=False):
            st.code(st.session_state.outline_prompt)

    # GENERATED OUTLINE
    if st.session_state.outline:
        st.subheader("Generated Outline")
        st.text_area(
            "Outline",
            st.session_state.outline,
            height=300
        )

    # DRAFT PROMPT
    if st.session_state.draft_prompt:
        with st.expander("Draft Prompt", expanded=False):
            st.code(st.session_state.draft_prompt)

    # GENERATED DRAFT
    if st.session_state.draft:
        st.subheader("Generated Draft")
        st.text_area(
            "Draft",
            st.session_state.draft,
            height=500
        )

    # REFINEMENT PROMPT
    if st.session_state.refine_prompt:
        with st.expander("Refinement Prompt", expanded=False):
            st.code(st.session_state.refine_prompt)

    # REFINED CONTENT
    if st.session_state.refined_content:
        st.subheader("Refined Content")
        st.text_area(
            "Refined Version",
            st.session_state.refined_content,
            height=500
        )


# -----------------------------------------------------
# RIGHT SECTION
# -----------------------------------------------------

with col2:

    st.subheader("Content Evaluation")

    if st.session_state.evaluation_report:

        evaluation_df = pd.DataFrame(
            list(st.session_state.evaluation_report.items()),
            columns=["Metric", "Value"]
        )

        st.table(evaluation_df)

    else:
        st.info("Evaluation report will appear here after generating a draft or refining content.")

    st.markdown("---")

    st.subheader("Current Content Details")

    details = {
        "Content Type": content_type,
        "Topic": topic,
        "Tone": tone,
        "Audience": target_audience,
        "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    details_df = pd.DataFrame(
        list(details.items()),
        columns=["Field", "Value"]
    )

    st.table(details_df)


# -----------------------------------------------------
# FOOTER
# -----------------------------------------------------

st.markdown("---")

st.caption(
    "Built with Streamlit · Generative AI · Prompt Engineering"
)