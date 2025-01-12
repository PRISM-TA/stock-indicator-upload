from lib.models.MarketData import MarketData
from lib.db.session import create_db_session
from lib.indicators.MarketIndicators import MarketIndicators
from lib.models.EquityIndicators import EquityIndicators

from dotenv import load_dotenv
import os
from sqlalchemy import select, and_
import pandas as pd

def get_market_data(db_session, 
                   tickers=None, 
                   start_date=None, 
                   end_date=None, 
                   data_type=None):
    print("\n[DEBUG] Starting get_market_data function")
    print(f"[DEBUG] Parameters: tickers={tickers}, start_date={start_date}, end_date={end_date}, data_type={data_type}")
    
    try:
        with db_session() as session:
            # Start building the query
            query = select(MarketData)
            
            # Apply conditions if provided
            conditions = []
            if tickers:
                conditions.append(MarketData.ticker.in_(tickers))
            if start_date:
                conditions.append(MarketData.report_date >= start_date)
            if end_date:
                conditions.append(MarketData.report_date <= end_date)
            if data_type:
                conditions.append(MarketData.type == data_type)
                
            # Add all conditions using where
            if conditions:
                query = query.where(and_(*conditions))
                
            # Execute query
            print("[DEBUG] Executing database query")
            results = session.execute(query).scalars().all()
            print(f"[DEBUG] Query returned {len(results)} records")
            
            # Convert results to dictionary of DataFrames
            data_dict = {}
            for result in results:
                ticker = result.ticker
                if ticker not in data_dict:
                    data_dict[ticker] = []
                    
                data_dict[ticker].append({
                    'Date': result.report_date,
                    'Open': result.open,
                    'Close': result.close,
                    'Low': result.low,
                    'High': result.high,
                    'Volume': result.volume,
                    'Type': result.type
                })
            
            # Convert lists to DataFrames
            print("[DEBUG] Converting results to DataFrames")
            for ticker in data_dict:
                data_dict[ticker] = pd.DataFrame(data_dict[ticker])
                data_dict[ticker].set_index('Date', inplace=True)
                data_dict[ticker].sort_index(inplace=True)
                print(f"[DEBUG] DataFrame for {ticker} shape: {data_dict[ticker].shape}")
                
            return data_dict
            
    except Exception as e:
        print(f"[ERROR] Error in get_market_data: {str(e)}")
        raise

def upload_indicators(db_session, indicators_df, ticker):
    print(f"\n[DEBUG] Starting upload_indicators for {ticker}")
    print(f"[DEBUG] Indicators DataFrame shape: {indicators_df.shape}")
    
    try:
        with db_session() as session:
            # Convert index to column
            indicators_df = indicators_df.reset_index()
            
            # Create list to store all records
            records = []
            
            print("[DEBUG] Creating indicator objects")
            # Create EquityIndicators objects for each row
            for _, row in indicators_df.iterrows():
                indicator = EquityIndicators(
                    ticker=ticker,
                    report_date=row['Date'],
                    rsi_1=row.get('RSI_1'),
                    rsi_2=row.get('RSI_2'),
                    rsi_3=row.get('RSI_3'),
                    rsi_4=row.get('RSI_4'),
                    rsi_5=row.get('RSI_5'),
                    rsi_6=row.get('RSI_6'),
                    rsi_7=row.get('RSI_7'),
                    rsi_8=row.get('RSI_8'),
                    rsi_9=row.get('RSI_9'),
                    rsi_10=row.get('RSI_10'),
                    rsi_11=row.get('RSI_11'),
                    rsi_12=row.get('RSI_12'),
                    rsi_13=row.get('RSI_13'),
                    rsi_14=row.get('RSI_14'),
                    rsi_15=row.get('RSI_15'),
                    rsi_16=row.get('RSI_16'),
                    rsi_17=row.get('RSI_17'),
                    rsi_18=row.get('RSI_18'),
                    rsi_19=row.get('RSI_19'),
                    rsi_20=row.get('RSI_20'),
                    sma_10=row.get('SMA_10'),
                    sma_20=row.get('SMA_20'),
                    sma_50=row.get('SMA_50'),
                    sma_200=row.get('SMA_200'),
                    ema_10=row.get('EMA_10'),
                    ema_20=row.get('EMA_20'),
                    ema_50=row.get('EMA_50'),
                    ema_200=row.get('EMA_200'),
                    macd_12_26_9_line=row.get('MACD_12_26_9_line'),
                    macd_12_26_9_signal=row.get('MACD_12_26_9_signal'),
                    macd_12_26_9_histogram=row.get('MACD_12_26_9_histogram'),
                    rv_10=row.get('RV_10'),
                    rv_20=row.get('RV_20'),
                    rv_30=row.get('RV_30'),
                    rv_60=row.get('RV_60'),
                    hls_10=row.get('HLS_10'),
                    hls_20=row.get('HLS_20'),
                    obv=row.get('OBV')
                )
                records.append(indicator)
            
            print(f"[DEBUG] Created {len(records)} indicator objects")
            
            # Bulk insert records
            print("[DEBUG] Starting bulk insert")
            session.bulk_save_objects(records)
            session.commit()
            
            print(f"[SUCCESS] Successfully uploaded {len(records)} indicators for {ticker}")
            
    except Exception as e:
        print(f"[ERROR] Error in upload_indicators for {ticker}: {str(e)}")
        session.rollback()
        raise

