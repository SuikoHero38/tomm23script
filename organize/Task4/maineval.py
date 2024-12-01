import pandas as pd
import matplotlib.pyplot as plt

# Create a DataFrame with the provided data
data = {
    'Year': [2023, 2023, 2023, 2023, 2023, 2022, 2022, 2022, 2021, 2021, 2021, 2021, 2020, 2019, 2019, 2019, 2017, 2017, 
             2017, 2016, 2015, 2023, 2023, 2023, 2023, 2023, 2023, 2023, 2023, 2023, 2023, 2022, 2022, 2022, 2022, 2022,
             2021, 2021, 2021, 2021, 2019, 2019, 2019, 2018, 2016, 2015, 2015, 2015, 2015, 2014, 2023, 2023, 2022, 2019,
             2023, 2023, 2022, 2014, 2023, 2023, 2023, 2023, 2023, 2023, 2023, 2023, 2023, 2023, 2022, 2022, 2022, 2022,
             2022, 2021, 2021, 2021, 2021, 2021, 2021, 2020, 2020, 2019, 2018, 2016, 2015],
    'Evaluation': [
        "AP", "AP", "AP", "UWP", "UP,UE,UWP", "AP", "UP,UE,UWP", "AP", "UP,UWP", "UP,UE,UWP", "AP,UWP", "AP", "AP,UP",
        "AP", "UP,UE,UWP", "AP", "AP", "UE,UWP", "UE", "AP", "UWP", "AP", "AP", "AP", "UE,UWP", "UWP", "UWP", "UP,UWP",
        "UWP", "UP,UE,UWP", "UWP", "UWP", "UE", "UWP", "UWP", "UP,UE,UWP", "AP,UWP", "UP,UE,UWP", "UE,UWP", "UP,UWP",
        "UE,UWP", "UP,UE,UWP", "UP,UWP", "UWP", "AP", "UE,UWP", "UE,UWP", "UWP", "UP,UE,UWP", "UWP", "AP", "AP", "UWP",
        "AP", "UWP", "AP", "UWP", "AP", "AP,UP", "AP,UP", "AP,UE", "AP,UP,UWP", "AP", "AP", "AP", "AP", "AP", "AP", "AP",
        "AP", "AP", "AP", "AP,UE,UWP", "AP", "AP", "AP", "AP", "AP", "AP,UP,UE,UWP", "AP", "AP,UE", "AP,UP", "AP", "AP",
        "AP"
    ]
}

df = pd.DataFrame(data)

# Split the 'Evaluation' field and expand into separate rows
df['Evaluation'] = df['Evaluation'].str.split(',')
df = df.explode('Evaluation').reset_index(drop=True)

# Count the occurrences of each evaluation type per year
count_df = df.groupby(['Year', 'Evaluation']).size().unstack(fill_value=0)

# Plotting
ax = count_df.plot(kind='bar', stacked=True, figsize=(14, 8), colormap='viridis')
ax.set_title('Evolution of Evaluation Scenarios Per Year')
ax.set_xlabel('Year')
ax.set_ylabel('Total Papers')
ax.legend(title='Evaluation', bbox_to_anchor=(1.05, 1), loc='upper left')

# Display values on bars
for container in ax.containers:
    ax.bar_label(container, label_type='center')

plt.tight_layout()
plt.show()
