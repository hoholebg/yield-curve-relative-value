"""
Nelson-Siegel & Svensson Yield Curve Parametric Fitting Models
"""

import numpy as np
from scipy.optimize import minimize

class NelsonSiegelCurve:
    """
    Nelson-Siegel yield curve parameterization:
    y(t) = beta0 + beta1 * ((1 - exp(-t/tau)) / (t/tau)) + beta2 * (((1 - exp(-t/tau)) / (t/tau)) - exp(-t/tau))
    """
    
    def __init__(self, beta0: float = 0.03, beta1: float = -0.02, beta2: float = 0.01, tau: float = 2.0):
        self.beta0 = beta0
        self.beta1 = beta1
        self.beta2 = beta2
        self.tau = tau

    def yield_at_maturity(self, t: float) -> float:
        if t <= 0:
            return float(self.beta0 + self.beta1)
        factor1 = (1.0 - np.exp(-t / self.tau)) / (t / self.tau)
        factor2 = factor1 - np.exp(-t / self.tau)
        return float(self.beta0 + self.beta1 * factor1 + self.beta2 * factor2)

    def fit(self, maturities: np.ndarray, observed_yields: np.ndarray):
        """Fit Nelson-Siegel parameters to observed market yields via SLSQP optimization."""
        def objective(params):
            b0, b1, b2, t_val = params
            if t_val <= 0.01:
                return 1e9
            pred = np.array([NelsonSiegelCurve(b0, b1, b2, t_val).yield_at_maturity(m) for m in maturities])
            return np.sum((pred - observed_yields) ** 2)

        init_params = [0.03, -0.01, 0.01, 2.0]
        res = minimize(objective, init_params, method="Nelder-Mead")
        self.beta0, self.beta1, self.beta2, self.tau = res.x
        return self
