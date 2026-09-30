"""
=============================================================================
Visualizer Module: Institutional Equity Research Chart Generator
=============================================================================
Generates 6 publication-ready, institutional-grade equity research charts
using Matplotlib:
1. Revenue Trend & YoY Growth Rate (Dual-axis)
2. Profitability Waterfall / Trend (EBITDA, EBIT, Net Profit)
3. Operating & Net Margin Trajectory
4. Competitor Benchmark (TCS vs Infosys vs HCLTech)
5. Cash Flow Quality & Free Cash Flow Conversion
6. Valuation Sensitivity Heatmap (WACC vs Terminal Growth Rate)
"""

import os
from typing import Dict, Any
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
import pandas as pd


# Set Institutional Style Configuration
GS_PALETTE = {
    "navy_primary": "#0A2540",
    "navy_secondary": "#1E3A8A",
    "steel_blue": "#2563EB",
    "light_blue": "#60A5FA",
    "gold_accent": "#D97706",
    "gold_light": "#FBBF24",
    "emerald": "#059669",
    "slate_dark": "#1E293B",
    "slate_text": "#334155",
    "grid_color": "#E2E8F0",
    "bg_color": "#FFFFFF",
    "card_bg": "#F8FAFC",
}

plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = ["DejaVu Sans", "Helvetica", "Arial", "Lucida Grande"]
plt.rcParams["axes.edgecolor"] = "#CBD5E1"
plt.rcParams["axes.linewidth"] = 0.8


def get_charts_dir() -> str:
    """Return absolute path to charts directory."""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    chart_dir = os.path.abspath(os.path.join(current_dir, "..", "output", "charts"))
    os.makedirs(chart_dir, exist_ok=True)
    return chart_dir


def plot_revenue_trend(df: pd.DataFrame, ratios: pd.DataFrame, output_dir: str = None) -> str:
    """
    Dual-axis chart: Revenue (INR Cr) as primary bar chart and YoY Growth % as secondary line.
    """
    if output_dir is None:
        output_dir = get_charts_dir()

    fig, ax1 = plt.subplots(figsize=(8.5, 4.8), dpi=300)
    fig.patch.set_facecolor(GS_PALETTE["bg_color"])
    ax1.set_facecolor(GS_PALETTE["bg_color"])

    years = [y.upper() for y in df.index]
    revenues = df["Revenue from Operations"] / 1000.0  # In Thousands of Crores (or Lakh Cr)
    growth = ratios["Revenue_Growth_YoY_pct"]

    # Bar chart for revenue
    x = np.arange(len(years))
    width = 0.45
    bars = ax1.bar(
        x,
        revenues,
        width,
        color=GS_PALETTE["navy_primary"],
        alpha=0.92,
        label="Revenue from Operations (₹ '000 Cr)",
        edgecolor=GS_PALETTE["navy_secondary"],
        linewidth=1.0,
        zorder=3,
    )

    # Data labels on bars
    for bar, rev_actual in zip(bars, df["Revenue from Operations"]):
        height = bar.get_height()
        ax1.annotate(
            f"₹{rev_actual:,.0f} Cr",
            xy=(bar.get_x() + bar.get_width() / 2, height),
            xytext=(0, 4),
            textcoords="offset points",
            ha="center",
            va="bottom",
            fontsize=9.5,
            fontweight="bold",
            color=GS_PALETTE["navy_primary"],
        )

    ax1.set_ylabel("Revenue (₹ in '000 Crores)", fontsize=10.5, fontweight="bold", color=GS_PALETTE["slate_text"])
    ax1.set_xticks(x)
    ax1.set_xticklabels(years, fontsize=10.5, fontweight="bold", color=GS_PALETTE["slate_text"])
    ax1.set_ylim(0, 300)
    ax1.grid(True, linestyle="--", alpha=0.6, color=GS_PALETTE["grid_color"], zorder=0)

    # Secondary axis for YoY growth
    ax2 = ax1.twinx()
    line = ax2.plot(
        x[1:],
        growth[1:],
        color=GS_PALETTE["gold_accent"],
        marker="o",
        linewidth=2.8,
        markersize=7,
        label="YoY Revenue Growth (%)",
        zorder=4,
    )

    for i in range(1, len(years)):
        val = growth.iloc[i]
        ax2.annotate(
            f"+{val:.1f}%",
            xy=(x[i], val),
            xytext=(0, 9),
            textcoords="offset points",
            ha="center",
            fontsize=9.5,
            fontweight="bold",
            color=GS_PALETTE["gold_accent"],
            bbox=dict(boxstyle="round,pad=0.2", facecolor="#FFFBEB", edgecolor=GS_PALETTE["gold_accent"], alpha=0.9),
        )

    ax2.set_ylabel("YoY Growth Rate (%)", fontsize=10.5, fontweight="bold", color=GS_PALETTE["gold_accent"])
    ax2.set_ylim(0, 25)

    # Title & Subtitle
    plt.title(
        "TCS Revenue Trajectory & Organic Growth (FY21 - FY24)\n"
        "Consistent Top-Line Compounding Reflecting Cloud & Digital Transformation Scale",
        fontsize=12,
        fontweight="bold",
        color=GS_PALETTE["slate_dark"],
        pad=16,
        loc="left",
    )

    # Combined Legend
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc="upper left", frameon=True, facecolor=GS_PALETTE["card_bg"], edgecolor=GS_PALETTE["grid_color"], fontsize=9)

    plt.figtext(0.08, -0.04, "Source: TCS Audited Consolidated Annual Reports | Institutional Equity Research Framework", fontsize=8, color="#64748B")

    plt.tight_layout()
    chart_path = os.path.join(output_dir, "revenue_growth_trend.png")
    plt.savefig(chart_path, dpi=300, bbox_inches="tight")
    plt.close()
    return chart_path


