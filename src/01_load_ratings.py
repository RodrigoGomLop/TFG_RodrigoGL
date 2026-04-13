import pandas as pd

# Ruta al archivo
path = "data/raw/ol_dump_ratings_2025-11-06.txt"

# Cargar dataset
df = pd.read_csv(
    path,
    sep="\t",
    header=None,
    names=["work_id", "edition_id", "rating", "date"]
)

# limpieza de datos
# eliminar columna edition_id
df = df.drop(columns=["edition_id"])

# limpiar work_id (quitar "/works/")
df["work_id"] = df["work_id"].str.replace("/works/", "", regex=False)

# Convertir tipos
df["rating"] = df["rating"].astype(int)
df["date"] = pd.to_datetime(df["date"])

# Crear user_id artificial
df["user_id"] = df.index

# Reordenar columnas
df = df[["user_id", "work_id", "rating", "date"]]

# Validamos y vemos si hay nulos o valores extraños

print("INFO:")
print(df.info())

print("\nDESCRIBE:")
print(df["rating"].describe())

print("\nVALORES NULOS:")
print(df.isnull().sum())

# guardamos el dataset limpio

output_path = "data/processed/ratings_clean.csv"
df.to_csv(output_path, index=False)

print(f"\nDataset guardado en: {output_path}")


