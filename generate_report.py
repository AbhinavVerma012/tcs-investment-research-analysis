"""
=============================================================================
Equity Research Report Generator: Institutional HTML & PDF Builder
Institutional Equity Research Report Layout
=============================================================================
Compiles the complete 10-section equity research report into:
1. output/reports/TCS_Equity_Research_Report.html (Self-contained, interactive,
   with base64 embedded charts and printable CSS).
2. output/reports/TCS_Equity_Research_Report.pdf (Print-to-PDF generated via
   headless Google Chrome).
"""

import os
import sys
import base64
import subprocess
from typing import Dict

# Ensure project root is in path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from src.valuation_model import TCSValuationModel


def image_to_base64(image_path: str) -> str:
    """Converts a PNG image to a base64 data URI for portable offline viewing."""
    if not os.path.exists(image_path):
        return ""
    with open(image_path, "rb") as img_file:
        b64_str = base64.b64encode(img_file.read()).decode("utf-8")
    return f"data:image/png;base64,{b64_str}"


def build_html_report(output_dir: str = None) -> str:
    """Compiles the HTML report with embedded styles and figures."""
    charts_dir = os.path.join(project_root, "output", "charts")

    if output_dir is None:
        output_dir = os.path.join(project_root, "output", "reports")
    os.makedirs(output_dir, exist_ok=True)

    html_path = os.path.join(output_dir, "TCS_Equity_Research_Report.html")

    # Encode all 6 charts to base64
    img_rev = image_to_base64(os.path.join(charts_dir, "revenue_growth_trend.png"))
    img_prof = image_to_base64(os.path.join(charts_dir, "profitability_breakdown.png"))
    img_marg = image_to_base64(os.path.join(charts_dir, "operating_margin_trends.png"))
    img_peer = image_to_base64(os.path.join(charts_dir, "competitor_comparison.png"))
    img_cash = image_to_base64(os.path.join(charts_dir, "cashflow_conversion_capex.png"))
    img_sens = image_to_base64(os.path.join(charts_dir, "dcf_sensitivity_matrix.png"))

    # Dynamically obtain valuation metrics from valuation engine
    val_model = TCSValuationModel()
    dcf_res = val_model.run_dcf()
    dcf_val = dcf_res["implied_value_per_share_inr"]  # 2113.89
    wacc_pct = dcf_res["wacc_pct"]                    # 11.98
    tg_pct = dcf_res["terminal_growth_pct"]          # 4.25
    sum_pv_fcff = dcf_res["sum_pv_forecast_cashflows_cr"]  # 216813.60
    pv_tv = dcf_res["pv_terminal_value_cr"]          # 507469.19
    tv_share_pct = dcf_res["terminal_value_share_pct"]  # 70.07
    ev_cr = dcf_res["enterprise_value_cr"]            # 724282.79
    net_cash_cr = dcf_res["net_cash_cr"]              # 40522.00
    equity_val_cr = dcf_res["implied_equity_value_cr"] # 764804.79
    shares_cr = dcf_res["shares_outstanding_cr"]      # 361.80

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>TCS Equity Research Report | Fundamental Analysis & Valuation</title>
<style>
  :root {{
    --gs-navy: #0A2540;
    --gs-navy-light: #1E3A8A;
    --gs-blue: #2563EB;
    --gs-gold: #D97706;
    --gs-gold-light: #FEF3C7;
    --gs-text: #0F172A;
    --gs-muted: #475569;
    --gs-border: #CBD5E1;
    --gs-card: #F8FAFC;
    --gs-green: #059669;
    --gs-green-light: #ECFDF5;
  }}

  * {{
    box-sizing: border-box;
    margin: 0;
    padding: 0;
  }}

  body {{
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    color: var(--gs-text);
    background-color: #F1F5F9;
    line-height: 1.55;
    font-size: 13.5px;
  }}

  .document-container {{
    max-width: 1040px;
    margin: 24px auto;
    background: #FFFFFF;
    box-shadow: 0 4px 20px rgba(0,0,0,0.08);
    border-radius: 4px;
    overflow: hidden;
  }}

  /* HEADER BLOCK */
  .report-header {{
    background: linear-gradient(135deg, var(--gs-navy) 0%, #112233 100%);
    color: #FFFFFF;
    padding: 28px 36px;
    border-bottom: 4px solid var(--gs-gold);
  }}

  .header-top-row {{
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 12px;
  }}

  .badge-category {{
    background: rgba(255,255,255,0.15);
    color: #E2E8F0;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 1px;
    text-transform: uppercase;
    padding: 4px 10px;
    border-radius: 3px;
    display: inline-block;
  }}

  .header-date {{
    font-size: 12px;
    color: #94A3B8;
  }}

  .report-title {{
    font-size: 26px;
    font-weight: 800;
    letter-spacing: -0.5px;
    margin-bottom: 4px;
    color: #FFFFFF;
  }}

  .report-subtitle {{
    font-size: 14px;
    color: #CBD5E1;
    font-weight: 400;
    margin-bottom: 18px;
  }}

  /* METRICS STRIP */
  .metrics-strip {{
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 12px;
    background: rgba(255, 255, 255, 0.08);
    padding: 14px 16px;
    border-radius: 6px;
    border: 1px solid rgba(255,255,255,0.12);
  }}

  .metric-item {{
    border-right: 1px solid rgba(255,255,255,0.12);
    padding-right: 10px;
  }}
  .metric-item:last-child {{
    border-right: none;
  }}

  .metric-label {{
    font-size: 10px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    color: #94A3B8;
    margin-bottom: 2px;
  }}

  .metric-value {{
    font-size: 17px;
    font-weight: 800;
    color: #FFFFFF;
  }}

  .metric-sub {{
    font-size: 11px;
    color: #38BDF8;
    font-weight: 500;
  }}

  /* MAIN CONTENT AREA */
  .content-body {{
    padding: 36px 40px;
  }}

  .section-block {{
    margin-bottom: 32px;
  }}

  h2 {{
    font-size: 17px;
    font-weight: 800;
    color: var(--gs-navy);
    text-transform: uppercase;
    letter-spacing: 0.4px;
    border-bottom: 2px solid var(--gs-navy);
    padding-bottom: 6px;
    margin-bottom: 14px;
  }}

  h3 {{
    font-size: 14.5px;
    font-weight: 700;
    color: var(--gs-navy-light);
    margin: 16px 0 8px 0;
  }}

  p {{
    margin-bottom: 12px;
    color: var(--gs-text);
    text-align: justify;
  }}

  ul, ol {{
    margin-left: 20px;
    margin-bottom: 12px;
  }}

  li {{
    margin-bottom: 5px;
  }}

  /* CALLOUT BOXES */
  .callout-box {{
    background-color: var(--gs-card);
    border-left: 4px solid var(--gs-navy-light);
    padding: 14px 18px;
    margin: 14px 0;
    border-radius: 0 4px 4px 0;
  }}

  .callout-box.gold {{
    border-left-color: var(--gs-gold);
    background-color: #FFFDF7;
  }}

  .callout-box.green {{
    border-left-color: var(--gs-green);
    background-color: var(--gs-green-light);
  }}

  .callout-title {{
    font-weight: 700;
    font-size: 12.5px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-bottom: 4px;
    color: var(--gs-navy);
  }}

  /* TABLES */
  table.fin-table {{
    width: 100%;
    border-collapse: collapse;
    margin: 14px 0 20px 0;
    font-size: 12px;
  }}

  table.fin-table th {{
    background-color: var(--gs-navy);
    color: #FFFFFF;
    font-weight: 700;
    text-align: right;
    padding: 8px 10px;
    border: 1px solid var(--gs-navy);
  }}

  table.fin-table th:first-child {{
    text-align: left;
  }}

  table.fin-table td {{
    padding: 7px 10px;
    border: 1px solid var(--gs-border);
    text-align: right;
  }}

  table.fin-table td:first-child {{
    text-align: left;
    font-weight: 600;
  }}

  table.fin-table tr:nth-child(even) {{
    background-color: var(--gs-card);
  }}

  table.fin-table tr.total-row td {{
    font-weight: 700;
    background-color: #E2E8F0;
    border-top: 2px solid var(--gs-navy);
  }}

  /* CHART EXHIBIT STYLES */
  .chart-card {{
    background: #FFFFFF;
    border: 1px solid var(--gs-border);
    border-radius: 6px;
    padding: 16px;
    margin: 18px 0;
    box-shadow: 0 2px 6px rgba(0,0,0,0.04);
  }}

  .chart-card img {{
    width: 100%;
    height: auto;
    display: block;
    border-radius: 4px;
  }}

  .chart-caption {{
    font-size: 11px;
    color: var(--gs-muted);
    margin-top: 8px;
    font-style: italic;
    border-top: 1px dashed var(--gs-border);
    padding-top: 6px;
  }}

  /* GRID TWO COLUMN */
  .grid-two {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 16px;
  }}

  /* FOOTER */
  .report-footer {{
    background: #0F172A;
    color: #94A3B8;
    padding: 24px 40px;
    font-size: 11px;
    line-height: 1.5;
    border-top: 3px solid var(--gs-gold);
  }}

  .report-footer p {{
    margin-bottom: 8px;
    color: #94A3B8;
  }}

  /* PRINT MEDIA QUERIES FOR PDF EXPORT */
  @media print {{
    body {{
      background: #FFFFFF;
      font-size: 11.5px;
    }}
    .document-container {{
      box-shadow: none;
      margin: 0;
      width: 100%;
      max-width: 100%;
    }}
    .content-body {{
      padding: 16px 20px;
    }}
    .page-break {{
      page-break-before: always;
    }}
    .chart-card {{
      box-shadow: none;
      border: 1px solid #CBD5E1;
      page-break-inside: avoid;
    }}
    table.fin-table {{
      page-break-inside: avoid;
    }}
  }}
