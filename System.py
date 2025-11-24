# System.py

import streamlit as st
from streamlit_option_menu import option_menu

from dictionaries import cost_elements, models


def render_system_view(selected_system: str) -> None:
    left_col, right_col = st.columns([1, 3])

    with left_col:
        # 2nd level: cost element menu
        element_list = cost_elements.get(selected_system, [])
        selected_element = option_menu(
            "Cost element selector",
            element_list,
            icons=["caret-right"] * len(element_list),
            menu_icon="list",
            default_index=0,
            orientation="vertical",
            key=f"element_menu_{selected_system}",
        )

        # 3rd level: only for elements that have models (for now: Consumables)
        selected_item_name = None
        selected_item_code = None

        element_models = models.get(selected_element, {})
        if element_models:
            display_items = [
                f"{name} : {code}" for name, code in element_models.items()
            ]
            selected_display = option_menu(
                selected_element,
                display_items,
                icons=["dot"] * len(display_items),
                menu_icon="chevron-right",
                default_index=0,
                orientation="vertical",
                key=f"item_menu_{selected_system}_{selected_element}",
            )
            parts = selected_display.split(" : ")
            selected_item_name = parts[0]
            selected_item_code = parts[1] if len(parts) > 1 else None
        else:
            selected_item_name = selected_element

        st.markdown(
            """
            <div class="left-panel-card">
                <div class="left-panel-title">Time period selector</div>
                <div class="helper-text">Time period options (to be added)</div>
            </div>
            <div class="left-panel-card">
                <div class="left-panel-title">Upload diesel scenario</div>
                <div class="helper-text">Uploaded data page (to be added)</div>
            </div>
            <div class="left-panel-card">
                <div class="run-button-holder">
                    <button class="run-btn">Run Local Simulation</button>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with right_col:
        if selected_item_code:
            header = f"Cost breakdown: {selected_item_name} {selected_item_code}"
        else:
            header = f"Cost breakdown: {selected_element}"

        st.markdown(
            f"<div class='section-heading'>{header}</div>",
            unsafe_allow_html=True,
        )

        chart_col1, chart_col2 = st.columns(2)
        with chart_col1:
            st.markdown(
                "<div class='section-heading'>Monthly cost</div>",
                unsafe_allow_html=True,
            )
            st.markdown(
                "<div class='placeholder-box'>Monthly cost chart placeholder</div>",
                unsafe_allow_html=True,
            )

        with chart_col2:
            st.markdown(
                "<div class='section-heading'>Cumulative cost</div>",
                unsafe_allow_html=True,
            )
            st.markdown(
                "<div class='placeholder-box'>Cumulative cost chart placeholder</div>",
                unsafe_allow_html=True,
            )

        st.markdown("<br/>", unsafe_allow_html=True)

        lower_left, lower_right = st.columns([1.4, 1.4])
        with lower_left:
            st.markdown(
                "<div class='section-heading'>Table of cost drivers over time</div>",
                unsafe_allow_html=True,
            )
            st.markdown(
                "<div class='placeholder-box'>Actual / Budget / Simulation per month</div>",
                unsafe_allow_html=True,
            )

        with lower_right:
            st.markdown(
                "<div class='section-heading'>Impact on system</div>",
                unsafe_allow_html=True,
            )
            st.markdown(
                f"""
                <div class='drivers-box'>
                    <div class='drivers-title'>Impact on {selected_system}<br/>
                        <span style='font-size:11px; font-weight:400;'>(everything else remains constant)</span>
                    </div>
                    <div>{selected_system} : R</div>
                    <div>{selected_element} : R</div>
                    <div><span style='color:#15803d; font-weight:600;'>
                        {selected_item_name}{f" : {selected_item_code}" if selected_item_code else ""} : R
                    </span></div>
                </div>
                """,
                unsafe_allow_html=True,
            )
