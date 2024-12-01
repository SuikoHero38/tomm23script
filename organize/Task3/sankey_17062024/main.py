import pandas as pd
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

# Parse input data
data = """
Algorithm Performance [14] Application
Algorithm Performance [6] Evaluation
Algorithm Performance [3] Model
Algorithm Performance [2] System
Algorithm Performance [28] Technique
User Experience [6] Application
User Experience [19] Evaluation
User Experience [1] Model
User Experience [4] Technique
User Performance [2] Application
User Performance [6] Evaluation
User Performance [1] Technique
Environment & Practices [3] Application
Environment & Practices [8] Evaluation
Environment & Practices [2] System
Environment & Practices [1] Technique
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
Authorization [2] Mixed Reality
Authorization [6] Augmented Reality
Authorization [1] Virtual Reality
Confidentiality [8] Augmented Reality
Confidentiality [2] Mixed Reality
Confidentiality [3] Virtual Reality
Non-repudiation [2] Augmented Reality
Non-repudiation [1] Virtual Reality
Unlinkability [2] Augmented Reality
Unlinkability [2] Virtual Reality
Unlinkability [1] Extended Reality
Integrity [7] Virtual Reality
Integrity [1] Augmented Reality
Policy [1] Virtual Reality
Policy [2] Augmented Reality
Policy [1] Mixed Reality
Deniability [1] Virtual Reality
Deniability [1] Mixed Reality
Deniability [1] Augmented Reality
Awareness [5] Augmented Reality
Awareness [3] Virtual Reality
Awareness [1] Extended Reality
Availability [1] Extended Reality
Availability [1] Mixed Reality
Availability [2] Augmented Reality
Authentication [12] Virtual Reality
Authentication [5] Augmented Reality
Authentication [1] Extended Reality
Anonymity [3] Augmented Reality
Anonymity [4] Virtual Reality
Anonymity [1] Mixed Reality
Unobservability [7] Virtual Reality
Unobservability [1] Extended Reality
Unobservability [3] Mixed Reality
Unobservability [2] Augmented Reality
Identification [4] Virtual Reality
Identification [2] Augmented Reality
Identification [1] Extended Reality
"""

# Function to parse the input data
def parse_data(data):
    links = []
    lines = data.strip().split('\n')
    for line in lines:
        source, weight_target = line.split(' [')
        weight, target = weight_target.split('] ')
        links.append([source.strip(), target.strip(), int(weight)])
    return links

# Parse the data
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
        pad=45,
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

fig.update_layout(
    font_size=10,
    height=800,
    width=1200,
    margin=dict(l=20, r=20, t=20, b=20),
    autosize=False,
    hovermode="closest"
)

# Save as SVG
fig.write_image("sankey_diagram3temp.svg", format='svg')

print("Sankey diagram has been saved as sankey_diagram.svg")