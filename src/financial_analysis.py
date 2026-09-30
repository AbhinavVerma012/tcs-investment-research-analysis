"""
=============================================================================
Financial Statement & Ratio Analysis Engine
Institutional Equity Research Financial Analysis
=============================================================================
Computes key financial performance indicators, growth trajectories, profitability
margins, capital return metrics (ROE, ROA, ROCE), leverage, cash flow conversion,
and a 3-stage DuPont decomposition for TCS.
"""

from typing import Dict, Any
import pandas as pd
import numpy as np


def calculate_cagr(start_val: float, end_val: float, periods: int) -> float:
    """Calculates Compound Annual Growth Rate (CAGR)."""
    if start_val <= 0 or periods <= 0:
        return 0.0
    return ((end_val / start_val) ** (1.0 / periods) - 1.0) * 100.0


def compute_financial_ratios(df: pd.DataFrame) -> pd.DataFrame:
    """
    Computes key financial ratios from the transposed historical financial statements.
    
    Args:
        df (pd.DataFrame): Transposed historical statements with fiscal years as rows.
        
    Returns:
        pd.DataFrame: Comprehensive ratio table with years as rows.
    """
    ratios = pd.DataFrame(index=df.index)

    # 1. Growth Ratios (YoY %)
    ratios["Revenue_Growth_YoY_pct"] = df["Revenue from Operations"].pct_change() * 100.0
    ratios["EBITDA_Growth_YoY_pct"] = df["EBITDA"].pct_change() * 100.0
    ratios["Net_Profit_Growth_YoY_pct"] = df["Net Profit (PAT)"].pct_change() * 100.0
    ratios["EPS_Growth_YoY_pct"] = df["Diluted EPS (INR)"].pct_change() * 100.0

    # 2. Profitability Margins (%)
    ratios["EBITDA_Margin_pct"] = (df["EBITDA"] / df["Revenue from Operations"]) * 100.0
    ratios["EBIT_Margin_pct"] = (df["EBIT (Operating Profit)"] / df["Revenue from Operations"]) * 100.0
    ratios["Net_Profit_Margin_pct"] = (df["Net Profit (PAT)"] / df["Revenue from Operations"]) * 100.0

    # 3. Capital Efficiency & Return Ratios (%)
    # Return on Equity (ROE) = Net Profit / Total Equity
    ratios["ROE_pct"] = (df["Net Profit (PAT)"] / df["Total Shareholders Equity"]) * 100.0

    # Return on Assets (ROA) = Net Profit / Total Assets
    ratios["ROA_pct"] = (df["Net Profit (PAT)"] / df["Total Assets"]) * 100.0

    # Return on Capital Employed (ROCE) = EBIT / (Total Equity + Total Debt)
    capital_employed = df["Total Shareholders Equity"] + df["Total Debt (inc. Leases)"]
    ratios["ROCE_pct"] = (df["EBIT (Operating Profit)"] / capital_employed) * 100.0

    # 4. Solvency & Liquidity Ratios
    # Debt-to-Equity (Leases included as debt under Ind AS 116 / IFRS 16)
    ratios["Debt_to_Equity_Ratio"] = df["Total Debt (inc. Leases)"] / df["Total Shareholders Equity"]
    
    # Traditional Bank Debt to Equity (Zero bank debt)
    ratios["Bank_Debt_to_Equity_Ratio"] = df["Total Borrowings (Bank Debt)"] / df["Total Shareholders Equity"]

    # Net Debt = Total Debt - Cash & Liquid Investments
    ratios["Net_Debt_INR_Cr"] = df["Total Debt (inc. Leases)"] - df["Cash & Liquid Investments"]

    # 5. Cash Flow & Quality of Earnings Ratios
    ratios["OCF_to_Net_Profit_Conversion_pct"] = (df["Cash Flow from Operations (OCF)"] / df["Net Profit (PAT)"]) * 100.0
    ratios["FCF_to_Net_Profit_Conversion_pct"] = (df["Free Cash Flow (FCF)"] / df["Net Profit (PAT)"]) * 100.0
    ratios["CapEx_to_Revenue_pct"] = (df["Capital Expenditures (CapEx)"] / df["Revenue from Operations"]) * 100.0

    # 6. DuPont Analysis (3-Stage Decomposition):
    # ROE = Net Profit Margin * Asset Turnover * Financial Leverage
    # Net Profit Margin = Net Profit / Revenue
    # Asset Turnover = Revenue / Total Assets
    # Financial Leverage (Equity Multiplier) = Total Assets / Total Equity
    ratios["DuPont_Net_Margin_pct"] = ratios["Net_Profit_Margin_pct"]
    ratios["DuPont_Asset_Turnover_x"] = df["Revenue from Operations"] / df["Total Assets"]
    ratios["DuPont_Equity_Multiplier_x"] = df["Total Assets"] / df["Total Shareholders Equity"]
    ratios["DuPont_Reconstructed_ROE_pct"] = (
        (ratios["DuPont_Net_Margin_pct"] / 100.0)
        * ratios["DuPont_Asset_Turnover_x"]
        * ratios["DuPont_Equity_Multiplier_x"]
    ) * 100.0

    return ratios