def plot_profitability_breakdown(df: pd.DataFrame, output_dir: str = None) -> str:
    """
    Clustered bar chart showing EBITDA, EBIT, and Net Profit across FY21 - FY24.
    """
    if output_dir is None:
        output_dir = get_charts_dir()

    fig, ax = plt.subplots(figsize=(8.5, 4.8), dpi=300)
    fig.patch.set_facecolor(GS_PALETTE["bg_color"])
    ax.set_facecolor(GS_PALETTE["bg_color"])

    years = [y.upper() for y in df.index]
    x = np.arange(len(years))
    width = 0.25

    ebitda = df["EBITDA"]
    ebit = df["EBIT (Operating Profit)"]
    pat = df["Net Profit (PAT)"]

    rects1 = ax.bar(x - width, ebitda, width, label="EBITDA", color=GS_PALETTE["navy_primary"], alpha=0.95, zorder=3)
    rects2 = ax.bar(x, ebit, width, label="EBIT (Operating Profit)", color=GS_PALETTE["steel_blue"], alpha=0.9, zorder=3)
    rects3 = ax.bar(x + width, pat, width, label="Net Profit (PAT)", color=GS_PALETTE["gold_accent"], alpha=0.95, zorder=3)

    # Annotate Net Profit
    for rect, p in zip(rects3, pat):
        h = rect.get_height()
        ax.annotate(
            f"₹{p:,.0f}",
            xy=(rect.get_x() + rect.get_width() / 2, h),
            xytext=(0, 3),
            textcoords="offset points",
            ha="center",
            va="bottom",
            fontsize=8.5,
            fontweight="bold",
            color=GS_PALETTE["slate_dark"],
        )

    ax.set_ylabel("INR in Crores (₹ Cr)", fontsize=10.5, fontweight="bold", color=GS_PALETTE["slate_text"])
    ax.set_xticks(x)
    ax.set_xticklabels(years, fontsize=10.5, fontweight="bold", color=GS_PALETTE["slate_text"])
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda y, _: f"₹{int(y):,}"))
    ax.set_ylim(0, 80000)
    ax.grid(True, linestyle="--", alpha=0.6, color=GS_PALETTE["grid_color"], zorder=0)

    plt.title(
        "TCS Profitability Cascade: EBITDA vs. EBIT vs. Net Profit (FY21 - FY24)\n"
        "Steady Profit Expansion Underpinned by Operational Discipline and Cost Control",
        fontsize=12,
        fontweight="bold",
        color=GS_PALETTE["slate_dark"],
        pad=16,
        loc="left",
    )

    ax.legend(loc="upper left", frameon=True, facecolor=GS_PALETTE["card_bg"], edgecolor=GS_PALETTE["grid_color"], fontsize=9.5)
    plt.figtext(0.08, -0.04, "Source: TCS Audited Consolidated Annual Reports | Currency in INR Crores", fontsize=8, color="#64748B")

    plt.tight_layout()
    chart_path = os.path.join(output_dir, "profitability_breakdown.png")
    plt.savefig(chart_path, dpi=300, bbox_inches="tight")
    plt.close()
    return chart_path


