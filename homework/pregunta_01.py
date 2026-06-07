"""
Escriba el codigo que ejecute la accion solicitada en la pregunta.
"""

import os
import pandas as pd
from pathlib import Path
 
 
def pregunta_01():
    df = pd.read_csv("files/input/solicitudes_de_credito.csv",
                     sep=";", index_col=0, dtype={"estrato": str})

    def limpiar(serie, recortar=True):
        s = serie.str.lower()
        if recortar:
            s = s.str.strip()
        return s.str.replace(r"\s+", " ", regex=True)

    for col in ["sexo", "tipo_de_emprendimiento", "idea_negocio", "línea_credito"]:
        df[col] = limpiar(df[col])

    # barrio: sin strip inicial, luego reemplazar _ y -
    df["barrio"] = limpiar(df["barrio"], recortar=False)
    df["barrio"] = df["barrio"].str.replace("_", " ", regex=False)
    df["barrio"] = df["barrio"].str.replace("-", " ", regex=False)
    df["barrio"] = limpiar(df["barrio"], recortar=False)
    df["barrio"] = df["barrio"].str.replace(r"no\.\s*(\d+)", r"no. \1", regex=True)
    df["barrio"] = limpiar(df["barrio"], recortar=False)

    for col in ["idea_negocio", "línea_credito"]:
        df[col] = df[col].str.replace("_", " ", regex=False)
        df[col] = df[col].str.replace("-", " ", regex=False)
        df[col] = limpiar(df[col])

    df["estrato"] = df["estrato"].str.strip().astype(int).astype(str)
    df = df.replace("", float("nan")).dropna()

    df["monto_del_credito"] = (
        df["monto_del_credito"].astype(str).str.strip()
        .str.replace(r"[\$\s,]", "", regex=True)
        .str.replace(r"\.00$", "", regex=True)
        .astype(int)
    )

    # fecha: normalizar a DD/MM/YYYY
    serie = df["fecha_de_beneficio"].astype(str).str.strip()
    seg = serie.str.split("/", expand=True)
    anio_inicio = seg[0].str.len() == 4
    dia = seg[0].where(~anio_inicio, seg[2])
    mes = seg[1]
    anio = seg[2].where(~anio_inicio, seg[0])
    df["fecha_de_beneficio"] = dia.str.zfill(2) + "/" + mes.str.zfill(2) + "/" + anio

    df["comuna_ciudadano"] = df["comuna_ciudadano"].astype(int)
    df = df.drop_duplicates()

    os.makedirs("files/output", exist_ok=True)
    df.to_csv("files/output/solicitudes_de_credito.csv", sep=";", index=False)
 

    """
    Realice la limpieza del archivo "files/input/solicitudes_de_credito.csv".
    El archivo tiene problemas como registros duplicados y datos faltantes.
    Tenga en cuenta todas las verificaciones discutidas en clase para
    realizar la limpieza de los datos.

    El archivo limpio debe escribirse en "files/output/solicitudes_de_credito.csv"

    """
