import numpy as np

class RealizedVolatilityIndicator:
    """Calculates the Realized Volatility over a specified time frame."""

    def __init__(self, indicator: np.ndarray, timeFrame: int = 21, trading_days: int = 252):
        """
        Initialize Realized Volatility calculator.

        Args:
            indicator (np.ndarray): Array of price values
            timeFrame (int): Period for volatility calculation (default: 21 days)
            trading_days (int): Number of trading days in a year (default: 252)
        """
        self.indicator: np.ndarray = indicator
        self.timeFrame: int = timeFrame
        self.trading_days: int = trading_days
        
    def calculate(self, index: int) -> float:
        """
        Calculate the annualized Realized Volatility for a given index.
        Returns 0.0 if there isn't enough data in the lookback window.

        Args:
            index (int): The index to calculate volatility for.

        Returns:
            float: The annualized volatility value as a percentage, or 0.0 if insufficient data.
        """
        # Return 0 if we don't have enough data points for the full window
        if index < self.timeFrame - 1:
            return 0.0
            
        # Get the window of prices
        start_index: int = index - self.timeFrame + 1
        prices: np.ndarray = self.indicator[start_index:index + 1]
        
        # Verify we have the correct window size
        if len(prices) != self.timeFrame:
            return 0.0
            
        # Calculate daily returns
        returns: np.ndarray = np.diff(np.log(prices))
        
        # Calculate volatility
        daily_vol: float = np.std(returns, ddof=1)  # Using sample standard deviation
        
        # Annualize volatility and convert to percentage
        annual_vol: float = daily_vol * np.sqrt(self.trading_days) * 100
        
        return float(annual_vol)