import streamlit as st
import pandas as pd
import numpy as np
from streamlit_mermaid import st_mermaid
from utils import (
    load_scenario_data,
    calculate_scenario_metrics,
    create_scenario_mermaid,
    fmt0,
    fmt2
)

def setup_page():
    st.set_page_config(
        layout="wide",
        page_title="Diesel Scenario Analyzer",
    )
    
    hide_streamlit_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)
    
    st.markdown(
        """
        <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            background: #ffffff;
            min-height: 100vh;
        }

        .main-container {
            background: #ffffff;
            border-radius: 12px;
            margin: 20px;
            padding: 30px;
            border: 1px solid #e6f2e6;
        }

        .upload-section {
            background: #f8fffb;
            border-radius: 12px;
            padding: 25px;
            margin-bottom: 30px;
            border: 2px dashed #4caf50;
            transition: all 0.3s ease;
        }

        .upload-section:hover {
            border-color: #2e7d32;
            background: #f1f8e9;
        }

        .upload-title {
            font-size: 28px;
            font-weight: 700;
            color: #2e7d32;
            margin-bottom: 8px;
            text-align: center;
        }

        .upload-subtitle {
            font-size: 14px;
            color: #666666;
            margin-bottom: 20px;
            text-align: center;
        }

        .diagram-container {
            background: #f8fffb;
            border-radius: 12px;
            padding: 30px;
            margin: 25px 0;
            border: 1px solid #e6f2e6;
        }

        .simulation-btn {
            background: #4caf50;
            color: white;
            border: none;
            padding: 12px 35px;
            border-radius: 8px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
        }

        .simulation-btn:hover {
            background: #2e7d32;
            transform: translateY(-2px);
        }

        .file-info {
            background: #f1f8e9;
            border-radius: 8px;
            padding: 15px;
            margin-top: 15px;
            border-left: 4px solid #4caf50;
        }

        .metric-card {
            background: white;
            border-radius: 10px;
            padding: 20px;
            margin: 10px 0;
            border: 1px solid #e6f2e6;
            box-shadow: 0 2px 8px rgba(76, 175, 80, 0.1);
        }

        .metric-title {
            font-size: 16px;
            font-weight: 600;
            color: #2e7d32;
            margin-bottom: 10px;
        }

        .metric-value {
            font-size: 24px;
            font-weight: 700;
            margin-bottom: 5px;
            color: #1b5e20;
        }

        .metric-label {
            font-size: 12px;
            color: #666666;
        }

        .actual-badge {
            background: #e8f5e9;
            color: #2e7d32;
            padding: 4px 12px;
            border-radius: 12px;
            font-size: 11px;
            font-weight: 600;
        }

        .budget-badge {
            background: #f1f8e9;
            color: #4caf50;
            padding: 4px 12px;
            border-radius: 12px;
            font-size: 11px;
            font-weight: 600;
        }

        .card-header {
            background: #4caf50;
            color: white;
            padding: 15px 20px;
            border-radius: 8px 8px 0 0;
            margin: -20px -20px 15px -20px;
            font-weight: 600;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

def create_header():
    st.markdown('<div class="upload-title">Diesel Scenario Analysis</div>', unsafe_allow_html=True)
    st.markdown('<div class="upload-subtitle">Upload your diesel scenario data to visualize cost drivers and performance metrics</div>', unsafe_allow_html=True)

def create_upload_section():
    st.markdown('<div class="upload-section">', unsafe_allow_html=True)
    
    uploaded = st.file_uploader(
        "Drag and drop your Excel file here",
        type=["xlsx"],
        key="diesel_scenario_file",
        help="Upload diesel scenario Excel file (max 3MB)"
    )

    if uploaded:
        st.markdown(f'''
        <div class="file-info">
            <strong>{uploaded.name}</strong> • {uploaded.size // 1024} KB • Ready for analysis
        </div>
        ''', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    return uploaded

def create_metric_cards(metrics):
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f'''
        <div class="metric-card">
            <div class="card-header">Cost Overview</div>
            <div class="metric-value">R {fmt0(metrics["diesel_actual"])}</div>
            <div class="metric-label">Actual Cost</div>
            <span class="actual-badge">ACTUAL</span>
        </div>
        ''', unsafe_allow_html=True)
    
    with col2:
        st.markdown(f'''
        <div class="metric-card">
            <div class="card-header">Budget Analysis</div>
            <div class="metric-value">R {fmt0(metrics["diesel_budget"])}</div>
            <div class="metric-label">Budget Cost</div>
            <span class="budget-badge">BUDGET</span>
        </div>
        ''', unsafe_allow_html=True)
    
    with col3:
        st.markdown(f'''
        <div class="metric-card">
            <div class="card-header">Production Volume</div>
            <div class="metric-value">{fmt0(metrics["total_t_actual"])} T</div>
            <div class="metric-label">Total Production</div>
            <span class="actual-badge">ACTUAL</span>
        </div>
        ''', unsafe_allow_html=True)
    
    with col4:
        st.markdown(f'''
        <div class="metric-card">
            <div class="card-header">Efficiency Metrics</div>
            <div class="metric-value">{fmt2(metrics["con_actual"])} L/T</div>
            <div class="metric-label">Consumption Rate</div>
            <span class="actual-badge">ACTUAL</span>
        </div>
        ''', unsafe_allow_html=True)

def create_simulation_button():
    col1, col2, col3 = st.columns([2, 1, 2])
    with col2:
        if st.button("Run Scenario Simulation", key="simulate", use_container_width=True):
            st.success("Scenario simulation completed successfully!")

def main():
    setup_page()
    
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    
    create_header()
    uploaded = create_upload_section()

    if uploaded:
        df = load_scenario_data(uploaded)
        metrics = calculate_scenario_metrics(df)
        create_metric_cards(metrics)
        
        mermaid_code = create_scenario_mermaid(
            metrics["diesel_actual"], metrics["diesel_budget"],
            metrics["qty_actual"], metrics["qty_budget"],
            metrics["price_actual"], metrics["price_budget"],
            metrics["con_actual"], metrics["con_budget"],
            metrics["ob_actual"], metrics["ob_budget"],
            metrics["rom_actual"], metrics["rom_budget"]
        )
        
        st.markdown('<div class="diagram-container">', unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1, 8, 1])
        with col2:
            st_mermaid(mermaid_code, height=500)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        default_metrics = {
            'qty_actual': np.nan, 'qty_budget': np.nan,
            'price_actual': np.nan, 'price_budget': np.nan,
            'con_actual': np.nan, 'con_budget': np.nan,
            'ob_actual': np.nan, 'ob_budget': np.nan,
            'rom_actual': np.nan, 'rom_budget': np.nan,
            'diesel_actual': np.nan, 'diesel_budget': np.nan,
            'total_t_actual': np.nan, 'total_t_budget': np.nan
        }
        create_metric_cards(default_metrics)
        
        mermaid_code = create_scenario_mermaid(
            np.nan, np.nan, np.nan, np.nan, np.nan, np.nan,
            np.nan, np.nan, np.nan, np.nan, np.nan, np.nan
        )
        
        st.markdown('<div class="diagram-container">', unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1, 8, 1])
        with col2:
            st_mermaid(mermaid_code, height=500)
        st.markdown('</div>', unsafe_allow_html=True)

    create_simulation_button()
    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()