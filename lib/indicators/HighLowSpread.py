import numpy as np

class HighLowSpreadIndicator:
    """Calculates the High-Low Spread (price range) over a specified time frame."""

    def __init__(self, high_prices: np.ndarray, low_prices: np.ndarray, timeFrame: int = 14):
        """
        Initialize High-Low Spread calculator.

        Args:
            high_prices (np.ndarray): Array of high prices
            low_prices (np.ndarray): Array of low prices
            timeFrame (int): Period for spread calculation (default: 14 days)
        """
        self.high_prices: np.ndarray = high_prices
        self.low_prices: np.ndarray = low_prices
        self.timeFrame: int = timeFrame
        
    def calculate(self, index: int) -> float:
        """
        Calculate the average High-Low Spread for a given index.

        Args:
            index (int): The index to calculate spread for.

        Returns:
            float: The average spread value as a percentage of the low price.
        """
        if index < 0:
            return 0.0
            
        # Get the window of prices
        start_index: int = max(0, index - self.timeFrame + 1)
        high_window: np.ndarray = self.high_prices[start_index:index + 1]
        low_window: np.ndarray = self.low_prices[start_index:index + 1]
        
        if len(high_window) == 0 or len(low_window) == 0:
            return 0.0
            
        # Calculate daily spreads as percentage
        daily_spreads: np.ndarray = ((high_window - low_window) / low_window) * 100
        
        # Return average spread over the period
        return float(np.mean(daily_spreads))