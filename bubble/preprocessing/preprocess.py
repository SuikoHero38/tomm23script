import pandas as pd

def read_csv_data(file_path):
    # Read CSV, assuming first row is header and actual data starts from second row
    return pd.read_csv(file_path, header=0, skiprows=[1])

def parse_txt_input(file_path):
    with open(file_path, 'r') as file:
        combinations = [line.strip().split(',') for line in file if line.strip()]
    return combinations

def compute_values_for_combination(data, comb):
    category_column_map = {
        'evaluation': 'Evaluation Scenario 2 Long',
        'metaverse': 'Metaverse Component Long',
        'reality': 'Reality Long',
        'venue': 'Venue Modified',
        'strategy': 'Research Strategy 2 Modified',
        'papertype': 'Paper Type',
        'properties': 'Properties'
    }

    x_column = category_column_map[comb[0]]
    y_column = category_column_map[comb[1]]
    color_column = category_column_map[comb[2]]

    result = []
    for x_val in category_values[comb[0]]:
        for y_val in category_values[comb[1]]:
            for color_val in category_values[comb[2]]:
                filtered_data = data[(data[x_column].str.contains(x_val, na=False)) &
                                     (data[y_column].str.contains(y_val, na=False)) &
                                     (data[color_column].str.contains(color_val, na=False))]
                count = filtered_data.shape[0]  # Menghitung jumlah baris yang memenuhi kriteria
                if count > 0:  # Hanya tambahkan ke hasil jika count lebih dari 0
                    result.append(f"{x_val},{y_val},{color_val},{count}")
    return result

def write_results_to_file(results, filename):
    with open(filename, 'w') as file:
        for line in results:
            file.write(line + '\n')

# Mapping of categories to possible values (as an example)
category_values = {
    'evaluation': ['Algorithm Performance', 'Environment and Practices', 'User Performance', 'User Experience'],
    'metaverse': ['Virtual World', 'Lifelogging', 'Augmented Reality', 'Mirror World'],
    'reality': ['Virtual Reality', 'Augmented Reality', 'Mixed Reality', 'Extended Reality'],
    'strategy': ['Benchmarking', 'Human Experimentation', 'Interview', 'Questionnaire', 'Data Science', 'Engineering Research', 'Meta Science'],
    'papertype': ['Application', 'Evaluation', 'Model', 'System', 'Technique'],
    'venue': ['VR', 'CHI', 'UIST', 'TVCG', 'Other Venues', 'USS', 'SP']
}

# Example file paths
csv_file_path = 'dataset.csv'
txt_file_path = 'input.txt'
output_path_template = 'outputpreprocess/output_{}.txt'

# Main execution
data = read_csv_data(csv_file_path)
combinations = parse_txt_input(txt_file_path)

for i, comb in enumerate(combinations):
    results = compute_values_for_combination(data, comb)
    output_filename = output_path_template.format(i + 1)
    write_results_to_file(results, output_filename)