def plot_operating_margin_trends(ratios: pd.DataFrame, output_dir: str = None) -> str:
    """
    Line chart tracking EBITDA Margin, EBIT Margin, and Net Profit Margin over 4 years.
    """
    if output_dir is None:
        output_dir = get_charts_dir()

    fig, ax = plt.subplots(figsize=(8.5, 4.6), dpi=300)
    fig.patch.set_facecolor(GS_PALETTE["bg_color"])
    ax.set_facecolor(GS_PALETTE["bg_color"])

    years = [y.upper() for y in ratios.index]
    x = np.arange(len(years))

    ebitda_m = ratios["EBITDA_Margin_pct"]
    ebit_m = ratios["EBIT_Margin_pct"]
    net_m = ratios["Net_Profit_Margin_pct"]

    ax.plot(x, ebitda_m, marker="s", color=GS_PALETTE["navy_primary"], linewidth=2.6, markersize=7, label="EBITDA Margin (%)", zorder=3)
    ax.plot(x, ebit_m, marker="o", color=GS_PALETTE["steel_blue"], linewidth=2.6, markersize=7, label="EBIT Margin (%)", zorder=3)
    ax.plot(x, net_m, marker="^", color=GS_PALETTE["gold_accent"], linewidth=2.6, markersize=7, label="Net Profit Margin (%)", zorder=3)

    # Annotate points
    for i in range(len(years)):
        ax.annotate(f"{ebitda_m.iloc[i]:.1f}%", xy=(x[i], ebitda_m.iloc[i]), xytext=(0, 6), textcoords="offset points", ha="center", fontsize=8.5, fontweight="bold", color=GS_PALETTE["navy_primary"])
        ax.annotate(f"{ebit_m.iloc[i]:.1f}%", xy=(x[i], ebit_m.iloc[i]), xytext=(0, 6), textcoords="offset points", ha="center", fontsize=8.5, fontweight="bold", color=GS_PALETTE["steel_blue"])
        ax.annotate(f"{net_m.iloc[i]:.1f}%", xy=(x[i], net_m.iloc[i]), xytext=(0, -12), textcoords="offset points", ha="center", fontsize=8.5, fontweight="bold", color=GS_PALETTE["gold_accent"])

    ax.set_ylabel("Margin Percentage (%)", fontsize=10.5, fontweight="bold", color=GS_PALETTE["slate_text"])
    ax.set_xticks(x)
    ax.set_xticklabels(years, fontsize=10.5, fontweight="bold", color=GS_PALETTE["slate_text"])
    ax.set_ylim(15, 32)
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda y, _: f"{int(y)}%"))
    ax.grid(True, linestyle="--", alpha=0.6, color=GS_PALETTE["grid_color"], zorder=0)

    plt.title(
        "TCS Operating Margin Stability Analysis (FY21 - FY24)\n"
        "Industry-Leading Profit Margins Maintained Across Volatile Macroeconomic Cycles",
        fontsize=12,
        fontweight="bold",
        color=GS_PALETTE["slate_dark"],
        pad=16,
        loc="left",
    )

    ax.legend(loc="lower left", frameon=True, facecolor=GS_PALETTE["card_bg"], edgecolor=GS_PALETTE["grid_color"], fontsize=9.5)
    plt.figtext(0.08, -0.04, "Source: Audited Financial Accounts | Margins calculated as % of Revenue from Operations", fontsize=8, color="#64748B")

    plt.tight_layout()
    chart_path = os.path.join(output_dir, "operating_margin_trends.png")
    plt.savefig(chart_path, dpi=300, bbox_inches="tight")
    plt.close()
    return chart_path


