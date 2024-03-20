import pandas as pd

# Data Parsing and Cleanup
# Read the CSV file
df = pd.read_csv('trading_log.csv', parse_dates=['Timestamp'])

# Read the CSV file containing security exchange mapping
symbol_exchange_df = pd.read_csv('security_exchange_mapping.csv')

# Read the CSV file containing average prices for symbols
average_prices_df = pd.read_csv('average_prices.csv')

# Merge the two CSV files with trading log data
df = pd.merge(df, symbol_exchange_df, on='Symbol', how='left')
df = pd.merge(df, average_prices_df, on='Symbol', how='left')

# Print the first few rows to inspect the data
print("Original Data:")
print(df.head())

# Check for missing values
print("\nMissing Values:")
print(df.isnull().sum())

# Handle missing values (e.g., drop rows with missing values or fill with appropriate values)
df = df.dropna(subset=['Order ID', 'Trader', 'Exchange_x', 'Symbol', 'Order Type', 'Order Size', 'Fill Size', 'Price', 'Symbol', 'Exchange_y', 'Average Price'])

# Convert data types if necessary
df['Order Size'] = df['Order Size'].astype(float)
df['Fill Size'] = df['Fill Size'].astype(float)
df['Price'] = df['Price'].astype(float)
df['Average Price'] = df['Average Price'].astype(float)

# Calculate additional features
df['Slippage'] = abs(df['Price'] - df['Fill Size'] / df['Order Size'])
df['Position'] = df.groupby(['Trader', 'Symbol'])['Fill Size'].cumsum()

# Print the updated DataFrame
print("\nProcessed Data:")
print(df.head())

# Check if the exchange in the trading log matches the correct exchange for each symbol
df['Exchange Match'] = df['Exchange_x'] == df['Exchange_y']

# Filter out trades where the exchange information does not match
mismatched_trades = df[~df['Exchange Match']]

# Print the mismatched trades
print("\nMismatched Trades:")
print(mismatched_trades)

# Establish Baseline
# Calculate statistical measures for various metrics
order_size_stats = df['Order Size'].describe()
fill_size_stats = df['Fill Size'].describe()
slippage_stats = df['Slippage'].describe()

# Print the statistical measures
print("\nOrder Size Statistics:")
print(order_size_stats)
print("\nFill Size Statistics:")
print(fill_size_stats)
print("\nSlippage Statistics:")
print(slippage_stats)

# Identify normal ranges
order_size_mean = order_size_stats['mean']
order_size_std = order_size_stats['std']
order_size_normal_range = (order_size_mean - 2 * order_size_std, order_size_mean + 2 * order_size_std)

fill_size_mean = fill_size_stats['mean']
fill_size_std = fill_size_stats['std']
fill_size_normal_range = (fill_size_mean - 2 * fill_size_std, fill_size_mean + 2 * fill_size_std)

slippage_mean = slippage_stats['mean']
slippage_std = slippage_stats['std']
slippage_normal_range = (slippage_mean - 2 * slippage_std, slippage_mean + 2 * slippage_std)

print("\nNormal Ranges:")
print("Order Size Normal Range:", order_size_normal_range)
print("Fill Size Normal Range:", fill_size_normal_range)
print("Slippage Normal Range:", slippage_normal_range)

# Identify Anomalies
# Detect outliers based on normal ranges
order_size_outliers = df[(df['Order Size'] < order_size_normal_range[0]) | (df['Order Size'] > order_size_normal_range[1])]
fill_size_outliers = df[(df['Fill Size'] < fill_size_normal_range[0]) | (df['Fill Size'] > fill_size_normal_range[1])]
slippage_outliers = df[(df['Slippage'] < slippage_normal_range[0]) | (df['Slippage'] > slippage_normal_range[1])]
print("\nOrder Size Anomalies:")
print(order_size_outliers)
print("\nFill Size Anomalies:")
print(fill_size_outliers)
print("\nSlippage Anomalies:")
print(slippage_outliers)

# Detect unusual order sequences
df['Order Sequence'] = df.groupby(['Trader', 'Symbol'])['Order ID'].rank().astype(int)
unusual_order_sequences = df[df.groupby(['Trader', 'Symbol'])['Order Sequence'].diff().abs() > 1]
print("\nUnusual Order Sequences:")
print(unusual_order_sequences)

# Detect excessive trading activity
trading_volume = df.groupby(['Trader', 'Symbol', pd.Grouper(freq='1h', key='Timestamp')])['Order Size'].sum()
excessive_trading = trading_volume[trading_volume > trading_volume.quantile(0.99)]
print("\nExcessive Trading Activity:")
print(excessive_trading)

# Detect anomalies in price difference
price_difference_stats = df['Average Price'].describe()
price_difference_mean = price_difference_stats['mean']
price_difference_std = price_difference_stats['std']
price_difference_normal_range = (price_difference_mean - 2 * price_difference_std, price_difference_mean + 2 * price_difference_std)
price_difference_outliers = df[(df['Average Price'] < price_difference_normal_range[0]) | (df['Average Price'] > price_difference_normal_range[1])]
print("\nPrice Difference Anomalies:")
print(price_difference_outliers)

# Concatenate the DataFrame 
anomalies = pd.concat([order_size_outliers, fill_size_outliers, slippage_outliers, unusual_order_sequences, excessive_trading], ignore_index=True)
anomalies = anomalies.drop_duplicates()
print("\nAnomalies:")
print(anomalies)

# Calculate trader positions at the start and end of the trading day
start_of_day = df['Timestamp'].min()
end_of_day = df['Timestamp'].max()

# Group both Trader and Timestamp to get each trader (a frequency of one day)
trader_positions_start = df.groupby(['Trader', pd.Grouper(key='Timestamp', freq='D')])['Position'].first()
trader_positions_end = df.groupby(['Trader', pd.Grouper(key='Timestamp', freq='D')])['Position'].last()

print("\nTrader Positions at Start of Day:")
print(trader_positions_start)
print("\nTrader Positions at End of Day:")
print(trader_positions_end)