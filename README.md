# Black-Scholes Option Pricer

A Python implementation of the Black-Scholes option pricing model with full Greeks calculation.

## Installation
```bash
pip install numpy scipy
```

## Usage
```python
from black_scholes import BlackScholes

option = BlackScholes(
    S=100,           # Current stock price
    K=100,         # Strike price
    T=1.0, # Time to expiration in years
    r=0.05,# Risk-free rate (5%)
    sigma=0.20     # Volatility (20%)
)

# Get individual values
print(option.call_price())
print(option.call_delta())
print(option.gamma())

# Get full summary
option.summary()
```

## Greeks Included

| Greek | Description |
|-------|-------------|
| Delta | Price sensitivity to underlying movement |
| Gamma | Rate of change of delta |
| Theta | Time decay (daily by default) |
| Vega | Sensitivity to volatility changes |
| Rho | Sensitivity to interest rate changes |

## Assumptions

This implementation assumes:
- European-style options (no early exercise)
- No dividends
- Constant volatility
- Constant risk-free rate
