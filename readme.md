=== HOW TO ===

=== CHANGING CONFIG ===
1. Update the main.py file to change the tickers, features, and custom parameters
2. Comment out the upload code
3. Validate output with the CSV file
4. Uncomment the upload code
5. Update the database model (on DBeaver columns + lib/models/EquityIndicators.py)
6. Upload the data to the database

=== ADDING NEW INDICATORS ===
1. Add the feature class under lib/indicators, following the format of existing classes
2. Update the MarketIndicators class in main.py to include the new feature
3. Update the main.py file to add the  features, and corresponding custom parameters
4. Comment out the upload code
5. Validate output with the CSV file
6. Uncomment the upload code
7. Update the database model (on DBeaver columns + lib/models/EquityIndicators.py)
8. Upload the data to the database