import json
import pandas as pd
import ast

# cargamos works id pero solo los que tienen ratings ya que el dataset es muy grande
# y lo que vamos a usar son los libros que tienen ratings

ratings = pd.read_csv("data/processed/ratings_clean.csv")
work_ids_needed = set(ratings["work_id"].unique())

print(f"Work IDs a buscar: {len(work_ids_needed)}")

# la ultima columna del dataset es un json con toda la información del libro
# pero el dataset es muy grande así que lo vamos a leer línea por línea y solo extraeremos
# la información de los libros que necesitamos

path = "data/raw/ol_dump_works_2025-11-06.txt"

filtered_data = []

with open(path, "r", encoding="utf-8") as f:
    for i, line in enumerate(f):
        
        parts = line.split("\t")
        
        if len(parts) < 5:
            continue
        
        work_id = parts[1].replace("/works/", "")
        
        if work_id in work_ids_needed:
            try:
                json_data = json.loads(parts[4])
                
                title = json_data.get("title", None)
                subjects = json_data.get("subjects", None)
                
                filtered_data.append({
                    "work_id": work_id,
                    "title": title,
                    "subjects": subjects
                })
            
            except:
                continue
        
        if i % 500000 == 0:
            print(f"Líneas procesadas: {i}")

# Convertimos en un dataframe de pandas

df = pd.DataFrame(filtered_data)

print("Antes de limpieza:", len(df))

# limpieza de datos

# eliminar nulos
df = df.dropna(subset=["subjects"])

# eliminar listas vacías
df = df[df["subjects"] != "[]"]

print("Después de limpieza:", len(df))

# convertimos las cadenas de texto que representan listas en listas reales

def parse_subjects(x):
    try:
        return ast.literal_eval(x) if isinstance(x, str) else x
    except:
        return []

df["subjects"] = df["subjects"].apply(parse_subjects)

# convertir a string las listas
df["subjects_str"] = df["subjects"].apply(lambda x: " ".join(x))

# dataset final con las columnas necesarias

df = df[["work_id", "title", "subjects_str"]]

print(df.head())

# guardamos el dataset limpio

df.to_csv("data/processed/works_clean.csv", index=False)

print("works_clean.csv guardado")