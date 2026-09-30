# Tata Consultancy Services (TCS) — Equity Research & Financial Analysis Report

[![Python Version](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Sector](https://img.shields.io/badge/Sector-Global%20IT%20Services-darkblue.svg)](https://www.tcs.com/)
[![Focus](https://img.shields.io/badge/Focus-Equity%20Research%20%26%20Valuation-darkblue.svg)](#objective)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

An institutional-grade **Investment Research & Financial Analysis Report** on **Tata Consultancy Services Ltd. (NSE: TCS.NS / BSE: 532540)**, India’s largest IT services company and the world’s second-largest technology consultancy by market capitalization.

This project is prepared for **Equity Research, Asset Management, and Investment Analysis** portfolio demonstration. It illustrates how a **Computer Science & Engineering (B.Tech CSE)** background is applied to execute rigorous fundamental financial modeling, cash flow valuation, competitive benchmarking, and institutional-quality data visualization.

---

## 📌 Executive Summary of Deliverables

* **Full Equity Research Report (Markdown)**: [`REPORT.md`](file:///Users/abhinavverma/Documents/Investment%20Research%20&%20Financial%20Analysis%20Report/REPORT.md) — 10-section comprehensive institutional equity research report.
* **Publication PDF Report**: [`output/reports/TCS_Equity_Research_Report.pdf`](file:///Users/abhinavverma/Documents/Investment%20Research%20&%20Financial%20Analysis%20Report/output/reports/TCS_Equity_Research_Report.pdf) — Ready-to-print research report compiled via headless Chrome.
* **Interactive HTML Report**: [`output/reports/TCS_Equity_Research_Report.html`](file:///Users/abhinavverma/Documents/Investment%20Research%20&%20Financial%20Analysis%20Report/output/reports/TCS_Equity_Research_Report.html) — Self-contained document with base64 embedded charts and paged print CSS.
* **Multi-Tab Excel Financial Model**: [`data/tcs_financial_model.xlsx`](file:///Users/abhinavverma/Documents/Investment%20Research%20&%20Financial%20Analysis%20Report/data/tcs_financial_model.xlsx) — Dynamic Excel workbook with historical statements, ratio sheets, peer benchmarks, and formulaic DCF model.
* **High-Resolution Research Exhibits**: [`output/charts/`](file:///Users/abhinavverma/Documents/Investment%20Research%20&%20Financial%20Analysis%20Report/output/charts/) — 6 publication-ready charts (300 DPI) rendered in an institutional corporate palette.

---

## 🎯 Objective

1. **Fundamental Valuation & Research**: Analyze 4 years of audited consolidated annual financial statements (FY21–FY24) for Tata Consultancy Services to evaluate top-line compounding, margin defense, free cash flow conversion, and return on capital.
2. **Competitive Peer Benchmarking**: Benchmark TCS against its primary Tier-1 Indian IT peers (**Infosys** and **HCLTech**) across scale, growth, profitability, balance sheet leverage, and valuation multiples.
3. **Intrinsic Cash Flow Modeling**: Formulate an illustrative 5-Year Unlevered Discounted Cash Flow (DCF) model and Weighted Average Cost of Capital (WACC) via the Capital Asset Pricing Model (CAPM), coupled with a 2D sensitivity analysis.
4. **Institutional Non-Promotional Stance**: Emphasize factual financial analysis, explicit assumptions, risk factors, and key monitorables without speculative buy/sell claims or stock-price guarantees.

---

## 🛠️ Tools Used & Tech Stack

| Component | Technology | Role & Purpose |
| :--- | :--- | :--- |
| **Language** | **Python 3.10+** | Core programming language for data processing, financial algorithms, and pipeline execution. |
| **Data Processing** | **Pandas & NumPy** | Financial statement transposition, CAGR calculations, ratio engines, and sensitivity matrix generation. |
| **Data Visualization** | **Matplotlib** | High-resolution (300 DPI) institutional charts styled with an executive corporate palette (`#0A2540`, `#1E3A8A`, `#D97706`). |
| **Financial Modeling** | **OpenPyXL** | Automated creation of a 5-tab Microsoft Excel financial workbook containing live Excel formulas, custom number formats, and styling. |
| **Report Generation** | **Google Chrome Headless** | Compiles self-contained HTML reports with embedded base64 figures into a publication-grade PDF. |
| **Data Sources** | **Audited Annual Reports** | Audited Ind AS consolidated annual financial statements, notes to accounts, and National Stock Exchange (NSE) market data. |

---

## 📈 Financial Concepts Demonstrated

### 1. Financial Statement Analysis (3-Statement Modeling)
* **Income Statement**: Analyzed the waterfall from Revenue from Operations (₹240,893 Cr in FY24) through Employee Expenses (57.1% of revenue), EBITDA (₹67,571 Cr, 28.1% margin), Operating EBIT (₹62,586 Cr, 26.0% margin), and Net Profit (₹46,099 Cr, 19.1% margin).
* **Balance Sheet**: Zero bank debt. Total liabilities include lease liabilities of ₹8,386 Cr under Ind AS 116. Cash & liquid investments of ₹48,908 Cr yield a **net cash surplus of ₹40,522 Cr**.
* **Cash Flow Statement**: Cash from Operations (OCF) was ₹48,908 Cr (106.1% conversion of PAT). CapEx was ₹3,800 Cr (1.58% of revenue), generating **₹45,108 Cr in Free Cash Flow (FCF)**.

### 2. DuPont 3-Stage Return on Equity (ROE) Decomposition
Deconstructs why TCS achieves an extraordinary **51.15% ROE**:
$$\text{ROE} = \underbrace{\frac{\text{Net Income}}{\text{Revenue}}}_{\text{Net Margin: } 19.14\%} \times \underbrace{\frac{\text{Revenue}}{\text{Total Assets}}}_{\text{Asset Turnover: } 1.51\text{x}} \times \underbrace{\frac{\text{Total Assets}}{\text{Shareholders' Equity}}}_{\text{Financial Leverage: } 1.77\text{x}} = 51.15\%$$
* **Takeaway**: High ROE is not artificially created via risky bank debt. It is driven by high operating margins (~19%), rapid asset turnover (~1.5x), and returning >85% of net income to shareholders via dividends/buybacks, keeping the equity base lean.

### 3. Valuation Analysis (DCF & Relative Multiples)
* **CAPM & Cost of Equity ($K_e$)**:
  $$K_e = R_f + \beta \times \text{ERP} = 7.10\% + 0.82 \times 6.00\% = 12.02\%$$
  where $R_f = 7.10\%$ (10Y Indian G-Sec), $\text{ERP} = 6.00\%$, and $\beta = 0.82$ (defensive mega-cap IT).
* **Weighted Average Cost of Capital (WACC)**: Blended WACC calculated at **11.98%** given 99.4% equity and 0.6% lease debt weight.
* **Unlevered Free Cash Flow (FCFF)**:
  $$\text{FCFF} = \text{EBIT} \times (1 - t) + \text{D\&A} - \text{CapEx} - \Delta \text{NWC}$$
* **Gordon Growth Terminal Value**:
  $$\text{Terminal Value} = \frac{\text{FCFF}_{FY29E} \times (1 + g)}{\text{WACC} - g} = \frac{66,274 \times (1 + 0.0425)}{0.11977 - 0.0425} = ₹8,93,602\text{ Cr}$$
* **Implied Baseline Fair Value**: **₹2,113.89 per share** (~16.7x FY24 P/E).
* **Market Comparison Context**: In contrast to the baseline 5-year DCF value (₹2,113.89), TCS currently trades in the market at **₹3,850.00 per share** (~30.3x P/E, in line with its 5-year average of 29.5x). In equity research, this spread reflects the *franchise longevity premium* that investors place on a debt-free market leader capable of sustaining 50%+ ROE over a multi-decade horizon rather than fading after 5 years.
* **Sensitivity Matrix**: Implemented a 2D cross-table evaluating implied fair value across WACC (11.0% to 13.0%) and Terminal Growth (3.5% to 5.0%), generating intrinsic values from ₹1,781 to ₹2,627 per share.
* **Relative Valuation**: Benchmarked TCS’s LTM P/E (30.3x) and EV/EBITDA (20.2x) against its 5-year average (29.5x) and peers (Infosys 25.4x, HCLTech 26.2x).

### 4. Solvency, Liquidity & Capital Allocation
* **Capital Return Policy**: Evaluated TCS's continuous return of >85% of annual profits through regular dividends, special dividends, and share buybacks (₹1,20,000+ Cr returned over FY22–FY24).
* **Solvency**: Debt-to-Equity ratio of 0.09x (representing lease obligations only; bank debt is ₹0.00).

---

## 📊 Key Analytical Findings: TCS vs. Peers (FY24)

| Metric | TCS | Infosys | HCLTech | Analytical Commentary |
| :--- | :---: | :---: | :---: | :--- |
| **Revenue from Operations** | **₹2,40,893 Cr** | ₹1,53,670 Cr | ₹1,09,913 Cr | Scale leader (1.57x Infosys, 2.19x HCLTech). |
| **YoY Revenue Growth (%)** | +6.8% | +4.7% | **+8.3%** | HCLTech outperformed on engineering & software services. |
| **EBIT Operating Margin (%)** | **24.6%** | 20.7% | 18.2% | **TCS commands +390 bps over INFY and +640 bps over HCLT.** |
| **Net Profit Margin (%)** | **19.1%** | 17.1% | 14.3% | Strongest bottom-line conversion in the IT sector. |
| **Return on Equity (ROE %)** | **51.1%** | 31.8% | 23.4% | Industry-leading capital efficiency. |
| **Voluntary Attrition (LTM %)** | **12.5%** | 13.8% | 12.8% | Lowest employee turnover protects margins and client continuity. |
| **Net Cash on Balance Sheet** | **₹40,522 Cr** | ₹14,200 Cr | ₹7,800 Cr | Fortress balance sheet with zero commercial bank debt. |
| **P/E Valuation Multiple (x)** | **30.3x** | 25.4x | 26.2x | Commands quality valuation premium supported by margin resilience. |

---

## 📁 Project Architecture & Folder Structure

```
Investment Research & Financial Analysis Report/
│
├── README.md                      # Comprehensive project documentation & guide
├── REPORT.md                      # Complete 10-section institutional equity research report
├── run_analysis.py                # Master pipeline runner (data -> analysis -> charts -> report)
├── generate_excel_model.py        # Generates multi-tab openpyxl Excel financial model
├── generate_report.py             # Generates HTML report & compiles PDF via headless Chrome
│
├── data/                          # Audited financial datasets & Excel models
│   ├── tcs_financials_historical.csv  # 4-year consolidated statements (FY21-FY24)
│   ├── peer_comparison_fy24.csv       # FY24 metrics for TCS, Infosys, and HCLTech
│   ├── segment_breakdown_fy24.csv     # Industry vertical & geographic revenue distribution
│   └── tcs_financial_model.xlsx       # Multi-tab institutional Excel model with formulas
│
├── src/                           # Clean, modular Python analytical engines
│   ├── __init__.py                # Package initialization
│   ├── data_loader.py             # Ingestion, schema validation & data formatting
│   ├── financial_analysis.py      # CAGRs, profitability, return ratios, DuPont analysis
│   ├── valuation_model.py         # CAPM, WACC, 5-Yr FCFF, DCF & sensitivity matrix
│   └── visualizer.py              # Publication-grade Matplotlib chart generator (300 DPI)
│
└── output/                        # Final publication assets
    ├── charts/                    # High-resolution PNG figures
    │   ├── revenue_growth_trend.png
    │   ├── profitability_breakdown.png
    │   ├── operating_margin_trends.png
    │   ├── competitor_comparison.png
    │   ├── cashflow_conversion_capex.png
    │   └── dcf_sensitivity_matrix.png
    └── reports/                   # Publication-ready equity research reports
        ├── TCS_Equity_Research_Report.html  # Portable, self-contained interactive report
        └── TCS_Equity_Research_Report.pdf   # Institutional printable PDF report
```

---

## 🚀 How to Run the Analysis

### 1. Prerequisites
Ensure Python 3.9+ is installed on your system. The required standard dependencies are:
```bash
pip install pandas matplotlib openpyxl numpy
```

### 2. Execute the Master Pipeline
Run the master pipeline script from the project root:
```bash
python3 run_analysis.py
```
This single command executes:
1. Data loading and mathematical consistency verification across all statements.
2. Calculation of growth rates, profitability margins, return ratios, and DuPont decomposition.
3. Execution of the DCF model, WACC calculation, and sensitivity matrix generation.
4. Rendering of all 6 publication charts into `output/charts/`.
5. Generation of the 5-tab Excel financial workbook `data/tcs_financial_model.xlsx`.
6. Compilation of the full research report into `output/reports/TCS_Equity_Research_Report.html` and `TCS_Equity_Research_Report.pdf`.

### 3. Running Individual Modules
To test or inspect individual modules independently:
```bash
# Test data ingestion and print parsed tables
python3 src/data_loader.py

# Run financial ratios and DuPont decomposition
python3 src/financial_analysis.py

# Run DCF valuation and display sensitivity table
python3 src/valuation_model.py

# Re-render charts
python3 src/visualizer.py

# Generate Excel financial model only
python3 generate_excel_model.py

# Compile HTML and PDF reports only
python3 generate_report.py
```

---

## 💡 What I Learned from the Project

As a **B.Tech Computer Science & Engineering student** pivoting toward quantitative equity research and financial analysis:

1. **Financial Statements Are Dynamic Systems, Not Static Spreadsheets**: Building this project reinforced how the three financial statements interconnect. I learned how operating profit (EBIT) translates through non-cash working capital adjustments and capital expenditures into true Unlevered Free Cash Flow (FCFF), and how capital allocation decisions (share buybacks) directly influence return on equity (ROE).
2. **DuPont Decomposition Bridges Operations and Accounting**: Unpacking ROE via DuPont revealed that TCS's 51% ROE is not a result of debt leverage (which would introduce solvency risk), but rather superior asset turnover and an industry-leading operating margin moat (24.6%–26.0%).
3. **Valuation Is About Explicit Scenarios, Not Guesswork**: Coming from an engineering and algorithmic mindset, I initially looked at valuation as an optimization problem. Through DCF modeling, I realized that valuation is an exercise in **grounded scenario analysis**—sensitizing cost of equity (WACC) and terminal growth ($g$) to reflect macro interest rates and secular industry headwinds.
4. **Institutional Quality Lies in Discipline**: Moving beyond retail "stock tips" to produce an institutional research report taught me the importance of maintaining an objective tone: balancing company strengths (scale, low attrition, net cash) against genuine risks (US discretionary IT budget freeze, currency fluctuations, and Generative AI billing deflation).

---

## ⚖️ Ethical Conduct & Regulatory Disclaimer

*This project is conducted strictly for educational, academic, and professional portfolio demonstration purposes as part of a student equity research and financial modeling portfolio. It does NOT constitute investment advice, financial solicitation, or a recommendation to buy, hold, or sell any security. All historical statements are drawn from publicly available annual reports filed by Tata Consultancy Services Ltd, Infosys Ltd, and HCL Technologies Ltd. Cash flow projections, DCF scenarios, and sensitivity tables are illustrative analytical models based on stated hypothetical assumptions and do not represent price targets.*
