import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict

# Read the input CSV
input_filename = '../input.csv'  # Adjust the path as necessary
df = pd.read_csv(input_filename)

# Expand the 'Strategy' and 'Topic' columns into separate rows
df_strategy_expanded = df.drop('Topic', axis=1).assign(Strategy=df['Strategy'].str.split(',')).explode('Strategy')
df_topic_expanded = df.drop('Strategy', axis=1).assign(Topic=df['Topic'].str.split(',')).explode('Topic')

# Aggregate data for strategies and topics per year
strategy_counts_per_year = df_strategy_expanded.groupby(['Year', 'Strategy']).size().unstack(fill_value=0)
topic_counts_per_year = df_topic_expanded.groupby(['Year', 'Topic']).size().unstack(fill_value=0)

# Menghitung total dari setiap kategori
strategy_totals = df_strategy_expanded.groupby('Strategy').size()
topic_totals = df_topic_expanded.groupby('Topic').size()

# Mengurutkan data berdasarkan total secara descending (dari besar ke kecil)
strategy_order = strategy_totals.sort_values(ascending=True).index.tolist()
topic_order = topic_totals.sort_values(ascending=True).index.tolist()

# Menggunakan urutan ini untuk menyusun ulang kolom DataFrame
strategy_counts_per_year = strategy_counts_per_year[strategy_order]
topic_counts_per_year = topic_counts_per_year[topic_order]

# Mengubah data untuk stackplot
strategy_stackplot_data = strategy_counts_per_year.transpose()
topic_stackplot_data = topic_counts_per_year.transpose()

# Fungsi untuk menggambar stackplot
def plot_stackplot(df, title, filename):
    # Pastikan tidak ada data negatif
    df[df < 0] = 0
    
    fig, ax = plt.subplots(figsize=(12, 6))
    x = df.columns.astype(str)  # Pastikan kolom tahun adalah string
    y = df.values
    labels = df.index.tolist()  # Dapatkan list label dari index DataFrame
    
    # Urutkan berdasarkan kolom terakhir untuk mendapatkan urutan tumpukan di plot
    order = np.argsort(y[:, -1])[::-1]  # Urutkan dari yang terbesar ke yang terkecil
    y = y[order]  # Reorder baris berdasarkan urutan
    labels = [labels[i] for i in order]  # Reorder label berdasarkan urutan yang sama
    
    # Buat stackplot
    stack_coll = ax.stackplot(x, y, labels=labels, baseline='wiggle')
    
    # Styling
    plt.title(title, fontsize=20)
    plt.ylabel('Total', fontsize=20)
    plt.xlabel('Year', fontsize=20)
    plt.xticks(rotation=45, fontsize=14)
    plt.yticks(fontsize=14)
    plt.legend(loc='upper left', fontsize=12)
    plt.tight_layout()
    plt.savefig(filename, format='svg')
    plt.close(fig)

# Example usage
plot_stackplot(strategy_stackplot_data, 'Strategy Stackplot', 'strategy_stackplot3.svg')
plot_stackplot(topic_stackplot_data, 'Topic Stackplot', 'topic_stackplot3.svg')

print("Stackplot charts have been saved as separate SVG files.")
