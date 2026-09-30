"""
=============================================================================
Valuation Analysis Engine: DCF Model & Multiples Benchmark
Institutional Equity Research Valuation Framework
=============================================================================
This module implements:
1. WACC (Weighted Average Cost of Capital) calculation via CAPM.
2. 5-Year Unlevered Free Cash Flow (FCFF) forecast (FY25E - FY29E).
3. Terminal Value calculation using the Gordon Growth Model.
4. Enterprise Value to Equity Value bridge (Net Cash adjustment).
5. 2-Dimensional Sensitivity Matrix (WACC vs Terminal Growth).
6. Relative P/E multiple benchmarking across historical bands and peers.

NOTE: All valuation figures are illustrative scenario models based on explicit
assumptions and do not constitute price targets or investment recommendations.
"""

from typing import Dict, List, Tuple, Any
import numpy as np
import pandas as pd


class TCSValuationModel:
    """
    Illustrative Discounted Cash Flow (DCF) and Relative Valuation Model for TCS.
    """

    def __init__(
        self,
        rf: float = 0.0710,          # 10Y Indian Government Bond Yield (7.10%)
        erp: float = 0.0600,         # Equity Risk Premium for India (6.00%)
        beta: float = 0.82,          # TCS Adjusted Beta (defensive IT)
        pretax_cost_debt: float = 0.0750,  # Incremental borrowing rate on leases (7.50%)
        tax_rate: float = 0.2517,    # Statutory corporate tax rate (25.17%)
        terminal_growth: float = 0.0425,   # Long-term sustainable growth (4.25%)
        shares_outstanding_cr: float = 361.8, # Shares outstanding in Crores
        fy24_revenue_cr: float = 240893.0,
        fy24_ebit_cr: float = 62586.0,
        fy24_cash_cr: float = 48908.0,
        fy24_debt_cr: float = 8386.0,
    ):
        self.rf = rf
        self.erp = erp
        self.beta = beta
        self.pretax_cost_debt = pretax_cost_debt
        self.tax_rate = tax_rate
        self.terminal_growth = terminal_growth
        self.shares_cr = shares_outstanding_cr
        self.fy24_revenue = fy24_revenue_cr
        self.fy24_ebit = fy24_ebit_cr
        self.fy24_cash = fy24_cash_cr
        self.fy24_debt = fy24_debt_cr

    def calculate_wacc(self) -> Dict[str, float]:
        """
        Calculates Cost of Equity (CAPM) and Weighted Average Cost of Capital (WACC).
        """
        cost_of_equity = self.rf + (self.beta * self.erp)
        after_tax_cost_debt = self.pretax_cost_debt * (1.0 - self.tax_rate)

        # Market values
        market_cap_est = self.shares_cr * 3850.0  # Approx baseline market cap
        total_enterprise_capital = market_cap_est + self.fy24_debt

        weight_equity = market_cap_est / total_enterprise_capital
        weight_debt = self.fy24_debt / total_enterprise_capital

        wacc = (weight_equity * cost_of_equity) + (weight_debt * after_tax_cost_debt)

        return {
            "risk_free_rate_pct": self.rf * 100.0,
            "equity_risk_premium_pct": self.erp * 100.0,
            "beta": self.beta,
            "cost_of_equity_pct": cost_of_equity * 100.0,
            "pretax_cost_of_debt_pct": self.pretax_cost_debt * 100.0,
            "after_tax_cost_of_debt_pct": after_tax_cost_debt * 100.0,
            "weight_equity_pct": weight_equity * 100.0,
            "weight_debt_pct": weight_debt * 100.0,
            "wacc_pct": wacc * 100.0,
            "wacc_decimal": wacc,
        }

    def project_5yr_free_cash_flows(
        self,
        growth_rates: List[float] = None,
        ebit_margins: List[float] = None,
    ) -> pd.DataFrame:
        """
        Projects 5 years of Unlevered Free Cash Flow (FCFF) for FY25E through FY29E.
        
        Assumptions:
        - CapEx: 1.6% of Revenue (in line with historical asset-light model)
        - D&A: 2.1% of Revenue
        - NWC Change: 1.0% of incremental Revenue
        - Effective Tax Rate: 25.17%
        """
        if growth_rates is None:
            # Conservative baseline growth trajectory
            growth_rates = [0.065, 0.080, 0.085, 0.080, 0.075]  # FY25E to FY29E
        if ebit_margins is None:
            # Resilient operating margin band
            ebit_margins = [0.250, 0.252, 0.252, 0.250, 0.248]  # FY25E to FY29E

        years = ["FY25E", "FY26E", "FY27E", "FY28E", "FY29E"]
        projection_data = []

        prev_rev = self.fy24_revenue

        for i, year in enumerate(years):
            g = growth_rates[i]
            margin = ebit_margins[i]

            rev = prev_rev * (1.0 + g)
            delta_rev = rev - prev_rev
            ebit = rev * margin
            nopat = ebit * (1.0 - self.tax_rate)
            dna = rev * 0.0210
            capex = rev * 0.0160
            delta_nwc = delta_rev * 0.0100

            # FCFF = NOPAT + D&A - CapEx - Delta NWC
            fcff = nopat + dna - capex - delta_nwc

            projection_data.append({
                "Fiscal_Year": year,
                "Revenue_Growth_pct": g * 100.0,
                "Revenue_INR_Cr": rev,
                "EBIT_Margin_pct": margin * 100.0,
                "EBIT_INR_Cr": ebit,
                "NOPAT_INR_Cr": nopat,
                "Depr_Amort_INR_Cr": dna,
                "CapEx_INR_Cr": capex,
                "Delta_NWC_INR_Cr": delta_nwc,
                "FCFF_INR_Cr": fcff,
            })
            prev_rev = rev

        return pd.DataFrame(projection_data).set_index("Fiscal_Year")

    def run_dcf(
        self,
        custom_wacc: float = None,
        custom_terminal_growth: float = None,
    ) -> Dict[str, Any]:
        """
        Executes complete DCF valuation including PV of forecast cash flows,
        terminal value calculation, enterprise value, and equity value per share.
        """
        wacc_dict = self.calculate_wacc()
        wacc = custom_wacc if custom_wacc is not None else wacc_dict["wacc_decimal"]
        tg = custom_terminal_growth if custom_terminal_growth is not None else self.terminal_growth

        projections = self.project_5yr_free_cash_flows()

        # Discount cash flows to present value (Mid-year convention: year - 0.5)
        pv_fcff_list = []
        for idx, (yr, row) in enumerate(projections.iterrows()):
            t = (idx + 1) - 0.5  # Mid-year convention
            discount_factor = 1.0 / ((1.0 + wacc) ** t)
            pv_fcff = row["FCFF_INR_Cr"] * discount_factor
            pv_fcff_list.append(pv_fcff)

        projections["PV_FCFF_INR_Cr"] = pv_fcff_list
        sum_pv_fcff = sum(pv_fcff_list)

        # Terminal Value via Gordon Growth Model
        final_yr_fcff = projections.iloc[-1]["FCFF_INR_Cr"]
        terminal_cash_flow = final_yr_fcff * (1.0 + tg)
        terminal_value = terminal_cash_flow / (wacc - tg)

        # Discount Terminal Value to PV (at period 5)
        pv_terminal_value = terminal_value / ((1.0 + wacc) ** 5.0)

        # Enterprise Value
        enterprise_value = sum_pv_fcff + pv_terminal_value

        # Bridge: EV to Equity Value
        # Net Cash = Cash & Liquid Investments - Total Debt
        net_cash = self.fy24_cash - self.fy24_debt
        implied_equity_value = enterprise_value + net_cash
        implied_share_price = implied_equity_value / self.shares_cr

        return {
            "wacc_pct": round(wacc * 100.0, 2),
            "terminal_growth_pct": round(tg * 100.0, 2),
            "projections_df": projections,
            "sum_pv_forecast_cashflows_cr": round(sum_pv_fcff, 2),
            "terminal_value_cr": round(terminal_value, 2),
            "pv_terminal_value_cr": round(pv_terminal_value, 2),
            "terminal_value_share_pct": round((pv_terminal_value / enterprise_value) * 100.0, 2),
            "enterprise_value_cr": round(enterprise_value, 2),
            "cash_equivalents_cr": round(self.fy24_cash, 2),
            "debt_lease_liabilities_cr": round(self.fy24_debt, 2),
            "net_cash_cr": round(net_cash, 2),
            "implied_equity_value_cr": round(implied_equity_value, 2),
            "shares_outstanding_cr": self.shares_cr,
            "implied_value_per_share_inr": round(implied_share_price, 2),
        }

    def generate_sensitivity_matrix(
        self,
        wacc_range: List[float] = None,
        tg_range: List[float] = None,
    ) -> pd.DataFrame:
        """
        Creates a 2D sensitivity grid comparing implied share prices across
        varying WACC and Terminal Growth Rates.
        """
        if wacc_range is None:
            wacc_range = [0.110, 0.115, 0.120, 0.125, 0.130]
        if tg_range is None:
            tg_range = [0.0350, 0.0400, 0.0425, 0.0450, 0.0500]

        matrix = {}
        for tg in tg_range:
            col_name = f"g = {tg*100:.2f}%"
            matrix[col_name] = []
            for w in wacc_range:
                res = self.run_dcf(custom_wacc=w, custom_terminal_growth=tg)
                matrix[col_name].append(res["implied_value_per_share_inr"])

        row_names = [f"WACC = {w*100:.2f}%" for w in wacc_range]
        df_sens = pd.DataFrame(matrix, index=row_names)
        df_sens.index.name = "Discount Rate (WACC)"
        return df_sens

    def get_relative_valuation_comparison(self) -> pd.DataFrame:
        """
        Summarizes peer valuation metrics and historical TCS multiple bands.
        """
        data = [
            {"Entity": "TCS (Current CMP ~₹3,850)", "P/E (x)": 30.3, "EV/EBITDA (x)": 20.2, "FCF Yield (%)": 3.2, "Div Yield (%)": 1.8},
            {"Entity": "TCS 5-Year Historical Average", "P/E (x)": 29.5, "EV/EBITDA (x)": 19.8, "FCF Yield (%)": 3.4, "Div Yield (%)": 2.1},
            {"Entity": "TCS 5-Year Peak Multiples (2021)", "P/E (x)": 39.5, "EV/EBITDA (x)": 26.4, "FCF Yield (%)": 2.4, "Div Yield (%)": 1.4},
            {"Entity": "TCS 5-Year Trough Multiples (2020)", "P/E (x)": 22.0, "EV/EBITDA (x)": 14.5, "FCF Yield (%)": 4.6, "Div Yield (%)": 2.8},
            {"Entity": "Infosys (FY24 Peer)", "P/E (x)": 25.4, "EV/EBITDA (x)": 17.6, "FCF Yield (%)": 3.6, "Div Yield (%)": 2.3},
            {"Entity": "HCLTech (FY24 Peer)", "P/E (x)": 26.2, "EV/EBITDA (x)": 16.1, "FCF Yield (%)": 4.1, "Div Yield (%)": 3.4},
        ]
        return pd.DataFrame(data).set_index("Entity")


