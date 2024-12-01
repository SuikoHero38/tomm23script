import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Corrected data with equal length lists
data = {
    'Year': [2023, 2023, 2023, 2023, 2023],
    'Evaluation': ['AP', 'AP', 'AP', 'UWP', 'UP,UE,UWP']
}

# Create DataFrame
df = pd.DataFrame(data)

# Split the 'Evaluation' column by comma and explode
df = df.assign(Evaluation=df['Evaluation'].str.split(',')).explode('Evaluation')

# Pivot table to count occurrences
df_counts = df.pivot_table(index='Year', columns='Evaluation', aggfunc='size', fill_value=0)

# Ensure columns are ordered as desired
ordered_columns = ['UWP', 'UP', 'UE', 'AP']
df_counts = df_counts[ordered_columns]

# Plotting
fig, ax = plt.subplots(figsize=(10, 6))

colors = {
    'UWP': 'gold',
    'UP': 'lightgrey',
    'UE': 'coral',
    'AP': 'royalblue'
}

# Plot each bar and add the count on top
for column in df_counts.columns:
    ax.bar(df_counts.index, df_counts[column], label=column, color=colors[column])

# Add the numbers on the bars or on top
for i, year in enumerate(df_counts.index):
    y_offset = 0
    for column in df_counts.columns:
        count = df_counts.at[year, column]
        if count > 0:
            if y_offset == 0:
                ax.text(year, y_offset + count/2, int(count), ha='center', va='center', color='black' if colors[column] in ['gold', 'lightgrey'] else 'white', fontsize=8)
            else:
                ax.text(year, y_offset + count/2, int(count), ha='center', va='center', color='black' if colors[column] in ['gold', 'lightgrey'] else 'white', fontsize=8)
        y_offset += count

# Reverse the order of the legend
handles, labels = ax.get_legend_handles_labels()
ax.legend(handles[::-1], labels[::-1], loc='upper left')

ax.set_xlabel('Years', fontsize=12)
ax.set_ylabel('Total Papers', fontsize=12)
ax.set_title('')

plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig('evaluation_counts_stacked_bar2.png', format='png')
plt.savefig('evaluation_counts_stacked_bar2.svg', format='svg')
plt.show()
