import pandas as pd

def expand_and_count(df, column, subtopics=None):
    # Expand and strip spaces
    df_expanded = df.drop(column, axis=1).join(
        df[column].str.split(',').apply(
            lambda x: [item.strip() for item in x] if x else []
        ).explode().reset_index(drop=True).rename(column)
    )
    
    counts = df_expanded.groupby(['Paper Type', column]).size().unstack(fill_value=0)

    # Tambahkan baris 'Total' sebelum pengurutan
    counts.loc['Total'] = counts.sum()

    # Urutkan jika ada subtopics
    if subtopics:
        sorted_counts = pd.DataFrame()
        for group, topics in subtopics.items():
            relevant_topics = [topic for topic in topics if topic in counts.columns]
            if relevant_topics:
                sub_df = counts.loc[:, relevant_topics]
                sub_total = sub_df.loc['Total', :].sort_values(ascending=False)
                sorted_counts = pd.concat([sorted_counts, counts.loc[:, sub_total.index]], axis=1)
        counts = sorted_counts

    return counts

# Load data
input_filename = '../input.csv'
df = pd.read_csv(input_filename)

# Sub Topik untuk pengelompokan
sub_topics = {
    'Security': ['Authorization', 'Authentication', 'Confidentiality', 'Integrity', 'Availability', 'Identification', 'Non-repudiation'],
    'Privacy': ['Anonymity', 'Unobservability', 'Awareness', 'Policy', 'Unlinkability', 'Deniability']
}

# Pengolahan
aggregated_df = expand_and_count(df, 'Topic', subtopics=sub_topics)

# Untuk kolom lainnya
columns_to_process = ['Strategy', 'Metaverse', 'Reality', 'Evaluation']
for column in columns_to_process:
    temp_df = expand_and_count(df, column)
    aggregated_df = pd.concat([aggregated_df, temp_df], axis=1)

# Simpan ke CSV
aggregated_df.to_csv('output_aggregated.csv')

# Buat LaTeX table
def create_latex_table(df):
    return df.fillna('').applymap(lambda x: f"{int(x)}" if pd.notnull(x) and x != '' else '').to_latex(index=False, escape=False)

latex_code = create_latex_table(aggregated_df)
with open('output_latex.txt', 'w') as f:
    f.write(latex_code)

print("Aggregated data saved to 'output_aggregated.csv'. LaTeX code saved to 'output_latex.txt'.")
