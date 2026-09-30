#!/usr/bin/env python3
"""
=============================================================================
MASTER PIPELINE: TCS Investment Research & Financial Analysis Report
Institutional Equity Research & Financial Analysis Pipeline
=============================================================================
Author: Abhinav Verma (B.Tech CSE -> Quantitative Finance & Equity Research)
Focus: Fundamental Financial Analysis & Valuation Modeling
Company: Tata Consultancy Services Ltd (NSE: TCS.NS / BSE: 532540)
=============================================================================

This master script coordinates the end-to-end investment research pipeline:
1. Data Ingestion & Integrity Validation
2. Comprehensive Financial Statement & 4-Year Ratio Analysis
3. DuPont 3-Stage Return on Equity Decomposition
4. Peer Benchmarking (TCS vs Infosys vs HCLTech)
5. Illustrative Discounted Cash Flow (DCF) & CAPM/WACC Modeling
6. 2D Valuation Sensitivity Matrix (WACC vs Terminal Growth)
7. Institutional Matplotlib Chart Rendering (Publication Quality)
8. Multi-Tab Financial Model Excel Workbook (.xlsx) Generation
9. HTML & PDF Equity Research Report Generation
"""

import os
import sys
import time

# Ensure project root is in sys.path
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.data_loader import load_all_datasets
from src.financial_analysis import compute_financial_ratios, generate_executive_financial_summary
from src.valuation_model import TCSValuationModel
from src.visualizer import generate_all_charts
from generate_excel_model import generate_excel_model
from generate_report import build_html_report, convert_html_to_pdf


def print_banner():
    banner = """
========================================================================================
     INSTITUTIONAL EQUITY RESEARCH & FINANCIAL ANALYSIS PIPELINE
     TATA CONSULTANCY SERVICES LTD (NSE: TCS.NS) | SECTOR: GLOBAL IT SERVICES
========================================================================================
    """
    print(banner)


