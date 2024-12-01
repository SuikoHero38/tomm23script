import pandas as pd
import matplotlib.pyplot as plt

# Define the color map
color_map = {
    'Virtual World': 'blue',
    'Lifelogging': 'green',
    'Augmented Reality': 'red',
    'Mirror World': 'purple',
    'Virtual Reality': 'cyan',
    'Mixed Reality': 'magenta',
    'Extended Reality': 'orange'
}


def load_reference_data(filepath):
    config_data = {}
    current_config = None
    data = []
    with open(filepath, 'r') as file:
        for line in file:
            line = line.strip()
            if '>' in line:
                if current_config and data:
                    column_names = current_config.split(' > ')
                    df = pd.DataFrame(data, columns=column_names)
                    config_data[current_config] = df
                    data = []
                current_config = line  # Update the current configuration
            elif ',' in line:
                parts = [part.strip() for part in line.split(',')]
                if len(parts) == len(current_config.split(' > ')):
                    data.append(parts)
                    
        if current_config and data:
            column_names = current_config.split(' > ')
            df = pd.DataFrame(data, columns=column_names)
            config_data[current_config] = df

    return config_data

def plot_bubble_chart(data, x, y, size, color, output_filename, show_grid=True):
    plt.figure(figsize=(10, 8))
    # Ensure all color categories are in the map, otherwise assign a default color
    bubble_colors = data[color].map(color_map).fillna('gray')  # Using gray for unmapped categories

    scatter = plt.scatter(data[x], data[y], s=data[size].astype(float) * 100, c=bubble_colors, alpha=0.6, edgecolors='w', linewidth=2)
    
    plt.xlabel(x)
    plt.ylabel(y)
    plt.title(f'Bubble Chart: {x} vs {y} by {color}')

    # Create a custom legend for color mapping
    from matplotlib.lines import Line2D
    legend_elements = [Line2D([0], [0], marker='o', color='w', label=k, markerfacecolor=v, markersize=10) for k, v in color_map.items()]
    plt.legend(handles=legend_elements, title="Categories")

    if show_grid:
        plt.grid(True)
    else:
        plt.grid(False)

    plt.savefig(output_filename, format='svg')
    plt.close()


def main():
    reference_data = load_reference_data('reference.txt')
    with open('input.txt', 'r') as file:
        configurations = [line.strip().lower() for line in file if line.strip()]
    
    for config in configurations:
        parts = config.split(',')
        config_key = ' > '.join(parts)
        if config_key in reference_data:
            data = reference_data[config_key]
            x, y, color = parts[:3]
            output_filename = f"{x}_{y}_{color}.svg"
            plot_bubble_chart(data, x, y, 'size', color, output_filename, show_grid=True)  # Set show_grid to False to hide grid
            print(f"Chart saved as {output_filename}")
        else:
            print(f"No data available for configuration: {config_key}")

if __name__ == "__main__":
    main()
