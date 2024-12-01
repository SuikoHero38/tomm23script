import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.sankey import Sankey

# Fungsi untuk membaca data dari file
def read_data(file_path):
    data = []
    skip_line = True  # Skip lines until we find the start of data
    with open(file_path, 'r') as f:
        for line in f:
            if line.strip().startswith("//"):
                skip_line = False  # Found the start of data section, stop skipping lines
                continue
            if not skip_line:
                parts = line.strip().split('[')
                if len(parts) == 2:  # Ensure the line is in expected format
                    source, rest = parts
                    value, target = rest.split(']')
                    data.append([source.strip(), target.strip(), int(value.strip())])
    df = pd.DataFrame(data, columns=['Source', 'Target', 'Value'])
    # Mencetak DataFrame ke konsol
    print(df)
    # Menyimpan DataFrame ke file CSV
    df.to_csv('output.csv', index=False)
    return df

# Fungsi untuk menggambar Sankey diagram
def draw_sankey(df, filename='sankey_diagram.svg'):
    label_list = pd.concat([df['Source'], df['Target']]).unique().tolist()
    label_dict = {name: idx for idx, name in enumerate(label_list)}

    flows = []
    for index, row in df.iterrows():
        source_idx = label_dict[row['Source']]
        target_idx = label_dict[row['Target']]
        value = row['Value']
        flows.append((source_idx, target_idx, value))

    # Menyiapkan flows dan labels untuk Sankey diagram
    sankey_flows = [flow[2] for flow in flows]
    sankey_labels = [None] * len(label_list)  # Create a list of None labels to avoid matplotlib error
    orientations = [0 for _ in sankey_flows]  # Set all orientations to 0 for simplicity

    # Menggambar diagram
    fig, ax = plt.subplots()
    sankey = Sankey(ax=ax, unit=None)
    sankey.add(flows=sankey_flows, labels=sankey_labels, orientations=orientations, facecolor='lightblue', alpha=0.5)
    sankey.finish()
    plt.tight_layout()
    plt.savefig(filename, format='svg')
    plt.close(fig)

# Main
if __name__ == '__main__':
    file_path = 'input.txt'  # Sesuaikan dengan path file Anda
    data = read_data(file_path)
    draw_sankey(data, 'sankey_diagram_updated.svg')
