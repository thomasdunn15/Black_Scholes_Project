import numpy as np
from scipy.stats import norm

class BlackScholes:
    def __init__(self, S, K, T, r, sigma):
        """
        S: Current stock price
        K: Strike price
        T: Time to expiration in years
        r: Risk-free interest rate (decimal)
        sigma: Volatility (decimal)
        """

        self.S = S
        self.K = K
        self.T = T
        self.r = r
        self.sigma = sigma

        self.d1 = self._calculate_d1()
        self.d2 = self._calculate_d2()

    def _calculate_d1(self):
        """
        This whole function should just be the formula of d1 which is [ln(S/K) + (r + σ²/2) × T] / (σ × √T)
        I need to break this down and get the variables and then take the respective calculations of those variables
        and then return that value
        """

        numerator = (
                np.log(self.S / self.K)
                + (self.r + (self.sigma ** 2) / 2) * self.T
        )
        denominator = self.sigma * np.sqrt(self.T)

        return numerator / denominator

    def _calculate_d2(self):
        #this function should just be d1 - volatility times sqrt of time

        return self.d1 - self.sigma * np.sqrt(self.T)

    def call_price(self):
        """
        call price is just getting the call price which is determined by this formula: S×N(d1) - K×e^(-rT)×N(d2)
        """

        discount_factor = np.exp(-self.r * self.T)

        return (
                self.S * norm.cdf(self.d1)
                - self.K * discount_factor * norm.cdf(self.d2)
        )

    def put_price(self):
        """
        Put price is the inverse of call price determined by this formula: K×e^(-rT)×N(-d2) - S×N(-d1)
        """

        discount_factor = np.exp(-self.r * self.T)

        return (
                self.K * discount_factor * norm.cdf(-self.d2)
                - self.S * norm.cdf(-self.d1)
        )

    def call_delta(self):
        """ Should just be derivative of d1 or cumulative normal distribution of d1"""
        return norm.cdf(self.d1)

    def put_delta(self):
        """same thing as call delta, just -1 to get the negative delta"""
        return norm.cdf(self.d1) - 1

    def gamma(self):
        """This function should find the derivative of delta using this function: n(d1) / (S×σ×√T)"""
        denominator = self.S * self.sigma * np.sqrt(self.T)

        return norm.pdf(self.d1) / denominator


    def call_theta(self):
        """
        This should find the time decay noted by this formula: -[S×n(d1)×σ]/(2√T) - r×K×e^(-rT)×N(d2)
        Make sure to recognize the distinction of This formula from the put_theta formula.
        """

        priceDistVol = -(self.S * norm.pdf(self.d1) * self.sigma)/(2 * np.sqrt(self.T))
        rateStrikeExp = self.r * self.K * np.exp(-self.r * self.T)

        return (priceDistVol - rateStrikeExp*norm.cdf(self.d2)) / 365



    def put_theta(self):

        priceDistVol = -(self.S * norm.pdf(self.d1) * self.sigma) / (2 * np.sqrt(self.T))
        rateStrikeExp = self.r * self.K * np.exp(-self.r * self.T)

        return (priceDistVol + rateStrikeExp * norm.cdf(-self.d2)) / 365

    def vega(self):
        """
        This function should return How much the option price changes when
        implied volatility changes by 1%. Function is S×√T×n(d1)
        """

        return (self.S * np.sqrt(self.T) * norm.pdf(self.d1)) / 100

    def call_rho(self):
        """
        Different for calls and puts, rho calculates how much
        the option price changes when interest rates change by 1%.
        Function for call_rho is: K×T×e^(-rT)×N(d2).
        """

        return (self.K * self.T * np.exp(-self.r * self.T)*norm.cdf(self.d2)) / 100


    def put_rho(self):
        return (-self.K * self.T * np.exp(-self.r * self.T)*norm.cdf(-self.d2)) / 100

    def summary(self):
        print(f"{'=' * 40}")
        print(f"Black-Scholes Option Pricer")
        print(f"{'=' * 40}")
        print(f"Stock Price (S):     ${self.S:.2f}")
        print(f"Strike Price (K):    ${self.K:.2f}")
        print(f"Time to Expiry (T):  {self.T:.4f} years")
        print(f"Risk-Free Rate (r):  {self.r * 100:.2f}%")
        print(f"Volatility (σ):      {self.sigma * 100:.2f}%")
        print(f"{'=' * 40}")
        print(f"Call Price:          ${self.call_price():.4f}")
        print(f"Put Price:           ${self.put_price():.4f}")
        print(f"{'=' * 40}")
        print(f"Call Delta:          {self.call_delta():.4f}")
        print(f"Put Delta:           {self.put_delta():.4f}")
        print(f"Gamma:               {self.gamma():.4f}")
        print(f"Call Theta (daily):  {self.call_theta():.4f}")
        print(f"Put Theta (daily):   {self.put_theta():.4f}")
        print(f"Vega (per 1%):       {self.vega():.4f}")
        print(f"Call Rho (per 1%):   {self.call_rho():.4f}")
        print(f"Put Rho (per 1%):    {self.put_rho():.4f}")
        print(f"{'=' * 40}")

if __name__ == '__main__':
    option = BlackScholes(S=100, K=100, T=1.0, r=0.05, sigma=0.20)
    print(option.summary())
