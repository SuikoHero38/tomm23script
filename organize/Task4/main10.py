import pandas as pd
import matplotlib.pyplot as plt
from collections import defaultdict

# Read the input CSV
#input_filename = '../inputsecurity.csv'  # Adjust the path as necessary
input_filename = '../inputprivacy.csv'  # Adjust the path as necessary
df = pd.read_csv(input_filename)

# Expand the 'Strategy' and 'Topic' columns into separate rows
df_Strategy_expanded = df.drop('Topic', axis=1).assign(Strategy=df['Strategy'].str.split(',')).explode('Strategy')
df_Topic_expanded = df.drop('Strategy', axis=1).assign(Topic=df['Topic'].str.split(',')).explode('Topic')

# Aggregate data for strategies and Topics per year
Strategy_counts_per_year = df_Strategy_expanded.groupby(['Year', 'Strategy']).size().unstack(fill_value=0)
Topic_counts_per_year = df_Topic_expanded.groupby(['Year', 'Topic']).size().unstack(fill_value=0)

# Menghitung total dari setiap kategori
Strategy_totals = df_Strategy_expanded.groupby('Strategy').size()
Topic_totals = df_Topic_expanded.groupby('Topic').size()

# Mengurutkan data berdasarkan total secara descending (dari besar ke kecil)
Strategy_order = Strategy_totals.sort_values(ascending=False).index.tolist()
Topic_order = Topic_totals.sort_values(ascending=False).index.tolist()

# Menggunakan urutan ini untuk menyusun ulang kolom DataFrame
Strategy_counts_per_year = Strategy_counts_per_year[Strategy_order]
Topic_counts_per_year = Topic_counts_per_year[Topic_order]

# Plotting
def plot_data(df, title, line_filename, stacked_area_filename):
    # Define the font size
    font_size = 20  # You can adjust this value as needed
    legend_font_size = 12  # And this for the legend font size
    
    color_palette = [
        '#1f77b4',  # muted blue
        '#ff7f0e',  # safety orange
        '#2ca02c',  # cooked asparagus green
        '#d62728',  # brick red
        '#9467bd',  # muted purple
        '#8c564b',  # chestnut brown
        '#e377c2',  # raspberry yogurt pink
        '#7f7f7f',  # middle gray
        '#bcbd22',  # curry yellow-green
        '#17becf',  # blue-teal
        '#aec7e8',  # light blue
        '#ffbb78',  # light orange
        '#98df8a',  # light green
        '#ff9896',  # light red
        '#c5b0d5',  # light purple
        '#c49c94',  # light brown
        '#f7b6d2',  # light pink
        '#c7c7c7',  # light gray
        '#dbdb8d',  # light yellow-green
        '#9edae5'   # light teal
    ]

    # Line chart
    fig, ax = plt.subplots(figsize=(10, 6))
    #df.plot(kind='line', ax=ax, marker='o')
    df.plot(kind='line', ax=ax, marker='o', color=color_palette[:df.shape[1]])
    ax.set_xlim(left=df.index.min(), right=df.index.max())  # Set x limits
    #plt.title(f'{title} Per Year (Line Chart)', fontsize=font_size)
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
    
    plt.savefig(f"{line_filename}11.svg", format='svg')
    plt.close(fig)  # Close the figure to free up memory

    # Stacked area chart
    fig, ax = plt.subplots(figsize=(10, 6))
    #df.plot(kind='area', ax=ax, stacked=True, alpha=0.4)
    df.plot(kind='area', ax=ax, stacked=True, alpha=0.4, color=color_palette[:df.shape[1]])
    ax.set_xlim(left=df.index.min(), right=df.index.max())  # Set x limits
    #plt.title(f'{title} Per Year (Line Chart)', fontsize=font_size)
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
    
    
    plt.savefig(f"{stacked_area_filename}11.svg", format='svg')
    plt.close(fig)  # Close the figure to free up memory

# Example usage
plot_data(Strategy_counts_per_year, 'Strategy Counts', 'Strategy_counts_line', 'Strategy_counts_stacked_area')
plot_data(Topic_counts_per_year, 'Security & Privacy Counts', 'Topic_counts_line', 'topic_counts_stacked_area')

print("Charts have been saved as separate SVG files.")