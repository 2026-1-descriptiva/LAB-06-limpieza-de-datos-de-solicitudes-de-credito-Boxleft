"""
Ejecuta este script desde la raíz del proyecto (donde está la carpeta files/).
Te dará la información exacta para encontrar el problema.
"""
import pandas as pd
 
df0 = pd.read_csv("files/input/solicitudes_de_credito.csv", sep=";")
df0 = df0.drop(columns=["Unnamed: 0"])
df0 = df0.dropna()
 
print("=" * 60)
print(f"Filas totales tras dropna: {len(df0)}")
print("=" * 60)
 
# 1. Revisar caracteres raros en cada columna de texto
text_cols = ["sexo", "tipo_de_emprendimiento", "idea_negocio",
             "barrio", "línea_credito", "monto_del_credito", "fecha_de_beneficio"]
 
print("\n--- Valores únicos con caracteres especiales ---")
for col in text_cols:
    col_series = df0[col].astype(str)
    # Buscar \r, \n, tabs, espacios al inicio/final
    has_cr    = col_series.str.contains("\r", na=False).sum()
    has_nl    = col_series.str.contains("\n", na=False).sum()
    has_trail = (col_series != col_series.str.strip()).sum()
    if has_cr or has_nl or has_trail:
        print(f"  '{col}': \\r={has_cr}, \\n={has_nl}, trailing/leading spaces={has_trail}")
 
# 2. Mostrar valores únicos de columnas clave
print("\n--- línea_credito valores únicos (raw) ---")
for v in df0["línea_credito"].unique():
    print(f"  {repr(v)}")
 
print("\n--- barrio con underscore o guion ---")
mask = df0["barrio"].str.contains(r"[_\-]", na=False)
print(df0.loc[mask, "barrio"].value_counts().head(20).to_string())
 
print("\n--- barrio con trailing underscore ---")
mask2 = df0["barrio"].str.endswith("_")
print(df0.loc[mask2, "barrio"].value_counts().head(20).to_string())
 
# 3. Pipeline actual vs. esperado
print("\n" + "=" * 60)
print("Resultado del pipeline ACTUAL (sin correcciones):")
df = df0.copy()
for col in ["sexo", "tipo_de_emprendimiento", "idea_negocio", "barrio", "línea_credito"]:
    df[col] = df[col].str.lower().str.strip().str.replace("_", " ", regex=False)
df["monto_del_credito"] = (
    df["monto_del_credito"]
    .str.replace(r"[\$,\s]", "", regex=True)
    .str.replace(".00", "", regex=False)
)
df["fecha_de_beneficio"] = pd.to_datetime(
    df["fecha_de_beneficio"], format="mixed", dayfirst=True
).dt.strftime("%Y-%m-%d")
df = df.drop_duplicates(
    subset=["sexo", "tipo_de_emprendimiento", "barrio", "estrato",
            "comuna_ciudadano", "fecha_de_beneficio", "monto_del_credito", "línea_credito"]
)
df["monto_del_credito"] = df["monto_del_credito"].astype(int)
df["comuna_ciudadano"] = df["comuna_ciudadano"].astype(int)
print(f"  Total: {len(df)}")
print(f"  sexo:  {df.sexo.value_counts().to_list()}")
print(f"  tipo:  {df.tipo_de_emprendimiento.value_counts().to_list()}")
print(f"  línea: {df.línea_credito.value_counts().to_list()}")
print(f"  estrato: {df.estrato.value_counts().to_list()}")
 
print("\nEsperado:")
print("  Total: 10206")
print("  sexo:  [6617, 3589]")
print("  tipo:  [5636, 2205, 2201, 164]")
print("  línea: [10020, 70, 55, 33, 21, 4, 1, 1, 1]")
print("  estrato: [5023, 3151, 2029, 3]")