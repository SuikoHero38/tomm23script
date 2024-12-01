import pandas as pd
import matplotlib.pyplot as plt
import os
import re
from matplotlib.lines import Line2D

# Define the color map by category
category_color_map = {
    'metaverse': {
        'Virtual World': 'blue',
        'Lifelogging': 'green',
        'Augmented Reality': 'red',
        'Mirror World': 'purple'
    },
    'reality': {
        'Virtual Reality': 'cyan',
        'Augmented Reality': 'red',
        'Mixed Reality': 'magenta',
        'Extended Reality': 'orange'
    },
    'papertype': {
        'Application': 'blue',
        'Evaluation': 'green',
        'Model': 'red',
        'System': 'purple',
        'Technique': 'cyan'
    }
}

def load_reference_data(filepath, config):
    # Menyesuaikan nama kolom berdasarkan config dari input.txt
    # config terdiri dari [x, y, color, size]
    column_names = ['X', 'Y', 'Color', 'Size']  # Memetakan langsung ke nama kolom yang lebih umum dan konsisten
    df = pd.read_csv(filepath, header=None, names=column_names)
    print("Loaded data columns:", df.columns)  # Debug: Cetak nama kolom yang dimuat
    return df
    
def get_category_map(color_category):
    # Return relevant color map based on the color category
    print(category_color_map.get(color_category.lower(), {}))
    return category_color_map.get(color_category.lower(), {})

def numerical_sort(file):
    """ Helper function to extract numbers for sorting. """
    parts = re.split(r'(\d+)', file)
    parts[1::2] = map(int, parts[1::2])  # Convert numerical strings to integers
    return parts

def plot_bubble_chart(data, x_label, y_label, color_category, output_filename, show_grid=True):
    plt.figure(figsize=(10, 8))

    print("Data 'Color' before normalization:", data['Color'].unique())  # Cetak nilai 'Color' sebelum normalisasi

    # Normalisasi data 'Color'
    data['Color'] = data['Color'].str.strip().str.title()  # Normalisasi data
    print("Normalized 'Color' data:", data['Color'].unique())  # Cetak nilai 'Color' setelah normalisasi

    color_map = get_category_map(color_category)
    print("Color map used for category '{}':".format(color_category), color_map)  # Cetak color_map yang digunakan

    bubble_colors = data['Color'].map(color_map).fillna('gray')  # Pemetaan warna
    print("Mapped colors after applying color map:", bubble_colors.unique())  # Cetak warna yang berhasil dipetakan

    scatter = plt.scatter(data['X'], data['Y'], s=data['Size'].astype(float) * 100, c=bubble_colors, alpha=0.6, edgecolors='w', linewidth=2)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(f'Bubble Chart: {x_label} vs {y_label} by {color_category}')

    legend_elements = [Line2D([0], [0], marker='o', color='w', label=k, markerfacecolor=v, markersize=10) for k, v in color_map.items()]
    plt.legend(handles=legend_elements, title=color_category.capitalize())

    if show_grid:
        plt.grid(True)
    else:
        plt.grid(False)

    plt.savefig(output_filename, format='svg')
    plt.close()

    print(f"Chart saved as {output_filename}")
    
def main():
    input_directory = 'preprocessing/outputpreprocess/'
    output_directory = 'bubbleoutput/'
    config_path = 'preprocessing/input.txt'
    
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # Load configurations from input.txt
    with open(config_path, 'r') as f:
        configurations = [line.strip().split(',') for line in f.readlines()]

    # Get files and sort them numerically based on part of the filename
    files = [f for f in os.listdir(input_directory) if f.startswith('output_') and f.endswith('.txt')]
    files.sort(key=numerical_sort)  # Sort files numerically

    for i, file in enumerate(files):
        if i < len(configurations):
            config = configurations[i]
            print("Current configuration:", config)  # Debug: Cetak konfigurasi saat ini
            print('File:', file)  # Show which file is being processed
            x_label, y_label, color_category, _ = config
            file_path = os.path.join(input_directory, file)
            data = load_reference_data(file_path, config)  # Load data with dynamic column configuration
            formatted_x_label = x_label.replace(' ', '_').lower()
            formatted_y_label = y_label.replace(' ', '_').lower()
            formatted_color_category = color_category.replace(' ', '_').lower()
            output_filename = os.path.join(output_directory, f"output_{i + 1}_{formatted_x_label}_{formatted_y_label}_{formatted_color_category}.svg")
            plot_bubble_chart(data, x_label, y_label, color_category, output_filename, show_grid=True)
            print(f"Chart saved as {output_filename}")
        else:
            print("Not enough configurations in input.txt to match all output files.")

if __name__ == "__main__":
    main()