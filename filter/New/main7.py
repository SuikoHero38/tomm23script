import csv

# Define a function to check if any of the keywords exist in the given text and return the ones found
def has_keywords_and_return_found(text, keywords):
    text_lower = (text or "").lower()
    found_keywords = [keyword for keyword in keywords if keyword.lower() in text_lower]
    return found_keywords

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
                
                found_keywords_group1 = []
                for column in ['Title', 'Abstract', 'Keywords']:
                    found_keywords_group1.extend(has_keywords_and_return_found(row.get(column, ''), keywords_group1))
                found_in_group1 = '_'.join(set(found_keywords_group1))  # Remove duplicates and join
                
                found_in_group2 = '_'.join(column for column in ['Title', 'Abstract', 'Keywords'] if any(keyword.lower() in (row.get(column, '') or "").lower() for keyword in keywords_group2))
                
                if found_in_group1 and found_in_group2:
                    row['Found In Group1'] = found_in_group1
                    row['Found In Group2'] = found_in_group2
                    row['Keywords Group1 Detected'] = ', '.join(set(found_keywords_group1))  # Add detected keywords from group1
                    row['Duplicate'] = duplicate_mark
                    all_records_with_keywords.append(row)
                elif len(none_records_examples) < 5 and not duplicate_mark:
                    none_records_examples.append(row)

    # Save all records with keywords to a new CSV file
    with open(output_file, 'w', encoding='utf-8', newline='') as out_file:
        if all_records_with_keywords:
            fieldnames = reader.fieldnames + ['Found In Group1', 'Found In Group2', 'Keywords Group1 Detected', 'Duplicate']
            writer = csv.DictWriter(out_file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(all_records_with_keywords)

    return none_records_examples

# Define your keywords
keywords_group1 = ["energy", "green", "power", "consumption"]
keywords_group2 = ["energy", "green", "power", "consumption"]
input_files = [f'input{i}new.csv' for i in range(1, 10)]  # Adjust range for the number of files
output_file = 'records_for_green_security.csv'

# Analyze files and save results
none_records_examples = analyze_and_save_files(input_files, output_file, keywords_group1, keywords_group2)

# Print 5 examples of records with no keywords found
print("5 examples of records with no keywords found:")
for record in none_records_examples:
    print(record)
