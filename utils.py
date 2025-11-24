import numpy as np
import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt


# -------------------------------------------------------------------
# DATA PREP
# -------------------------------------------------------------------
def get_data(file_name):
    df = pd.read_excel(file_name)
    df["Date"] = pd.to_datetime(df["Date"], dayfirst=True, errors="coerce")
    df = df.dropna(subset=["Date"])
    df = df.set_index("Date").sort_index()
    df["year_month"] = df.index.year * 100 + df.index.month
    df["year"] = df.index.year
    return df


def prepare_diesel_data(df: pd.DataFrame) -> pd.DataFrame:
    df.index = pd.to_datetime(df.index, errors="coerce")

    base_cols = ["Diesel (R)", "Diesel (R) Budget"]
    df_diesel = df[base_cols].copy()
    df_diesel["Month"] = df_diesel.index.month

    monthly = df_diesel.groupby("Month")[base_cols].sum().reset_index()

    all_months = pd.DataFrame({"Month": range(1, 13)})
    monthly = (
        all_months.merge(monthly, on="Month", how="left")
        .fillna(0)
        .sort_values("Month")
    )

    monthly = monthly[monthly["Diesel (R)"] > 0]

    monthly["Cum_Actual"] = monthly["Diesel (R)"].cumsum()
    monthly["Cum_Budget"] = monthly["Diesel (R) Budget"].cumsum()

    return monthly


def apply_epbcs_and_simulation(
    monthly: pd.DataFrame, scenario_df: pd.DataFrame | None
) -> pd.DataFrame:
    """
    Enrich `monthly` with EPBCS and Simulation.

    If scenario_df is provided and valid:
        EPBCS     = monthly sum of scenario 'Diesel (R) Budget'
        Simulation= monthly sum of scenario 'Diesel (R)'
    Otherwise:
        Generate near-realistic synthetic EPBCS/Simulation based on
        Budget/Actual with small random noise.
    """
    out = monthly.copy()

    # ----- CASE 1: no scenario → synthetic EPBCS & Simulation -----
    if (
        scenario_df is None
        or scenario_df.empty
        or "Date" not in scenario_df.columns
        or "Diesel (R)" not in scenario_df.columns
        or "Diesel (R) Budget" not in scenario_df.columns
    ):
        rng = np.random.default_rng(42)

        epbcs_factor = rng.normal(loc=1.02, scale=0.03, size=len(out))
        sim_factor = rng.normal(loc=1.00, scale=0.05, size=len(out))

        out["EPBCS"] = out["Diesel (R) Budget"] * epbcs_factor
        out["Simulation"] = out["Diesel (R)"] * sim_factor

        return out

    # ----- CASE 2: scenario provided → aggregate from scenario file -----
    df = scenario_df.copy()
    df["Date"] = pd.to_datetime(df["Date"], dayfirst=True, errors="coerce")
    df = df.dropna(subset=["Date"])
    df["Month"] = df["Date"].dt.month

    epbcs_month = (
        df.groupby("Month")["Diesel (R) Budget"]
        .sum()
        .reset_index(name="EPBCS")
    )
    sim_month = (
        df.groupby("Month")["Diesel (R)"]
        .sum()
        .reset_index(name="Simulation")
    )

    out = out.merge(epbcs_month, on="Month", how="left")
    out = out.merge(sim_month, on="Month", how="left")
    out[["EPBCS", "Simulation"]] = out[["EPBCS", "Simulation"]].fillna(0)

    return out


# -------------------------------------------------------------------
# COMMON LAYOUT
# -------------------------------------------------------------------
def _base_layout(title, y_title):
    return dict(
        title=dict(text=title, x=0.01, xanchor="left", font=dict(size=16)),
        xaxis=dict(
            title="Month",
            tickmode="linear",
            tick0=1,
            dtick=1,
            linecolor="#94a3b8",
            mirror=True,
        ),
        yaxis=dict(
            title=y_title,
            linecolor="#94a3b8",
            mirror=True,
            zeroline=True,
            zerolinecolor="#e2e8f0",
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
        ),
        plot_bgcolor="#ffffff",
        paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=40, r=20, t=60, b=40),
    )


