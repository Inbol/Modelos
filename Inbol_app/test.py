import argparse
import pandas as pd
import numpy as np
import joblib
import sys

FEATURES = [
    'GrLivArea', 'ExterQual', 'GarageCars', 'LotArea', 'BsmtFinSF1',
    'OverallQual', 'TotalBsmtSF', '1stFlrSF', 'GarageArea', '2ndFlrSF',
    'YearBuilt', 'YearRemodAdd', 'LandContour', 'TotRmsAbvGrd', 'OverallCond'
]

EXTERQUAL_MAP = {
    "Ex": 5,  # Excellent
    "Gd": 4,  # Good
    "TA": 3,  # Typical/Average
    "Fa": 2,  # Fair
    "Po": 1   # Poor
}

def main(model_path: str, test_csv: str, out_csv: str):
    # Carga del modelo
    print(f"[info] Cargando modelo desde: {model_path}")
    model = joblib.load(model_path)

    # Carga de test.csv
    print(f"[info] Leyendo test set: {test_csv}")
    test_df = pd.read_csv(test_csv)

    # Verificación de Id
    if "Id" not in test_df.columns:
        print("[error] 'test.csv' no contiene la columna 'Id'.", file=sys.stderr)
        sys.exit(1)

    # Asegurar columnas y preprocesamiento mínimo
    missing = [c for c in FEATURES if c not in test_df.columns]
    if missing:
        print(f"[error] Faltan columnas en test.csv: {missing}", file=sys.stderr)
        sys.exit(1)

    X_test = test_df[FEATURES].copy()

    # Mapear ExterQual (ordinal)
    if "ExterQual" in X_test.columns:
        X_test["ExterQual"] = X_test["ExterQual"].map(EXTERQUAL_MAP)
        # Si quedara NaN por algún valor raro, intenta degradarlo a 'TA' (=3)
        X_test["ExterQual"] = X_test["ExterQual"].fillna(3)

    # Nota: LandContour queda como string para que el OneHotEncoder del pipeline lo procese.

    # Predicción de SalePrice sobre test set
    print("[info] Prediciendo SalePrice...")
    preds = model.predict(X_test)

    # Generación del CSV de submission
    submission = pd.DataFrame({
        "Id": test_df["Id"],
        "SalePrice": preds
    })

    submission.to_csv(out_csv, index=False)
    print(f"[ok] Submission generada: {out_csv}")
    print(submission.head())

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Genera submission de Kaggle para House Prices.")
    parser.add_argument("--model", default="modelo.pkl", help="Ruta al modelo .pkl")
    parser.add_argument("--test", default="test.csv", help="Ruta a test.csv")
    parser.add_argument("--out", default="submission_rf.csv", help="Ruta de salida para el CSV de submission")
    args = parser.parse_args()

    main(args.model, args.test, args.out)
