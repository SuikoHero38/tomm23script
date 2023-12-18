import pandas as pd
from collections import defaultdict
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Load the CSV file
df = pd.read_csv('dataset.csv')

# Define a default dictionary to hold concatenated strings for each group
grouped_texts = defaultdict(lambda: defaultdict(str))

# Function to safely convert to string and concatenate
def safe_str_concat(existing, addition):
    if pd.notna(addition):
        return existing + str(addition) + ' '
    return existing

# Iterate over the DataFrame rows
for _, row in df.iterrows():
    if pd.notna(row['Paper Type (Final)']):
        paper_type = row['Paper Type (Final)']
        # Safely concatenate texts based on the group
        grouped_texts[paper_type]['title'] = safe_str_concat(grouped_texts[paper_type]['title'], row.get('Title'))
        grouped_texts[paper_type]['abstract'] = safe_str_concat(grouped_texts[paper_type]['abstract'], row.get('Abstract'))
        grouped_texts[paper_type]['keywords'] = safe_str_concat(grouped_texts[paper_type]['keywords'], row.get('Keywords'))

# Function to write texts to files
def write_to_file(filename, text):
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(text.strip())

# Write each group's text to separate text files
for group, texts in grouped_texts.items():
    write_to_file(f'{group}_titles.txt', texts['title'])
    write_to_file(f'{group}_abstracts.txt', texts['abstract'])
    write_to_file(f'{group}_keywords.txt', texts['keywords'])
    write_to_file(f'{group}_titles_abstracts.txt', texts['title'] + texts['abstract'])
    write_to_file(f'{group}_titles_keywords.txt', texts['title'] + texts['keywords'])
    write_to_file(f'{group}_abstracts_keywords.txt', texts['abstract'] + texts['keywords'])
    write_to_file(f'{group}_all.txt', texts['title'] + texts['abstract'] + texts['keywords'])
    
# Function to generate word cloud from text
def generate_wordcloud(text, filename):
    # Generate the word cloud
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)

    # Display the word cloud using matplotlib
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    
    # Save the word cloud to a file
    plt.savefig(f'{filename}.png')
    plt.close()

# Function to read text from file
def read_text_from_file(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        return file.read()

# Create word clouds for each group and text type
for group in grouped_texts.keys():
    for text_type in ['titles', 'abstracts', 'keywords', 'titles_abstracts', 'titles_keywords', 'abstracts_keywords', 'all']:
        text = read_text_from_file(f'{group}_{text_type}.txt')
        generate_wordcloud(text, f'{group}_{text_type}_wordcloud')
