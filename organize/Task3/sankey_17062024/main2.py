import pandas as pd
import plotly.graph_objects as go
import matplotlib.colors as mcolors

# Function to parse the input data
def parse_data(data):
    links = []
    lines = data.strip().split('\n')
    for line in lines:
        source, weight_target = line.split(' [')
        weight, target = weight_target.split('] ')
        links.append([source.strip(), target.strip(), int(weight)])
    return links

# Parse input data
data = """
AP [14] Application
AP [6] Evaluation
AP [3] Model
AP [2] System
AP [28] Technique
UE [6] Application
UE [19] Evaluation
UE [1] Model
UE [4] Technique
UP [2] Application
UP [6] Evaluation
UP [1] Technique
UWP [3] Application
UWP [8] Evaluation
UWP [2] System
UWP [1] Technique
Application [6] USS
Application [1] UIST
Application [1] TVCG
Application [6] Other Venues
Application [2] CHI
Application [2] VR_Conf
Application [3] SP
Evaluation [4] USS
Evaluation [11] Other Venues
Evaluation [7] CHI
Evaluation [2] SP
Evaluation [3] VR_Conf
Evaluation [2] UIST
Evaluation [1] TVCG
Model [4] Other Venues
System [1] CHI
System [3] Other Venues
Technique [2] SP
Technique [10] Other Venues
Technique [3] USS
Technique [2] UIST
Technique [3] TVCG
Technique [8] VR_Conf
USS [2] Authorization
USS [2] Confidentiality
USS [1] Non-repudiation
USS [2] Policy
USS [1] Integrity
USS [4] Unobservability
USS [1] Unlinkability
UIST [1] Unlinkability
UIST [2] Awareness
UIST [1] Integrity
UIST [1] Confidentiality
TVCG [1] Integrity
TVCG [1] Confidentiality
TVCG [2] Anonymity
TVCG [1] Unobservability
Other Venues [3] Confidentiality
Other Venues [2] Policy
Other Venues [2] Availability
Other Venues [8] Authentication
Other Venues [1] Non-repudiation
Other Venues [3] Identification
Other Venues [2] Unobservability
Other Venues [4] Awareness
Other Venues [3] Integrity
Other Venues [4] Authorization
Other Venues [1] Unlinkability
Other Venues [1] Anonymity
CHI [1] Deniability
CHI [2] Awareness
CHI [2] Confidentiality
CHI [1] Unobservability
CHI [2] Identification
CHI [1] Authentication
CHI [1] Authorization
VR_Conf [4] Authentication
VR_Conf [1] Integrity
VR_Conf [1] Confidentiality
VR_Conf [3] Unobservability
VR_Conf [1] Deniability
VR_Conf [1] Identification
VR_Conf [1] Unlinkability
VR_Conf [1] Anonymity
SP [1] Authorization
SP [2] Anonymity
SP [1] Awareness
SP [2] Authentication
SP [1] Identification
Authorization [2] MR
Authorization [6] AR
Authorization [1] VR
Confidentiality [8] AR
Confidentiality [2] MR
Confidentiality [3] VR
Non-repudiation [2] AR
Non-repudiation [1] VR
Unlinkability [2] AR
Unlinkability [2] VR
Unlinkability [1] XR
Integrity [7] VR
Integrity [1] AR
Policy [1] VR
Policy [2] AR
Policy [1] MR
Deniability [1] VR
Deniability [1] MR
Deniability [1] AR
Awareness [5] AR
Awareness [3] VR
Awareness [1] XR
Availability [1] XR
Availability [1] MR
Availability [2] AR
Authentication [12] VR
Authentication [5] AR
Authentication [1] XR
Anonymity [3] AR
Anonymity [4] VR
Anonymity [1] MR
Unobservability [7] VR
Unobservability [1] XR
Unobservability [3] MR
Unobservability [2] AR
Identification [4] VR
Identification [2] AR
Identification [1] XR
"""

links = parse_data(data)

# Create a DataFrame from the parsed data
df = pd.DataFrame(links, columns=['source', 'target', 'value'])

# Combine 'Augmented Reality' and 'AR' to have the same color
df['source'] = df['source'].replace('Augmented Reality', 'AR')
df['target'] = df['target'].replace('Augmented Reality', 'AR')

# Prepare data for Sankey diagram
all_nodes = list(pd.unique(df[['source', 'target']].values.ravel('K')))
source_indices = [all_nodes.index(src) for src in df['source']]
target_indices = [all_nodes.index(tgt) for tgt in df['target']]

# Create a gradient of colors for the nodes
color_palette = list(mcolors.CSS4_COLORS.values())
node_colors = [color_palette[i % len(color_palette)] for i in range(len(all_nodes))]

# Ensure 'AR' is consistently colored
ar_color = mcolors.CSS4_COLORS['deepskyblue']
for i, node in enumerate(all_nodes):
    if node == 'AR':
        node_colors[i] = ar_color

# Add numbers to labels
node_labels = [f"{node}: {sum(df[df['source'] == node]['value']) + sum(df[df['target'] == node]['value'])}" for node in all_nodes]

# Generate link colors
link_colors = [node_colors[all_nodes.index(src)] for src in df['source']]

# Create the Sankey diagram
fig = go.Figure(data=[go.Sankey(
    node=dict(
        pad=15,
        thickness=20,
        line=dict(color="black", width=0.5),
        label=node_labels,
        color=node_colors
    ),
    link=dict(
        source=source_indices,
        target=target_indices,
        value=df['value'],
        color=link_colors
    )
)])

# Add annotations for node labels
for i, label in enumerate(node_labels):
    fig.add_annotation(
        x=fig.data[0].node.x[i] if fig.data[0].node.x is not None else 0.5,
        y=fig.data[0].node.y[i] + 0.1 if fig.data[0].node.y is not None else 0.5,
        text=label,
        showarrow=False,
        font=dict(size=10)
    )

# Set figure title and layout
fig.update_layout(
    title_text="Sankey Diagram of Research Paper Associations",
    font=dict(size=10),
    height=800,
    width=1200
)

# Save the figure as an SVG file
fig.write_image("sankey_diagram.svg", format='svg')

print("Sankey diagram has been saved as sankey_diagram.svg")