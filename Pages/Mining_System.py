import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
from utils import (
    get_data, 
    prepare_diesel_data, 
    create_monthly_chart, 
    create_cumulative_chart,
    create_cost_drivers_table,
    create_impact_card
)
from dictionaries import Data, Variable, Elements

# Configuration and styling
def setup_page():
    st.set_page_config(
        layout="wide",
        page_title="Mining System",
    )
    
    st.markdown(
        """
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        body {background-color:#f5f6f7;}
        
        .title-card {
            width: 100%;
            background-color:#e6e6e6;
            padding: 12px 0;
            border-radius:6px;
            border:1px solid #d0d0d0;
            text-align:center;
            font-size:22px;
            font-weight:600;
            color:#333333;
            margin-bottom:25px;
        }
        
        div.stButton > button {
            background-color:#ffffff;
            border:1px solid #cccccc;
            border-radius:6px;
            padding:16px 18px;
            font-size:20px;
            font-weight:600;
            color:#444444;
            width:100%;
            text-align:left;
            margin-bottom:25px;
        }
        div.stButton > button:hover {
            border-color:#999999;
            background-color:#f5f5f5;
        }
        
        .equal-height-card {
            border:1px solid #ccc;
            padding:15px;
            border-radius:6px;
            background-color:#fafafa;
            color:#333;
        }
        
        .bottom-card {
            min-height:230px;
        }
        
        .equal-height-card table {
            width:100%;
            border-collapse:collapse;
            font-size:13px;
        }
        .equal-height-card table td {
            padding:6px;
        }
        .equal-height-card table tr:nth-child(even) {
            background-color:#ffffff;
        }
        .equal-height-card table tr:nth-child(odd) {
            background-color:#f3f3f3;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

def create_sidebar():
    with st.sidebar:
        selected_element = option_menu(
            "Cost Elements",
            Variable["Mining System"],
            default_index=0,
            orientation="vertical",
            key="cost_element_menu",
        )

        selected_item_name = None
        selected_item_code = None

        element_items = Elements.get(selected_element, {})
        if element_items:
            display_items = [f"{name} : {code}" for name, code in element_items.items()]
            selected_display = option_menu(
                selected_element,
                display_items,
                default_index=0,
                orientation="vertical",
                key=f"item_menu_{selected_element}",
            )
            if selected_display:
                name, code = selected_display.split(" : ")
                selected_item_name = name.strip()
                selected_item_code = code.strip()
    
    return selected_item_name, selected_item_code

def create_title_card(selected_item_name, selected_item_code):
    display_code = (
        selected_item_code
        if selected_item_name == "Diesel" and selected_item_code
        else "406105"
    )
    
    st.markdown(
        f"""
        <div class="title-card">
            Cost breakdown: Diesel {display_code}
        </div>
        """,
        unsafe_allow_html=True,
    )
    return display_code

def create_upload_section():
    upload_col, _ = st.columns([1.5, 3])
    with upload_col:
        goto_scenarios = st.button("Upload diesel scenario", key="goto_scenarios")
        if goto_scenarios:
            try:
                st.switch_page("pages/Scenarios.py")
            except Exception:
                st.experimental_set_query_params(page="Scenarios")

def display_diesel_analysis(df, display_code):
    if df.empty:
        st.warning("No data available for Diesel.")
        return

    monthly = prepare_diesel_data(df)
    
    # Create charts
    fig_month = create_monthly_chart(monthly, display_code)
    fig_cum = create_cumulative_chart(monthly, display_code)
    
    # Display charts
    chart1, chart2 = st.columns(2)
    chart1.plotly_chart(fig_month, use_container_width=True)
    chart2.plotly_chart(fig_cum, use_container_width=True)
    
    # Display bottom cards
    bottom_left, bottom_right = st.columns([2, 1.2])
    with bottom_left:
        st.markdown(create_cost_drivers_table(monthly), unsafe_allow_html=True)
    with bottom_right:
        st.markdown(create_impact_card(display_code), unsafe_allow_html=True)

def main():
    setup_page()
    
    # Sidebar
    selected_item_name, selected_item_code = create_sidebar()
    
    # Title
    display_code = create_title_card(selected_item_name, selected_item_code)
    
    # Upload section
    create_upload_section()
    
    # Main content
    try:
        df = get_data(Data["Mining System"])

        if selected_item_name == "Diesel":
            display_diesel_analysis(df, display_code)
        else:
            st.write("Select Consumables → Diesel from the sidebar.")
            
    except Exception as e:
        st.error(str(e))

if __name__ == "__main__":
    main()