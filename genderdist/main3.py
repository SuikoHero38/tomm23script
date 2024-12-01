import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.lines import Line2D  # Import for custom legend handles

def plot_gender_distribution(df, gender, output_filename):
    # Prepare data
    df['Participant Percentage'] = df[f'{gender} Participant Number'] / df['Participant Number'] * 100
    #df['Marker'] = df['Question Available'].apply(lambda x: 'o' if x == 'Yes' else 's')

    # Define specific colors for each Paper Type
    paper_type_colors = {
        'Application': 'red',
        'Evaluation': 'green',
        'Model': 'orange',
        'Technique': 'blue',
        #'System': 'purple'  # Adding an example for 'System' type
    }

    # Plot
    fig, ax = plt.subplots()

    # Plot each Paper Type separately
    for paper_type, color in paper_type_colors.items():
        for question in ['Yes', 'No']:
            subset = df[(df['Paper Type'] == paper_type) & (df['Question Available'] == question)]
            marker = 'o' #if question == 'Yes' else 's'
            ax.scatter(subset['Participant Number'], subset['Participant Percentage'],
                       marker=marker, alpha=0.7, color=color)

    # Customize the y-axis to show percentages up to 100%
    ax.set_ylim(0, 100)
    ax.set_yticks(range(0, 101, 25))
    ax.set_yticklabels([f"{i}%" for i in range(0, 101, 25)])

    # Add grid lines for better readability
    ax.grid(True, which='both', linestyle='--', linewidth=0.5)

    # Set the labels and title
    ax.set_xlabel('Participant Number')
    ax.set_ylabel(f'{gender} Participant Percentage')
    #ax.set_title(f'{gender} Participant Distribution by Paper Type and Question Availability', pad=20)
    ax.set_title(f'{gender} Participant Distribution by Paper Type', pad=20)

    # Create custom legend handles
    paper_type_handles = [Line2D([0], [0], marker='o', color=color, label=paper_type, linestyle='None')
                          for paper_type, color in paper_type_colors.items()]

    # Adjust the figure size if necessary
    fig.set_size_inches(10, 6)

    # Create legends outside the plot area
    paper_type_legend = ax.legend(handles=paper_type_handles, title='Paper Type', loc='upper right', bbox_to_anchor=(1.2, 1))

    # Adjust layout to make room for the legends
    plt.tight_layout(rect=[0, 0, 1, 1])  # You may not need to adjust this if bbox_to_anchor is set correctly

    # Save the figure
    plt.savefig(output_filename, bbox_inches='tight')
    plt.close(fig)

# Read CSV file
df = pd.read_csv('dataset2.csv')

# Plot and save for Male and Female
plot_gender_distribution(df, 'Male', 'male_participant_distribution5.png')
plot_gender_distribution(df, 'Female', 'female_participant_distribution5.png')