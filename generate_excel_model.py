"""
=============================================================================
Excel Financial Model Generator: TCS Equity Research & Valuation Model
Institutional Equity Research Excel Financial Model
=============================================================================
Generates a multi-tab, institutional-grade financial model in Microsoft Excel
format (.xlsx) using openpyxl, complete with:
- Cover & Executive Overview
- Historical Income Statement (FY21 - FY24)
- Balance Sheet & Cash Flow Statement
- Ratio Analysis & 3-Stage DuPont Breakdown
- Peer Comparison (TCS vs Infosys vs HCLTech)
- 5-Year DCF Model with Excel Formulas & Sensitivity Matrix
"""

import os
import openpyxl
import pandas as pd
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

from src.data_loader import load_tcs_historical, load_peer_comparison, load_segment_breakdown
from src.financial_analysis import compute_financial_ratios
from src.valuation_model import TCSValuationModel


# Style Palette
NAVY_HEADER = "0A2540"
NAVY_SUBHEADER = "1E3A8A"
LIGHT_BLUE_FILL = "F0F4F8"
ZEBRA_FILL = "F8FAFC"
ACCENT_GOLD = "D97706"
BORDER_COLOR = "CBD5E1"
TEXT_DARK = "0F172A"
TEXT_MUTED = "475569"


def apply_header_style(cell, text: str, bg_color: str = NAVY_HEADER, font_size: int = 11, bold: bool = True):
    cell.value = text
    cell.font = Font(name="Calibri", size=font_size, bold=bold, color="FFFFFF")
    cell.fill = PatternFill(start_color=bg_color, end_color=bg_color, fill_type="solid")
    cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)


def apply_data_cell(cell, value, num_format: str = None, bold: bool = False, align: str = "right", bg_color: str = None):
    cell.value = value
    cell.font = Font(name="Calibri", size=10, bold=bold, color=TEXT_DARK)
    cell.alignment = Alignment(horizontal=align, vertical="center")
    if bg_color:
        cell.fill = PatternFill(start_color=bg_color, end_color=bg_color, fill_type="solid")
    if num_format:
        cell.number_format = num_format

    thin_border = Border(
        left=Side(style="thin", color=BORDER_COLOR),
        right=Side(style="thin", color=BORDER_COLOR),
        top=Side(style="thin", color=BORDER_COLOR),
        bottom=Side(style="thin", color=BORDER_COLOR),
    )
    cell.border = thin_border


def autofit_columns(ws, min_width=12, max_width=35):
    for col in ws.columns:
        col_letter = get_column_letter(col[0].column)
        max_len = 0
        for cell in col:
            val_str = str(cell.value or "")
            if cell.number_format and "%" in cell.number_format:
                val_str += "%"
            max_len = max(max_len, len(val_str))
        ws.column_dimensions[col_letter].width = max(min(max_len + 3, max_width), min_width)


