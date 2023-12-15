import csv
import re

def matches_condition(row, keywords):
    # Columns to search
    columns_to_search = ['Title', 'Document Title', 'Abstract Note', 'Abstract', 'Manual Tags', 'Author Keywords','Keywords']

    # Check for 'AND' and 'OR' operations
    if ' AND ' in keywords:
        left, right = keywords.split('AND')
        return matches_condition(row, left.strip()) and matches_condition(row, right.strip())
    
    elif ' OR ' in keywords:
        or_keywords = keywords.split(' OR ')
        return any(matches_condition(row, kw.strip()) for kw in or_keywords)
    
    # Base case: search for the individual keyword in the specified columns
    else:
        for col in columns_to_search:
            if col in row and keywords.lower() in row[col].lower():
                return True
        return False


def search_csv(input_file, output_file, keywords):
    with open(input_file, 'r', encoding='utf-8') as csv_file:
        reader = csv.DictReader(csv_file)
        matching_rows = [row for row in reader if matches_condition(row, keywords)]
        
        if matching_rows:
            with open(output_file, 'w', encoding='utf-8', newline='') as out_file:
                writer = csv.DictWriter(out_file, fieldnames=matching_rows[0].keys())
                writer.writeheader()
                writer.writerows(matching_rows)
            
            print(f"Saved {len(matching_rows)} matching rows to {output_file}")
        else:
            print("No rows matched the criteria.")

if __name__ == '__main__':
    input_file = 'Inputx.csv'  # Change this to your CSV file's name, change x with number e.g. 1,2,3 and so on
    output_file = 'Outputx.csv'  # Name of the file to save results, change x with number e.g. 1,2,3 and so on
    #You may iterate the code

    keywords = input("Enter your keywords (you can use AND, OR, and parentheses): ") #Use "metaverse" OR "extended reality" OR "mixed reality" OR "augmented reality" OR "virtual reality"
    search_csv(input_file, output_file, keywords)
