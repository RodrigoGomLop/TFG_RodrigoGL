import pandas as pd

# ruta al archivo.
path = "data/raw/ol_dump_ratings_2025-11-06.txt"

# cargar dataset.
df = pd.read_csv(
    path,
    sep="\t",
    header=None,
    names=["work_id", "edition_id", "rating", "date"]
)

# numero de registros.
print("\nNUMERO DE REGISTROS:")
print(len(df))

# analisis de nulos.
print("\nNULOS POR COLUMNA:")
print(df.isnull().sum())

print("\nPORCENTAJE DE NULOS:")
print((df.isnull().sum() / len(df)) * 100)

# validacion de ratings.
print("\nDISTRIBUCION DE RATINGS:")
print(df["rating"].value_counts().sort_index())

# validacion temporal.
print("\nFECHA MINIMA:")
print(df["date"].min())

print("\nFECHA MAXIMA:")
print(df["date"].max())

# eliminar columna edition_id.
df = df.drop(columns=["edition_id"])

# limpiar work_id.
df["work_id"] = df["work_id"].str.replace("/works/", "", regex=False)

# numero de libros unicos.
print("\nLIBROS UNICOS:")
print(df["work_id"].nunique())

# convertir tipos.
df["rating"] = pd.to_numeric(df["rating"], errors="coerce")
df["date"] = pd.to_datetime(df["date"], errors="coerce")

# comprobar si la conversion ha generado nulos.
print("\nNULOS TRAS CONVERSION:")
print(df.isnull().sum())

# comprobacion del rango de ratings.
print("\nRANGO DE RATINGS:")
print("Minimo:", df["rating"].min())
print("Maximo:", df["rating"].max())

# crear user_id artificial.
df["user_id"] = df.index

# reordenar columnas.
df = df[["user_id", "work_id", "rating", "date"]]

# informacion general.
print("\nINFO:")
df.info()

# estadisticas descriptivas.
print("\nDESCRIBE:")
print(df["rating"].describe())

# validacion final de nulos.
print("\nVALORES NULOS:")
print(df.isnull().sum())

# analisis de duplicados.
duplicates = df.duplicated().sum()

print("\nDUPLICADOS:")
print(duplicates)

if duplicates > 0:
    df = df.drop_duplicates()
    print(f"Se eliminaron {duplicates} registros duplicados")

# guardar dataset limpio.
output_path = "data/processed/ratings_clean.csv"
df.to_csv(output_path, index=False)

print(f"\nDataset guardado en: {output_path}")


