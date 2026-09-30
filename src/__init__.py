"""
TCS Equity Research & Financial Analysis Package
Institutional Equity Research Analytical Engine
"""

from .data_loader import load_tcs_historical, load_peer_comparison, load_segment_breakdown
from .financial_analysis import compute_financial_ratios, generate_executive_financial_summary
from .valuation_model import TCSValuationModel
from .visualizer import generate_all_charts
