import csv

# Define a function to check if any of the keywords exist in the given text
def has_keywords(text, keywords):
    text_lower = (text or "").lower()
    return any(keyword.lower() in text_lower for keyword in keywords)

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
                
                # Check for group 1 keywords in each column
                found_in_group1 = '_'.join(column for column in ['Title', 'Abstract', 'Keywords'] if has_keywords(row.get(column, ''), keywords_group1))
                # Check for group 2 keywords in each column
                found_in_group2 = '_'.join(column for column in ['Title', 'Abstract', 'Keywords'] if has_keywords(row.get(column, ''), keywords_group2))
                
                # If at least one keyword from each group is found in any of the columns, add the row to the results
                if found_in_group1 and found_in_group2:
                    row['Found In Group1'] = found_in_group1
                    row['Found In Group2'] = found_in_group2
                    row['Duplicate'] = duplicate_mark
                    all_records_with_keywords.append(row)
                elif len(none_records_examples) < 5 and not duplicate_mark:
                    none_records_examples.append(row)

    # Save all records with keywords to a new CSV file
    with open(output_file, 'w', encoding='utf-8', newline='') as out_file:
        if all_records_with_keywords:
            fieldnames = reader.fieldnames + ['Found In Group1', 'Found In Group2', 'Duplicate']
            writer = csv.DictWriter(out_file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(all_records_with_keywords)

    return none_records_examples

# Define your keywords
keywords_group1 = ["metaverse", "extended reality", "mixed reality", "augmented reality", "virtual reality"]
#keywords_group2 = ["security", "privacy","authentication","attack","access","control","threat"]
keywords_group2 = ["security", "privacy","authentication","attack","access control"]
input_files = [f'input{i}new.csv' for i in range(1, 2)]  # Adjust range for the number of files
output_file = 'records_both2.csv'

# Analyze files and save results
none_records_examples = analyze_and_save_files(input_files, output_file, keywords_group1, keywords_group2)

# Print 5 examples of records with no keywords found
print("5 examples of records with no keywords found:")
for record in none_records_examples:
    print(record)