</style>
</head>
<body>

<div class="document-container">

  <!-- INSTITUTIONAL HEADER -->
  <header class="report-header">
    <div class="header-top-row">
      <span class="badge-category">Equity Research &bull; Initiation of Coverage</span>
      <span class="header-date">Institutional Equity Research Format &bull; Consolidated Audited Data</span>
    </div>
    <h1 class="report-title">Tata Consultancy Services Ltd. (TCS)</h1>
    <div class="report-subtitle">
      NSE: <strong>TCS.NS</strong> &bull; BSE: <strong>532540</strong> &bull; Sector: <strong>Global IT Services & Consulting</strong> &bull; Report Type: <strong>Fundamental & Valuation Analysis</strong>
    </div>

    <div class="metrics-strip">
      <div class="metric-item">
        <div class="metric-label">Current Market Price</div>
        <div class="metric-value">₹3,850.00</div>
        <div class="metric-sub">52-Wk: ₹3,313 - ₹4,585</div>
      </div>
      <div class="metric-item">
        <div class="metric-label">Market Capitalization</div>
        <div class="metric-value">₹13.90 Lakh Cr</div>
        <div class="metric-sub">~$168 Billion USD</div>
      </div>
      <div class="metric-item">
        <div class="metric-label">Valuation Multiples</div>
        <div class="metric-value">30.3x P/E</div>
        <div class="metric-sub">20.2x EV/EBITDA</div>
      </div>
      <div class="metric-item">
        <div class="metric-label">Capital Productivity</div>
        <div class="metric-value">51.1% ROE</div>
        <div class="metric-sub">Net Cash: ₹40,522 Cr</div>
      </div>
    </div>
  </header>

  <!-- BODY CONTENT -->
  <main class="content-body">

    <!-- 1. EXECUTIVE SUMMARY -->
    <section class="section-block">
      <h2>1. Executive Summary</h2>
      <p>
        Tata Consultancy Services (TCS) is the benchmark flagship enterprise of the Tata Group and India’s premier information technology exporter. Employing over 601,000 technology professionals across 55 countries, TCS operates an integrated global delivery model supporting mission-critical digital enterprise transformations for Global Fortune 500 corporations.
      </p>

      <div class="callout-box gold">
        <div class="callout-title">Core Research Findings & Analytical Summary</div>
        <ul>
          <li><strong>Structural Top-Line Resilience:</strong> Consolidated revenue grew from ₹164,177 Cr in FY21 to ₹240,893 Cr in FY24 (13.63% CAGR), cementing its position as India's scale leader.</li>
          <li><strong>Defensible Operating Margins:</strong> FY24 EBIT operating margin reached 25.98%, representing a +390 bps advantage over Infosys (20.7%) and +640 bps over HCLTech (18.2%), driven by low employee attrition (12.5%) and delivery discipline.</li>
          <li><strong>Exceptional Free Cash Flow:</strong> Generated ₹48,908 Cr in Operating Cash Flow and ₹45,108 Cr in Free Cash Flow in FY24, converting 97.8% of reported Net Profit into distributable cash.</li>
          <li><strong>Illustrative DCF Valuation:</strong> Using an 11.98% WACC and a 4.25% terminal growth rate, our conservative 5-year illustrative DCF framework indicates a baseline intrinsic value of <strong>₹{dcf_val:,.2f} per share</strong>. The prevailing market price (₹3,850.00, 30.3x P/E) reflects a substantial franchise quality premium where investors price in extended high-return cash flow compounding beyond standard 5-year forecast horizons.</li>
        </ul>
      </div>

      <table class="fin-table">
        <thead>
          <tr>
            <th>Key Metric (₹ Cr)</th>
            <th>FY21</th>
            <th>FY22</th>
            <th>FY23</th>
            <th>FY24</th>
            <th>3-Yr CAGR</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>Revenue from Operations</td>
            <td>164,177</td>
            <td>191,754</td>
            <td>225,458</td>
            <td>240,893</td>
            <td>+13.6%</td>
          </tr>
          <tr>
            <td>EBITDA</td>
            <td>45,710</td>
            <td>53,731</td>
            <td>63,120</td>
            <td>67,571</td>
            <td>+13.9%</td>
          </tr>
          <tr>
            <td>EBIT (Operating Profit)</td>
            <td>41,645</td>
            <td>49,131</td>
            <td>58,098</td>
            <td>62,586</td>
            <td>+14.5%</td>
          </tr>
          <tr class="total-row">
            <td>Net Profit (PAT)</td>
            <td>32,430</td>
            <td>38,327</td>
            <td>42,147</td>
            <td>46,099</td>
            <td>+12.4%</td>
          </tr>
          <tr>
            <td>Diluted EPS (₹)</td>
            <td>₹86.80</td>
            <td>₹104.75</td>
            <td>₹115.19</td>
            <td>₹126.88</td>
            <td>+13.5%</td>
          </tr>
          <tr>
            <td>Free Cash Flow (FCF)</td>
            <td>36,784</td>
            <td>38,765</td>
            <td>40,838</td>
            <td>45,108</td>
            <td>+7.0%</td>
          </tr>
        </tbody>
      </table>
    </section>

    <!-- 2. COMPANY ANALYSIS -->
    <section class="section-block">
      <h2>2. Company Analysis & Operational Profile</h2>
      <p>
        TCS deploys its proprietary <strong>Global Network Delivery Model (GNDM™)</strong>, orchestrating projects through seamless collaboration across onshore strategic hubs and state-of-the-art offshore technology campuses.
      </p>

      <div class="grid-two">
        <div class="callout-box">
          <div class="callout-title">Revenue by Industry Vertical (FY24)</div>
          <ul>
            <li><strong>BFSI:</strong> 32.0% (Core banking, risk, insurance platforms)</li>
            <li><strong>Consumer Business:</strong> 15.7% (Retail, CPG, travel)</li>
            <li><strong>Life Sciences & Healthcare:</strong> 10.9% (Clinical analytics)</li>
            <li><strong>Manufacturing:</strong> 8.7% (IoT, smart factory)</li>
            <li><strong>Technology & Services:</strong> 8.7% (Engineering)</li>
            <li><strong>Communication & Media:</strong> 6.6% (5G operations)</li>
            <li><strong>Regional & Others:</strong> 17.4%</li>
          </ul>
        </div>
        <div class="callout-box">
          <div class="callout-title">Revenue by Geography (FY24)</div>
          <ul>
            <li><strong>North America:</strong> 50.1% (Primary anchor)</li>
            <li><strong>United Kingdom:</strong> 16.6% (Public sector & finance)</li>
            <li><strong>Continental Europe:</strong> 15.2% (SAP modernization)</li>
            <li><strong>Asia Pacific:</strong> 7.8% (Singapore, Japan, ANZ)</li>
            <li><strong>India:</strong> 5.5% (Mission-critical e-governance)</li>
            <li><strong>MEA & Latin America:</strong> 4.8%</li>
          </ul>
        </div>
      </div>
    </section>

    <!-- EXHIBIT 1 & 2 -->
    <div class="chart-card">
      <img src="{img_rev}" alt="Exhibit 1: TCS Revenue Growth Trend">
      <div class="chart-caption">Exhibit 1: TCS Consolidated Revenue Trajectory and YoY Growth Rates (FY21 – FY24). Dual-axis analysis illustrating top-line expansion to ₹240,893 Cr.</div>
    </div>

    <div class="chart-card">
      <img src="{img_prof}" alt="Exhibit 2: Profitability Breakdown">
      <div class="chart-caption">Exhibit 2: TCS Profitability Cascade (EBITDA vs. EBIT vs. Net Profit). Steady expansion supported by robust operational cost containment.</div>
    </div>

    <!-- 3. INDUSTRY ANALYSIS -->
    <section class="section-block">
      <h2>3. Global IT Services Industry Dynamics</h2>
      <p>
        The global enterprise IT spend is undergoing a fundamental structural transition. Following an unprecedented digital modernization surge during 2020–2022, corporate buyers have adopted a cautious stance toward non-discretionary tech consulting. Enterprise priority has decisively shifted toward:
      </p>
      <ol>
        <li><strong>Vendor Consolidation:</strong> Rationalizing tech suppliers to achieve 15–20% operational cost take-outs. As India's largest and most reliable player, TCS is a premier net share gainer.</li>
        <li><strong>Cloud Migration to Cloud Optimization:</strong> Transitioning from raw cloud infrastructure hosting to FinOps, workload rationalization, and cyber hardening.</li>
        <li><strong>Enterprise AI Integration:</strong> Moving beyond conversational AI proof-of-concepts into structured data pipelines, private LLMs, and automated workflow agents (TCS AI WisdomNext™).</li>
      </ol>
    </section>

    <!-- 4. FINANCIAL STATEMENT ANALYSIS -->
    <section class="section-block">
      <h2>4. Comprehensive Financial Statement Analysis</h2>
      <p>
        Over the FY21–FY24 cycle, TCS maintained pristine financial health. Revenue grew at a 13.6% CAGR, Operating Profit at 14.5%, and Net Profit at 12.4%.
      </p>

      <div class="chart-card">
        <img src="{img_marg}" alt="Exhibit 3: Operating Margin Trends">
        <div class="chart-caption">Exhibit 3: Operating and Net Margin Stability (FY21 – FY24). EBITDA margin sustained at ~28.1%, EBIT margin at ~26.0%, and PAT margin at ~19.1%.</div>
      </div>

      <div class="chart-card">
        <img src="{img_cash}" alt="Exhibit 4: Cash Flow Quality & CapEx">
        <div class="chart-caption">Exhibit 4: Cash Flow Quality & Capital Intensity. Operating Cash Flow (₹48,908 Cr) and Free Cash Flow (₹45,108 Cr) highlight superior earnings quality.</div>
      </div>
    </section>

    <!-- 5. RATIO ANALYSIS & DUPONT -->
    <section class="section-block">
      <h2>5. Financial Ratio Analysis & DuPont Decomposition</h2>
      <p>
        TCS generates an exceptional <strong>Return on Equity (ROE) of 51.1%</strong> in FY24. We perform a 3-Stage DuPont Analysis to isolate the underlying fundamental drivers.
      </p>

      <table class="fin-table">
        <thead>
          <tr>
            <th>DuPont Component</th>
            <th>Formula</th>
            <th>FY21</th>
            <th>FY22</th>
            <th>FY23</th>
            <th>FY24</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>1. Net Profit Margin (%)</td>
            <td>Net Profit / Revenue</td>
            <td>19.75%</td>
            <td>19.99%</td>
            <td>18.69%</td>
            <td>19.14%</td>
          </tr>
          <tr>
            <td>2. Asset Turnover (x)</td>
            <td>Revenue / Total Assets</td>
            <td>1.16x</td>
            <td>1.33x</td>
            <td>1.54x</td>
            <td>1.51x</td>
          </tr>
          <tr>
            <td>3. Equity Multiplier (x)</td>
            <td>Total Assets / Equity</td>
            <td>1.64x</td>
            <td>1.62x</td>
            <td>1.63x</td>
            <td>1.77x</td>
          </tr>
          <tr class="total-row">
            <td>Reconstructed ROE (%)</td>
            <td>(1) &times; (2) &times; (3)</td>
            <td>37.68%</td>
            <td>43.18%</td>
            <td>46.80%</td>
            <td>51.15%</td>
          </tr>
        </tbody>
      </table>

      <div class="callout-box green">
        <div class="callout-title">DuPont Analytical Insight</div>
        <p style="margin:0;">
          TCS’s 51.1% ROE is not manufactured via high financial debt (traditional bank borrowings are ₹0). Instead, it stems from genuine operational profitability (~19.1% net margin), robust capital turnover (₹1.51 revenue per ₹1.00 assets), and an aggressive capital return policy (>87% dividend payout) preventing cash drag on the equity base.
        </p>
      </div>
    </section>

    <!-- 6. PEER COMPARISON -->
    <section class="section-block">
      <h2>6. Competitor Benchmark: TCS vs. Infosys vs. HCLTech</h2>
      <p>
        A comparative evaluation of Tier-1 Indian IT peers across FY24 audited financial figures highlights TCS's scale and margin superiority:
      </p>

      <div class="chart-card">
        <img src="{img_peer}" alt="Exhibit 5: Competitor Comparison">
        <div class="chart-caption">Exhibit 5: Tier-1 Indian IT Peer Benchmarking (FY24). TCS leads across Revenue Scale, EBIT Operating Margin, and ROE.</div>
      </div>

      <table class="fin-table">
        <thead>
          <tr>
            <th>Operational & Financial Metric</th>
            <th>TCS</th>
            <th>Infosys</th>
            <th>HCLTech</th>
            <th>Strategic Commentary</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>Revenue from Operations (₹ Cr)</td>
            <td>240,893</td>
            <td>153,670</td>
            <td>109,913</td>
            <td>TCS is 1.57x Infosys and 2.19x HCLTech</td>
          </tr>
          <tr>
            <td>YoY Top-Line Growth (%)</td>
            <td>+6.8%</td>
            <td>+4.7%</td>
            <td>+8.3%</td>
            <td>HCLTech led in FY24 via engineering services</td>
          </tr>
          <tr>
            <td>Operating Margin (EBIT %)</td>
            <td><strong>24.6%</strong></td>
            <td>20.7%</td>
            <td>18.2%</td>
            <td><strong>TCS commands +390 bps over INFY</strong></td>
          </tr>
          <tr>
            <td>Return on Equity (ROE %)</td>
            <td><strong>51.1%</strong></td>
            <td>31.8%</td>
            <td>23.4%</td>
            <td>TCS capital efficiency leads the peer group</td>
          </tr>
          <tr>
            <td>LTM Employee Attrition (%)</td>
            <td><strong>12.5%</strong></td>
            <td>13.8%</td>
            <td>12.8%</td>
            <td>Industry lowest attrition supports margin defense</td>
          </tr>
          <tr class="total-row">
            <td>Price-to-Earnings (P/E Multiple, x)</td>
            <td>30.3x</td>
            <td>25.4x</td>
            <td>26.2x</td>
            <td>TCS commands a well-justified quality premium</td>
          </tr>
        </tbody>
      </table>
    </section>

    <!-- 7. VALUATION ANALYSIS -->
    <section class="section-block">
      <h2>7. Valuation Analysis: Illustrative DCF & Sensitivity</h2>
      <p>
        We build a 5-Year Unlevered Discounted Cash Flow (DCF) model based on explicit, realistic assumptions. All figures represent illustrative financial scenarios.
      </p>

      <div class="callout-box">
        <div class="callout-title">CAPM & WACC Parameter Derivation</div>
        <ul>
          <li><strong>Risk-Free Rate ($R_f$):</strong> 7.10% (10Y Indian Government Benchmark Bond)</li>
          <li><strong>Equity Risk Premium (ERP):</strong> 6.00% (Institutional India Market Risk Premium)</li>
          <li><strong>Beta ($\beta$):</strong> 0.82 (Defensive large-cap technology profile)</li>
          <li><strong>Cost of Equity ($K_e$):</strong> 7.10% + (0.82 &times; 6.00%) = <strong>12.02%</strong></li>
          <li><strong>Blended WACC:</strong> <strong>{wacc_pct:.2f}%</strong> (Equity weight 99.4%, Lease debt 0.6%)</li>
          <li><strong>Terminal Growth Rate ($g$):</strong> <strong>{tg_pct:.2f}%</strong> (Sustainable long-term IT expansion)</li>
        </ul>
      </div>

      <table class="fin-table">
        <thead>
          <tr>
            <th>Cash Flow Line Item (₹ Cr)</th>
            <th>FY25E</th>
            <th>FY26E</th>
            <th>FY27E</th>
            <th>FY28E</th>
            <th>FY29E</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>Projected Revenue</td>
            <td>256,551</td>
            <td>277,075</td>
            <td>300,626</td>
            <td>324,677</td>
            <td>349,027</td>
          </tr>
          <tr>
            <td>Operating EBIT (24.8% - 25.2%)</td>
            <td>64,138</td>
            <td>69,823</td>
            <td>75,758</td>
            <td>81,169</td>
            <td>86,559</td>
          </tr>
          <tr>
            <td>NOPAT (EBIT &times; [1 - 25.17%])</td>
            <td>47,994</td>
            <td>52,248</td>
            <td>56,690</td>
            <td>60,739</td>
            <td>64,772</td>
          </tr>
          <tr>
            <td>(+) D&amp;A (-) CapEx (-) &Delta;NWC</td>
            <td>1,126</td>
            <td>1,180</td>
            <td>1,268</td>
            <td>1,383</td>
            <td>1,502</td>
          </tr>
          <tr class="total-row">
            <td>Unlevered Free Cash Flow (FCFF)</td>
            <td>49,120</td>
            <td>53,428</td>
            <td>57,958</td>
            <td>62,122</td>
            <td>66,274</td>
          </tr>
          <tr>
            <td>PV of FCFF (at WACC {wacc_pct:.2f}%)</td>
            <td>₹46,418</td>
            <td>₹45,087</td>
            <td>₹43,676</td>
            <td>₹41,805</td>
            <td>₹39,827</td>
          </tr>
        </tbody>
      </table>

      <table class="fin-table">
        <thead>
          <tr>
            <th>DCF Valuation Step</th>
            <th>Figure (₹ Cr)</th>
            <th>Per Share (₹)</th>
            <th>% of Enterprise Value</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>Cumulative PV of 5-Year Forecast FCFF</td>
            <td>₹{sum_pv_fcff:,.2f} Cr</td>
            <td>₹{(sum_pv_fcff / shares_cr):,.2f}</td>
            <td>{(100.0 - tv_share_pct):.1f}%</td>
          </tr>
          <tr>
            <td>Present Value of Terminal Value</td>
            <td>₹{pv_tv:,.2f} Cr</td>
            <td>₹{(pv_tv / shares_cr):,.2f}</td>
            <td>{tv_share_pct:.1f}%</td>
          </tr>
          <tr>
            <td>Implied Enterprise Value (EV)</td>
            <td>₹{ev_cr:,.2f} Cr</td>
            <td>₹{(ev_cr / shares_cr):,.2f}</td>
            <td>100.0%</td>
          </tr>
          <tr>
            <td>(+) Cash &amp; Liquid Investments (FY24)</td>
            <td>₹48,908.00 Cr</td>
            <td>₹{(48908.0 / shares_cr):,.2f}</td>
            <td>—</td>
          </tr>
          <tr>
            <td>(-) Total Debt &amp; Lease Liabilities (FY24)</td>
            <td>(₹8,386.00 Cr)</td>
            <td>(₹{(8386.0 / shares_cr):,.2f})</td>
            <td>—</td>
          </tr>
          <tr>
            <td>Net Cash Surplus Added</td>
            <td>₹{net_cash_cr:,.2f} Cr</td>
            <td>₹{(net_cash_cr / shares_cr):,.2f}</td>
            <td>—</td>
          </tr>
          <tr class="total-row">
            <td>Implied Baseline Equity Value</td>
            <td>₹{equity_val_cr:,.2f} Cr</td>
            <td>₹{dcf_val:,.2f}</td>
            <td>Baseline 5-Year Horizon</td>
          </tr>
        </tbody>
      </table>

      <div class="callout-box">
        <div class="callout-title">DCF Baseline vs. Market Price Analysis</div>
        <p style="margin:0;">
          The 5-year illustrative DCF yields a baseline intrinsic value of <strong>₹{dcf_val:,.2f} per share</strong>. In comparison, TCS currently trades in the market at <strong>₹3,850.00 per share</strong> (30.3x FY24 P/E). This differential highlights the "franchise longevity premium" that the market prices into elite market leaders: the public equity market anticipates that TCS will continue to reinvest and compound cash flows at a 50%+ ROE for 15 to 20+ years, rather than transitioning to a modest terminal growth rate of 4.25% after only five years.
        </p>
      </div>

      <div class="chart-card">
        <img src="{img_sens}" alt="Exhibit 6: DCF Valuation Sensitivity Matrix">
        <div class="chart-caption">Exhibit 6: Valuation Sensitivity Matrix Heatmap. Implied share prices under varying WACC (11.0%–13.0%) and Terminal Growth rates (3.5%–5.0%). Base case indicated at ₹{dcf_val:,.2f}.</div>
      </div>
    </section>

    <!-- 8. RISK ANALYSIS -->
    <section class="section-block">
      <h2>8. Risk Analysis & Institutional Sensitivity</h2>
      <ul>
        <li><strong>Macroeconomic Discretionary Spending Risk:</strong> Exposure to US (50.1%) and European BFSI (32.0%) exposes TCS to project deferrals during interest rate or banking crises.</li>
        <li><strong>Foreign Exchange Risk:</strong> With >90% of revenue in USD/GBP/EUR and >65% of costs in INR, a 100 bps rupee appreciation trims ~30–35 bps from operating margins without hedging.</li>
        <li><strong>Wage Inflation & Onshore Staffing:</strong> Rising localized visa costs and onshore technical compensation can pressure margins during high-inflation regimes.</li>
        <li><strong>GenAI Deflation:</strong> Automation of baseline coding and maintenance contracts risks compressing billing hours unless offset by higher-value architecture work.</li>
      </ul>
    </section>

    <!-- 9. INVESTMENT THESIS -->
    <section class="section-block">
      <h2>9. Investment Thesis & Research Synthesis</h2>
      <div class="callout-box green">
        <div class="callout-title">Institutional Research Conclusion: Fundamental & Valuation Analysis</div>
        <p style="margin:0;">
          TCS is an elite cash cow with a negative net debt balance sheet (₹40,522 Cr net cash), superior operating margin defense (24.6%–26.0%), and peer-leading ROE (51.1%). Our baseline 5-year illustrative DCF framework yields an intrinsic value of <strong>₹{dcf_val:,.2f} per share</strong> under conservative macro assumptions. At current market prices (CMP ₹3,850.00, ~30.3x P/E), the stock trades at an embedded franchise premium inline with its 5-year historical average of 29.5x P/E, reflecting market expectations of persistent multi-decade reinvestment and dividend distribution. Investors should monitor quarterly TCV bookings ($8B–$10B threshold) and BFSI discretionary budget recovery as key indicators of medium-term earnings trajectory.
        </p>
      </div>
    </section>

  </main>

  <!-- FOOTER & DISCLAIMER -->
  <footer class="report-footer">
    <p><strong>REGULATORY & RESEARCH DISCLAIMER:</strong> This report is prepared strictly for academic and career demonstration purposes as part of a student equity research and financial modeling portfolio. This document does not constitute an offer, solicitation, or recommendation to purchase or sell any security. All figures are compiled from publicly available audited annual filings (FY21–FY24). DCF valuations and projections represent illustrative hypothetical models based on stated assumptions and do not represent price targets.</p>
    <p>&copy; 2026 Abhinav Verma &bull; Equity Research & Financial Modeling Portfolio &bull; All Rights Reserved.</p>
  </footer>

</div>

</body>
</html>
"""

    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"HTML Report successfully compiled at: {html_path}")
    return html_path


def convert_html_to_pdf(html_path: str, output_pdf_path: str = None) -> str:
    """Uses headless Chrome to compile pixel-perfect PDF."""
    if output_pdf_path is None:
        report_dir = os.path.dirname(html_path)
        output_pdf_path = os.path.join(report_dir, "TCS_Equity_Research_Report.pdf")

    chrome_cmd = [
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        "--headless",
        "--disable-gpu",
        "--run-all-compositor-stages-before-draw",
        f"--print-to-pdf={output_pdf_path}",
        f"file://{html_path}",
    ]

    try:
        subprocess.run(chrome_cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(f"PDF Report successfully compiled at: {output_pdf_path}")
        return output_pdf_path
    except Exception as e:
        print(f"Warning: Headless Chrome PDF generation encountered: {e}")
        return ""


if __name__ == "__main__":
    html = build_html_report()
    convert_html_to_pdf(html)
