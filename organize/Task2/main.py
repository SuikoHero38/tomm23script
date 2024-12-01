import csv
from collections import defaultdict, Counter
from os.path import join, dirname

def process_multiple_values(value):
    # Split the values by comma and strip whitespace
    return [item.strip() for item in value.split(',') if item]

def update_counts(counts_dict, paper_type, values, unique_values):
    for value in values:
        counts_dict[paper_type][value] += 1
        unique_values[value] += 1

# Initialize a nested dictionary to store counts and a Counter for unique values
counts = defaultdict(lambda: defaultdict(int))
unique_values = {'Topic': Counter(), 'Strategy': Counter(), 'Metaverse': Counter(), 'Evaluation': Counter()}

# Define the file paths
input_filename = join(dirname(__file__), '..', 'input.csv')
output_filename = 'output.csv'

# Read the input CSV and update counts
with open(input_filename, mode='r', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    for row in reader:
        paper_type = row['Paper Type']
        topics = process_multiple_values(row['Topic'])
        strategies = process_multiple_values(row['Strategy'])
        metavarses = process_multiple_values(row['Metaverse'])
        evaluations = process_multiple_values(row['Evaluation'])
        
        # Update counts for each column
        update_counts(counts, paper_type, topics, unique_values['Topic'])
        update_counts(counts, paper_type, strategies, unique_values['Strategy'])
        update_counts(counts, paper_type, metavarses, unique_values['Metaverse'])
        update_counts(counts, paper_type, evaluations, unique_values['Evaluation'])

# Write the counts to the output CSV
with open(output_filename, mode='w', encoding='utf-8', newline='') as file:
    writer = csv.writer(file)
    
    # Write the unique values for each category
    for category, values_counter in unique_values.items():
        writer.writerow([category + ' Unique Values:'] + list(values_counter.keys()))
    
    # Write headers
    headers = ['Paper Type', 'Topic', 'Strategy', 'Metaverse', 'Evaluation']
    writer.writerow(headers)
    
    # Write rows
    for paper_type, values_dict in counts.items():
        row = [paper_type]
        for category in headers[1:]:
            row.append(', '.join(f'{key}: {value}' for key, value in values_dict.items() if key.startswith(category)))
        writer.writerow(row)

print(f"Table has been generated in '{output_filename}'.")
