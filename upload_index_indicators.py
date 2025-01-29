from lib.models.MarketData import MarketData
from lib.db.session import create_db_session
from lib.indicators.MarketIndicators import MarketIndicators
from lib.models.IndexIndicators import IndexIndicators

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
            
            # Delete existing records for this ticker
            deleted_count = session.query(IndexIndicators)\
                                 .filter(IndexIndicators.ticker == ticker)\
                                 .delete()
            
            print(f"[DEBUG] Deleted {deleted_count} existing records for {ticker}")
            
            # Create list to store all records
            records = []
            
            print("[DEBUG] Creating indicator objects")
            # Create IndexIndicators objects for each row
            for _, row in indicators_df.iterrows():
                indicator = IndexIndicators(
                    ticker=ticker,
                    report_date=row['Date'],
                    rsi_5=row.get('RSI_5'),
                    rsi_20=row.get('RSI_20'),
                    rsi_50=row.get('RSI_50'),  
                    rsi_200=row.get('RSI_200'),
                    pct_5=row.get('PCT_5'), 
                    pct_20=row.get('PCT_20'),
                    pct_50=row.get('PCT_50'),
                    pct_200=row.get('PCT_200')
                )
                records.append(indicator)
            
            print(f"[DEBUG] Created {len(records)} indicator objects")
            
            # Bulk insert all records
            print("[DEBUG] Starting bulk insert")
            session.bulk_save_objects(records)
            
            # Commit all changes
            session.commit()
            
            print(f"[SUCCESS] Successfully processed {len(indicators_df)} indicators for {ticker}")
            print(f"         Deleted: {deleted_count}, Inserted: {len(records)}")
            
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
       'SPX',
       'NDX'
    ]

    features = ['RSI', 'PCT']
    print(f"[DEBUG] Processing tickers: {tickers}")
    print(f"[DEBUG] Features to calculate: {features}")
    
    custom_params = {
        'RSI': {'periods': [5, 20, 50, 200]},
        'PCT': {'periods': [5, 20, 50, 200]} # Add Percentage Change
    }
    
    print("[DEBUG] Fetching market data")
    # Get market data from database
    market_data = get_market_data(
        db_session,
        tickers=tickers,
        data_type='index'
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