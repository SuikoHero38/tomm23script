import csv
from collections import defaultdict

# Define a function to check if any of the keywords exist in the given text
def has_keywords(text, keywords_group1, keywords_group2):
    text_lower = (text or "").lower()
    return any(kw1.lower() in text_lower for kw1 in keywords_group1) and any(kw2.lower() in text_lower for kw2 in keywords_group2)

# Define a function to analyze the file
def analyze_and_save_files(input_files, output_file, keywords_group1, keywords_group2):
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
                    'Title': has_keywords(row.get('Title', ''), keywords_group1, keywords_group2),
                    'Abstract': has_keywords(row.get('Abstract', ''), keywords_group1, keywords_group2),
                    'Keywords': has_keywords(row.get('Keywords', ''), keywords_group1, keywords_group2),
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

# Define your keywords
keywords_group1 = ["metaverse", "extended reality", "mixed reality", "augmented reality", "virtual reality"]
keywords_group2 = ["security", "privacy"]
input_files = [f'input{i}new.csv' for i in range(11, 12)]  # Adjust range for the number of files
output_file = 'records_with_keywords7.csv'

# Analyze files and save results
none_records_examples = analyze_and_save_files(input_files, output_file, keywords_group1, keywords_group2)

# Print 5 examples of records with no keywords found
print("5 examples of records with no keywords found:")
for record in none_records_examples:
    print(record)
