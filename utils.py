import numpy as np
import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt


def get_data(file_name):
    """
    1. Load Excel to DataFrame
    2. Parse 'Date' as datetime and set as index
    3. Add year and year_month columns
    """
    df = pd.read_excel(file_name)
    df["Date"] = pd.to_datetime(df["Date"], dayfirst=True, errors="coerce")
    df = df.dropna(subset=["Date"])
    df = df.set_index("Date").sort_index()
    df["year_month"] = df.index.year * 100 + df.index.month
    df["year"] = df.index.year
    return df

def prepare_diesel_data(df):
    df.index = pd.to_datetime(df.index, errors="coerce")
    df_diesel = df[["Diesel (R)", "Diesel (R) Budget"]].copy()
    df_diesel["Month"] = df_diesel.index.month

    monthly = (
        df_diesel.groupby("Month")[["Diesel (R)", "Diesel (R) Budget"]]
        .sum()
        .reset_index()
    )

    all_months = pd.DataFrame({"Month": range(1, 13)})
    monthly = (
        all_months
        .merge(monthly, on="Month", how="left")
        .fillna(0)
        .sort_values("Month")
    )
    monthly = monthly[monthly["Diesel (R)"] > 0]

    monthly["Cum_Actual"] = monthly["Diesel (R)"].cumsum()
    monthly["Cum_Budget"] = monthly["Diesel (R) Budget"].cumsum()
    
    return monthly

def create_monthly_chart(monthly, display_code):
    ACTUAL_COLOR = "#145A32"
    BUDGET_COLOR = "#82E0AA"

    fig_month = go.Figure()
    fig_month.add_bar(
        x=monthly["Month"],
        y=monthly["Diesel (R)"],
        name="Actual",
        marker_color=ACTUAL_COLOR,
    )
    fig_month.add_bar(
        x=monthly["Month"],
        y=monthly["Diesel (R) Budget"],
        name="Budget",
        marker_color=BUDGET_COLOR,
    )
    fig_month.update_layout(
        title=f"Monthly cost – Diesel {display_code}",
        xaxis_title="Month",
        yaxis_title="Diesel cost (R)",
        barmode="group",
        plot_bgcolor="white",
    )
    return fig_month

def create_cumulative_chart(monthly, display_code):
    ACTUAL_COLOR = "#145A32"
    BUDGET_COLOR = "#82E0AA"

    fig_cum = go.Figure()
    fig_cum.add_bar(
        x=monthly["Month"],
        y=monthly["Cum_Actual"],
        name="Actual",
        marker_color=ACTUAL_COLOR,
    )
    fig_cum.add_bar(
        x=monthly["Month"],
        y=monthly["Cum_Budget"],
        name="Budget",
        marker_color=BUDGET_COLOR,
    )
    fig_cum.update_layout(
        title=f"Cumulative cost – Diesel {display_code}",
        xaxis_title="Month",
        yaxis_title="Cumulative diesel cost (R)",
        barmode="group",
        plot_bgcolor="white",
    )
    return fig_cum

def create_cost_drivers_table(monthly):
    month_labels = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                    "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

    actual_vals = [f"{v:,.0f}" if v > 0 else "" for v in monthly["Diesel (R)"]]
    budget_vals = [f"{v:,.0f}" if v > 0 else "" for v in monthly["Diesel (R) Budget"]]
    sim_vals = [""] * len(actual_vals)

    header_cells = "".join(
        f'<td style="padding:6px;">{m}</td>'
        for m in month_labels[:len(actual_vals)]
    )
    actual_cells = "".join(f"<td>{v}</td>" for v in actual_vals)
    budget_cells = "".join(f"<td>{v}</td>" for v in budget_vals)
    simulation_cells = "".join(f"<td>{v}</td>" for v in sim_vals)

    return f"""
    <div class="equal-height-card bottom-card">
        <div style="font-size:18px; font-weight:600; margin-bottom:10px;">
            Table of cost drivers for diesel over time
        </div>
        <table>
            <tr style="font-weight:600;">
                <td>Cost</td>
                {header_cells}
            </tr>
            <tr><td>Actuals</td>{actual_cells}</tr>
            <tr><td>Budget</td>{budget_cells}</tr>
            <tr><td>Simulation</td>{simulation_cells}</tr>
        </table>
    </div>
    """

def create_impact_card(display_code):
    return f"""
    <div class="equal-height-card bottom-card">
        <div style="font-size:18px; font-weight:600; margin-bottom:5px;">
            Impact on Mining System
        </div>
        <div style="font-size:12px; opacity:0.8; margin-bottom:10px;">
            (everything else remains constant)
        </div>
        <div>
            &gt; Mining System : R<br>
            &gt; Consumables : R<br>
            &gt; Diesel : {display_code} : R
        </div>
    </div>
    """

