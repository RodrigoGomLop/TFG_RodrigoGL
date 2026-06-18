import json
import pandas as pd
import ast

# cargar ratings para obtener los work_id necesarios.

ratings = pd.read_csv("data/processed/ratings_clean.csv")
work_ids_needed = set(ratings["work_id"].unique())

print(f"Work IDs a buscar: {len(work_ids_needed)}")

# lectura del dump de works.

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

# convertir a dataframe.

df = pd.DataFrame(filtered_data)

print("\nNUMERO DE REGISTROS:")
print(len(df))

# analisis inicial.

print("\nNULOS POR COLUMNA:")
print(df.isnull().sum())

print("\nPORCENTAJE DE NULOS:")
print((df.isnull().sum() / len(df)) * 100)

print("\nDUPLICADOS POR WORK_ID:")
print(df["work_id"].duplicated().sum())

print("\nANTES DE LIMPIEZA:")
print(len(df))

# nulos antes de limpiar.

print("\nNULOS ANTES DE LIMPIAR:")
print(df.isnull().sum())

# limpieza.

df = df.dropna(subset=["subjects"])

df = df[df["subjects"] != "[]"]

print("\nDESPUES DE LIMPIEZA:")
print(len(df))

# nulos despues de limpiar.

print("\nNULOS DESPUES DE LIMPIAR:")
print(df.isnull().sum())

# convertir listas.

def parse_subjects(x):
    try:
        return ast.literal_eval(x) if isinstance(x, str) else x
    except:
        return []

df["subjects"] = df["subjects"].apply(parse_subjects)

# longitud de subjects.

df["subjects_length"] = df["subjects"].apply(
    lambda x: len(x) if isinstance(x, list) else 0
)

print("\nESTADISTICAS DE LONGITUD DE SUBJECTS:")
print(df["subjects_length"].describe())

# convertir listas a texto.

df["subjects_str"] = df["subjects"].apply(
    lambda x: " ".join(map(str, x))
)

# dataset final.

df = df[["work_id", "title", "subjects_str"]]

print("\nMUESTRA DEL DATASET:")
print(df.head())

# guardar dataset.

df.to_csv(
    "data/processed/works_clean.csv",
    index=False
)

print("\nworks_clean.csv guardado")