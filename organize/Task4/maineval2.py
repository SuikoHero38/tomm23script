import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Read the input CSV
input_filename = '../inputeval.csv'  # Adjust the path as necessary
df = pd.read_csv(input_filename)

# Expand the 'Strategy2', 'Topic2', and 'Metaverse2' columns into separate rows
Evaluation2=df['Evaluation2'].str.split(',').explode('Evaluation2')

# Aggregate data for all categories per year
Evaluation2_counts_per_year = Evaluation2.groupby(['Year', 'Evaluation2']).size().unstack(fill_value=0)

# Sorting totals
Evaluation2_order = Evaluation2_counts_per_year.sum().sort_values(ascending=False).index.tolist()

# Reorder columns based on sorted order
Evaluation2_counts_per_year = Evaluation2_counts_per_year[Evaluation2_order]

# Generate a color palette with different colors
unique_topics = pd.concat([df_Evaluation2_expanded['Evaluation2']]).unique()
color_palette = sns.color_palette("Paired", len(unique_topics))

#print(unique_topics)
#print(enumerate(unique_topics))

# Manually set color for 'Augmented Reality' and 'AR'
ar_color = color_palette[0]  # First color in the palette
color_dict = {topic: color_palette[i] for i, topic in enumerate(unique_topics)}

def plot_data_counts(df, title, bar_filename):
    font_size = 20
    legend_font_size = 12

    # Stacked bar chart
    fig, ax = plt.subplots(figsize=(10, 6))
    df.plot(kind='bar', ax=ax, stacked=True, color=[color_dict[col] for col in df.columns])
    plt.ylabel('Total Papers', fontsize=font_size)
    plt.xlabel('Year', fontsize=font_size)
    plt.xticks(rotation=45, fontsize=font_size)
    plt.yticks(fontsize=font_size)
    ax.legend(fontsize=legend_font_size)
    plt.tight_layout()
    
    # Add numbers on the bars
    for p in ax.patches:
        width, height = p.get_width(), p.get_height()
        x, y = p.get_xy() 
        if height > 0:  # Only add text if height is greater than 0
            ax.text(x + width/2, y + height/2, int(height), ha='center', va='center', fontsize=font_size*0.5)

    # Get legend handles and labels
    handles, labels = ax.get_legend_handles_labels()
    # Reverse the order for the legend
    ax.legend(reversed(handles), reversed(labels), fontsize=legend_font_size)
    
    plt.savefig(f"{bar_filename}2.svg", format='svg')
    plt.close(fig)  # Close the figure to free up memory

# Example usage with counts data
plot_data_counts(Evaluation2_counts_per_year, 'Evaluation2 Counts', 'Evaluation2_counts_stacked_bar')

print("Charts have been saved as separate SVG files.")
