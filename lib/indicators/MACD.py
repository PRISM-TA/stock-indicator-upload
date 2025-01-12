import numpy as np
from lib.indicators.EMA import EMAIndicator

class MACDIndicator:
    """Calculates the MACD (Moving Average Convergence Divergence)."""

    def __init__(self, indicator: np.ndarray, 
                 fast_period: int = 12, 
                 slow_period: int = 26,
                 signal_period: int = 9):
        """
        Initialize MACD calculator.

        Args:
            indicator (np.ndarray): Array of price values
            fast_period (int): Short-term EMA period (default: 12)
            slow_period (int): Long-term EMA period (default: 26)
            signal_period (int): Signal line EMA period (default: 9)
        """
        self.indicator: np.ndarray = indicator
        self.fast_ema = EMAIndicator(indicator, fast_period)
        self.slow_ema = EMAIndicator(indicator, slow_period)
        
        # Calculate MACD line values to use for signal line
        self.macd_values = np.array([self.calculate_macd(i) for i in range(len(indicator))])
        self.signal_ema = EMAIndicator(self.macd_values, signal_period)

    def calculate_macd(self, index: int) -> float:
        """Calculate MACD line (Fast EMA - Slow EMA)."""
        fast_value = self.fast_ema.calculate(index)
        slow_value = self.slow_ema.calculate(index)
        return float(fast_value - slow_value)

    def calculate_signal(self, index: int) -> float:
        """Calculate Signal line (EMA of MACD line)."""
        return float(self.signal_ema.calculate(index))

    def calculate_histogram(self, index: int) -> float:
        """Calculate MACD histogram (MACD line - Signal line)."""
        macd_value = self.calculate_macd(index)
        signal_value = self.calculate_signal(index)
        return float(macd_value - signal_value)