import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Read the input CSV
input_filename = '../input.csv'  # Adjust the path as necessary
df = pd.read_csv(input_filename)

# Expand the 'Strategy2', 'Topic2', and 'Metaverse2' columns into separate rows
df_Strategy2_expanded = df.drop(['Topic2', 'Metaverse2', 'Evaluation2', 'Reality'], axis=1).assign(Strategy2=df['Strategy2'].str.split(',')).explode('Strategy2')
df_Topic2_expanded = df.drop(['Strategy2', 'Metaverse2', 'Evaluation2', 'Reality'], axis=1).assign(Topic2=df['Topic2'].str.split(',')).explode('Topic2')
df_Metaverse2_expanded = df.drop(['Strategy2', 'Topic2', 'Evaluation2', 'Reality'], axis=1).assign(Metaverse2=df['Metaverse2'].str.split(',')).explode('Metaverse2')
df_Evaluation2_expanded = df.drop(['Strategy2', 'Topic2', 'Metaverse2', 'Reality'], axis=1).assign(Evaluation2=df['Evaluation2'].str.split(',')).explode('Evaluation2')
df_Reality2_expanded = df.drop(['Strategy2', 'Topic2', 'Metaverse2', 'Evaluation2'], axis=1).assign(Reality=df['Reality'].str.split(',')).explode('Reality')

# Filter for 'Security' and 'Privacy' in Topic2
df_Topic2_Security = df_Topic2_expanded[df_Topic2_expanded['Topic2'] == 'Security']
df_Topic2_Privacy = df_Topic2_expanded[df_Topic2_expanded['Topic2'] == 'Privacy']

# Aggregate data for all categories per year
Strategy2_counts_per_year = df_Strategy2_expanded.groupby(['Year', 'Strategy2']).size().unstack(fill_value=0)
Topic2_counts_per_year = df_Topic2_expanded.groupby(['Year', 'Topic2']).size().unstack(fill_value=0)
Topic2_Security_counts_per_year = df_Topic2_Security.groupby(['Year', 'Topic']).size().unstack(fill_value=0)
Topic2_Privacy_counts_per_year = df_Topic2_Privacy.groupby(['Year', 'Topic']).size().unstack(fill_value=0)
Metaverse2_counts_per_year = df_Metaverse2_expanded.groupby(['Year', 'Metaverse2']).size().unstack(fill_value=0)
Evaluation2_counts_per_year = df_Evaluation2_expanded.groupby(['Year', 'Evaluation2']).size().unstack(fill_value=0)
Reality2_counts_per_year = df_Reality2_expanded.groupby(['Year', 'Reality']).size().unstack(fill_value=0)

# Convert counts to percentages
Strategy2_counts_per_year_percentage = Strategy2_counts_per_year.div(Strategy2_counts_per_year.sum(axis=1), axis=0) * 100
Topic2_counts_per_year_percentage = Topic2_counts_per_year.div(Topic2_counts_per_year.sum(axis=1), axis=0) * 100
Topic2_Security_counts_per_year_percentage = Topic2_Security_counts_per_year.div(Topic2_Security_counts_per_year.sum(axis=1), axis=0) * 100
Topic2_Privacy_counts_per_year_percentage = Topic2_Privacy_counts_per_year.div(Topic2_Privacy_counts_per_year.sum(axis=1), axis=0) * 100
Metaverse2_counts_per_year_percentage = Metaverse2_counts_per_year.div(Metaverse2_counts_per_year.sum(axis=1), axis=0) * 100
Evaluation2_counts_per_year_percentage = Evaluation2_counts_per_year.div(Evaluation2_counts_per_year.sum(axis=1), axis=0) * 100
Reality2_counts_per_year_percentage = Reality2_counts_per_year.div(Reality2_counts_per_year.sum(axis=1), axis=0) * 100

# Sorting totals is no longer needed as percentages normalize values
Strategy2_order = Strategy2_counts_per_year_percentage.sum().sort_values(ascending=False).index.tolist()
Topic2_order = Topic2_counts_per_year_percentage.sum().sort_values(ascending=False).index.tolist()
TopicSec_order = Topic2_Security_counts_per_year_percentage.sum().sort_values(ascending=False).index.tolist()
TopicPri_order = Topic2_Privacy_counts_per_year_percentage.sum().sort_values(ascending=False).index.tolist()
Metaverse2_order = Metaverse2_counts_per_year_percentage.sum().sort_values(ascending=False).index.tolist()
Evaluation2_order = Evaluation2_counts_per_year_percentage.sum().sort_values(ascending=False).index.tolist()
Reality2_order = Reality2_counts_per_year_percentage.sum().sort_values(ascending=False).index.tolist()

# Reorder columns based on sorted order
Strategy2_counts_per_year_percentage = Strategy2_counts_per_year_percentage[Strategy2_order]
Topic2_counts_per_year_percentage = Topic2_counts_per_year_percentage[Topic2_order]
Topic2_Security_counts_per_year_percentage = Topic2_Security_counts_per_year_percentage[TopicSec_order]
Topic2_Privacy_counts_per_year_percentage = Topic2_Privacy_counts_per_year_percentage[TopicPri_order]
Metaverse2_counts_per_year_percentage = Metaverse2_counts_per_year_percentage[Metaverse2_order]
Evaluation2_counts_per_year_percentage = Evaluation2_counts_per_year_percentage[Evaluation2_order]
Reality2_counts_per_year_percentage = Reality2_counts_per_year_percentage[Reality2_order]

