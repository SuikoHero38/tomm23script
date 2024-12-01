import pandas as pd

def explode(df, columns, sep=','):
    new_rows = []
    for _, row in df.iterrows():
        split_values = str(row[columns]).split(sep)
        for val in split_values:
            new_row = row.to_dict()
            new_row[columns] = val.strip()
            new_rows.append(new_row)
    return pd.DataFrame(new_rows)

# Baca file CSV
input_filename = 'inputmetaverse.csv'  # Ganti dengan path file input Anda
output_filename = 'outputmetaverse.csv'  # Ganti dengan path file output Anda

df = pd.read_csv(input_filename)

# Misahkan kolom 'B' yang dipisahkan oleh koma
df_exploded = explode(df, 'Metaverse')

# Tulis hasil ke file CSV baru
df_exploded.to_csv(output_filename, index=False)

print("Proses selesai. File output disimpan sebagai", output_filename)
