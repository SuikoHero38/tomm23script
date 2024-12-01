import pandas as pd
import plotly.graph_objects as go
import itertools
import os

def create_sankey(df, column_order, filename):
    labels = []
    source = []
    target = []
    value = []  # Initialize value here
    value_counts = {}  # To keep track of the frequency of each value

    # Prepare data
    for col in column_order:
        df[col] = df[col].apply(lambda x: x.split(',') if isinstance(x, str) else x)

    for i in range(len(column_order)-1):
        current_col, next_col = column_order[i], column_order[i+1]

        for _, row in df.iterrows():
            for val1 in row[current_col] if isinstance(row[current_col], list) else [row[current_col]]:
                val1 = f"{current_col}: {val1}"
                if val1 not in labels:
                    labels.append(val1)
                    value_counts[val1] = 0
                value_counts[val1] += 1
                for val2 in row[next_col] if isinstance(row[next_col], list) else [row[next_col]]:
                    val2 = f"{next_col}: {val2}"
                    if val2 not in labels:
                        labels.append(val2)
                        value_counts[val2] = 0
                    value_counts[val2] += 1

                    source.append(labels.index(val1))
                    target.append(labels.index(val2))
                    value.append(1)

    # Update labels with frequency count
    labels = [f"{label} ({value_counts[label]})" for label in labels]

    # Generate node colors
    node_colors = ['blue', 'green', 'red', 'cyan', 'magenta', 'yellow', 'black', 'purple', 'orange', 'grey'] * (len(labels) // 10 + 1)

    # Create the Sankey diagram
    fig = go.Figure(data=[go.Sankey(
        node=dict(
            pad=15,
            thickness=20,
            line=dict(color='black', width=0.5),
            label=labels,
            color=node_colors[:len(labels)]
        ),
        link=dict(
            source=source,
            target=target,
            value=value
        ))])

    # Save the figure
    fig.write_image(filename)

if __name__ == '__main__':
    # Read the CSV file
    df = pd.read_csv('dataset.csv')

    # All columns to consider for Sankey diagrams
    all_columns = ['Evaluation Scenario', 'Paper Type', 'Publication Venue', 'Research Topic', 'Metaverse Component']

    # Create the sankey_diagrams folder if it doesn't exist
    os.makedirs('sankey_diagrams', exist_ok=True)
    
    filename = f'sankey.png'
    create_sankey(df, list(all_columns), filename)
    print(f"Sankey diagram saved as {filename}")

    # Generate Sankey diagrams for all permutations of column names
    #for permutation in itertools.permutations(all_columns):
    #    filename = f'sankey_diagrams/sankey_{"_".join(permutation)}.png'
    #    create_sankey(df, list(permutation), filename)
    #    print(f"Sankey diagram saved as {filename}")
