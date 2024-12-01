import pandas as pd
import matplotlib.pyplot as plt
from collections import defaultdict

# Read the input CSV
input_filename = '../input.csv'  # Adjust the path as necessary
df = pd.read_csv(input_filename)

# Expand the 'Strategy' and 'Topic' columns into separate rows
df_strategy_expanded = df.drop('Topic', axis=1).assign(Strategy=df['Strategy'].str.split(',')).explode('Strategy')
df_topic_expanded = df.drop('Strategy', axis=1).assign(Topic=df['Topic'].str.split(',')).explode('Topic')

# Aggregate data for strategies and topics per year
strategy_counts_per_year = df_strategy_expanded.groupby(['Year', 'Strategy']).size().unstack(fill_value=0)
topic_counts_per_year = df_topic_expanded.groupby(['Year', 'Topic']).size().unstack(fill_value=0)

# Plotting
def plot_data(df, title, line_filename, stacked_area_filename):
    # Define the font size
    font_size = 20  # You can adjust this value as needed
    legend_font_size = 12  # And this for the legend font size

    # Line chart
    fig, ax = plt.subplots(figsize=(10, 6))
    df.plot(kind='line', ax=ax, marker='o')
    ax.set_xlim(left=df.index.min(), right=df.index.max())  # Set x limits
    plt.title(f'{title} Per Year (Line Chart)', fontsize=font_size)
    plt.ylabel('Total', fontsize=font_size)
    plt.xlabel('Year', fontsize=font_size)
    plt.xticks(rotation=45, fontsize=font_size)
    plt.yticks(fontsize=font_size)
    ax.legend(fontsize=legend_font_size)
    plt.tight_layout()
    plt.savefig(f"{line_filename}2.svg", format='svg')
    plt.close(fig)  # Close the figure to free up memory

    # Stacked area chart
    fig, ax = plt.subplots(figsize=(10, 6))
    df.plot(kind='area', ax=ax, stacked=True, alpha=0.4)
    ax.set_xlim(left=df.index.min(), right=df.index.max())  # Set x limits
    plt.title(f'{title} Per Year (Line Chart)', fontsize=font_size)
    plt.ylabel('Total', fontsize=font_size)
    plt.xlabel('Year', fontsize=font_size)
    plt.xticks(rotation=45, fontsize=font_size)
    plt.yticks(fontsize=font_size)
    ax.legend(fontsize=legend_font_size)
    plt.tight_layout()
    plt.savefig(f"{stacked_area_filename}2.svg", format='svg')
    plt.close(fig)  # Close the figure to free up memory

# Example usage
plot_data(strategy_counts_per_year, 'Strategy Counts', 'strategy_counts_line', 'strategy_counts_stacked_area')
plot_data(topic_counts_per_year, 'Topic Counts', 'topic_counts_line', 'topic_counts_stacked_area')

print("Charts have been saved as separate SVG files.")
