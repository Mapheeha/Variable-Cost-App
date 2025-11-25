import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import numpy as np
from streamlit_mermaid import st_mermaid

from utils import (
    get_data,
    prepare_diesel_data,
    create_monthly_chart,
    create_cumulative_chart,
    create_cost_drivers_table,
    create_impact_card,
    load_scenario_data,
    calculate_scenario_metrics,
    create_scenario_mermaid,
    fmt0,
    fmt2,
    apply_epbcs_and_simulation,   # must exist in utils.py
)

from dictionaries import Data, Variable, Elements


SIDEBAR_MENU_STYLE = {
    "container": {
        "padding": "0",
        "background-color": "#ffffff",
        "border-radius": "12px",
    },
    "icon": {"display": "none"},
    "nav-link": {
        "font-size": "14px",
        "text-align": "left",
        "padding": "10px 18px",
        "color": "#0f172a",
        "margin": "2px 6px",
        "--hover-color": "#e0f0ff",
    },
    "nav-link-selected": {
        "background-color": "#0b4f91",
        "color": "#ffffff",
        "font-weight": "600",
        "border-radius": "8px",
    },
}


def setup_page():
    st.set_page_config(
        layout="wide",
        page_title="Mining System",
        initial_sidebar_state="expanded",
    )

    st.markdown(
        """
        <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        .stApp {
            background: linear-gradient(180deg, #0b4f91 0px, #0b4f91 220px, #e9f2ff 220px);
        }

        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}

        .block-container {
            padding-top: 1.5rem;
            padding-bottom: 3rem;
        }

        .title-card {
            width: 100%;
            background: #0b4f91;
            padding: 14px 0;
            border-radius: 10px;
            border: 1px solid #0b4f91;
            box-shadow: 0 6px 14px rgba(15, 23, 42, 0.35);
            text-align: center;
            font-size: 22px;
            font-weight: 600;
            color: #ffffff;
            margin-bottom: 22px;
        }

        div.stButton > button {
            background: #0b4f91;
            border: none;
            border-radius: 999px;
            padding: 10px 24px;
            font-size: 15px;
            font-weight: 600;
            color: #ffffff;
            width: 100%;
            text-align: center;
            box-shadow: 0 4px 10px rgba(15, 23, 42, 0.25);
            transition: all 0.18s ease-in-out;
        }
        div.stButton > button:hover {
            background: #1459b3;
            transform: translateY(-1px);
            box-shadow: 0 8px 18px rgba(15, 23, 42, 0.3);
        }
        div.stButton > button:active {
            transform: translateY(0px) scale(0.99);
            box-shadow: 0 2px 6px rgba(15, 23, 42, 0.25);
        }

        .chart-strip {
            width: 100%;
            background: #0b4f91;
            border-radius: 999px;
            padding: 4px 16px;
            display: grid;
            grid-template-columns: 1fr 1fr;
            column-gap: 12px;
            margin-bottom: 10px;
            box-shadow: 0 4px 12px rgba(15, 23, 42, 0.35);
        }
        .chart-tab {
            background: #ffffff;
            color: #0b4f91;
            text-align: center;
            font-size: 14px;
            font-weight: 600;
            border-radius: 999px;
            padding: 6px 0;
        }

        .date-label {
            font-size: 12px;
            font-weight: 500;
            color: #ffffff;
            margin-bottom: 2px;
        }

        .stDateInput > div > div {
            background: #0b4f91;
            border-radius: 999px;
            border: 1px solid #0b4f91;
            box-shadow: 0 3px 8px rgba(15, 23, 42, 0.35);
        }
        .stDateInput > div > div input {
            background: transparent;
            color: #ffffff;
        }
        .stDateInput > div > div svg {
            stroke: #ffffff;
        }

        .equal-height-card {
            border: 1px solid #d0ddf5;
            padding: 15px 18px;
            border-radius: 10px;
            background-color: #ffffff;
            color: #111827;
            box-shadow: 0 3px 10px rgba(15, 23, 42, 0.06);
            transition: all 0.18s ease-in-out;
        }
        .equal-height-card.bottom-card {
            min-height: 230px;
        }
        .equal-height-card:hover {
            border-color: #0b4f91;
            box-shadow: 0 10px 22px rgba(15, 23, 42, 0.18);
            transform: translateY(-2px);
        }

        .equal-height-card table {
            width: 100%;
            border-collapse: collapse;
            font-size: 13px;
        }
        .equal-height-card table td {
            padding: 6px 4px;
        }
        .equal-height-card table tr:nth-child(even) {
            background-color: #f3f7ff;
        }
        .equal-height-card table tr:nth-child(odd) {
            background-color: #ffffff;
        }
        .equal-height-card table tr:first-child td {
            border-bottom: 1px solid #d0ddf5;
        }

        .scenario-container {
            background: #ffffff;
            border-radius: 12px;
            margin-top: 40px;
            padding: 30px;
            border: 1px solid #d0ddf5;
            box-shadow: 0 4px 14px rgba(15, 23, 42, 0.08);
        }

        .scenario-title {
            font-size: 26px;
            font-weight: 700;
            color: #0b4f91;
            margin-bottom: 4px;
            text-align: center;
        }

        .scenario-subtitle {
            font-size: 14px;
            color: #6b7280;
            margin-bottom: 20px;
            text-align: center;
        }

        .upload-section {
            background: #f5f8ff;
            border-radius: 12px;
            padding: 25px;
            margin-bottom: 30px;
            border: 2px dashed #0b4f91;
            transition: all 0.3s ease;
        }
        .upload-section:hover {
            border-color: #1459b3;
            background: #e6f0ff;
        }

        .file-info {
            background: #e6f0ff;
            border-radius: 8px;
            padding: 12px 15px;
            margin-top: 12px;
            border-left: 4px solid #0b4f91;
            font-size: 13px;
            color: #111827;
        }

        .metric-card {
            background: white;
            border-radius: 10px;
            padding: 20px;
            margin: 10px 0;
            border: 1px solid #d0ddf5;
            box-shadow: 0 2px 8px rgba(15, 23, 42, 0.06);
        }

        .card-header {
            background: #0b4f91;
            color: white;
            padding: 12px 16px;
            border-radius: 8px 8px 0 0;
            margin: -20px -20px 10px -20px;
            font-weight: 600;
            font-size: 14px;
        }

        .metric-value {
            font-size: 22px;
            font-weight: 700;
            margin-bottom: 4px;
            color: #0b4f91;
        }

        .metric-label {
            font-size: 12px;
            color: #6b7280;
        }

        .actual-badge {
            background: #e0ecff;
            color: #0b4f91;
            padding: 4px 12px;
            border-radius: 12px;
            font-size: 11px;
            font-weight: 600;
        }

        .budget-badge {
            background: #edf2ff;
            color: #1459b3;
            padding: 4px 12px;
            border-radius: 12px;
            font-size: 11px;
            font-weight: 600;
        }

        .diagram-container {
            background: #f5f8ff;
            border-radius: 12px;
            padding: 30px;
            margin: 25px 0;
            border: 1px solid #d0ddf5;
        }

        .simulation-row {
            margin-top: 10px;
        }
        .simulation-row button {
            background: #0b4f91;
            color: white;
            border: none;
            padding: 12px 35px;
            border-radius: 999px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        .simulation-row button:hover {
            background: #1459b3;
            transform: translateY(-2px);
            box-shadow: 0 6px 16px rgba(15, 23, 42, 0.25);
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def create_sidebar():
    with st.sidebar:
        st.markdown(
            "<h3 style='color:#f9fafb; margin-bottom:10px;'>Cost Elements</h3>",
            unsafe_allow_html=True,
        )

        selected_element = option_menu(
            "",
            Variable["Mining System"],
            default_index=0,
            orientation="vertical",
            key="cost_element_menu",
            styles=SIDEBAR_MENU_STYLE,
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
                styles=SIDEBAR_MENU_STYLE,
            )
            if selected_display:
                name, code = selected_display.split(" : ")
                selected_item_name = name.strip()
                selected_item_code = code.strip()

    return selected_element, selected_item_name, selected_item_code


def create_title_card(selected_item_name, selected_item_code):
    # Use the selected element’s name + code; default to Diesel 406105
    if selected_item_name and selected_item_code:
        title_name = selected_item_name
        display_code = selected_item_code
    else:
        title_name = "Diesel"
        display_code = "406105"

    st.markdown(
        f"""
        <div class="title-card">
            Cost breakdown: {title_name} {display_code}
        </div>
        """,
        unsafe_allow_html=True,
    )
    return display_code


def create_upload_trigger(show_button: bool):
    """Show the 'Upload diesel scenario' button only when `show_button` is True."""
    if not show_button:
        return
    trigger_col, _ = st.columns([1.5, 3])
    with trigger_col:
        if st.button("Upload diesel scenario", key="btn_show_scenario"):
            st.session_state["show_scenario"] = True


def display_diesel_analysis(df, display_code):
    if df.empty:
        st.warning("No data available for Diesel.")
        return

    min_date = df.index.min().date()
    max_date = df.index.max().date()

    left_space, date_area = st.columns([2.3, 1.2])
    with date_area:
        from_col, to_col = st.columns(2)

        with from_col:
            st.markdown('<div class="date-label">From</div>', unsafe_allow_html=True)
            start_date = st.date_input(
                "",
                min_date,
                min_value=min_date,
                max_value=max_date,
                key="start_date",
                label_visibility="collapsed",
                format="YYYY/MM/DD",
            )

        with to_col:
            st.markdown('<div class="date-label">To</div>', unsafe_allow_html=True)
            end_date = st.date_input(
                "",
                max_date,
                min_value=min_date,
                max_value=max_date,
                key="end_date",
                label_visibility="collapsed",
                format="YYYY/MM/DD",
            )

    if start_date > end_date:
        start_date, end_date = end_date, start_date

    st.session_state["sim_start_date"] = start_date
    st.session_state["sim_end_date"] = end_date

    mask = (df.index.date >= start_date) & (df.index.date <= end_date)
    df_filtered = df.loc[mask]

    if df_filtered.empty:
        st.warning("No data in the selected date range.")
        return

    monthly = prepare_diesel_data(df_filtered)

    # Add EPBCS + Simulation series if a scenario has been loaded
    scenario_df = st.session_state.get("scenario_df")
    monthly = apply_epbcs_and_simulation(monthly, scenario_df)

    fig_month = create_monthly_chart(monthly, display_code)
    fig_cum = create_cumulative_chart(monthly, display_code)

    st.markdown(
        """
        <div class="chart-strip">
            <div class="chart-tab">Monthly cost</div>
            <div class="chart-tab">Cumulative cost</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    chart1, chart2 = st.columns(2)
    chart1.plotly_chart(fig_month, use_container_width=True)
    chart2.plotly_chart(fig_cum, use_container_width=True)

    bottom_left, bottom_right = st.columns([2, 1.2])
    with bottom_left:
        st.markdown(create_cost_drivers_table(monthly), unsafe_allow_html=True)
    with bottom_right:
        st.markdown(create_impact_card(display_code), unsafe_allow_html=True)


# ---------- SCENARIO SECTION (bottom of page) ----------


def create_scenario_upload_section():
    st.markdown('<div class="upload-section">', unsafe_allow_html=True)

    uploaded = st.file_uploader(
        "Drag and drop your Excel file here",
        type=["xlsx"],
        key="diesel_scenario_file",
        help="Upload diesel scenario Excel file (max 20MB)",
    )

    if uploaded:
        st.markdown(
            f"""
            <div class="file-info">
                <strong>{uploaded.name}</strong> • {uploaded.size // 1024} KB • Ready for analysis
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("</div>", unsafe_allow_html=True)
    return uploaded


def create_scenario_metric_cards(metrics):
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(
            f"""
        <div class="metric-card">
            <div class="card-header">Cost Overview</div>
            <div class="metric-value">R {fmt0(metrics["diesel_actual"])}</div>
            <div class="metric-label">Actual diesel cost</div>
            <span class="actual-badge">ACTUAL</span>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            f"""
        <div class="metric-card">
            <div class="card-header">Budget Analysis</div>
            <div class="metric-value">R {fmt0(metrics["diesel_budget"])}</div>
            <div class="metric-label">Budget diesel cost</div>
            <span class="budget-badge">BUDGET</span>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with col3:
        st.markdown(
            f"""
        <div class="metric-card">
            <div class="card-header">Production Volume</div>
            <div class="metric-value">{fmt0(metrics["total_t_actual"])} T</div>
            <div class="metric-label">Total production (OB + ROM)</div>
            <span class="actual-badge">ACTUAL</span>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with col4:
        st.markdown(
            f"""
        <div class="metric-card">
            <div class="card-header">Efficiency</div>
            <div class="metric-value">{fmt2(metrics["con_actual"])} L/T</div>
            <div class="metric-label">Diesel consumption rate</div>
            <span class="actual-badge">ACTUAL</span>
        </div>
        """,
            unsafe_allow_html=True,
        )


def display_scenario_section():
    if not st.session_state.get("show_scenario", False):
        return

    st.markdown('<div class="scenario-container">', unsafe_allow_html=True)
    st.markdown(
        '<div class="scenario-title">Diesel Scenario Analysis</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="scenario-subtitle">Upload your diesel scenario data to visualize cost drivers and performance metrics</div>',
        unsafe_allow_html=True,
    )

    uploaded = create_scenario_upload_section()

    sim_row = st.columns([2, 1, 2])
    with sim_row[1]:
        run_clicked = st.button(
            "Run Scenario Simulation",
            key="simulate_scenario",
            use_container_width=True,
        )

    # When button is clicked, update the stored scenario
    if run_clicked:
        if not uploaded:
            st.warning(
                "Please upload a diesel scenario Excel file before running the simulation."
            )
        else:
            df_scenario = load_scenario_data(uploaded)

            start = st.session_state.get("sim_start_date")
            end = st.session_state.get("sim_end_date")

            if start and end and "Date" in df_scenario.columns:
                df_scenario["Date"] = pd.to_datetime(
                    df_scenario["Date"], errors="coerce"
                )
                mask = (
                    (df_scenario["Date"].dt.date >= start)
                    & (df_scenario["Date"].dt.date <= end)
                )
                df_scenario = df_scenario.loc[mask]

            if df_scenario.empty:
                st.warning(
                    "No scenario data in the selected date range. "
                    "Please adjust the date filter or upload another file."
                )
            else:
                # store scenario dataframe for charts and diagram
                st.session_state["scenario_df"] = df_scenario.copy()

    # Always draw metrics + diagram whenever we have a scenario in session
    scenario_df = st.session_state.get("scenario_df")
    if scenario_df is not None and not scenario_df.empty:
        metrics = calculate_scenario_metrics(scenario_df)
        create_scenario_metric_cards(metrics)

        mermaid_code = create_scenario_mermaid(
            metrics["diesel_actual"],
            metrics["diesel_budget"],
            metrics["qty_actual"],
            metrics["qty_budget"],
            metrics["price_actual"],
            metrics["price_budget"],
            metrics["con_actual"],
            metrics["con_budget"],
            metrics["ob_actual"],
            metrics["ob_budget"],
            metrics["rom_actual"],
            metrics["rom_budget"],
        )

        st.markdown('<div class="diagram-container">', unsafe_allow_html=True)
        left, centre, right = st.columns([1, 8, 1])
        with centre:
            st_mermaid(mermaid_code, height=500)
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)


def main():
    setup_page()

    if "show_scenario" not in st.session_state:
        st.session_state["show_scenario"] = False

    selected_element, selected_item_name, selected_item_code = create_sidebar()
    display_code = create_title_card(selected_item_name, selected_item_code)

    # Only show upload button (and therefore scenario section) for Diesel
    is_diesel = selected_item_name == "Diesel"
    create_upload_trigger(show_button=is_diesel)

    try:
        df = get_data(Data["Mining System"])

        if is_diesel:
            display_diesel_analysis(df, display_code)
            display_scenario_section()
        else:
            # For Blasting / Drilling / others: no charts or scenario – just the title.
            if not selected_item_name:
                st.write("Select Cost Elements → Diesel from the sidebar.")
    except Exception as e:
        st.error(str(e))


if __name__ == "__main__":
    main()
