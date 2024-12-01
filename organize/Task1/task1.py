import pandas as pd

# Load the CSV file
df = pd.read_csv('../input.csv')

# Group the data and count, then reset index to turn the grouped object into a DataFrame
grouped = df.groupby(['Item Type', 'Venue']).size().reset_index(name='Total')

# Sort the result as per the specified order and by 'Total' (descending) then 'Venue' (alphabetically)
sorted_grouped = grouped.sort_values(by=['Item Type', 'Total'], ascending=[True, False])

# Save the result to a new CSV file
sorted_grouped.to_csv('output.csv', index=False)

print("Grouping and counting complete. Results saved to 'output.csv'.")