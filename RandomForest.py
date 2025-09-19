import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, KFold, GridSearchCV
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.metrics import make_scorer, r2_score, root_mean_squared_error
from sklearn.base import clone
import joblib

# Lista de features a usar y target
FEATURES = [
    'GrLivArea', 'ExterQual', 'GarageCars', 'LotArea', 'BsmtFinSF1',
    'OverallQual', 'TotalBsmtSF', '1stFlrSF', 'GarageArea', '2ndFlrSF',
    'YearBuilt', 'YearRemodAdd', 'LandContour', 'TotRmsAbvGrd', 'OverallCond'
]
TARGET = "SalePrice"

# Mapeo de ExterQual a valores ordinales
EXTERQUAL_MAP = {"Ex":5, "Gd":4, "TA":3, "Fa":2, "Po":1}

if __name__ == "__main__":
    # Cargar el dataset y filtrar solo las columnas necesarias
    df = pd.read_csv("train.csv")
    df = df[FEATURES + [TARGET]].copy()

    # Mapear ExterQual a ordinal
    df["ExterQual"] = df["ExterQual"].map(EXTERQUAL_MAP).fillna(3)

    # Separación de features (X) y target (y)
    X = df[FEATURES].copy()
    y = df[TARGET].copy()

    # Splits: train (70%), val (15%), test (15%)
    X_train, X_tmp, y_train, y_tmp = train_test_split(X, y, test_size=0.30, random_state=42)
    X_val, X_test, y_val, y_test = train_test_split(X_tmp, y_tmp, test_size=0.50, random_state=42)

    print(f"Train: {X_train.shape}, Val: {X_val.shape}, Test: {X_test.shape}")

    # Preprocesamiento
    # - Categóricas: imputar con la moda + OneHotEncoder
    # - Numéricas: imputar con la mediana
    cat_features = ["LandContour"]
    num_features = [c for c in FEATURES if c not in cat_features]

    preprocessor = ColumnTransformer(
        transformers=[
            ("cat", Pipeline(steps=[
                ("imputer", SimpleImputer(strategy="most_frequent")),
                ("ohe", OneHotEncoder(drop="first", handle_unknown="ignore"))
            ]), cat_features),
            ("num", Pipeline(steps=[
                ("imputer", SimpleImputer(strategy="median"))
            ]), num_features),
    ])

    # Pipeline: modelo y preprocesamiento
    rf = RandomForestRegressor(random_state=42, n_jobs=-1)
    pipe = Pipeline(steps=[("prep", preprocessor), ("rf", rf)])

    # Grid de hiperparámetros del Random Forest
    param_grid = {
        "rf__n_estimators": [200, 400, 800],
        "rf__max_depth": [None, 12, 24, 36],
        "rf__min_samples_split": [2, 5, 10],
        "rf__min_samples_leaf": [1, 2, 4],
        "rf__max_features": ["sqrt", 0.5],
        "rf__bootstrap": [True]
    }

    # GridSearch con cross-validation sobre el conjunto de entrenamiento
    cv = KFold(n_splits=5, shuffle=True, random_state=42)
    scoring = {
        "rmse": make_scorer(root_mean_squared_error, greater_is_better=False),
        "r2": "r2"
    }
    gs = GridSearchCV(
        estimator=pipe,
        param_grid=param_grid,
        scoring=scoring,
        refit="rmse",   # modelo que minimiza el RMSE
        cv=cv,
        n_jobs=-1,
        verbose=3
    )

    gs.fit(X_train, y_train)

    # Resultados del GridSearch
    best_rmse_cv = -gs.best_score_
    best_params = gs.best_params_
    best_idx = gs.best_index_
    best_r2_cv = gs.cv_results_["mean_test_r2"][best_idx]
    std_r2_cv = gs.cv_results_["std_test_r2"][best_idx]

    print("\n[GridSearch] Mejores hiperparámetros:")
    for k, v in best_params.items(): print(f"  {k}: {v}")
    print(f"[GridSearch] CV RMSE (train): {best_rmse_cv:.2f}")
    print(f"[GridSearch] CV R^2   (train): {best_r2_cv:.4f} ± {std_r2_cv:.4f}")

    # Evaluación en el conjunto de validación
    best_model_train = gs.best_estimator_
    y_val_pred = best_model_train.predict(X_val)
    print(f"[VAL]   R^2:  {r2_score(y_val, y_val_pred):.4f} | RMSE: {root_mean_squared_error(y_val, y_val_pred):.2f}")

    # Reentrenar en TRAIN+VAL con los mejores hiperparámetros
    X_trainval = pd.concat([X_train, X_val], axis=0)
    y_trainval = pd.concat([y_train, y_val], axis=0)

    final_model = clone(gs.best_estimator_)
    final_model.fit(X_trainval, y_trainval)

    # Evaluación con el conjunto de test (hold-out)
    y_test_pred = final_model.predict(X_test)
    print(f"[TEST]  R^2:  {r2_score(y_test, y_test_pred):.4f} | RMSE: {root_mean_squared_error(y_test, y_test_pred):.2f}")

    # Guardado del pipeline final
    out_path = "modelo.pkl"
    joblib.dump(final_model, out_path)
    print(f"\n[OK] Pipeline final (train+val) guardado en: {out_path}")