if __name__ == "__main__":
    model = TCSValuationModel()
    wacc_res = model.calculate_wacc()
    print("=== WACC CALCULATION ===")
    for k, v in wacc_res.items():
        print(f"  {k}: {v}")

    dcf_res = model.run_dcf()
    print("\n=== DCF BASE CASE SUMMARY ===")
    print(f"  WACC: {dcf_res['wacc_pct']}% | Terminal Growth: {dcf_res['terminal_growth_pct']}%")
    print(f"  PV of 5-Yr FCFF: ₹{dcf_res['sum_pv_forecast_cashflows_cr']:,.2f} Cr")
    print(f"  PV of Terminal Value: ₹{dcf_res['pv_terminal_value_cr']:,.2f} Cr ({dcf_res['terminal_value_share_pct']}% of EV)")
    print(f"  Enterprise Value: ₹{dcf_res['enterprise_value_cr']:,.2f} Cr")
    print(f"  Net Cash Added: ₹{dcf_res['net_cash_cr']:,.2f} Cr")
    print(f"  Implied Equity Value: ₹{dcf_res['implied_equity_value_cr']:,.2f} Cr")
    print(f"  Implied Value Per Share: ₹{dcf_res['implied_value_per_share_inr']:,.2f}")

    print("\n=== DCF SENSITIVITY MATRIX (₹ / Share) ===")
    sens = model.generate_sensitivity_matrix()
    print(sens)

    print("\n=== RELATIVE VALUATION BENCHMARK ===")
    rel = model.get_relative_valuation_comparison()
    print(rel)
