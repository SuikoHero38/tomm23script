import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from collections import defaultdict

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

# Menghitung total dari setiap kategori
Strategy2_totals = df_Strategy2_expanded.groupby('Strategy2').size()
Topic2_totals = df_Topic2_expanded.groupby('Topic2').size()
TopicSec_totals = df_Topic2_Security.groupby('Topic').size()
TopicPri_totals = df_Topic2_Privacy.groupby('Topic').size()
Metaverse2_totals = df_Metaverse2_expanded.groupby('Metaverse2').size()
Evaluation2_totals = df_Evaluation2_expanded.groupby('Evaluation2').size()
Reality2_totals = df_Reality2_expanded.groupby('Reality').size()

# Mengurutkan data berdasarkan total secara descending (dari besar ke kecil)
Strategy2_order = Strategy2_totals.sort_values(ascending=False).index.tolist()
Topic2_order = Topic2_totals.sort_values(ascending=False).index.tolist()
TopicSec_order = TopicSec_totals.sort_values(ascending=False).index.tolist()
TopicPri_order = TopicPri_totals.sort_values(ascending=False).index.tolist()
Metaverse2_order = Metaverse2_totals.sort_values(ascending=False).index.tolist()
Evaluation2_order = Evaluation2_totals.sort_values(ascending=False).index.tolist()
Reality2_order = Reality2_totals.sort_values(ascending=False).index.tolist()

# Menggunakan urutan ini untuk menyusun ulang kolom DataFrame
Strategy2_counts_per_year = Strategy2_counts_per_year[Strategy2_order]
Topic2_counts_per_year = Topic2_counts_per_year[Topic2_order]
Topic2_Security_counts_per_year = Topic2_Security_counts_per_year[TopicSec_order]
Topic2_Privacy_counts_per_year = Topic2_Privacy_counts_per_year[TopicPri_order]
Metaverse2_counts_per_year = Metaverse2_counts_per_year[Metaverse2_order]
Evaluation2_counts_per_year = Evaluation2_counts_per_year[Evaluation2_order]
Reality2_counts_per_year = Reality2_counts_per_year[Reality2_order]

# Create color index
unique_topics = pd.concat([df_Strategy2_expanded['Strategy2'], df_Topic2_expanded['Topic'], df_Topic2_expanded['Topic2'], df_Metaverse2_expanded['Metaverse2'], df_Evaluation2_expanded['Evaluation2'], df_Reality2_expanded['Reality']]).unique()
color_palette = sns.color_palette("tab20", len(unique_topics))
color_dict = dict(zip(unique_topics, color_palette))

def plot_data(df, title, line_filename, stacked_area_filename):
    font_size = 20
    legend_font_size = 12

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
    
    plt.savefig(f"{line_filename}14.svg", format='svg')
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
    
    
    plt.savefig(f"{stacked_area_filename}14.svg", format='svg')
    plt.close(fig)  # Close the figure to free up memory

# Example usage
plot_data(Strategy2_counts_per_year, 'Strategy Counts', 'Strategy2_counts_line', 'Strategy2_counts_stacked_area')
plot_data(Topic2_counts_per_year, 'Security & Privacy Counts', 'Topic_counts_line', 'topic_counts_stacked_area')
plot_data(Topic2_Security_counts_per_year, 'Security Topics', 'Security_counts_line', 'Security_counts_stacked_area')
plot_data(Topic2_Privacy_counts_per_year, 'Privacy Topics', 'Privacy_counts_line', 'Privacy_counts_stacked_area')
plot_data(Metaverse2_counts_per_year, 'Metaverse2 Counts', 'Metaverse2_counts_line', 'Metaverse2_counts_stacked_area')
plot_data(Evaluation2_counts_per_year, 'Evaluation2 Counts', 'Evaluation2_counts_line', 'Evaluation2_counts_stacked_area')
plot_data(Reality2_counts_per_year, 'Reality2 Counts', 'Reality2_counts_line', 'Reality2_counts_stacked_area')

print("Charts have been saved as separate SVG files.")