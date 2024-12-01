import pandas as pd
import matplotlib.pyplot as plt
from collections import defaultdict

# Read the input CSV
input_filename = '../input.csv'  # Adjust the path as necessary
df = pd.read_csv(input_filename)

# Expand the 'Strategy2' and 'Topic2' columns into separate rows
df_Strategy2_expanded = df.drop('Topic2', axis=1).assign(Strategy2=df['Strategy2'].str.split(',')).explode('Strategy2')
df_Topic2_expanded = df.drop('Strategy2', axis=1).assign(Topic2=df['Topic2'].str.split(',')).explode('Topic2')

# Aggregate data for strategies and Topic2s per year
Strategy2_counts_per_year = df_Strategy2_expanded.groupby(['Year', 'Strategy2']).size().unstack(fill_value=0)
Topic2_counts_per_year = df_Topic2_expanded.groupby(['Year', 'Topic2']).size().unstack(fill_value=0)

# Menghitung total dari setiap kategori
Strategy2_totals = df_Strategy2_expanded.groupby('Strategy2').size()
Topic2_totals = df_Topic2_expanded.groupby('Topic2').size()

# Mengurutkan data berdasarkan total secara descending (dari besar ke kecil)
Strategy2_order = Strategy2_totals.sort_values(ascending=False).index.tolist()
Topic2_order = Topic2_totals.sort_values(ascending=False).index.tolist()

# Menggunakan urutan ini untuk menyusun ulang kolom DataFrame
Strategy2_counts_per_year = Strategy2_counts_per_year[Strategy2_order]
Topic2_counts_per_year = Topic2_counts_per_year[Topic2_order]

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
    
    # Get legend handles and labels
    handles, labels = ax.get_legend_handles_labels()
    # Reverse the order for the legend
    ax.legend(reversed(handles), reversed(labels), fontsize=legend_font_size)
    
    plt.savefig(f"{line_filename}8.svg", format='svg')
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
    
    # Get legend handles and labels
    handles, labels = ax.get_legend_handles_labels()
    # Reverse the order for the legend
    ax.legend(reversed(handles), reversed(labels), fontsize=legend_font_size)
    
    
    plt.savefig(f"{stacked_area_filename}8.svg", format='svg')
    plt.close(fig)  # Close the figure to free up memory

# Example usage
plot_data(Strategy2_counts_per_year, 'Strategy Counts', 'Strategy2_counts_line', 'Strategy2_counts_stacked_area')
plot_data(Topic2_counts_per_year, 'Security & Privacy Counts', 'Topic_counts_line', 'topic_counts_stacked_area')

print("Charts have been saved as separate SVG files.")
