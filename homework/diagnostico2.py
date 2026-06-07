"""
diagnostico2.py - ejecutar desde la raiz del proyecto
"""
import pandas as pd

df0 = pd.read_csv("files/input/solicitudes_de_credito.csv", sep=";")
df0 = df0.drop(columns=["Unnamed: 0"])
df0 = df0.dropna()


def run_pipeline(df0, barrio_dash=False, idea_dash=False, linea_dash=True):
    df = df0.copy()
    for col in ["sexo", "tipo_de_emprendimiento", "idea_negocio", "barrio"]:
        s = df[col].str.lower().str.replace("_", " ", regex=False)
        if col == "barrio" and barrio_dash:
            s = s.str.replace("-", " ", regex=False)
        if col == "idea_negocio" and idea_dash:
            s = s.str.replace("-", " ", regex=False)
        df[col] = s.str.strip()

    lc = df["línea_credito"].str.lower().str.replace("_", " ", regex=False)
    if linea_dash:
        lc = lc.str.replace("-", " ", regex=False)
    df["línea_credito"] = lc.str.strip()

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
                "comuna_ciudadano", "fecha_de_beneficio", "monto_del_credito", "linea_credito"]
        if "linea_credito" in df.columns else
        ["sexo", "tipo_de_emprendimiento", "barrio", "estrato",
         "comuna_ciudadano", "fecha_de_beneficio", "monto_del_credito", "línea_credito"]
    )
    df["monto_del_credito"] = df["monto_del_credito"].astype(int)
    df["comuna_ciudadano"] = df["comuna_ciudadano"].astype(int)
    return df


print("Esperado: Total=10206  sexo=[6617, 3589]  tipo=[5636, 2205, 2201, 164]")
print("=" * 70)

combos = [
    ("barrio_dash=F  idea_dash=F  linea_dash=T", dict(barrio_dash=False, idea_dash=False, linea_dash=True)),
    ("barrio_dash=T  idea_dash=F  linea_dash=T", dict(barrio_dash=True,  idea_dash=False, linea_dash=True)),
    ("barrio_dash=F  idea_dash=T  linea_dash=T", dict(barrio_dash=False, idea_dash=True,  linea_dash=True)),
    ("barrio_dash=T  idea_dash=T  linea_dash=T", dict(barrio_dash=True,  idea_dash=True,  linea_dash=True)),
    ("barrio_dash=F  idea_dash=F  linea_dash=F", dict(barrio_dash=False, idea_dash=False, linea_dash=False)),
]

for label, kwargs in combos:
    df = run_pipeline(df0, **kwargs)
    sexo = df.sexo.value_counts().to_list()
    match = "  <--- MATCH" if sexo == [6617, 3589] else ""
    print(f"{label} | Total={len(df)} sexo={sexo}{match}")