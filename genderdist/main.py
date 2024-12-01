import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def plot_gender_distribution(df, gender, output_filename):
    # Prepare data
    df['Participant Percentage'] = df[f'{gender} Participant Number'] / df['Participant Number'] * 100
    df['Marker'] = df['Question Available'].apply(lambda x: 'o' if x == 'Yes' else 's')

    # Set colors for each Paper Type
    unique_paper_types = df['Paper Type'].unique()
    colors = sns.color_palette('husl', len(unique_paper_types))
    paper_type_colors = {paper_type: color for paper_type, color in zip(unique_paper_types, colors)}
    
    # Define specific colors for each Paper Type
    paper_type_colors = {
        'Application': 'red',
        'Evaluation': 'green',
        'Model': 'orange',
        'Technique': 'blue'
    }
    # The plotting function remains the same except you replace the color assignment with the one above

    # Plot
    fig, ax = plt.subplots()

    # Plot each Paper Type separately
    for paper_type in unique_paper_types:
        for question in ['Yes', 'No']:
            subset = df[(df['Paper Type'] == paper_type) & (df['Question Available'] == question)]
            marker = 'o' if question == 'Yes' else 's'
            label = f"{paper_type} with Question" if question == 'Yes' else f"{paper_type} without Question"
            #ax.scatter(subset['Participant Number'], subset['Participant Percentage'],label=label, marker=marker, alpha=0.7, color=paper_type_colors[paper_type])
            ax.scatter(subset['Participant Number'], subset['Participant Percentage'],label=label, marker=marker, alpha=0.7, color=paper_type_colors[paper_type])

            # Annotate points with 'Ref'
            #for i, row in subset.iterrows():
            #    ax.annotate(row['Ref'], (row['Participant Number'], row['Participant Percentage']),
            #                textcoords="offset points", xytext=(0,10), ha='center')

    # Customize the y-axis to show percentages up to 100%
    ax.set_ylim(0, 100)
    ax.set_yticks(range(0, 101, 25))
    ax.set_yticklabels([f"{i}%" for i in range(0, 101, 25)])

    # Add grid lines for better readability
    ax.grid(True, which='both', linestyle='--', linewidth=0.5)

    # Set the labels and title
    ax.set_xlabel('Participant Number')
    ax.set_ylabel(f'{gender} Participant Percentage')
    ax.set_title(f'{gender} Participant Distribution by Paper Type and Question Availability', pad=20)

    # Create legend
    handles, labels = ax.get_legend_handles_labels()
    by_label = dict(zip(labels, handles))  # Remove duplicates
    ax.legend(by_label.values(), by_label.keys(), title='Paper Type and Question Availability')

    # Save the figure
    plt.tight_layout()
    plt.savefig(output_filename, bbox_inches='tight')
    plt.close(fig)

# Read CSV file
df = pd.read_csv('dataset.csv')

# Plot and save for Male and Female
plot_gender_distribution(df, 'Male', 'male_participant_distribution.png')
plot_gender_distribution(df, 'Female', 'female_participant_distribution.png')
