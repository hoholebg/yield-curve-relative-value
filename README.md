# 📉 Yield Curve Dynamics & Corporate Bond Relative Value

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Yield curve parametric fitting engine (Nelson-Siegel & Svensson models) and credit spread relative value analyzer for institutional corporate bond portfolios ($1B+ AUM context).

## ⚡ Highlights
- **Nelson-Siegel Parameterization**: Non-linear optimization fitting zero-coupon benchmark curves across maturities from 3 months to 30 years.
- **Z-Spread & Basis Extraction**: Quantifies credit risk premium over benchmark curves.
- **Relative Value Trade Generator**: Detects mispriced bonds within credit rating peer groups (BUY/SELL signals based on Z-scores).

## 🚀 Quickstart
```bash
pip install -r requirements.txt
python main.py
```