# -------------------------------------------------------------------
# CHARTS – with EPBCS + SIMULATION LINES
# -------------------------------------------------------------------
def create_monthly_chart(monthly: pd.DataFrame, display_code: str):
    ACTUAL_COLOR = "#0b4f91"
    BUDGET_COLOR = "#5fa8ff"
    EPBCS_COLOR = "#16a34a"
    SIM_COLOR = "#f97316"

    x_vals = monthly["Month"]

    fig = go.Figure()

    fig.add_bar(
        x=x_vals,
        y=monthly["Diesel (R)"],
        name="Actual",
        marker_color=ACTUAL_COLOR,
        hovertemplate="Month: %{x}<br>Actual: R %{y:,.0f}<extra></extra>",
    )
    fig.add_bar(
        x=x_vals,
        y=monthly["Diesel (R) Budget"],
        name="Budget",
        marker_color=BUDGET_COLOR,
        hovertemplate="Month: %{x}<br>Budget: R %{y:,.0f}<extra></extra>",
    )

    if "EPBCS" in monthly.columns:
        fig.add_scatter(
            x=x_vals,
            y=monthly["EPBCS"],
            name="EPBCS forecast",
            mode="lines+markers",
            line=dict(color=EPBCS_COLOR, width=2, shape="spline"),
            marker=dict(size=5),
            hovertemplate="Month: %{x}<br>EPBCS: R %{y:,.0f}<extra></extra>",
        )

    if "Simulation" in monthly.columns:
        fig.add_scatter(
            x=x_vals,
            y=monthly["Simulation"],
            name="Simulation",
            mode="lines+markers",
            line=dict(color=SIM_COLOR, width=2, dash="dot", shape="spline"),
            marker=dict(size=5),
            hovertemplate="Month: %{x}<br>Simulation: R %{y:,.0f}<extra></extra>",
        )

    fig.update_layout(
        **_base_layout(f"Monthly cost – Diesel {display_code}", "Diesel cost (R)"),
        barmode="group",
    )

    return fig


def create_cumulative_chart(monthly: pd.DataFrame, display_code: str):
    ACTUAL_COLOR = "#0b4f91"
    BUDGET_COLOR = "#5fa8ff"
    EPBCS_COLOR = "#16a34a"
    SIM_COLOR = "#f97316"

    x_vals = monthly["Month"]

    cum_actual = monthly["Diesel (R)"].cumsum()
    cum_budget = monthly["Diesel (R) Budget"].cumsum()

    fig = go.Figure()

    fig.add_bar(
        x=x_vals,
        y=cum_actual,
        name="Actual (cum)",
        marker_color=ACTUAL_COLOR,
        hovertemplate="Month: %{x}<br>Cum Actual: R %{y:,.0f}<extra></extra>",
    )
    fig.add_bar(
        x=x_vals,
        y=cum_budget,
        name="Budget (cum)",
        marker_color=BUDGET_COLOR,
        hovertemplate="Month: %{x}<br>Cum Budget: R %{y:,.0f}<extra></extra>",
    )

    if "EPBCS" in monthly.columns:
        epbcs_cum = monthly["EPBCS"].cumsum()
        fig.add_scatter(
            x=x_vals,
            y=epbcs_cum,
            name="EPBCS forecast (cum)",
            mode="lines+markers",
            line=dict(color=EPBCS_COLOR, width=2, shape="spline"),
            marker=dict(size=5),
            hovertemplate="Month: %{x}<br>EPBCS (cum): R %{y:,.0f}<extra></extra>",
        )

    if "Simulation" in monthly.columns:
        sim_cum = monthly["Simulation"].cumsum()
        fig.add_scatter(
            x=x_vals,
            y=sim_cum,
            name="Simulation (cum)",
            mode="lines+markers",
            line=dict(color=SIM_COLOR, width=2, dash="dot", shape="spline"),
            marker=dict(size=5),
            hovertemplate="Month: %{x}<br>Simulation (cum): R %{y:,.0f}<extra></extra>",
        )

    fig.update_layout(
        **_base_layout(
            f"Cumulative cost – Diesel {display_code}",
            "Cumulative diesel cost (R)",
        ),
        barmode="group",
    )

    return fig


# -------------------------------------------------------------------
# TABLE + IMPACT CARD
# -------------------------------------------------------------------
def create_cost_drivers_table(monthly: pd.DataFrame):
    month_labels = [
        "Jan",
        "Feb",
        "Mar",
        "Apr",
        "May",
        "Jun",
        "Jul",
        "Aug",
        "Sep",
        "Oct",
        "Nov",
        "Dec",
    ]

    actual_vals = [f"{v:,.0f}" if v > 0 else "" for v in monthly["Diesel (R)"]]
    budget_vals = [f"{v:,.0f}" if v > 0 else "" for v in monthly["Diesel (R) Budget"]]

    if "EPBCS" in monthly.columns:
        epbcs_vals = [f"{v:,.0f}" if v > 0 else "" for v in monthly["EPBCS"]]
    else:
        epbcs_vals = [""] * len(actual_vals)

    if "Simulation" in monthly.columns:
        sim_vals = [f"{v:,.0f}" if v > 0 else "" for v in monthly["Simulation"]]
    else:
        sim_vals = [""] * len(actual_vals)

    header_cells = "".join(
        f'<td style="padding:6px; font-weight:600; color:#0b4f91;">{m}</td>'
        for m in month_labels[: len(actual_vals)]
    )
    actual_cells = "".join(f"<td>{v}</td>" for v in actual_vals)
    budget_cells = "".join(f"<td>{v}</td>" for v in budget_vals)
    epbcs_cells = "".join(f"<td>{v}</td>" for v in epbcs_vals)
    simulation_cells = "".join(f"<td>{v}</td>" for v in sim_vals)

    return f"""
    <div class="equal-height-card bottom-card">
        <div style="font-size:18px; font-weight:600; margin-bottom:10px; color:#0b4f91;">
            Table of cost drivers for diesel over time
        </div>
        <table>
            <tr>
                <td style="font-weight:600;">Cost</td>
                {header_cells}
            </tr>
            <tr><td>Actuals</td>{actual_cells}</tr>
            <tr><td>Budget</td>{budget_cells}</tr>
            <tr><td>EPBCS forecast</td>{epbcs_cells}</tr>
            <tr><td>Simulation</td>{simulation_cells}</tr>
        </table>
    </div>
    """


