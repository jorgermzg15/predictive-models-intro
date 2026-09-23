# Datos del caso MPG: carga y preparación (idénticas a las de la sesión 1)
import pandas as pd
import requests
import sqlite3
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder


def cargar_mpg():
    """Descarga la base SQLite del caso MPG y regresa el DataFrame sin nulos (392 autos)."""
    url = "https://raw.githubusercontent.com/davidjamesknight/SQLite_databases_for_learning_data_science/main/mpg.db"
    with open("mpg.db", "wb") as f:
        f.write(requests.get(url).content)

    query = """
    SELECT
        O.mpg,
        O.cylinders,
        O.displacement,
        O.horsepower,
        O.weight,
        O.acceleration,
        O.model_year,
        ORG.origin,
        N.name
    FROM
        Observation AS O
    JOIN
        Origin AS ORG ON O.origin_id = ORG.origin_id
    JOIN
        Name AS N ON O.name_id = N.name_id
    """
    df = pd.read_sql_query(query, sqlite3.connect("mpg.db"))

    # Sólo 'horsepower' tiene nulos (1.5% de las filas): se eliminan
    return df.dropna(subset=['horsepower'])


def preparar_mpg(df, test_size=0.2, random_state=42):
    """Split 80/20 y One-Hot de 'origin' con los autos americanos como referencia.

    Regresa X_train, X_test, y_train, y_test listos para modelar (todo numérico).
    """
    X = df.drop(columns=['mpg', 'name'])
    y = df['mpg']

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state
    )

    ohe = OneHotEncoder(drop=['usa'], sparse_output=False)
    dummies_train = pd.DataFrame(
        ohe.fit_transform(X_train[['origin']]),
        columns=ohe.get_feature_names_out(), index=X_train.index
    )
    dummies_test = pd.DataFrame(
        ohe.transform(X_test[['origin']]),
        columns=ohe.get_feature_names_out(), index=X_test.index
    )

    X_train_enc = pd.concat([X_train.drop(columns=['origin']), dummies_train], axis=1)
    X_test_enc = pd.concat([X_test.drop(columns=['origin']), dummies_test], axis=1)

    print(f"Train: {X_train_enc.shape} | Test: {X_test_enc.shape}")
    print(f"Variables: {list(X_train_enc.columns)}")
    return X_train_enc, X_test_enc, y_train, y_test
