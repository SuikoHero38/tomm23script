import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.lines import Line2D  # Import for custom legend handles
import matplotlib

# Adjust default plot font sizes for better readability
matplotlib.rcParams.update({'font.size': 14, 'axes.titlesize': 16, 'axes.labelsize': 14,
                            'xtick.labelsize': 12, 'ytick.labelsize': 12, 'legend.fontsize': 12})

def plot_gender_distribution(df, gender, output_filename):
    # Prepare data
    df['Participant Percentage'] = df[f'{gender} Participant Number'] / df['Participant Number'] * 100

    # Define specific colors for each Paper Type
    paper_type_colors = {
        'Application': 'red',
        'Evaluation': 'green',
        'Model': 'orange',
        'Technique': 'blue',
    }

    # Plot
    fig, ax = plt.subplots(figsize=(8, 4.8))  # Adjusted for a two-column paper

    # Plot each Paper Type separately
    for paper_type, color in paper_type_colors.items():
        subset = df[df['Paper Type'] == paper_type]
        marker = 'o'
        ax.scatter(subset['Participant Number'], subset['Participant Percentage'],
                   marker=marker, alpha=0.7, color=color, label=paper_type)

    # Customize the y-axis to show percentages up to 100%
    ax.set_ylim(0, 100)
    ax.set_yticks(range(0, 101, 20))
    ax.set_yticklabels([f"{i}%" for i in range(0, 101, 20)])

    # Add grid lines for better readability
    ax.grid(True, which='both', linestyle='--', linewidth=0.5)

    # Set the labels and title
    ax.set_xlabel('Participant Number')
    ax.set_ylabel(f'{gender} Participant Percentage')
    ax.set_title(f'{gender} Participant Distribution by Paper Type')

    # Create custom legend handles
    paper_type_handles = [Line2D([0], [0], marker='o', color=color, label=paper_type, linestyle='None')
                          for paper_type, color in paper_type_colors.items()]

    # Legend and layout adjustments
    ax.legend(handles=paper_type_handles, title='Paper Type', loc='lower right')

    # Adjust layout to make room for the legends
    plt.tight_layout()

    # Save the figure in different formats
    for fmt in ['pdf', 'png', 'svg']:
        plt.savefig(f"{output_filename}7.{fmt}", bbox_inches='tight', dpi=300)  # Higher DPI for better clarity

    plt.close(fig)

# Example usage
df = pd.read_csv('dataset2.csv')  # Make sure to have your dataset ready
plot_gender_distribution(df, 'Male', 'male_participant_distribution')
plot_gender_distribution(df, 'Female', 'female_participant_distribution')
