"""
=============================================================================
Data Loader Module: TCS & Indian IT Peer Data Ingestion & Validation
Institutional Equity Research Financial Pipeline
=============================================================================
This module provides clean and robust functions to load, validate,
and format historical financial statements and competitor benchmarks.
"""

import os
from typing import Dict, Tuple
import pandas as pd


def get_data_dir() -> str:
    """Return the absolute path to the data directory."""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.abspath(os.path.join(current_dir, "..", "data"))


def load_tcs_historical() -> pd.DataFrame:
    """
    Loads historical 4-year financial data for TCS (FY21-FY24).
    
    Returns:
        pd.DataFrame: Transposed financial statement with years as index
                      and financial line items as numeric columns.
    """
    data_path = os.path.join(get_data_dir(), "tcs_financials_historical.csv")
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"Data file not found at: {data_path}")

    # Read CSV
    raw_df = pd.read_csv(data_path)
    raw_df["metric"] = raw_df["metric"].str.strip()

    # Set metric as index and transpose so years (FY21, FY22, FY23, FY24) become rows
    df = raw_df.set_index("metric").T
    df.index.name = "fiscal_year"

    # Ensure all numerical values are float
    for col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # Perform basic data integrity validations
    assert not df.empty, "Historical dataframe is empty!"
    assert "Revenue from Operations" in df.columns, "Revenue metric missing from historical data"
    assert "Net Profit (PAT)" in df.columns, "PAT metric missing from historical data"

    return df


def load_peer_comparison() -> pd.DataFrame:
    """
    Loads peer financial and operational metrics for TCS, Infosys, and HCLTech (FY24).
    
    Returns:
        pd.DataFrame: Cleaned peer comparison DataFrame with company names as index.
    """
    data_path = os.path.join(get_data_dir(), "peer_comparison_fy24.csv")
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"Peer comparison file not found at: {data_path}")

    peer_df = pd.read_csv(data_path)
    peer_df["company"] = peer_df["company"].str.strip()
    return peer_df


def load_segment_breakdown() -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Loads TCS FY24 revenue breakdown across industry verticals and geographies.
    
    Returns:
        Tuple[pd.DataFrame, pd.DataFrame]: (verticals_df, geography_df)
    """
    data_path = os.path.join(get_data_dir(), "segment_breakdown_fy24.csv")
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"Segment data file not found at: {data_path}")

    seg_df = pd.read_csv(data_path)
    verticals = seg_df[seg_df["segment_type"] == "Vertical"].copy()
    geography = seg_df[seg_df["segment_type"] == "Geography"].copy()

    return verticals, geography


def load_all_datasets() -> Dict[str, pd.DataFrame]:
    """
    Convenience function to load all relevant datasets into a dictionary.
    """
    tcs_df = load_tcs_historical()
    peer_df = load_peer_comparison()
    vert_df, geo_df = load_segment_breakdown()

    return {
        "tcs_historical": tcs_df,
        "peer_comparison": peer_df,
        "verticals": vert_df,
        "geography": geo_df,
    }


if __name__ == "__main__":
    data = load_all_datasets()
    print("Successfully loaded datasets:")
    print("\n--- TCS Historical Financials (Head) ---")
    print(data["tcs_historical"][["Revenue from Operations", "EBITDA", "Net Profit (PAT)"]])
    print("\n--- Peer Comparison ---")
    print(data["peer_comparison"][["company", "revenue_cr", "ebit_margin_pct", "roe_pct", "pe_ratio"]])