def load_scenario_data(file):
    df = pd.read_excel(file)
    df.columns = [str(c).strip() for c in df.columns]
    return df

def fmt0(x):
    return f"{x:,.0f}" if pd.notnull(x) else "N/A"

def fmt2(x):
    return f"{x:,.2f}" if pd.notnull(x) else "N/A"

def calculate_scenario_metrics(df):
    ob_actual = df["OB (T)"].sum()
    ob_budget = df["OB (T) Budget"].sum()
    rom_actual = df["ROM (T)"].sum()
    rom_budget = df["ROM (T) Budget"].sum()
    total_t_actual = ob_actual + rom_actual
    total_t_budget = ob_budget + rom_budget

    con_actual = df["Con rate (l/t)"].mean()
    con_budget = df["Con rate (l/t) Budget"].mean()
    price_actual = df["Diesel (R)"].mean()
    price_budget = df["Diesel (R) Budget"].mean()

    qty_actual = con_actual * total_t_actual if pd.notnull(con_actual) and total_t_actual > 0 else np.nan
    qty_budget = con_budget * total_t_budget if pd.notnull(con_budget) and total_t_budget > 0 else np.nan

    diesel_actual = price_actual * qty_actual if pd.notnull(price_actual) and pd.notnull(qty_actual) else np.nan
    diesel_budget = price_budget * qty_budget if pd.notnull(price_budget) and pd.notnull(qty_budget) else np.nan

    metrics = {
        'ob_actual': ob_actual,
        'ob_budget': ob_budget,
        'rom_actual': rom_actual,
        'rom_budget': rom_budget,
        'total_t_actual': total_t_actual,
        'total_t_budget': total_t_budget,
        'con_actual': con_actual,
        'con_budget': con_budget,
        'price_actual': price_actual,
        'price_budget': price_budget,
        'qty_actual': qty_actual,
        'qty_budget': qty_budget,
        'diesel_actual': diesel_actual,
        'diesel_budget': diesel_budget
    }
    
    return metrics

def create_scenario_mermaid(diesel_actual, diesel_budget, qty_actual, qty_budget, 
                           price_actual, price_budget, con_actual, con_budget, 
                           ob_actual, ob_budget, rom_actual, rom_budget):
    return f"""
%%{{init: {{
  'theme': 'base',
  'flowchart': {{ 'curve': 'linear', 'useMaxWidth': true }},
  'themeVariables': {{
      'primaryColor': '#f8fffb',
      'primaryBorderColor': '#4caf50',
      'primaryTextColor': '#1b5e20',
      'lineColor': '#4caf50',
      'fontSize': '16px',
      'fontFamily': 'Arial'
  }}
}}}}%%

flowchart TD

classDef node fill:#f8fffb,stroke:#4caf50,stroke-width:2px,color:#1b5e20,rx:8,ry:8,padding:15px;

A["<b>Cost Analysis Period</b>"]:::node --> B["<b>Diesel Cost (R)</b><br/><span style='color:#2e7d32'>Actual: R {fmt0(diesel_actual)}</span><br/><span style='color:#4caf50'>Budget: R {fmt0(diesel_budget)}</span>"]:::node

B --> C["<b>Quantity (Liters)</b><br/><span style='color:#2e7d32'>Actual: {fmt0(qty_actual)}</span><br/><span style='color:#4caf50'>Budget: {fmt0(qty_budget)}</span>"]:::node
B --> D["<b>Price (R/Liter)</b><br/><span style='color:#2e7d32'>Actual: R {fmt2(price_actual)}</span><br/><span style='color:#4caf50'>Budget: R {fmt2(price_budget)}</span>"]:::node

C --> E["<b>Consumption Rate (L/T)</b><br/><span style='color:#2e7d32'>Actual: {fmt2(con_actual)}</span><br/><span style='color:#4caf50'>Budget: {fmt2(con_budget)}</span>"]:::node

E --> F["<b>OB Production (T)</b><br/><span style='color:#2e7d32'>Actual: {fmt0(ob_actual)}</span><br/><span style='color:#4caf50'>Budget: {fmt0(ob_budget)}</span>"]:::node
E --> G["<b>ROM Production (T)</b><br/><span style='color:#2e7d32'>Actual: {fmt0(rom_actual)}</span><br/><span style='color:#4caf50'>Budget: {fmt0(rom_budget)}</span>"]:::node
"""