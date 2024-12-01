import csv
from collections import defaultdict

# Define a function to check if any of the keywords exist in the given text
def has_keywords(text, keywords):
    return any(keyword.lower() in (text or "").lower() for keyword in keywords)

# Define a function to analyze the file
def analyze_and_save_files(input_files, output_file, keywords):
    all_records_with_keywords = []
    none_records_examples = []
    seen_titles = set()  # Set to keep track of titles we've seen

    for file_path in input_files:
        with open(file_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                title = row.get('Title', '').strip().lower()
                if title in seen_titles:
                    duplicate_mark = 'Duplicate'
                else:
                    duplicate_mark = ''
                    seen_titles.add(title)
                
                key_found_in = {
                    'Title': has_keywords(row.get('Title', ''), keywords),
                    'Abstract': has_keywords(row.get('Abstract', ''), keywords),
                    'Keywords': has_keywords(row.get('Keywords', ''), keywords),
                }
                # Create a string representation of where the keywords were found
                found_in = '_'.join(sorted(key for key, found in key_found_in.items() if found))
                if found_in:
                    row['Found In'] = found_in
                    row['Duplicate'] = duplicate_mark
                    all_records_with_keywords.append(row)
                elif len(none_records_examples) < 5 and not duplicate_mark:
                    none_records_examples.append(row)

    # Save all records with keywords to a new CSV file
    with open(output_file, 'w', encoding='utf-8', newline='') as out_file:
        if all_records_with_keywords:
            writer = csv.DictWriter(out_file, fieldnames=all_records_with_keywords[0].keys())
            writer.writeheader()
            writer.writerows(all_records_with_keywords)

    return none_records_examples

# Define your keywords and files
keywords = ["security", "privacy","authentication","attack","access control"]
#input_files = [f'input{i}new.csv' for i in range(1, 10)]  # Adjust range for the number of files
input_files = [f'records_with_keywords_group{i}_excluded.csv' for i in range(1, 2)]
output_file = 'records_with_keywords10.csv'

# Analyze files and save results
none_records_examples = analyze_and_save_files(input_files, output_file, keywords)

# Print 5 examples of records with no keywords found
print("5 examples of records with no keywords found:")
for record in none_records_examples:
    print(record)
