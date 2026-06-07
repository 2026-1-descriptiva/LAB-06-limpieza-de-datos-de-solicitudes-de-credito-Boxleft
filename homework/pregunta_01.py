"""
Escriba el codigo que ejecute la accion solicitada en la pregunta.
"""


import pandas as pd
from pathlib import Path
 
 
def pregunta_01():

    df = pd.read_csv("files/input/solicitudes_de_credito.csv", sep=";")
 
    # 1. Eliminar columna índice sobrante
    df = df.drop(columns=["Unnamed: 0"])
 
    # 2. Eliminar filas con valores nulos
    df = df.dropna()
 
    for col in ["sexo", "tipo_de_emprendimiento", "idea_negocio", "barrio"]:
        df[col] = (
            df[col]
            .str.lower()
            .str.replace("_", " ", regex=False)
            .str.strip()
        )
 
    # línea_credito sí necesita reemplazar guiones además de underscores
    # para unificar variantes como "empresarial-ed.-", "empresarial_ed._", "empresarial ed."
    df["línea_credito"] = (
        df["línea_credito"]
        .str.lower()
        .str.replace("_", " ", regex=False)
        .str.replace("-", " ", regex=False)
        .str.strip()
    )
 
    # 4. Limpiar monto_del_credito
    df["monto_del_credito"] = (
        df["monto_del_credito"]
        .str.replace(r"[\$,\s]", "", regex=True)
        .str.replace(".00", "", regex=False)
    )
 
    # 5. Unificar formato de fecha a YYYY-MM-DD
    df["fecha_de_beneficio"] = pd.to_datetime(
        df["fecha_de_beneficio"], format="mixed", dayfirst=True
    ).dt.strftime("%Y-%m-%d")
 
    # 6. Eliminar registros duplicados según columnas clave
    df = df.drop_duplicates(
        subset=[
            "sexo",
            "tipo_de_emprendimiento",
            "barrio",
            "estrato",
            "comuna_ciudadano",
            "fecha_de_beneficio",
            "monto_del_credito",
            "línea_credito",
        ]
    )
 
    # 7. Convertir tipos de datos finales
    df["monto_del_credito"] = df["monto_del_credito"].astype(int)
    df["comuna_ciudadano"] = df["comuna_ciudadano"].astype(int)
 
    # Guardar archivo limpio
    Path("files/output").mkdir(exist_ok=True)
    df.to_csv("files/output/solicitudes_de_credito.csv", index=False, sep=";")
 

    """
    Realice la limpieza del archivo "files/input/solicitudes_de_credito.csv".
    El archivo tiene problemas como registros duplicados y datos faltantes.
    Tenga en cuenta todas las verificaciones discutidas en clase para
    realizar la limpieza de los datos.

    El archivo limpio debe escribirse en "files/output/solicitudes_de_credito.csv"

    """