# Print the Strategy2_counts_per_year_percentage to the command line
print(Strategy2_counts_per_year_percentage)

# Print the Evaluation2_counts_per_year_percentage to the command line to the command line
print(Evaluation2_counts_per_year_percentage)

# Generate a color palette with different colors
unique_topics = pd.concat([df_Strategy2_expanded['Strategy2'], df_Topic2_expanded['Topic'], df_Metaverse2_expanded['Metaverse2'], df_Evaluation2_expanded['Evaluation2'], df_Reality2_expanded['Reality'],df_Topic2_expanded['Topic2']]).unique()
#unique_topics = pd.concat([df_Strategy2_expanded['Strategy2'],df_Evaluation2_expanded['Evaluation2']]).unique()
#unique_topics = pd.concat([df_Topic2_expanded['Topic2'], df_Topic2_expanded['Topic']]).unique()
#unique_topics = pd.concat([df_Metaverse2_expanded['Metaverse2'], df_Reality2_expanded['Reality']]).unique()
color_palette = sns.color_palette("Paired", len(unique_topics))

print(unique_topics)
print(enumerate(unique_topics))

# Manually set color for 'Augmented Reality' and 'AR'
ar_color = color_palette[0]  # First color in the palette
color_dict = {topic: color_palette[i] for i, topic in enumerate(unique_topics)}
color_dict['Augmented Reality'] = ar_color
color_dict['AR'] = ar_color

def plot_data_percentage(df, title, line_filename, stacked_area_filename):
    font_size = 20
    legend_font_size = 12

    # Line chart
    fig, ax = plt.subplots(figsize=(10, 6))
    df.plot(kind='line', ax=ax, marker='o', color=[color_dict[col] for col in df.columns])
    ax.set_xlim(left=df.index.min(), right=df.index.max())  # Set x limits
    plt.ylim(0, 100)  # Set y limits to remove gap at top
    plt.ylabel('Percentage', fontsize=font_size)
    plt.xlabel('Year', fontsize=font_size)
    plt.xticks(rotation=45, fontsize=font_size)
    plt.yticks(fontsize=font_size)
    ax.legend(fontsize=legend_font_size)
    plt.tight_layout()
    
    # Get legend handles and labels
    handles, labels = ax.get_legend_handles_labels()
    # Reverse the order for the legend
    ax.legend(reversed(handles), reversed(labels), fontsize=legend_font_size)
    
    plt.savefig(f"{line_filename}15.svg", format='svg')
    plt.close(fig)  # Close the figure to free up memory

    # Stacked area chart
    fig, ax = plt.subplots(figsize=(10, 6))
    df.plot(kind='area', ax=ax, stacked=True, alpha=0.6, color=[color_dict[col] for col in df.columns])
    ax.set_xlim(left=df.index.min(), right=df.index.max())  # Set x limits
    plt.ylim(0, 100)  # Set y limits to remove gap at top
    plt.ylabel('Percentage', fontsize=font_size)
    plt.xlabel('Year', fontsize=font_size)
    plt.xticks(rotation=45, fontsize=font_size)
    plt.yticks(fontsize=font_size)
    ax.legend(fontsize=legend_font_size)
    plt.tight_layout()
    
    # Get legend handles and labels
    handles, labels = ax.get_legend_handles_labels()
    # Reverse the order for the legend
    ax.legend(reversed(handles), reversed(labels), fontsize=legend_font_size)
    
    plt.savefig(f"{stacked_area_filename}15.svg", format='svg')
    plt.close(fig)  # Close the figure to free up memory

# Example usage with percentage data
plot_data_percentage(Strategy2_counts_per_year_percentage, 'Strategy Counts', 'Strategy2_counts_line', 'Strategy2_counts_stacked_area')
plot_data_percentage(Topic2_counts_per_year_percentage, 'Security & Privacy Counts', 'Topic_counts_line', 'Topic_counts_stacked_area')
plot_data_percentage(Topic2_Security_counts_per_year_percentage, 'Security Topics', 'Security_counts_line', 'Security_counts_stacked_area')
plot_data_percentage(Topic2_Privacy_counts_per_year_percentage, 'Privacy Topics', 'Privacy_counts_line', 'Privacy_counts_stacked_area')
plot_data_percentage(Metaverse2_counts_per_year_percentage, 'Metaverse2 Counts', 'Metaverse2_counts_line', 'Metaverse2_counts_stacked_area')
plot_data_percentage(Evaluation2_counts_per_year_percentage, 'Evaluation2 Counts', 'Evaluation2_counts_line', 'Evaluation2_counts_stacked_area')
plot_data_percentage(Reality2_counts_per_year_percentage, 'Reality2 Counts', 'Reality2_counts_line', 'Reality2_counts_stacked_area')

print("Charts have been saved as separate SVG files.")