def plot_peer_comparison(peer_df: pd.DataFrame, output_dir: str = None) -> str:
    """
    Four-quadrant or multi-bar visual benchmarking TCS against Infosys and HCLTech.
    """
    if output_dir is None:
        output_dir = get_charts_dir()

    fig, axes = plt.subplots(2, 2, figsize=(10, 7.5), dpi=300)
    fig.patch.set_facecolor(GS_PALETTE["bg_color"])

    companies = peer_df["company"].tolist()
    colors = [GS_PALETTE["navy_primary"], GS_PALETTE["steel_blue"], GS_PALETTE["gold_accent"]]

    # Panel 1: Revenue Scale (INR Cr)
    ax1 = axes[0, 0]
    ax1.set_facecolor(GS_PALETTE["bg_color"])
    bars1 = ax1.bar(companies, peer_df["revenue_cr"] / 1000.0, color=colors, alpha=0.9, zorder=3)
    ax1.set_title("Revenue Scale (FY24, ₹ '000 Cr)", fontsize=11, fontweight="bold", color=GS_PALETTE["slate_dark"])
    ax1.set_ylabel("₹ '000 Crores", fontsize=9.5, color=GS_PALETTE["slate_text"])
    ax1.set_ylim(0, 300)
    ax1.grid(True, linestyle="--", alpha=0.6, color=GS_PALETTE["grid_color"], zorder=0)
    for bar, val in zip(bars1, peer_df["revenue_cr"]):
        ax1.annotate(f"₹{val:,.0f} Cr", xy=(bar.get_x() + bar.get_width() / 2, bar.get_height()), xytext=(0, 3), textcoords="offset points", ha="center", fontsize=8.5, fontweight="bold")

    # Panel 2: EBIT Operating Margin (%)
    ax2 = axes[0, 1]
    ax2.set_facecolor(GS_PALETTE["bg_color"])
    bars2 = ax2.bar(companies, peer_df["ebit_margin_pct"], color=colors, alpha=0.9, zorder=3)
    ax2.set_title("Operating Margin (EBIT %, FY24)", fontsize=11, fontweight="bold", color=GS_PALETTE["slate_dark"])
    ax2.set_ylabel("EBIT Margin (%)", fontsize=9.5, color=GS_PALETTE["slate_text"])
    ax2.set_ylim(0, 32)
    ax2.grid(True, linestyle="--", alpha=0.6, color=GS_PALETTE["grid_color"], zorder=0)
    for bar, val in zip(bars2, peer_df["ebit_margin_pct"]):
        ax2.annotate(f"{val:.1f}%", xy=(bar.get_x() + bar.get_width() / 2, bar.get_height()), xytext=(0, 3), textcoords="offset points", ha="center", fontsize=8.5, fontweight="bold")

    # Panel 3: Return on Equity (ROE %)
    ax3 = axes[1, 0]
    ax3.set_facecolor(GS_PALETTE["bg_color"])
    bars3 = ax3.bar(companies, peer_df["roe_pct"], color=colors, alpha=0.9, zorder=3)
    ax3.set_title("Return on Equity (ROE %, FY24)", fontsize=11, fontweight="bold", color=GS_PALETTE["slate_dark"])
    ax3.set_ylabel("ROE (%)", fontsize=9.5, color=GS_PALETTE["slate_text"])
    ax3.set_ylim(0, 65)
    ax3.grid(True, linestyle="--", alpha=0.6, color=GS_PALETTE["grid_color"], zorder=0)
    for bar, val in zip(bars3, peer_df["roe_pct"]):
        ax3.annotate(f"{val:.1f}%", xy=(bar.get_x() + bar.get_width() / 2, bar.get_height()), xytext=(0, 3), textcoords="offset points", ha="center", fontsize=8.5, fontweight="bold")

    # Panel 4: P/E Valuation Multiples (x)
    ax4 = axes[1, 1]
    ax4.set_facecolor(GS_PALETTE["bg_color"])
    bars4 = ax4.bar(companies, peer_df["pe_ratio"], color=colors, alpha=0.9, zorder=3)
    ax4.set_title("Price-to-Earnings Ratio (P/E, x)", fontsize=11, fontweight="bold", color=GS_PALETTE["slate_dark"])
    ax4.set_ylabel("P/E Multiple (x)", fontsize=9.5, color=GS_PALETTE["slate_text"])
    ax4.set_ylim(0, 40)
    ax4.grid(True, linestyle="--", alpha=0.6, color=GS_PALETTE["grid_color"], zorder=0)
    for bar, val in zip(bars4, peer_df["pe_ratio"]):
        ax4.annotate(f"{val:.1f}x", xy=(bar.get_x() + bar.get_width() / 2, bar.get_height()), xytext=(0, 3), textcoords="offset points", ha="center", fontsize=8.5, fontweight="bold")

    plt.suptitle(
        "Tier-1 Indian IT Peer Benchmarking: TCS vs. Infosys vs. HCLTech (FY24)\n"
        "TCS Leads Industry in Scale, Operating Margin Defense, and Capital Efficiency (ROE)",
        fontsize=13,
        fontweight="bold",
        color=GS_PALETTE["slate_dark"],
        y=0.99,
    )

    plt.figtext(0.08, -0.02, "Source: Company Filings, NSE Market Data | Audited Financial Metrics FY24", fontsize=8, color="#64748B")

    plt.tight_layout()
    chart_path = os.path.join(output_dir, "competitor_comparison.png")
    plt.savefig(chart_path, dpi=300, bbox_inches="tight")
    plt.close()
    return chart_path


