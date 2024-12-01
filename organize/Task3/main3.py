import csv
from collections import defaultdict

def process_multiple_values(value):
    return [item.strip() for item in value.split(',') if item]

associations_to_calculate = [
    ('Evaluation', 'Paper Type'),
    ('Paper Type', 'Venue'),
    ('Venue', 'Topic'),
    ('Topic', 'Reality'),
]

association_counters = {assoc: defaultdict(lambda: defaultdict(int)) for assoc in associations_to_calculate}

input_filename = '../input.csv'  # Adjust the path if necessary

with open(input_filename, mode='r', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    for row in reader:
        for (column_a, column_b) in associations_to_calculate:
            values_a = process_multiple_values(row[column_a])
            values_b = process_multiple_values(row[column_b])
            for value_a in values_a:
                for value_b in values_b:
                    association_counters[(column_a, column_b)][value_a][value_b] += 1

# Identify venues with less than 5 occurrences to merge into "Other Venues"
other_venues_count = defaultdict(int)
for value_a, topics in association_counters[('Paper Type', 'Venue')].items():
    for venue, count in topics.items():
        if count < 5:
            other_venues_count[venue] += count

# Apply merging for "Other Venues"
for value_a, topics in list(association_counters[('Paper Type', 'Venue')].items()):
    for venue, count in list(topics.items()):
        if venue in other_venues_count:
            del association_counters[('Paper Type', 'Venue')][value_a][venue]
            association_counters[('Paper Type', 'Venue')][value_a]['Other Venues'] += count

# Adjust Topic associations to consider "Other Venues"
to_adjust = []
for value_a, topics in association_counters[('Venue', 'Topic')].items():
    if value_a in other_venues_count:
        to_adjust.append((value_a, topics))

for value_a, topics in to_adjust:
    for topic, count in topics.items():
        if value_a not in association_counters[('Venue', 'Topic')]:
            association_counters[('Venue', 'Topic')][value_a] = defaultdict(int)
        association_counters[('Venue', 'Topic')]['Other Venues'][topic] += count
    del association_counters[('Venue', 'Topic')][value_a]

output_filename = 'associations_count11.txt'

with open(output_filename, mode='w', encoding='utf-8') as output_file:
    for (column_a, column_b), counter in association_counters.items():
        output_file.write(f"//Associations between {column_a} and {column_b}:\n")
        for value_a, value_b_counts in counter.items():
            for value_b, count in value_b_counts.items():
                output_file.write(f"{value_a} [{count}] {value_b}\n")
        output_file.write("\n")
