from streamlit_lottie import st_lottie
import requests
import streamlit as st

st.set_page_config(
    page_title="Cost Management System",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    .block-container {
        padding-top: 0rem !important;
        background-color: white !important;
    }
    .sidebar .sidebar-content {
        background-color: white !important;
    }
    .stApp {
        background-color: white !important;
    }
    [data-testid="stAppViewContainer"] {
        background-color: white !important;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown("""
    <div style="
        margin-top: 0;
        padding: 25px 0px;
        text-align: center;
        background: #0b4f91;
        color: white;
        width: 100%;
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

vFile = "https://assets10.lottiefiles.com/packages/lf20_059pfp0Z5i.json"
r = requests.get(vFile)
LottieCode = None if r.status_code != 200 else r.json()

col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    st.markdown("<br><br>", unsafe_allow_html=True)
    if LottieCode:
        st_lottie(LottieCode, height=600, width=600, speed=1, loop=True, key="main_lottie")
    else:
        st.error("Failed to load animation")