def generate_excel_model(output_path: str = None) -> str:
    if output_path is None:
        data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "data"))
        output_path = os.path.join(data_dir, "tcs_financial_model.xlsx")

    tcs_df = load_tcs_historical()
    ratios_df = compute_financial_ratios(tcs_df)
    peer_df = load_peer_comparison()
    val_model = TCSValuationModel()
    dcf_res = val_model.run_dcf()
    sens_df = val_model.generate_sensitivity_matrix()

    wb = openpyxl.Workbook()
    # Remove default sheet
    wb.remove(wb.active)

    # =========================================================================
    # TAB 1: COVER & EXECUTIVE OVERVIEW
    # =========================================================================
    ws_cover = wb.create_sheet(title="Executive Summary")
    ws_cover.views.sheetView[0].showGridLines = True

    # Title Banner
    ws_cover.merge_cells("A1:G1")
    title_cell = ws_cover["A1"]
    title_cell.value = "TATA CONSULTANCY SERVICES LTD (TCS) — FINANCIAL MODEL & EQUITY VALUATION"
    title_cell.font = Font(name="Calibri", size=14, bold=True, color="FFFFFF")
    title_cell.fill = PatternFill(start_color=NAVY_HEADER, end_color=NAVY_HEADER, fill_type="solid")
    title_cell.alignment = Alignment(horizontal="center", vertical="center")
    ws_cover.row_dimensions[1].height = 36

    ws_cover.merge_cells("A2:G2")
    sub_cell = ws_cover["A2"]
    sub_cell.value = "Institutional Equity Research Format | Fundamental & Valuation Analysis | FY21 - FY24"
    sub_cell.font = Font(name="Calibri", size=11, italic=True, color="FFFFFF")
    sub_cell.fill = PatternFill(start_color=NAVY_SUBHEADER, end_color=NAVY_SUBHEADER, fill_type="solid")
    sub_cell.alignment = Alignment(horizontal="center", vertical="center")
    ws_cover.row_dimensions[2].height = 24

    overview_rows = [
        ("Ticker / Exchange", "TCS.NS (NSE) / 532540 (BSE)", "Sector", "Information Technology Services"),
        ("Current Share Price (CMP)", "₹3,850.00", "Market Capitalization", "₹13,90,000 Cr (~$168B USD)"),
        ("Shares Outstanding", "361.80 Cr", "Enterprise Value (EV)", "₹13,49,478 Cr"),
        ("52-Week Range", "₹3,313.00 - ₹4,585.00", "Free Float", "28.23% (Promoter: 71.77%)"),
        ("FY24 Revenue", "₹2,40,893 Cr", "FY24 Net Profit (PAT)", "₹46,099 Cr"),
        ("FY24 EBIT Margin", "24.6% - 25.8%", "FY24 Return on Equity (ROE)", "51.1%"),
        ("FY24 Free Cash Flow", "₹45,108 Cr", "FCF / PAT Conversion", "97.8%"),
        ("Net Cash on Balance Sheet", "₹40,522 Cr", "Traditional Debt", "₹0.00 (Zero Bank Debt)"),
    ]

    ws_cover["A4"] = "KEY METRICS SUMMARY & CORPORATE SNAPSHOT"
    ws_cover["A4"].font = Font(name="Calibri", size=11, bold=True, color=NAVY_HEADER)

    r = 5
    for item in overview_rows:
        apply_data_cell(ws_cover.cell(row=r, column=1), item[0], bold=True, align="left", bg_color=LIGHT_BLUE_FILL)
        apply_data_cell(ws_cover.cell(row=r, column=2), item[1], align="left")
        apply_data_cell(ws_cover.cell(row=r, column=4), item[2], bold=True, align="left", bg_color=LIGHT_BLUE_FILL)
        apply_data_cell(ws_cover.cell(row=r, column=5), item[3], align="left")
        r += 1

    ws_cover["A15"] = "WORKBOOK TABLE OF CONTENTS"
    ws_cover["A15"].font = Font(name="Calibri", size=11, bold=True, color=NAVY_HEADER)

    toc_items = [
        ("Tab 1: Executive Summary", "Overview, corporate metadata, key valuation multiples, and navigation"),
        ("Tab 2: Financial Statements", "Historical 4-year Income Statement, Balance Sheet, and Cash Flow (FY21-FY24)"),
        ("Tab 3: Ratio Analysis", "Growth, margins, capital return (ROE/ROA/ROCE), DuPont 3-stage decomposition"),
        ("Tab 4: Peer Benchmark", "TCS vs Infosys vs HCLTech FY24 operational & valuation comparison"),
        ("Tab 5: DCF Model", "5-year Unlevered FCF projection, WACC calculation, terminal value & sensitivity grid"),
    ]

    r = 16
    for title, desc in toc_items:
        apply_data_cell(ws_cover.cell(row=r, column=1), title, bold=True, align="left")
        apply_data_cell(ws_cover.cell(row=r, column=2), desc, align="left")
        ws_cover.merge_cells(start_row=r, start_column=2, end_row=r, end_column=6)
        r += 1

    ws_cover["A23"] = "DISCLAIMER: This financial model is built for academic and institutional equity research demonstration purposes."
    ws_cover["A23"].font = Font(name="Calibri", size=9, italic=True, color=TEXT_MUTED)

    autofit_columns(ws_cover)

    # =========================================================================
    # TAB 2: HISTORICAL FINANCIAL STATEMENTS
    # =========================================================================
    ws_fin = wb.create_sheet(title="Financial Statements")
    ws_fin.views.sheetView[0].showGridLines = True

    ws_fin.merge_cells("A1:F1")
    t = ws_fin["A1"]
    t.value = "TCS HISTORICAL FINANCIAL STATEMENTS (FY21 - FY24, INR Crores)"
    t.font = Font(name="Calibri", size=13, bold=True, color="FFFFFF")
    t.fill = PatternFill(start_color=NAVY_HEADER, end_color=NAVY_HEADER, fill_type="solid")
    t.alignment = Alignment(horizontal="center", vertical="center")
    ws_fin.row_dimensions[1].height = 28

    headers = ["Financial Statement Line Item", "FY21", "FY22", "FY23", "FY24", "3-Yr CAGR"]
    for c_idx, h in enumerate(headers, 1):
        apply_header_style(ws_fin.cell(row=3, column=c_idx), h, bg_color=NAVY_SUBHEADER)

    # Line items
    metrics_to_show = [
        ("INCOME STATEMENT", None, True),
        ("Revenue from Operations", "#,##0", False),
        ("Employee Benefit Expenses", "#,##0", False),
        ("Other Operating Expenses", "#,##0", False),
        ("EBITDA", "#,##0", True),
        ("Depreciation & Amortization", "#,##0", False),
        ("EBIT (Operating Profit)", "#,##0", True),
        ("Other Income", "#,##0", False),
        ("Finance Costs", "#,##0", False),
        ("Profit Before Tax (PBT)", "#,##0", False),
        ("Tax Expense", "#,##0", False),
        ("Net Profit (PAT)", "#,##0", True),
        ("Diluted EPS (INR)", "₹#,##0.00", True),
        ("BALANCE SHEET & LIQUIDITY", None, True),
        ("Total Shareholders Equity", "#,##0", False),
        ("Total Borrowings (Bank Debt)", "#,##0", False),
        ("Lease Liabilities", "#,##0", False),
        ("Total Debt (inc. Leases)", "#,##0", False),
        ("Cash & Liquid Investments", "#,##0", True),
        ("Total Assets", "#,##0", False),
        ("CASH FLOW STATEMENT", None, True),
        ("Cash Flow from Operations (OCF)", "#,##0", True),
        ("Capital Expenditures (CapEx)", "#,##0", False),
        ("Free Cash Flow (FCF)", "#,##0", True),
    ]

    curr_row = 4
    for item_name, num_fmt, is_bold in metrics_to_show:
        if num_fmt is None:
            # Section Header
            ws_fin.merge_cells(start_row=curr_row, start_column=1, end_row=curr_row, end_column=6)
            scell = ws_fin.cell(row=curr_row, column=1)
            scell.value = item_name
            scell.font = Font(name="Calibri", size=10, bold=True, color="FFFFFF")
            scell.fill = PatternFill(start_color=NAVY_HEADER, end_color=NAVY_HEADER, fill_type="solid")
            scell.alignment = Alignment(horizontal="left", vertical="center")
            curr_row += 1
            continue

        c1 = ws_fin.cell(row=curr_row, column=1)
        apply_data_cell(c1, item_name, bold=is_bold, align="left", bg_color=LIGHT_BLUE_FILL if is_bold else None)

        row_vals = []
        for yr_idx, yr in enumerate(["fy21", "fy22", "fy23", "fy24"], 2):
            val = tcs_df.loc[yr, item_name]
            row_vals.append(val)
            c = ws_fin.cell(row=curr_row, column=yr_idx)
            apply_data_cell(c, val, num_format=num_fmt, bold=is_bold, bg_color=LIGHT_BLUE_FILL if is_bold else None)

        # CAGR formula
        cagr_cell = ws_fin.cell(row=curr_row, column=6)
        if row_vals[0] > 0 and row_vals[-1] > 0:
            cagr_cell.value = f"=((E{curr_row}/B{curr_row})^(1/3))-1"
            cagr_cell.number_format = "0.0%"
        else:
            cagr_cell.value = "N/A"
        apply_data_cell(cagr_cell, cagr_cell.value, num_format="0.0%", bold=is_bold, bg_color=LIGHT_BLUE_FILL if is_bold else None)

        curr_row += 1

    autofit_columns(ws_fin)

    # =========================================================================
    # TAB 3: RATIO ANALYSIS & DUPONT
    # =========================================================================
    ws_rat = wb.create_sheet(title="Ratio Analysis")
    ws_rat.views.sheetView[0].showGridLines = True

    ws_rat.merge_cells("A1:E1")
    rt = ws_rat["A1"]
    rt.value = "TCS FINANCIAL RATIO ANALYSIS & 3-STAGE DUPONT DECOMPOSITION"
    rt.font = Font(name="Calibri", size=13, bold=True, color="FFFFFF")
    rt.fill = PatternFill(start_color=NAVY_HEADER, end_color=NAVY_HEADER, fill_type="solid")
    rt.alignment = Alignment(horizontal="center", vertical="center")
    ws_rat.row_dimensions[1].height = 28

    headers_rat = ["Financial Ratio / Metric", "FY21", "FY22", "FY23", "FY24"]
    for c_idx, h in enumerate(headers_rat, 1):
        apply_header_style(ws_rat.cell(row=3, column=c_idx), h, bg_color=NAVY_SUBHEADER)

    ratios_list = [
        ("GROWTH RATIOS", None),
        ("Revenue Growth (YoY)", "Revenue_Growth_YoY_pct", "0.0%"),
        ("EBITDA Growth (YoY)", "EBITDA_Growth_YoY_pct", "0.0%"),
        ("Net Profit Growth (YoY)", "Net_Profit_Growth_YoY_pct", "0.0%"),
        ("EPS Growth (YoY)", "EPS_Growth_YoY_pct", "0.0%"),
        ("PROFITABILITY MARGINS", None),
        ("EBITDA Margin (%)", "EBITDA_Margin_pct", "0.0%"),
        ("EBIT Operating Margin (%)", "EBIT_Margin_pct", "0.0%"),
        ("Net Profit Margin (%)", "Net_Profit_Margin_pct", "0.0%"),
        ("CAPITAL EFFICIENCY & RETURNS", None),
        ("Return on Equity (ROE)", "ROE_pct", "0.0%"),
        ("Return on Assets (ROA)", "ROA_pct", "0.0%"),
        ("Return on Capital Employed (ROCE)", "ROCE_pct", "0.0%"),
        ("SOLVENCY & LEVERAGE", None),
        ("Debt-to-Equity (inc. Leases)", "Debt_to_Equity_Ratio", "0.00x"),
        ("Bank Debt-to-Equity", "Bank_Debt_to_Equity_Ratio", "0.00x"),
        ("CASH CONVERSION & CAPITAL INTENSITY", None),
        ("Operating Cash Flow / Net Profit", "OCF_to_Net_Profit_Conversion_pct", "0.0%"),
        ("Free Cash Flow / Net Profit", "FCF_to_Net_Profit_Conversion_pct", "0.0%"),
        ("CapEx as % of Revenue", "CapEx_to_Revenue_pct", "0.0%"),
        ("DUPONT 3-STAGE DECOMPOSITION", None),
        ("1. Net Profit Margin (%)", "DuPont_Net_Margin_pct", "0.0%"),
        ("2. Asset Turnover (x)", "DuPont_Asset_Turnover_x", "0.00x"),
        ("3. Equity Multiplier / Leverage (x)", "DuPont_Equity_Multiplier_x", "0.00x"),
        ("Reconstructed ROE (1 x 2 x 3)", "DuPont_Reconstructed_ROE_pct", "0.0%"),
    ]

    curr_row = 4
    for r_entry in ratios_list:
        if r_entry[1] is None:
            # Section header
            ws_rat.merge_cells(start_row=curr_row, start_column=1, end_row=curr_row, end_column=5)
            scell = ws_rat.cell(row=curr_row, column=1)
            scell.value = r_entry[0]
            scell.font = Font(name="Calibri", size=10, bold=True, color="FFFFFF")
            scell.fill = PatternFill(start_color=NAVY_HEADER, end_color=NAVY_HEADER, fill_type="solid")
            curr_row += 1
            continue

        label, col_key, fmt = r_entry
        apply_data_cell(ws_rat.cell(row=curr_row, column=1), label, bold="ROE" in label or "Margin" in label, align="left")

        for yr_idx, yr in enumerate(["fy21", "fy22", "fy23", "fy24"], 2):
            val = ratios_df.loc[yr, col_key]
            # Convert percentage scale if needed for Excel percentage format
            if fmt == "0.0%":
                display_val = val / 100.0 if not pd.isna(val) else None
            else:
                display_val = val if not pd.isna(val) else None

            cell = ws_rat.cell(row=curr_row, column=yr_idx)
            apply_data_cell(cell, display_val, num_format=fmt, bold="ROE" in label or "Margin" in label)

        curr_row += 1

    autofit_columns(ws_rat)

    # =========================================================================
    # TAB 4: PEER COMPARISON BENCHMARK
    # =========================================================================
    ws_peer = wb.create_sheet(title="Peer Benchmark")
    ws_peer.views.sheetView[0].showGridLines = True

    ws_peer.merge_cells("A1:G1")
    pt = ws_peer["A1"]
    pt.value = "TIER-1 INDIAN IT PEER BENCHMARK (FY24 AUDITED FIGURES)"
    pt.font = Font(name="Calibri", size=13, bold=True, color="FFFFFF")
    pt.fill = PatternFill(start_color=NAVY_HEADER, end_color=NAVY_HEADER, fill_type="solid")
    pt.alignment = Alignment(horizontal="center", vertical="center")
    ws_peer.row_dimensions[1].height = 28

    peer_headers = ["Metric / Benchmark", "TCS (Tata Consultancy)", "Infosys", "HCLTech", "Peer Outperformance Leader"]
    for c_idx, h in enumerate(peer_headers, 1):
        apply_header_style(ws_peer.cell(row=3, column=c_idx), h, bg_color=NAVY_SUBHEADER)

    peer_metrics_table = [
        ("Revenue from Operations (₹ Cr)", 240893, 153670, 109913, "TCS (Scale Leader)", "#,##0"),
        ("YoY Revenue Growth (%)", 0.068, 0.047, 0.083, "HCLTech (8.3%)", "0.0%"),
        ("EBIT Operating Margin (%)", 0.246, 0.207, 0.182, "TCS (24.6% - Defensible Moat)", "0.0%"),
        ("Net Profit Margin (%)", 0.191, 0.171, 0.143, "TCS (19.1%)", "0.0%"),
        ("Return on Equity (ROE %)", 0.511, 0.318, 0.234, "TCS (51.1% - Exceptional Capital Return)", "0.0%"),
        ("Return on Capital Employed (ROCE %)", 0.624, 0.405, 0.281, "TCS (62.4%)", "0.0%"),
        ("Debt-to-Equity (Leases included)", 0.09, 0.11, 0.08, "All Virtually Debt-Free", "0.00x"),
        ("Price-to-Earnings (P/E Multiple, x)", 30.3, 25.4, 26.2, "TCS Commands Quality Premium", "0.0x"),
        ("EV / EBITDA (x)", 20.2, 17.6, 16.1, "TCS", "0.0x"),
        ("Dividend Yield (%)", 0.018, 0.023, 0.034, "HCLTech (3.4%)", "0.0%"),
        ("Market Capitalization (₹ Cr)", 1390000, 645000, 405000, "TCS (~$168B USD)", "#,##0"),
        ("LTM Attrition Rate (%)", 0.125, 0.138, 0.128, "TCS (12.5% - Industry Lowest)", "0.0%"),
        ("Total Headcount (Employees)", 601546, 317240, 227481, "TCS (>600k Workforce)", "#,##0"),
    ]

    r = 4
    for label, tcs_v, infy_v, hcl_v, leader, fmt in peer_metrics_table:
        apply_data_cell(ws_peer.cell(row=r, column=1), label, bold=True, align="left")
        apply_data_cell(ws_peer.cell(row=r, column=2), tcs_v, num_format=fmt, bold=True, bg_color=LIGHT_BLUE_FILL)
        apply_data_cell(ws_peer.cell(row=r, column=3), infy_v, num_format=fmt)
        apply_data_cell(ws_peer.cell(row=r, column=4), hcl_v, num_format=fmt)
        apply_data_cell(ws_peer.cell(row=r, column=5), leader, align="left", bold="TCS" in leader)
        r += 1

    autofit_columns(ws_peer)

    # =========================================================================
    # TAB 5: DCF VALUATION MODEL
    # =========================================================================
    ws_dcf = wb.create_sheet(title="DCF Valuation Model")
    ws_dcf.views.sheetView[0].showGridLines = True

    ws_dcf.merge_cells("A1:G1")
    dt = ws_dcf["A1"]
    dt.value = "TCS DISCOUNTED CASH FLOW (DCF) VALUATION MODEL & SENSITIVITY MATRIX"
    dt.font = Font(name="Calibri", size=13, bold=True, color="FFFFFF")
    dt.fill = PatternFill(start_color=NAVY_HEADER, end_color=NAVY_HEADER, fill_type="solid")
    dt.alignment = Alignment(horizontal="center", vertical="center")
    ws_dcf.row_dimensions[1].height = 28

    # Block 1: WACC & Capital Asset Pricing Model
    ws_dcf["A3"] = "WACC CALCULATION (CAPM METHODOLOGY)"
    ws_dcf["A3"].font = Font(name="Calibri", size=11, bold=True, color=NAVY_HEADER)

    wacc_data = [
        ("Risk-Free Rate (Rf - 10Y Indian G-Sec)", 0.0710, "0.00%"),
        ("Equity Risk Premium (ERP)", 0.0600, "0.00%"),
        ("Adjusted Beta (Beta)", 0.82, "0.00"),
        ("Cost of Equity (Ke = Rf + Beta * ERP)", "=B4+(B6*B5)", "0.00%"),
        ("Pre-Tax Cost of Debt (Kd - Leases)", 0.0750, "0.00%"),
        ("Statutory Corporate Tax Rate (t)", 0.2517, "0.00%"),
        ("After-Tax Cost of Debt [Kd * (1 - t)]", "=B8*(1-B9)", "0.00%"),
        ("Weight of Equity (We)", 0.9940, "0.00%"),
        ("Weight of Debt (Wd)", 0.0060, "0.00%"),
        ("Weighted Average Cost of Capital (WACC)", "=(B7*B11)+(B10*B12)", "0.00%"),
    ]

    for idx, (param, val, fmt) in enumerate(wacc_data, 4):
        apply_data_cell(ws_dcf.cell(row=idx, column=1), param, bold="WACC" in param or "Cost of Equity" in param, align="left")
        cell_val = ws_dcf.cell(row=idx, column=2)
        apply_data_cell(cell_val, val, num_format=fmt, bold="WACC" in param or "Cost of Equity" in param, bg_color=LIGHT_BLUE_FILL if "WACC" in param else None)

    # Block 2: 5-Year Cash Flow Projections Table
    ws_dcf["A15"] = "5-YEAR UNLEVERED FREE CASH FLOW (FCFF) PROJECTIONS (INR Crores)"
    ws_dcf["A15"].font = Font(name="Calibri", size=11, bold=True, color=NAVY_HEADER)

    proj_headers = ["Line Item / Assumption", "FY25E", "FY26E", "FY27E", "FY28E", "FY29E"]
    for c_idx, h in enumerate(proj_headers, 1):
        apply_header_style(ws_dcf.cell(row=16, column=c_idx), h, bg_color=NAVY_SUBHEADER)

    proj_df = dcf_res["projections_df"]

    proj_rows = [
        ("Revenue Growth Rate (%)", "Revenue_Growth_pct", "0.0%"),
        ("Projected Revenue", "Revenue_INR_Cr", "#,##0"),
        ("EBIT Margin (%)", "EBIT_Margin_pct", "0.0%"),
        ("Operating Profit (EBIT)", "EBIT_INR_Cr", "#,##0"),
        ("NOPAT [EBIT * (1 - t)]", "NOPAT_INR_Cr", "#,##0"),
        ("(+) Depreciation & Amortization (2.1% Rev)", "Depr_Amort_INR_Cr", "#,##0"),
        ("(-) Capital Expenditures (CapEx 1.6% Rev)", "CapEx_INR_Cr", "#,##0"),
        ("(-) Net Working Capital Change (1.0% Delta)", "Delta_NWC_INR_Cr", "#,##0"),
        ("Unlevered Free Cash Flow (FCFF)", "FCFF_INR_Cr", "#,##0"),
        ("Discount Period (Mid-year: t - 0.5)", None, "0.0"),
        ("Present Value of FCFF (PV)", "PV_FCFF_INR_Cr", "#,##0"),
    ]

    r = 17
    for p_label, p_col, p_fmt in proj_rows:
        apply_data_cell(ws_dcf.cell(row=r, column=1), p_label, bold="FCFF" in p_label or "Revenue" in p_label, align="left")
        for col_i, yr_str in enumerate(proj_df.index, 2):
            if p_col == "Revenue_Growth_pct" or p_col == "EBIT_Margin_pct":
                cell_v = proj_df.loc[yr_str, p_col] / 100.0
            elif p_col is None:
                cell_v = (col_i - 1) - 0.5  # 0.5, 1.5, 2.5, 3.5, 4.5
            else:
                cell_v = proj_df.loc[yr_str, p_col]

            cell = ws_dcf.cell(row=r, column=col_i)
            apply_data_cell(cell, cell_v, num_format=p_fmt, bold="FCFF" in p_label, bg_color=LIGHT_BLUE_FILL if "FCFF" in p_label else None)
        r += 1

    # Block 3: Enterprise Value to Equity Value Bridge
    ws_dcf["A29"] = "ENTERPRISE VALUE TO EQUITY VALUE BRIDGE (INR Crores)"
    ws_dcf["A29"].font = Font(name="Calibri", size=11, bold=True, color=NAVY_HEADER)

    bridge_data = [
        ("Cumulative PV of 5-Year Forecast FCFF", dcf_res["sum_pv_forecast_cashflows_cr"], "#,##0"),
        ("Terminal Growth Rate (g)", dcf_res["terminal_growth_pct"] / 100.0, "0.00%"),
        ("Terminal Value (at FY29E)", dcf_res["terminal_value_cr"], "#,##0"),
        ("Present Value of Terminal Value", dcf_res["pv_terminal_value_cr"], "#,##0"),
        ("Terminal Value Share of Enterprise Value", dcf_res["terminal_value_share_pct"] / 100.0, "0.0%"),
        ("Implied Enterprise Value (EV)", dcf_res["enterprise_value_cr"], "#,##0"),
        ("(+) Cash & Liquid Investments (FY24)", dcf_res["cash_equivalents_cr"], "#,##0"),
        ("(-) Debt & Lease Liabilities (FY24)", dcf_res["debt_lease_liabilities_cr"], "#,##0"),
        ("Net Cash Added", dcf_res["net_cash_cr"], "#,##0"),
        ("Implied Equity Value", dcf_res["implied_equity_value_cr"], "#,##0"),
        ("Shares Outstanding (Crores)", dcf_res["shares_outstanding_cr"], "#,##0.00"),
        ("Implied Value Per Share (INR)", dcf_res["implied_value_per_share_inr"], "₹#,##0.00"),
        ("Current Market Price (CMP Ref)", 3850.00, "₹#,##0.00"),
    ]

    r = 30
    for b_param, b_val, b_fmt in bridge_data:
        apply_data_cell(ws_dcf.cell(row=r, column=1), b_param, bold="Implied" in b_param, align="left")
        b_cell = ws_dcf.cell(row=r, column=2)
        apply_data_cell(b_cell, b_val, num_format=b_fmt, bold="Implied" in b_param, bg_color=LIGHT_BLUE_FILL if "Implied" in b_param else None)
        r += 1

    # Block 4: Sensitivity Table
    ws_dcf["D3"] = "DCF SENSITIVITY ANALYSIS (IMPLIED SHARE PRICE, ₹)"
    ws_dcf["D3"].font = Font(name="Calibri", size=11, bold=True, color=NAVY_HEADER)

    apply_header_style(ws_dcf.cell(row=4, column=4), "WACC \\ Growth", bg_color=NAVY_HEADER)
    for c_i, col_label in enumerate(sens_df.columns, 5):
        apply_header_style(ws_dcf.cell(row=4, column=c_i), col_label, bg_color=NAVY_SUBHEADER)

    for r_i, (row_label, row_data) in enumerate(sens_df.iterrows(), 5):
        apply_data_cell(ws_dcf.cell(row=r_i, column=4), row_label, bold=True, align="center", bg_color=LIGHT_BLUE_FILL)
        for c_i, val in enumerate(row_data, 5):
            apply_data_cell(ws_dcf.cell(row=r_i, column=c_i), val, num_format="₹#,##0", bold=True)

    autofit_columns(ws_dcf)

    wb.save(output_path)
    return output_path


if __name__ == "__main__":
    path = generate_excel_model()
    print(f"Financial Model successfully generated at: {path}")
