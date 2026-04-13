import pandas as pd

# carga de los 2 datasets limpios

ratings = pd.read_csv("data/processed/ratings_clean.csv")
works = pd.read_csv("data/processed/works_clean.csv")

print("Ratings:", ratings.shape)
print("Works:", works.shape)

# inner join para quedarnos solo con los libros que tienen ratings y su información

df = ratings.merge(works, on="work_id", how="inner")

print("Después del merge:", df.shape)

# validamos

print("\nColumnas:")
print(df.columns)

print("\nNulos:")
print(df.isnull().sum())

# mostramos el datset final y lo guardamos

print(df.head())
df.to_csv("data/processed/final_dataset.csv", index=False)
print("\nfinal_dataset.csv guardado")