def create_impact_card(display_code):
    return f"""
    <div class="equal-height-card bottom-card">
        <div style="font-size:18px; font-weight:600; margin-bottom:5px; color:#0b4f91;">
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


# -------------------------------------------------------------------
# SCENARIO HELPERS
# -------------------------------------------------------------------
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

    qty_actual = (
        con_actual * total_t_actual
        if pd.notnull(con_actual) and total_t_actual > 0
        else np.nan
    )
    qty_budget = (
        con_budget * total_t_budget
        if pd.notnull(con_budget) and total_t_budget > 0
        else np.nan
    )

    diesel_actual = (
        price_actual * qty_actual
        if pd.notnull(price_actual) and pd.notnull(qty_actual)
        else np.nan
    )
    diesel_budget = (
        price_budget * qty_budget
        if pd.notnull(price_budget) and pd.notnull(qty_budget)
        else np.nan
    )

    metrics = {
        "ob_actual": ob_actual,
        "ob_budget": ob_budget,
        "rom_actual": rom_actual,
        "rom_budget": rom_budget,
        "total_t_actual": total_t_actual,
        "total_t_budget": total_t_budget,
        "con_actual": con_actual,
        "con_budget": con_budget,
        "price_actual": price_actual,
        "price_budget": price_budget,
        "qty_actual": qty_actual,
        "qty_budget": qty_budget,
        "diesel_actual": diesel_actual,
        "diesel_budget": diesel_budget,
    }

    return metrics


def create_scenario_mermaid(
    diesel_actual,
    diesel_budget,
    qty_actual,
    qty_budget,
    price_actual,
    price_budget,
    con_actual,
    con_budget,
    ob_actual,
    ob_budget,
    rom_actual,
    rom_budget,
):
    return f"""
%%{{init: {{
  'theme': 'base',
  'flowchart': {{ 'curve': 'linear', 'useMaxWidth': true }},
  'themeVariables': {{
      'primaryColor': '#f8fbff',
      'primaryBorderColor': '#0b4f91',
      'primaryTextColor': '#0b4f91',
      'lineColor': '#0b4f91',
      'fontSize': '16px',
      'fontFamily': 'Arial'
  }}
}}}}%%

flowchart TD

classDef node fill:#f8fbff,stroke:#0b4f91,stroke-width:2px,color:#0b4f91,rx:8,ry:8,padding:15px;

A["<b>Cost Analysis Period</b>"]:::node --> B["<b>Diesel Cost (R)</b><br/><span style='color:#0b4f91'>Actual: R {fmt0(diesel_actual)}</span><br/><span style='color:#5fa8ff'>Budget: R {fmt0(diesel_budget)}</span>"]:::node

B --> C["<b>Quantity (Liters)</b><br/><span style='color:#0b4f91'>Actual: {fmt0(qty_actual)}</span><br/><span style='color:#5fa8ff'>Budget: {fmt0(qty_budget)}</span>"]:::node
B --> D["<b>Price (R/Liter)</b><br/><span style='color:#0b4f91'>Actual: R {fmt2(price_actual)}</span><br/><span style='color:#5fa8ff'>Budget: R {fmt2(price_budget)}</span>"]:::node

C --> E["<b>Consumption Rate (L/T)</b><br/><span style='color:#0b4f91'>Actual: {fmt2(con_actual)}</span><br/><span style='color:#5fa8ff'>Budget: {fmt2(con_budget)}</span>"]:::node

E --> F["<b>OB Production (T)</b><br/><span style='color:#0b4f91'>Actual: {fmt0(ob_actual)}</span><br/><span style='color:#5fa8ff'>Budget: {fmt0(ob_budget)}</span>"]:::node
E --> G["<b>ROM Production (T)</b><br/><span style='color:#0b4f91'>Actual: {fmt0(rom_actual)}</span><br/><span style='color:#5fa8ff'>Budget: {fmt0(rom_budget)}</span>"]:::node
"""