def plot_cashflow_capex(df: pd.DataFrame, output_dir: str = None) -> str:
    """
    Shows Cash Flow from Operations, CapEx, and Free Cash Flow generation.
    Highlights TCS's asset-light nature (>95% FCF conversion).
    """
    if output_dir is None:
        output_dir = get_charts_dir()

    fig, ax = plt.subplots(figsize=(8.5, 4.8), dpi=300)
    fig.patch.set_facecolor(GS_PALETTE["bg_color"])
    ax.set_facecolor(GS_PALETTE["bg_color"])

    years = [y.upper() for y in df.index]
    x = np.arange(len(years))
    width = 0.28

    ocf = df["Cash Flow from Operations (OCF)"]
    capex = df["Capital Expenditures (CapEx)"]
    fcf = df["Free Cash Flow (FCF)"]

    rects1 = ax.bar(x - width/2, ocf, width, label="Operating Cash Flow (OCF)", color=GS_PALETTE["navy_primary"], alpha=0.9, zorder=3)
    rects2 = ax.bar(x + width/2, fcf, width, label="Free Cash Flow (FCF = OCF - CapEx)", color=GS_PALETTE["emerald"], alpha=0.9, zorder=3)

    # Line for CapEx
    ax2 = ax.twinx()
    ax2.plot(x, capex, color=GS_PALETTE["gold_accent"], marker="o", linewidth=2.4, label="CapEx (Right Axis)", zorder=4)
    ax2.set_ylabel("CapEx (₹ in Crores)", fontsize=10, fontweight="bold", color=GS_PALETTE["gold_accent"])
    ax2.set_ylim(0, 6000)
    for i, c in enumerate(capex):
        ax2.annotate(f"₹{c:,.0f}", xy=(x[i], c), xytext=(0, 6), textcoords="offset points", ha="center", fontsize=8.5, fontweight="bold", color=GS_PALETTE["gold_accent"])

    for rect, f in zip(rects2, fcf):
        h = rect.get_height()
        ax.annotate(f"₹{f:,.0f} Cr", xy=(rect.get_x() + rect.get_width() / 2, h), xytext=(0, 3), textcoords="offset points", ha="center", va="bottom", fontsize=8.5, fontweight="bold", color=GS_PALETTE["emerald"])

    ax.set_ylabel("Cash Flow (₹ in Crores)", fontsize=10.5, fontweight="bold", color=GS_PALETTE["slate_text"])
    ax.set_xticks(x)
    ax.set_xticklabels(years, fontsize=10.5, fontweight="bold", color=GS_PALETTE["slate_text"])
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda y, _: f"₹{int(y):,}"))
    ax.set_ylim(0, 60000)
    ax.grid(True, linestyle="--", alpha=0.6, color=GS_PALETTE["grid_color"], zorder=0)

    plt.title(
        "TCS Cash Flow Quality & Asset-Light Capital Discipline (FY21 - FY24)\n"
        "Exceptional Cash Conversion With FCF Exceeding 95% of Reported Net Income",
        fontsize=12,
        fontweight="bold",
        color=GS_PALETTE["slate_dark"],
        pad=16,
        loc="left",
    )

    lines1, labels1 = ax.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax.legend(lines1 + lines2, labels1 + labels2, loc="upper left", frameon=True, facecolor=GS_PALETTE["card_bg"], edgecolor=GS_PALETTE["grid_color"], fontsize=9)

    plt.figtext(0.08, -0.04, "Source: Consolidated Cash Flow Statements | High cash conversion supports sustained dividend distribution", fontsize=8, color="#64748B")

    plt.tight_layout()
    chart_path = os.path.join(output_dir, "cashflow_conversion_capex.png")
    plt.savefig(chart_path, dpi=300, bbox_inches="tight")
    plt.close()
    return chart_path


