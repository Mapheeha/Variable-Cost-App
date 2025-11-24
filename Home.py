import streamlit as st

st.set_page_config(
    page_title="Cost Management System",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    /* Remove top padding */
    .block-container {
        padding-top: 0rem !important;
        background-color: white !important;
    }

    /* Remove sidebar background color */
    .sidebar .sidebar-content {
        background-color: white !important;
    }

    /* Remove overall app tint */
    .stApp {
        background-color: white !important;
    }

    /* Remove any Streamlit gray backgrounds */
    [data-testid="stAppViewContainer"] {
        background-color: white !important;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown("""
    <div style="
        margin-top: 0;
        padding: 20px 0px;
        text-align: center;
        background: white;
        color: black;
        width: 100%;
        border-bottom: 1px solid #ddd;
    ">
        <h1 style="
            font-size: 2.5rem;
            font-weight: 600;
            margin: 0;
        ">
            Welcome to Cost Management System
        </h1>
    </div>
    """,
    unsafe_allow_html=True
)
