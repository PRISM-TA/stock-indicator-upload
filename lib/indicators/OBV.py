import numpy as np

class OBVIndicator:
    """Calculates the On-Balance Volume (OBV)."""

    def __init__(self, close_prices: np.ndarray, volume: np.ndarray):
        """
        Initialize OBV calculator.

        Args:
            close_prices (np.ndarray): Array of closing prices
            volume (np.ndarray): Array of volume values
        """
        self.close_prices: np.ndarray = close_prices
        self.volume: np.ndarray = volume
        self._calculate_all_obv()
        
    def _calculate_all_obv(self) -> None:
        """Pre-calculate all OBV values efficiently."""
        self.obv_values = np.zeros(len(self.volume))
        
        # Initialize first value
        self.obv_values[0] = self.volume[0]
        
        # Calculate subsequent values
        for i in range(1, len(self.close_prices)):
            if self.close_prices[i] > self.close_prices[i-1]:
                self.obv_values[i] = self.obv_values[i-1] + self.volume[i]
            elif self.close_prices[i] < self.close_prices[i-1]:
                self.obv_values[i] = self.obv_values[i-1] - self.volume[i]
            else:
                self.obv_values[i] = self.obv_values[i-1]
        
    def calculate(self, index: int) -> float:
        """
        Get the OBV value for a given index.

        Args:
            index (int): The index to get OBV for.

        Returns:
            float: The OBV value.
        """
        if 0 <= index < len(self.obv_values):
            return float(self.obv_values[index])
        return 0.0