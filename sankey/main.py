import pandas as pd
import plotly.graph_objects as go
import itertools
import os

def create_sankey(df, column_order, filename):
    labels = []
    source = []
    target = []
    value = []

    # Prepare data
    for col in column_order:
        df[col] = df[col].apply(lambda x: x.split(',') if isinstance(x, str) else x)

    for i in range(len(column_order)-1):
        current_col, next_col = column_order[i], column_order[i+1]

        for _, row in df.iterrows():
            for val1 in row[current_col] if isinstance(row[current_col], list) else [row[current_col]]:
                if val1 not in labels:
                    labels.append(val1)
                for val2 in row[next_col] if isinstance(row[next_col], list) else [row[next_col]]:
                    if val2 not in labels:
                        labels.append(val2)

                    source.append(labels.index(val1))
                    target.append(labels.index(val2))
                    value.append(1)

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
    all_columns = ['Paper Type', 'Research Topic', 'Metaverse Component', 'Publication Venue', 'Evaluation Scenario']

    # Create the sankey_diagrams folder if it doesn't exist
    os.makedirs('sankey_diagrams', exist_ok=True)

    # Generate Sankey diagrams for all permutations of column names
    for permutation in itertools.permutations(all_columns):
        filename = f'sankey_diagrams/sankey_{"_".join(permutation)}.png'
        create_sankey(df, list(permutation), filename)
        print(f"Sankey diagram saved as {filename}")
