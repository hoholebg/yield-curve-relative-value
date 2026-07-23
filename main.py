import numpy as np
import pandas as pd
from src.nelson_siegel import NelsonSiegelCurve
from src.relative_value import BondRelativeValueAnalyzer

def main():
    print("=== Anaxis Asset Management - Yield Curve Dynamics & Relative Value Analysis ===")
    
    # 1. Benchmark Sovereign Yield Curve Fitting
    maturities = np.array([0.25, 0.5, 1.0, 2.0, 3.0, 5.0, 7.0, 10.0, 30.0])
    market_rates = np.array([0.038, 0.036, 0.034, 0.032, 0.031, 0.030, 0.031, 0.033, 0.037])
    
    ns = NelsonSiegelCurve().fit(maturities, market_rates)
    print(f"Fitted Nelson-Siegel Parameters:")
    print(f"  Beta0 (Long-term rate): {ns.beta0*100:.2f}%")
    print(f"  Beta1 (Slope):          {ns.beta1*100:.2f}%")
    print(f"  Beta2 (Curvature):      {ns.beta2*100:.2f}%")
    print(f"  Tau (Scale factor):     {ns.tau:.2f}")

    # 2. Corporate Bond Portfolio Relative Value Analysis
    bonds = pd.DataFrame([
        {"isin": "FR0010001", "name": "TotalEnergies 3.5%", "maturity_years": 4.5, "market_yield": 0.042, "credit_rating": "A"},
        {"isin": "FR0010002", "name": "Sanofi 2.8%", "maturity_years": 5.0, "market_yield": 0.035, "credit_rating": "A"},
        {"isin": "FR0010003", "name": "Schneider 4.0%", "maturity_years": 5.2, "market_yield": 0.051, "credit_rating": "A"},
        {"isin": "FR0010004", "name": "BNP Paribas 4.5%", "maturity_years": 7.0, "market_yield": 0.048, "credit_rating": "BBB"},
        {"isin": "FR0010005", "name": "Societe Generale 5.0%", "maturity_years": 7.5, "market_yield": 0.062, "credit_rating": "BBB"},
        {"isin": "FR0010006", "name": "Carrefour 3.8%", "maturity_years": 6.8, "market_yield": 0.043, "credit_rating": "BBB"}
    ])

    analyzer = BondRelativeValueAnalyzer(ns)
    res = analyzer.analyze_portfolio(bonds)
    
    print("\n=== Corporate Bond Relative Value Trade Signals ===")
    print(res[['name', 'maturity_years', 'market_yield', 'z_spread_bps', 'z_score_peer', 'signal']].to_string(index=False))

if __name__ == "__main__":
    main()
