import csv
from collections import defaultdict

# Function to process multiple values in a cell (assuming values are comma-separated)
def process_multiple_values(value):
    return [item.strip() for item in value.split(',') if item]

# Define associations to calculate
associations_to_calculate = [
    ('Evaluation', 'Paper Type'),
    ('Paper Type', 'Venue'),
    ('Venue', 'Topic'),
    ('Topic', 'Reality'),
    #('Topic', 'Metaverse'),
    #('Evaluation', 'Reality'),
    #('Evaluation', 'Metaverse'),
    #('Reality', 'Topic'),
    #('Metaverse', 'Topic'),
    #('Topic', 'Paper Type'),
    #('Paper Type', 'Venue'),
    #('Paper Type', 'Topic'),
    #('Paper Type', 'Strategy2'),
    #('Paper Type', 'Metaverse'),
    #('Paper Type', 'Reality'),
    #('Paper Type', 'Evaluation2'),
]

# Initialize counters for each association
association_counters = {assoc: defaultdict(lambda: defaultdict(int)) for assoc in associations_to_calculate}

# Read the input CSV and count associations
input_filename = '../input.csv'  # Adjust the path if the file is in a different location

# Define the output filename
output_filename = 'associations_count20.txt'

with open(input_filename, mode='r', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    for row in reader:
        for (column_a, column_b) in associations_to_calculate:
            values_a = process_multiple_values(row[column_a])
            values_b = process_multiple_values(row[column_b])
            for value_a in values_a:
                for value_b in values_b:
                    association_counters[(column_a, column_b)][value_a][value_b] += 1

# Open the output file and write the associations and their counts
with open(output_filename, mode='w', encoding='utf-8') as output_file:
    for (column_a, column_b), counter in association_counters.items():
        output_file.write(f"//Associations between {column_a} and {column_b}:\n")
        for value_a, value_b_counts in counter.items():
            for value_b, count in value_b_counts.items():
                output_file.write(f"{value_a} [{count}] {value_b}\n")
        output_file.write("\n")
