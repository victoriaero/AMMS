import pandas as pd

# Read the first CSV file into a DataFrame
df1 = pd.read_csv('data/discovery/com_users_discovery1-1086.csv')

# Read the second CSV file into another DataFrame
df2 = pd.read_csv('data/disboard/csvs/disboard1-50.csv')

# Merge the two DataFrames without duplicates based on the second column
merged_df = pd.concat([df1, df2]).drop_duplicates(subset=[' coluna2'])

# Save the merged DataFrame to a new CSV file
merged_df.to_csv('merged.csv', index=False)