def main():
    print("\n[DEBUG] Starting main function")
    load_dotenv()

    print("[DEBUG] Setting up database connection")
    # Setup database connection
    db_session = create_db_session(
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME")
    )
    
    print("[DEBUG] Initializing market indicators calculator")
    # Initialize market indicators calculator
    indicator_calculator = MarketIndicators()
    
    # Define parameters
    tickers = [
        'UNH',
        'MSFT',
        'MMM',
        'MRK',
        'HD',
        'DD',
        'KO',
        'VZ',
        'PG',
        'NKE',
        'GE',
        'CVX',
        'CAT',
        'XOM',
        'TRV',
        'UTX',
        'PFE',
        'BA',
        'WMT',
        'INTC',
        'AXP',
        'CSCO',
        'JPM',
        'JNJ',
        'MCD',
        'DIS',
        'IBM'
    ]

    features = ['RSI', 'SMA', 'EMA', 'MACD', 'RV', 'HLS', 'OBV']
    print(f"[DEBUG] Processing tickers: {tickers}")
    print(f"[DEBUG] Features to calculate: {features}")
    
    custom_params = {
        'RSI': {'periods': range(1, 21)},
        'SMA': {'periods': [10, 20, 50, 200]},
        'EMA': {'periods': [10, 20, 50, 200]},
        'MACD': {
                'fast_period': 12,
                'slow_period': 26,
                'signal_period': 9
        },
        'RV': {'periods': [10, 20, 30, 60]},
        'HLS': {'periods': [10, 20]},
        'OBV': {}
    }
    
    print("[DEBUG] Fetching market data")
    # Get market data from database
    market_data = get_market_data(
        db_session,
        tickers=tickers,
        data_type='equity'
    )
    
    # Calculate indicators for each ticker and upload to database
    for ticker, df in market_data.items():
        print(f"\n[DEBUG] Processing ticker: {ticker}")
        print(f"[DEBUG] Market data shape for {ticker}: {df.shape}")
        
        print(f"[DEBUG] Calculating indicators for {ticker}")
        indicators_df = indicator_calculator.calculate_features(
            df,
            features=features,
            custom_params=custom_params
        )
        
        print(f"[DEBUG] Uploading indicators for {ticker}")
        upload_indicators(db_session, indicators_df, ticker)
        
        print(f"[DEBUG] Saving backup CSV for {ticker}")
        indicators_df.to_csv(f"indicators_{ticker}.csv")
        print(f"[DEBUG] Completed processing for {ticker}")

if __name__ == "__main__":
    print("[DEBUG] Script started")
    main()
    print("[DEBUG] Script completed")