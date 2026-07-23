"""
Corporate Bond Relative Value & Credit Spread Arbitrage Identification
"""

import numpy as np
import pandas as pd
from src.nelson_siegel import NelsonSiegelCurve

class BondRelativeValueAnalyzer:
    """Identifies mispriced corporate bonds against modeled benchmark yield curves."""
    
    def __init__(self, curve: NelsonSiegelCurve):
        self.curve = curve

    def analyze_portfolio(self, bonds_df: pd.DataFrame) -> pd.DataFrame:
        """
        Calculates theoretical yields, Z-spreads, and flags trading signals.
        bonds_df must contain: ['isin', 'maturity_years', 'market_yield', 'credit_rating']
        """
        df = bonds_df.copy()
        df['theoretical_benchmark_yield'] = df['maturity_years'].apply(self.curve.yield_at_maturity)
        df['z_spread_bps'] = (df['market_yield'] - df['theoretical_benchmark_yield']) * 10000
        
        # Relative Value Z-score within credit rating peer group
        df['z_score_peer'] = df.groupby('credit_rating')['z_spread_bps'].transform(
            lambda x: (x - x.mean()) / (x.std() if x.std() > 0 else 1.0)
        )
        
        # Trading Signal: Buy if bond yield is abnormally high (Z-score > +1.5), Sell if yield too low (Z-score < -1.5)
        df['signal'] = 'HOLD'
        df.loc[df['z_score_peer'] > 1.5, 'signal'] = 'BUY (UNDERVLUED)'
        df.loc[df['z_score_peer'] < -1.5, 'signal'] = 'SELL (OVERVALUED)'
        
        return df
