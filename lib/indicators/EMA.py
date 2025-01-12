import numpy as np

class EMAIndicator:
    """Calculates the Exponential Moving Average (EMA) over a specified time frame."""

    def __init__(self, indicator: np.ndarray, timeFrame: int):
        """
        Initialize EMA calculator.

        Args:
            indicator (np.ndarray): Array of price values
            timeFrame (int): Period for EMA calculation
        """
        self.indicator: np.ndarray = indicator
        self.timeFrame: int = timeFrame
        self.smoothing: float = 2.0 / (timeFrame + 1)
        
        # Pre-calculate all EMA values to avoid recursion
        self.ema_values: np.ndarray = self._calculate_all_emas()

    def _calculate_all_emas(self) -> np.ndarray:
        """Calculate all EMA values at once using numpy."""
        ema_values = np.zeros_like(self.indicator, dtype=float)
        
        # First value is just the first price
        ema_values[0] = self.indicator[0]
        
        # Calculate subsequent values
        for i in range(1, len(self.indicator)):
            ema_values[i] = (self.indicator[i] * self.smoothing + 
                           ema_values[i-1] * (1 - self.smoothing))
            
        return ema_values

    def calculate(self, index: int) -> float:
        """
        Get the EMA value for a given index.

        Args:
            index (int): The index to get EMA for.

        Returns:
            float: The EMA value.
        """
        if index < 0:
            return 0.0
        
        return float(self.ema_values[index])