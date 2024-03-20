import pandas as pd
import matplotlib.pyplot as plt

# Part 1: Data Parsing and Preprocessing
# Read the CSV file
df = pd.read_csv('trading_log.csv', parse_dates=['Timestamp'])

# Print the first few rows to inspect the data
print("Original Data:")
print(df.head())

# Check for missing values
print("\nMissing Values:")
print(df.isnull().sum())

# Handle missing values (e.g., drop rows with missing values or fill with appropriate values)
df = df.dropna(subset=['Order ID', 'Trader', 'Exchange', 'Symbol', 'Order Type', 'Order Size', 'Fill Size', 'Price'])

# Convert data types if necessary
df['Order Size'] = df['Order Size'].astype(float)
df['Fill Size'] = df['Fill Size'].astype(float)
df['Price'] = df['Price'].astype(float)

# Calculate additional features
df['Slippage'] = abs(df['Price'] - df['Fill Size'] / df['Order Size'])

# Print the updated DataFrame
print("\nPreprocessed Data:")
print(df.head())

# Part 2: Establish Baseline
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

# Part 3: Identify Anomalies
# Detect outliers based on normal ranges
order_size_outliers = df[(df['Order Size'] < order_size_normal_range[0]) | (df['Order Size'] > order_size_normal_range[1])]
fill_size_outliers = df[(df['Fill Size'] < fill_size_normal_range[0]) | (df['Fill Size'] > fill_size_normal_range[1])]
slippage_outliers = df[(df['Slippage'] < slippage_normal_range[0]) | (df['Slippage'] > slippage_normal_range[1])]

# Detect unusual order sequences
df['Order Sequence'] = df.groupby(['Trader', 'Symbol'])['Order ID'].rank().astype(int)
unusual_order_sequences = df[df.groupby(['Trader', 'Symbol'])['Order Sequence'].diff().abs() > 1]

# Detect excessive trading activity
trading_volume = df.groupby(['Trader', 'Symbol', pd.Grouper(freq='1h', key='Timestamp')])['Order Size'].sum()
excessive_trading = trading_volume[trading_volume > trading_volume.quantile(0.99)]

# Detect wash trades
potential_wash_trades = df[df.duplicated(['Trader', 'Symbol', 'Timestamp', 'Order Size', 'Fill Size', 'Price'], keep=False)]

# Print the identified anomalies
print("\nOrder Size Anomalies:")
print(order_size_outliers)
print("\nFill Size Anomalies:")
print(fill_size_outliers)
print("\nSlippage Anomalies:")
print(slippage_outliers)
print("\nUnusual Order Sequences:")
print(unusual_order_sequences)
print("\nExcessive Trading Activity:")
print(excessive_trading)
print("\nPotential Wash Trades:")
print(potential_wash_trades)

# Part 4: Anomaly Investigation
# Gather additional context and information for identified anomalies
anomalies = pd.concat([order_size_outliers, fill_size_outliers, slippage_outliers, unusual_order_sequences, excessive_trading, potential_wash_trades], ignore_index=True)
anomalies = anomalies.drop_duplicates()

# Add additional analysis or investigation steps here
# ...

# Part 5: Reporting and Visualization
# Generate reports or visualizations for identified anomalies

# Scatter plot of Order Size anomalies
plt.figure(figsize=(10, 6))
plt.scatter(order_size_outliers.index, order_size_outliers['Order Size'], color='r', label='Anomalies')
plt.scatter(df[~df.isin(order_size_outliers).dropna()].index, df[~df.isin(order_size_outliers).dropna()]['Order Size'], color='g', label='Normal')
plt.title('Order Size Anomalies')
plt.xlabel('Index')
plt.ylabel('Order Size')
plt.legend()
plt.show()

# Histogram of Slippage anomalies
plt.figure(figsize=(10, 6))
plt.hist(slippage_outliers['Slippage'], bins=20, alpha=0.5, color='r', label='Anomalies')
plt.hist(df[~df.isin(slippage_outliers).dropna()]['Slippage'], bins=20, alpha=0.5, color='g', label='Normal')
plt.title('Slippage Anomalies')
plt.xlabel('Slippage')
plt.ylabel('Frequency')
plt.legend()
plt.show()