def plot_dcf_sensitivity_heatmap(sens_df: pd.DataFrame, output_dir: str = None) -> str:
    """
    Renders an institutional 2D sensitivity matrix heatmap for DCF implied share price.
    """
    if output_dir is None:
        output_dir = get_charts_dir()

    fig, ax = plt.subplots(figsize=(8.0, 4.8), dpi=300)
    fig.patch.set_facecolor(GS_PALETTE["bg_color"])
    ax.set_facecolor(GS_PALETTE["bg_color"])

    data = sens_df.values
    im = ax.imshow(data, cmap="Blues", aspect="auto")

    # Ticks & labels
    ax.set_xticks(np.arange(len(sens_df.columns)))
    ax.set_yticks(np.arange(len(sens_df.index)))
    ax.set_xticklabels(sens_df.columns, fontsize=9.5, fontweight="bold", color=GS_PALETTE["slate_text"])
    ax.set_yticklabels(sens_df.index, fontsize=9.5, fontweight="bold", color=GS_PALETTE["slate_text"])

    ax.set_xlabel("Terminal Growth Rate (g)", fontsize=10.5, fontweight="bold", color=GS_PALETTE["slate_dark"], labelpad=8)
    ax.set_ylabel("Discount Rate (WACC)", fontsize=10.5, fontweight="bold", color=GS_PALETTE["slate_dark"], labelpad=8)

    # Annotate values
    for i in range(len(sens_df.index)):
        for j in range(len(sens_df.columns)):
            val = data[i, j]
            # Choose text color based on cell lightness
            color = "white" if val > (data.max() + data.min()) / 2.05 else GS_PALETTE["slate_dark"]
            ax.text(j, i, f"₹{val:,.0f}", ha="center", va="center", color=color, fontsize=10, fontweight="bold")

    plt.title(
        "TCS Illustrative DCF Valuation Sensitivity Matrix (₹ / Share)\n"
        "Implied Share Value Across Cross-Sections of WACC and Terminal Growth Rates",
        fontsize=12,
        fontweight="bold",
        color=GS_PALETTE["slate_dark"],
        pad=16,
        loc="left",
    )

    cbar = fig.colorbar(im, ax=ax, fraction=0.03, pad=0.04)
    cbar.ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda y, _: f"₹{int(y):,}"))
    cbar.ax.tick_params(labelsize=8.5)

    plt.figtext(0.08, -0.04, "Note: Illustrative scenario analysis based on explicit discount rate and growth assumptions. Not a price target.", fontsize=8, color="#64748B")

    plt.tight_layout()
    chart_path = os.path.join(output_dir, "dcf_sensitivity_matrix.png")
    plt.savefig(chart_path, dpi=300, bbox_inches="tight")
    plt.close()
    return chart_path


def generate_all_charts(
    tcs_df: pd.DataFrame,
    ratios_df: pd.DataFrame,
    peer_df: pd.DataFrame,
    sens_df: pd.DataFrame,
    output_dir: str = None,
) -> Dict[str, str]:
    """Generates all 5 primary charts plus the DCF sensitivity heatmap."""
    if output_dir is None:
        output_dir = get_charts_dir()

    p1 = plot_revenue_trend(tcs_df, ratios_df, output_dir)
    p2 = plot_profitability_breakdown(tcs_df, output_dir)
    p3 = plot_operating_margin_trends(ratios_df, output_dir)
    p4 = plot_peer_comparison(peer_df, output_dir)
    p5 = plot_cashflow_capex(tcs_df, output_dir)
    p6 = plot_dcf_sensitivity_heatmap(sens_df, output_dir)

    return {
        "revenue_growth": p1,
        "profitability": p2,
        "margin_trends": p3,
        "peer_comparison": p4,
        "cashflow_capex": p5,
        "dcf_sensitivity": p6,
    }


if __name__ == "__main__":
    from data_loader import load_tcs_historical, load_peer_comparison
    from financial_analysis import compute_financial_ratios
    from valuation_model import TCSValuationModel

    tcs = load_tcs_historical()
    ratios = compute_financial_ratios(tcs)
    peers = load_peer_comparison()
    val_model = TCSValuationModel()
    sens = val_model.generate_sensitivity_matrix()

    chart_paths = generate_all_charts(tcs, ratios, peers, sens)
    print("All charts successfully generated:")
    for k, v in chart_paths.items():
        print(f"  {k} -> {v}")
