# Datos del caso Titanic: carga y preparación (idénticas a las de la sesión 2)
import numpy as np
import pandas as pd
import requests
import sqlite3
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder


def cargar_titanic():
    """Descarga la base SQLite del caso Titanic y regresa el DataFrame (891 pasajeros)."""
    url = "https://raw.githubusercontent.com/davidjamesknight/SQLite_databases_for_learning_data_science/main/titanic.db"
    with open("titanic.db", "wb") as f:
        f.write(requests.get(url).content)

    query = """
    SELECT
        O.survived,
        O.pclass,
        O.age,
        O.sibsp,
        O.parch,
        O.fare,
        O.adult_male,
        O.alone,
        S.sex,
        E.embarked
    FROM
        Observation AS O
    JOIN
        Sex AS S ON O.sex_id = S.sex_id
    JOIN
        Embarked AS E ON O.embarked_id = E.embarked_id
    """
    return pd.read_sql_query(query, sqlite3.connect("titanic.db"))


def preparar_titanic(df, test_size=0.2, random_state=42):
    """Split estratificado 80/20, imputación con datos de train, variables nuevas y dummies.

    Replica la sesión 2: se imputa 'age' con la mediana y 'embarked' con la moda (ambas de train),
    se crean 'viaja_solo' y 'es_menor', y las referencias de las dummies son 3ª clase,
    Southampton y mujer. Regresa X_train, X_test, y_train, y_test listos para modelar.
    """
    X = df.drop(columns=['survived', 'adult_male', 'alone'])
    y = df['survived']

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state, stratify=y
    )

    mediana_edad = X_train['age'].median()
    moda_puerto = X_train['embarked'].mode()[0]

    preparados = []
    for datos in (X_train, X_test):
        datos = datos.copy()
        datos['age'] = datos['age'].fillna(mediana_edad)
        datos['embarked'] = datos['embarked'].fillna(moda_puerto)
        datos['viaja_solo'] = np.where(datos['sibsp'] + datos['parch'] > 0, 0, 1)
        datos['es_menor'] = np.where(datos['age'] <= 16, 1, 0)
        preparados.append(datos.drop(columns=['sibsp', 'parch']))

    X_train_prep, X_test_prep = preparados
    categoricas = ['pclass', 'embarked', 'sex']

    ohe = OneHotEncoder(drop=[3, 'S', 'female'], sparse_output=False)
    dummies_train = pd.DataFrame(
        ohe.fit_transform(X_train_prep[categoricas]),
        columns=ohe.get_feature_names_out(), index=X_train_prep.index
    )
    dummies_test = pd.DataFrame(
        ohe.transform(X_test_prep[categoricas]),
        columns=ohe.get_feature_names_out(), index=X_test_prep.index
    )

    X_train_enc = pd.concat([X_train_prep.drop(columns=categoricas), dummies_train], axis=1)
    X_test_enc = pd.concat([X_test_prep.drop(columns=categoricas), dummies_test], axis=1)

    print(f"Train: {X_train_enc.shape} | Test: {X_test_enc.shape}")
    print(f"Variables: {list(X_train_enc.columns)}")
    return X_train_enc, X_test_enc, y_train, y_test
