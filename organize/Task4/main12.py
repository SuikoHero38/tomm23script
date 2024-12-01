import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Read the input CSV
input_filename = 'input.csv'  # Adjust the path as necessary
df = pd.read_csv(input_filename)

# Expand the 'Strategy2', 'Topic2', and 'Metaverse2' columns into separate rows
df_Strategy2_expanded = df.drop(['Topic2', 'Metaverse2'], axis=1).assign(Strategy2=df['Strategy2'].str.split(',')).explode('Strategy2')
df_Topic2_expanded = df.drop(['Strategy2', 'Metaverse2'], axis=1).assign(Topic2=df['Topic2'].str.split(',')).explode('Topic2')
df_Metaverse2_expanded = df.drop(['Strategy2', 'Topic2'], axis=1).assign(Metaverse2=df['Metaverse2'].str.split(',')).explode('Metaverse2')

# Filter for 'Security' and 'Privacy' in Topic2
df_Topic2_Security = df_Topic2_expanded[df_Topic2_expanded['Topic2'] == 'Security']
df_Topic2_Privacy = df_Topic2_expanded[df_Topic2_expanded['Topic2'] == 'Privacy']

# Create a color index for the unique topics
all_topics = pd.concat([df_Strategy2_expanded['Strategy2'], df_Topic2_expanded['Topic2'], df_Topic2_Security['Topic'], df_Topic2_Privacy['Topic'], df_Metaverse2_expanded['Metaverse2']]).unique()
color_palette = sns.color_palette("husl", len(all_topics))
color_dict = dict(zip(all_topics, color_palette))

# Aggregate data for all categories per year
Strategy2_counts_per_year = df_Strategy2_expanded.groupby(['Year', 'Strategy2']).size().unstack(fill_value=0)
Topic2_counts_per_year = df_Topic2_expanded.groupby(['Year', 'Topic2']).size().unstack(fill_value=0)
Security_counts_per_year = df_Topic2_Security.groupby(['Year', 'Topic']).size().unstack(fill_value=0)
Privacy_counts_per_year = df_Topic2_Privacy.groupby(['Year', 'Topic']).size().unstack(fill_value=0)
Metaverse2_counts_per_year = df_Metaverse2_expanded.groupby(['Year', 'Metaverse2']).size().unstack(fill_value=0)

def plot_data(df, title, filename, plot_type):
    font_size = 14
    fig, ax = plt.subplots(figsize=(12, 6))
    # Use color dictionary for consistent coloring across different charts
    color_list = [color_dict[column] for column in df.columns]
    if plot_type == 'line':
        df.plot(kind='line', ax=ax, marker='o', linewidth=2, markersize=5, color=color_list)
    elif plot_type == 'stacked_area':
        df.plot(kind='area', ax=ax, stacked=True, alpha=0.4, color=color_list)

    plt.ylabel('Total', fontsize=font_size)
    plt.xlabel('Year', fontsize=font_size)
    plt.title(f'{title} per Year ({plot_type.replace("_", " ").title()})', fontsize=font_size)
    plt.xticks(rotation=45, fontsize=font_size)
    plt.yticks(fontsize=font_size)
    ax.set_xlim(df.index.min(), df.index.max())  # Set x limits to data edges
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles, labels, title=title, fontsize=font_size, loc='upper left')
    plt.tight_layout()
    plt.savefig(f"{filename}_{plot_type}.svg", format='svg')
    plt.close(fig)

# Example usage
plot_data(Strategy2_counts_per_year, 'Strategy Data', 'Strategy2_counts', 'line')
plot_data(Strategy2_counts_per_year, 'Strategy Data', 'Strategy2_counts', 'stacked_area')
plot_data(Topic2_counts_per_year, 'Topic Data', 'Topic2_counts', 'line')
plot_data(Topic2_counts_per_year, 'Topic Data', 'Topic2_counts', 'stacked_area')
plot_data(Security_counts_per_year, 'Security Topic Data', 'Security_counts', 'line')
plot_data(Security_counts_per_year, 'Security Topic Data', 'Security_counts', 'stacked_area')
plot_data(Privacy_counts_per_year, 'Privacy Topic Data', 'Privacy_counts', 'line')
plot_data(Privacy_counts_per_year
