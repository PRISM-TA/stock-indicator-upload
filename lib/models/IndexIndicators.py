from sqlalchemy import Column, Date, Float, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class IndexIndicators(Base):
    __tablename__ = 'index_indicators'
    __table_args__ = {'schema': 'fyp'}

    # Composite primary key
    ticker = Column(String, primary_key=True)
    report_date = Column(Date, primary_key=True)
    
    # Technical indicators
    rsi_5 = Column(Float(4))
    rsi_20 = Column(Float(4))
    rsi_50 = Column(Float(4))
    rsi_200 = Column(Float(4))
    pct_5 = Column(Float(4)) # Add Percentage Change 
    pct_20 = Column(Float(4)) # Add Percentage Change
    pct_50 = Column(Float(4)) # Add Percentage Change
    pct_200 = Column(Float(4)) # Add Percentage Change

    def __repr__(self):
        return f"<IndexIndicators(date={self.report_date}, ticker={self.ticker})>"