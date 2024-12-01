import csv
from collections import defaultdict

# Initialize dictionaries to hold counts
strategy_per_year = defaultdict(lambda: defaultdict(int))
topic_per_year = defaultdict(lambda: defaultdict(int))

# Read the input CSV and count associations
input_filename = '../input.csv'  # Adjust the path if the file is in a different location

# Define the output filename
output_filename = 'output.txt'

with open(input_filename, mode='r', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        year = row['Year']
        strategies = row['Strategy'].split(',')  # Assuming strategies are separated by semicolons
        topics = row['Topic'].split(',')  # Assuming topics are separated by semicolons

        # Count strategies and topics per year
        for strategy in strategies:
            strategy_per_year[year][strategy.strip()] += 1
        for topic in topics:
            topic_per_year[year][topic.strip()] += 1

# Write the counts to a text file
with open(output_filename, mode='w', encoding='utf-8') as outfile:
    outfile.write("Strategy Counts Per Year:\n")
    for year, strategies in strategy_per_year.items():
        outfile.write(f"Year {year}:\n")
        for strategy, count in strategies.items():
            outfile.write(f"\t{strategy}: {count}\n")

    outfile.write("\nTopic Counts Per Year:\n")
    for year, topics in topic_per_year.items():
        outfile.write(f"Year {year}:\n")
        for topic, count in topics.items():
            outfile.write(f"\t{topic}: {count}\n")

print("The counts have been saved to output.txt.")
