import csv

# Define a function to check if any of the keywords exist in the given text
def has_keywords(text, keywords):
    text_lower = text.lower()
    return any(keyword.lower() in text_lower for keyword in keywords)

# Define a function to analyze the file
def analyze_and_save_files(input_files, output_file, keywords_group3):
    records_to_save = []

    for file_path in input_files:
        with open(file_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Check if the row contains any keywords from group3
                if not has_keywords(row['Title'], keywords_group3) and not has_keywords(row['Abstract'], keywords_group3):
                    records_to_save.append(row)

    # Save the records to a new CSV file
    with open(output_file, 'w', encoding='utf-8', newline='') as out_file:
        if records_to_save:
            writer = csv.DictWriter(out_file, fieldnames=reader.fieldnames)
            writer.writeheader()
            writer.writerows(records_to_save)

# Define your keywords for group3
keywords_group3 = ["protocol","wireless","network","artificial intelligence","machine learning"]
input_files = ['greensec1.csv']  # Update this with your actual input file paths
output_file = 'filtered_records.csv'

# Analyze files and save results
analyze_and_save_files(input_files, output_file, keywords_group3)

print("Filtered records saved to 'filtered_records.csv'.")
