# 🏡 Inbol – Modelo de Predicción de Avalúos

## 📌 Resumen ejecutivo
**Inbol** es un proyecto orientado a usuarios que desean vender o comprar inmuebles, ofreciendo un avalúo rápido, confiable y cercano al valor de mercado.

- 🎯 **Objetivo**: Reducir el tiempo promedio de venta de propiedades en un **50% en los próximos 24 meses**.
- 🏆 **KPI principal**: Avalúos con un error <10% antes de finalizar 2025.
- 📊 **Estado actual**: El modelo está integrado en la aplicación web de Inbol y ha sido validado con datos de **Ames, Iowa (EE.UU.)**.

---

## 📂 Dataset utilizado
- **Fuente**: [Kaggle – House Prices: Advanced Regression Techniques](https://www.kaggle.com/competitions/house-prices-advanced-regression-techniques)  
- **Archivo / versión**: `train.csv`  
- **Dimensiones**: 1460 filas × 81 columnas  
- **Periodo**: Tabular estático, sin fechas asociadas  
- **Data dictionary**: disponible en [`x_data_dictionary.csv`](https://github.com/Inbol/Modelos/blob/main/x_data_dictionary.csv)
- **Notebook**: generado utiizando el notebook [`EDAHousesPrices.ipynb`](https://colab.research.google.com/drive/1Byt3mMLdjIAmZ__GvRkc380zmx7Qjglf)

---

## ⚙️ Preparación de datos
El pipeline de preparación incluye:

1. Eliminación de variables con >40% de nulos  
2. Mapas ordinales en columnas de calidad y condición  
3. Imputación (mediana para numéricas, moda para categóricas)  
4. Clipping de outliers por cuantiles (0.5–99.5%)  
5. Agrupación de categorías poco frecuentes  
6. Codificación One-Hot para categóricas  
7. Estandarización de variables numéricas  

---

## 🧩 Snippet demostrativo reproducible
Dentro del notebook [`Modelo_house_pricing.ipynb`](https://colab.research.google.com/drive/1aQevN554fqF7oVN1AtNYYkK821wlpDr_?usp=sharing):

- **Ruta**: `/notebooks/Modelo_house_pricing.ipynb`  
- **Celda**: 3 – Función `make_preprocessor_tree()`

```python
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, FunctionTransformer
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
import numpy as np

# Variables numéricas: imputación con mediana + clipping por cuantiles
num_pipeline = Pipeline(steps=[
    ("imputer", SimpleImputer(strategy="median")),
    ("clip", FunctionTransformer(
        lambda X: np.clip(
            X,
            np.quantile(X, 0.005, axis=0),
            np.quantile(X, 0.995, axis=0)
        )
    ))
])

# Variables categóricas: imputación con moda + one-hot encoding
cat_pipeline = Pipeline(steps=[
    ("imputer", SimpleImputer(strategy="most_frequent")),
    ("encoder", OneHotEncoder(handle_unknown="ignore"))
])

preprocessor = ColumnTransformer(
    transformers=[
        ("num", num_pipeline, num_features),
        ("cat", cat_pipeline, cat_features)
    ]
)

