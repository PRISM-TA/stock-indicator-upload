from lib.indicators.RSI import RSIIndicator
from lib.indicators.SMA import SMAIndicator
from lib.indicators.EMA import EMAIndicator
from lib.indicators.MACD import MACDIndicator
from lib.indicators.RealizedVolatility import RealizedVolatilityIndicator
from lib.indicators.HighLowSpread import HighLowSpreadIndicator
from lib.indicators.OBV import OBVIndicator

from typing import List, Dict, Callable, Any
import pandas as pd
import numpy as np

class MarketIndicators:
    """Handles calculation of technical indicators for stock market data."""
    
    def __init__(self):
        self.feature_calculators: Dict[str, Callable] = {
            'RSI': self._calculate_rsi_features,
            'SMA': self._calculate_sma_features,
            'EMA': self._calculate_ema_features,
            'MACD': self._calculate_macd_features,
            'RV': self._calculate_rv_features,
            'HLS': self._calculate_hls_features,
            'OBV': self._calculate_obv_features
        }
        
        self.default_params: Dict[str, Dict[str, Any]] = {
            'RSI': {'periods': range(1, 21)},
            'SMA': {'periods': [50, 200]},
            'EMA': {'periods': [12, 26]},
            'MACD': {
                'fast_period': 12,
                'slow_period': 26,
                'signal_period': 9
            },
            'RV': {'periods': [10, 20, 30, 60]},
            'HLS': {'periods': [10, 20]},
            'OBV': {}
        }
    
    def _calculate_rsi_features(self, df: pd.DataFrame, close_prices: np.ndarray, 
                              params: Dict[str, Any]) -> pd.DataFrame:
        """Calculates RSI indicators for specified periods with padding."""

        def _apply_rsi_padding(df: pd.DataFrame, period: int) -> None:
            """Applies padding to the beginning and end of the DataFrame."""
            df.iloc[0, df.columns.get_loc(f'RSI_{period}')] = 0.0
            df.iloc[1, df.columns.get_loc(f'RSI_{period}')] = 100.0
            
            for j in range(2, len(df)):
                if j < period:
                    df.iloc[j, df.columns.get_loc(f'RSI_{period}')] = df.iloc[j, df.columns.get_loc(f'RSI_{j}')]
                    
        for period in params['periods']:
            rsi_indicator: RSIIndicator = RSIIndicator(close_prices, period)
            df[f'RSI_{period}'] = [rsi_indicator.calculate(j) for j in range(len(df))]
            print(df.head())
            _apply_rsi_padding(df, period)
        return df
    
    def _calculate_sma_features(self, df: pd.DataFrame, close_prices: np.ndarray, 
                              params: Dict[str, Any]) -> pd.DataFrame:
        """Calculates SMA indicators for specified periods."""
        for period in params['periods']:
            sma_indicator: SMAIndicator = SMAIndicator(close_prices, period)
            df[f'SMA_{period}'] = [sma_indicator.calculate(j) for j in range(len(df))]
        return df

    def _calculate_ema_features(self, df: pd.DataFrame, close_prices: np.ndarray, 
                              params: Dict[str, Any]) -> pd.DataFrame:
        """Calculates EMA indicators for specified periods."""
        for period in params['periods']:
            ema_indicator: EMAIndicator = EMAIndicator(close_prices, period)
            df[f'EMA_{period}'] = [ema_indicator.calculate(j) for j in range(len(df))]
        return df
    
    def _calculate_macd_features(self, df: pd.DataFrame, close_prices: np.ndarray, 
                               params: Dict[str, Any]) -> pd.DataFrame:
        """
        Calculates MACD indicators (MACD line, Signal line, and Histogram).
        """
        macd_indicator = MACDIndicator(
            close_prices,
            fast_period=params.get('fast_period', 12),
            slow_period=params.get('slow_period', 26),
            signal_period=params.get('signal_period', 9)
        )

        # Calculate MACD components
        df[f'MACD_{params.get('fast_period', 12)}_{params.get('slow_period', 26)}_{params.get('signal_period', 9)}_line'] = [macd_indicator.calculate_macd(j) for j in range(len(df))]
        df[f'MACD_{params.get('fast_period', 12)}_{params.get('slow_period', 26)}_{params.get('signal_period', 9)}_signal'] = [macd_indicator.calculate_signal(j) for j in range(len(df))]
        df[f'MACD_{params.get('fast_period', 12)}_{params.get('slow_period', 26)}_{params.get('signal_period', 9)}_histogram'] = [macd_indicator.calculate_histogram(j) for j in range(len(df))]
        
        return df
    
    def _calculate_rv_features(self, df: pd.DataFrame, close_prices: np.ndarray, 
                             params: Dict[str, Any]) -> pd.DataFrame:
        """
        Calculates Realized Volatility for specified periods.
        """
        trading_days = params.get('trading_days', 252)
        
        for period in params['periods']:
            rv_indicator = RealizedVolatilityIndicator(
                close_prices,
                timeFrame=period,
                trading_days=trading_days
            )
            
            # Calculate and store volatility values
            df[f'RV_{period}'] = [rv_indicator.calculate(j) for j in range(len(df))]
            
        return df

    def _calculate_hls_features(self, df: pd.DataFrame, 
                              params: Dict[str, Any]) -> pd.DataFrame:
        """
        Calculates High-Low Spread for specified periods.
        """
        high_prices: np.ndarray = df['High'].values
        low_prices: np.ndarray = df['Low'].values
        
        for period in params['periods']:
            hls_indicator = HighLowSpreadIndicator(
                high_prices=high_prices,
                low_prices=low_prices,
                timeFrame=period
            )
            
            # Calculate and store spread values
            df[f'HLS_{period}'] = [hls_indicator.calculate(j) for j in range(len(df))]
            
        return df

    def _calculate_obv_features(self, df: pd.DataFrame, close_prices: np.ndarray, 
                                params: Dict[str, Any]) -> pd.DataFrame:
            """
            Calculates On-Balance Volume (OBV) and its moving average if specified.
            """
            volume: np.ndarray = df['Volume'].values
            
            # Calculate OBV
            obv_indicator = OBVIndicator(close_prices, volume)
            df['OBV'] = [obv_indicator.calculate(j) for j in range(len(df))]
            
            return df

    def calculate_features(self, df: pd.DataFrame, 
                         features: List[str] = None, 
                         custom_params: Dict[str, Dict[str, Any]] = None) -> pd.DataFrame:
        """Calculates specified technical indicators for the given data."""
        
        # Create a copy to avoid modifying original data
        df = df.copy()
        
        # Extract close prices
        close_prices: np.ndarray = df['Close'].values
        
        features = features or list(self.feature_calculators.keys())
        params = {**self.default_params}
        if custom_params:
            params.update(custom_params)
        
        for feature in features:
            if feature in self.feature_calculators:
                if feature == 'HLS':
                    df = self.feature_calculators[feature](df, params[feature])
                else:
                    df = self.feature_calculators[feature](df, close_prices, params[feature])
        
        return df