def generate_executive_financial_summary(df: pd.DataFrame, ratios: pd.DataFrame) -> Dict[str, Any]:
    """
    Summarizes high-level corporate highlights, 3-year CAGRs, and current FY24 operational status.
    """
    fy21_rev = df.loc["fy21", "Revenue from Operations"]
    fy24_rev = df.loc["fy24", "Revenue from Operations"]
    rev_cagr_3yr = calculate_cagr(fy21_rev, fy24_rev, 3)

    fy21_pat = df.loc["fy21", "Net Profit (PAT)"]
    fy24_pat = df.loc["fy24", "Net Profit (PAT)"]
    pat_cagr_3yr = calculate_cagr(fy21_pat, fy24_pat, 3)

    fy21_eps = df.loc["fy21", "Diluted EPS (INR)"]
    fy24_eps = df.loc["fy24", "Diluted EPS (INR)"]
    eps_cagr_3yr = calculate_cagr(fy21_eps, fy24_eps, 3)

    fy24_fcf = df.loc["fy24", "Free Cash Flow (FCF)"]
    fy24_ocf = df.loc["fy24", "Cash Flow from Operations (OCF)"]
    fy24_cash = df.loc["fy24", "Cash & Liquid Investments"]
    fy24_net_cash = fy24_cash - df.loc["fy24", "Total Debt (inc. Leases)"]

    return {
        "revenue_fy24_inr_cr": fy24_rev,
        "revenue_3yr_cagr_pct": round(rev_cagr_3yr, 2),
        "pat_fy24_inr_cr": fy24_pat,
        "pat_3yr_cagr_pct": round(pat_cagr_3yr, 2),
        "eps_fy24_inr": fy24_eps,
        "eps_3yr_cagr_pct": round(eps_cagr_3yr, 2),
        "ebit_margin_fy24_pct": round(ratios.loc["fy24", "EBIT_Margin_pct"], 2),
        "net_margin_fy24_pct": round(ratios.loc["fy24", "Net_Profit_Margin_pct"], 2),
        "roe_fy24_pct": round(ratios.loc["fy24", "ROE_pct"], 2),
        "roce_fy24_pct": round(ratios.loc["fy24", "ROCE_pct"], 2),
        "ocf_fy24_inr_cr": fy24_ocf,
        "fcf_fy24_inr_cr": fy24_fcf,
        "fcf_conversion_fy24_pct": round(ratios.loc["fy24", "FCF_to_Net_Profit_Conversion_pct"], 2),
        "net_cash_fy24_inr_cr": round(fy24_net_cash, 2),
        "debt_to_equity_fy24": round(ratios.loc["fy24", "Debt_to_Equity_Ratio"], 2),
    }


if __name__ == "__main__":
    from data_loader import load_tcs_historical
    tcs_data = load_tcs_historical()
    ratios_data = compute_financial_ratios(tcs_data)
    summary = generate_executive_financial_summary(tcs_data, ratios_data)

    print("=== TCS 4-YEAR FINANCIAL RATIOS ===")
    print(ratios_data[["Revenue_Growth_YoY_pct", "EBIT_Margin_pct", "Net_Profit_Margin_pct", "ROE_pct", "ROCE_pct", "Debt_to_Equity_Ratio"]])
    print("\n=== EXECUTIVE FINANCIAL SUMMARY ===")
    for k, v in summary.items():
        print(f"  {k}: {v}")
