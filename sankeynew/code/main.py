import os

def parse_reference_file(filename):
    transitions = {}
    current_key = ""
    with open(filename, 'r') as file:
        for line in file:
            if line.strip() and line.startswith('#'):
                continue
            if '>' in line:
                current_key = line.strip()
                transitions[current_key] = []
            elif '[' in line and ']' in line:
                transitions[current_key].append(line.strip())
    return transitions

def process_input_line(line, transitions):
    categories = line.strip().split(',')
    result = []
    for i in range(len(categories) - 1):
        key = f"{categories[i]} > {categories[i+1]}"
        if key in transitions:
            result.extend(transitions[key])
        else:
            result.append(f"No transition data available for {key}")
    return result

def main():
    transitions = parse_reference_file('reference.txt')
    with open('input.txt', 'r') as infile:
        lines = infile.readlines()

    for line in lines:
        categories = line.strip().split(',')
        filename_suffix = "_".join(categories)  # Create the filename based on the categories sequence
        result = process_input_line(line, transitions)
        output_filename = f"output/{filename_suffix}.txt"
        with open(output_filename, 'w') as outfile:
            outfile.write("\n".join(result))
            print(f"Output written to {output_filename}")

if __name__ == "__main__":
    main()