def main():
    start_time = time.time()
    print_banner()

    # -------------------------------------------------------------------------
    # STEP 1: INGESTION & DATA INTEGRITY
    # -------------------------------------------------------------------------
    print("[1/6] Ingesting and validating audited financial statements & peer data...")
    datasets = load_all_datasets()
    tcs_df = datasets["tcs_historical"]
    peer_df = datasets["peer_comparison"]
    print("      ✓ Loaded 4-year historical statements (FY21 - FY24)")
    print("      ✓ Loaded Tier-1 peer dataset (TCS, Infosys, HCLTech)")
    print("      ✓ Loaded segment breakdowns (Industry Verticals & Geographies)")

    # -------------------------------------------------------------------------
    # STEP 2: FINANCIAL STATEMENT & RATIO ENGINE
    # -------------------------------------------------------------------------
    print("\n[2/6] Executing Financial Statement & Ratio Analysis Engine...")
    ratios_df = compute_financial_ratios(tcs_df)
    exec_summary = generate_executive_financial_summary(tcs_df, ratios_df)

    print("\n      --- Key Financial Performance Metrics ---")
    print(f"      • FY24 Revenue:           ₹{exec_summary['revenue_fy24_inr_cr']:,.0f} Cr (3-Yr CAGR: +{exec_summary['revenue_3yr_cagr_pct']}%)")
    print(f"      • FY24 Net Profit (PAT):  ₹{exec_summary['pat_fy24_inr_cr']:,.0f} Cr (3-Yr CAGR: +{exec_summary['pat_3yr_cagr_pct']}%)")
    print(f"      • FY24 Operating EBIT:    ₹{tcs_df.loc['fy24', 'EBIT (Operating Profit)']:,.0f} Cr (Margin: {exec_summary['ebit_margin_fy24_pct']}%)")
    print(f"      • FY24 Return on Equity:  {exec_summary['roe_fy24_pct']}% (Capital Efficiency Leader)")
    print(f"      • FY24 Free Cash Flow:    ₹{exec_summary['fcf_fy24_inr_cr']:,.0f} Cr (FCF/PAT: {exec_summary['fcf_conversion_fy24_pct']}%)")
    print(f"      • Net Cash on Balance:    ₹{exec_summary['net_cash_fy24_inr_cr']:,.0f} Cr (Zero Bank Debt)")

    print("\n      --- DuPont 3-Stage ROE Decomposition (FY24) ---")
    print(f"      • Net Profit Margin:      {ratios_df.loc['fy24', 'DuPont_Net_Margin_pct']:.2f}%")
    print(f"      • Asset Turnover:         {ratios_df.loc['fy24', 'DuPont_Asset_Turnover_x']:.2f}x")
    print(f"      • Financial Leverage:     {ratios_df.loc['fy24', 'DuPont_Equity_Multiplier_x']:.2f}x")
    print(f"      • Reconstructed ROE:      {ratios_df.loc['fy24', 'DuPont_Reconstructed_ROE_pct']:.2f}%")

    # -------------------------------------------------------------------------
    # STEP 3: VALUATION & DCF SENSITIVITY ENGINE
    # -------------------------------------------------------------------------
    print("\n[3/6] Running DCF Valuation & CAPM/WACC Modeling...")
    val_model = TCSValuationModel()
    wacc_details = val_model.calculate_wacc()
    dcf_results = val_model.run_dcf()
    sens_matrix = val_model.generate_sensitivity_matrix()

    print(f"      • Cost of Equity (CAPM):  {wacc_details['cost_of_equity_pct']:.2f}% (Rf: {wacc_details['risk_free_rate_pct']}%, ERP: {wacc_details['equity_risk_premium_pct']}%, Beta: {wacc_details['beta']})")
    print(f"      • Blended WACC:           {dcf_results['wacc_pct']:.2f}%")
    print(f"      • Terminal Growth Rate:   {dcf_results['terminal_growth_pct']:.2f}%")
    print(f"      • Cumulative PV (5-Yr):   ₹{dcf_results['sum_pv_forecast_cashflows_cr']:,.2f} Cr")
    print(f"      • PV of Terminal Value:   ₹{dcf_results['pv_terminal_value_cr']:,.2f} Cr ({dcf_results['terminal_value_share_pct']}% of EV)")
    print(f"      • Net Cash Added:         ₹{dcf_results['net_cash_cr']:,.2f} Cr")
    print(f"      • Implied Base Fair Value: ₹{dcf_results['implied_value_per_share_inr']:,.2f} / share (Ref CMP: ₹3,850.00)")

    # -------------------------------------------------------------------------
    # STEP 4: VISUALIZATION GENERATION
    # -------------------------------------------------------------------------
    print("\n[4/6] Rendering Institutional Equity Research Charts...")
    charts = generate_all_charts(tcs_df, ratios_df, peer_df, sens_matrix)
    for name, cpath in charts.items():
        print(f"      ✓ Rendered {name:16} -> {os.path.relpath(cpath, PROJECT_ROOT)}")

    # -------------------------------------------------------------------------
    # STEP 5: EXCEL FINANCIAL MODEL GENERATION
    # -------------------------------------------------------------------------
    print("\n[5/6] Building Multi-Tab Excel Financial Model (.xlsx)...")
    excel_path = generate_excel_model()
    print(f"      ✓ Excel Workbook built   -> {os.path.relpath(excel_path, PROJECT_ROOT)}")

    # -------------------------------------------------------------------------
    # STEP 6: REPORT GENERATION (HTML & PDF)
    # -------------------------------------------------------------------------
    print("\n[6/6] Compiling Publication Equity Research Reports (HTML & PDF)...")
    html_report = build_html_report()
    print(f"      ✓ HTML Research Report   -> {os.path.relpath(html_report, PROJECT_ROOT)}")

    pdf_report = convert_html_to_pdf(html_report)
    if pdf_report and os.path.exists(pdf_report):
        print(f"      ✓ PDF Research Report    -> {os.path.relpath(pdf_report, PROJECT_ROOT)}")
    else:
        print("      ! PDF generation notice: Open the HTML report in Google Chrome and select 'Print to PDF'.")

    elapsed = time.time() - start_time
    print(f"\n========================================================================================")
    print(f"  PIPELINE EXECUTION COMPLETE IN {elapsed:.2f} SECONDS")
    print(f"========================================================================================")
    print("  Deliverable Files Summary:")
    print("   • Master Markdown Report : REPORT.md")
    print("   • Formatted HTML Report  : output/reports/TCS_Equity_Research_Report.html")
    print("   • Publication PDF Report : output/reports/TCS_Equity_Research_Report.pdf")
    print("   • Multi-Tab Excel Model  : data/tcs_financial_model.xlsx")
    print("   • High-Res Charts (6x)   : output/charts/*.png")
    print("========================================================================================\n")


if __name__ == "__main__":
    main()
