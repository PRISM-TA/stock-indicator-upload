import numpy as np

class PercentageChangeIndicator:
    """Calculates the percentage change over a specified time frame."""

    def __init__(self, indicator: np.ndarray, timeFrame: int = 5):
        """
        Initialize the percentage change indicator.

        Args:
            indicator (np.ndarray): Array of price/value data
            timeFrame (int): Number of days to calculate percentage change over (default=5)
        """
        self.indicator: np.ndarray = indicator
        self.timeFrame: int = timeFrame

    def calculate(self, index: int) -> float:
        """
        Calculate the percentage change for a given index.

        Args:
            index (int): The index to calculate percentage change for.

        Returns:
            float: The percentage change value.
            Returns 0.0 if there's not enough historical data.
        """
        if index < self.timeFrame - 1:
            return 0.0

        current_value: float = self.indicator[index]
        past_value: float = self.indicator[index - (self.timeFrame - 1)]
        
        # Avoid division by zero
        if past_value == 0:
            return 0.0
            
        return ((current_value - past_value) / past_value) * 100.0