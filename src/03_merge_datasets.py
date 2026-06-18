import pandas as pd

# carga de los 2 datasets limpios.

ratings = pd.read_csv("data/processed/ratings_clean.csv")
works = pd.read_csv("data/processed/works_clean.csv")

print("Ratings:", ratings.shape)
print("Works:", works.shape)

# merge

df = ratings.merge(works, on="work_id", how="inner")


print("Despues del merge:", df.shape)

# eliminacion de nulos
df = df.dropna(subset=["subjects_str"])

# porcentaje de registros conservados.

retention = len(df) / len(ratings) * 100

print("\nPORCENTAJE DE REGISTROS CONSERVADOS:")
print(f"{retention:.2f}%")

# validacion de columnas.

print("\nCOLUMNAS:")
print(df.columns)

# validacion de nulos.

print("\nNULOS:")
print(df.isnull().sum())

# validacion de duplicados.

print("\nDUPLICADOS:")
print(df.duplicated().sum())

# numero de libros unicos.

print("\nLIBROS UNICOS:")
print(df["work_id"].nunique())

# numero de usuarios.

print("\nUSUARIOS:")
print(df["user_id"].nunique())

# estadisticas de ratings.

print("\nESTADISTICAS DE RATING:")
print(df["rating"].describe())

# muestra del dataset.

print("\nMUESTRA:")
print(df.head())

# guardar dataset final.

df.to_csv(
    "data/processed/final_dataset.csv",
    index=False
)

print("\nfinal_dataset.csv guardado")