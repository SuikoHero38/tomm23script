import pandas as pd

def expand_and_count(df, column, subtopics=None):
    # Expand and strip spaces
    df_expanded = df.drop(column, axis=1).join(
        df[column].str.split(',').apply(
            lambda x: [item.strip() for item in x] if x else []
        ).explode().reset_index(drop=True).rename(column)
    )
    
    counts = df_expanded.groupby(['Paper Type', column]).size().unstack(fill_value=0)
    counts.loc['Total'] = counts.sum()  # Tambahkan baris 'Total'

    # Urutkan berdasarkan 'Total', jika ada subtopics, urutkan dalam grup subtopics terlebih dahulu
    if subtopics:
        sorted_counts = pd.DataFrame()
        for group, topics in subtopics.items():
            relevant_topics = [topic for topic in topics if topic in counts.columns]
            sub_df = counts[relevant_topics] if relevant_topics else pd.DataFrame()
            sub_df_sorted = sub_df.sort_values(by='Total', ascending=False, axis=1)
            sorted_counts = pd.concat([sorted_counts, sub_df_sorted], axis=1)
        counts = pd.concat([sorted_counts, counts.drop(columns=[topic for sublist in subtopics.values() for topic in sublist if topic in counts.columns])], axis=1)
    counts_sorted = counts.sort_values(by='Total', ascending=False, axis=1)
    
    return counts_sorted

# Load data
input_filename = '../input.csv'
df = pd.read_csv(input_filename)

# Sub Topik untuk pengelompokan
sub_topics = {
    'Security': ['Authorization', 'Authentication', 'Confidentiality', 'Integrity', 'Availability', 'Identification', 'Non-repudiation'],
    'Privacy': ['Anonymity', 'Unobservability', 'Awareness', 'Policy', 'Unlinkability', 'Deniability']
}

# Initialize an empty DataFrame for the aggregated results
aggregated_df = pd.DataFrame()

# Process 'Topic' with subtopics
aggregated_df = pd.concat([aggregated_df, expand_and_count(df, 'Topic', sub_topics), pd.DataFrame({' ': ''}, index=[0, 'Total'])], axis=1)

# Process the other columns and sort by 'Total'
columns_to_process = ['Strategy', 'Metaverse', 'Reality', 'Evaluation']
for column in columns_to_process:
    temp_df = expand_and_count(df, column).sort_values(by='Total', ascending=False, axis=1)
    # Add a space (' ') column for visual separation between categories
    aggregated_df = pd.concat([aggregated_df, temp_df, pd.DataFrame({' ': ''}, index=[0, 'Total'])], axis=1)

# Drop the last empty column for visual separation
aggregated_df = aggregated_df.iloc[:, :-1]

# Save the aggregated data to a CSV file
aggregated_df.to_csv('output_aggregated2.csv')

# Function to create LaTeX table code without NaN and with integers
def create_latex_table(df):
    return df.fillna('').applymap(lambda x: f"{int(x)}" if pd.notnull(x) and x != '' else '').to_latex(index=False, escape=False)

# Save the LaTeX code to a TXT file
latex_code = create_latex_table(aggregated_df)
with open('output_latex2.txt', 'w') as f:
    f.write(latex_code)

print("Aggregated data saved to 'output_aggregated.csv'. LaTeX code saved to 'output_latex.txt'.")
