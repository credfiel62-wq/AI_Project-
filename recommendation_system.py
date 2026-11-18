import os

import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier


CSV_FILE = "products.csv"
FEATURES = ["feature1", "feature2", "feature3"]

# Genera 100 productos de ejemplo si todavía no existe el archivo CSV.
if not os.path.exists(CSV_FILE):
	rng = np.random.default_rng(42)
	values = rng.random((100, 3))
	labels = (values[:, 0] + values[:, 1] > values[:, 2]).astype(int)
	products = pd.DataFrame(values, columns=FEATURES)
	products["label"] = labels
	products.to_csv(CSV_FILE, index=False)

# Carga los datos y separa las características de las etiquetas.
data = pd.read_csv(CSV_FILE)
X = data[FEATURES]
y = data["label"]

# Divide los productos en conjuntos de entrenamiento y prueba.
X_train, X_test, y_train, y_test = train_test_split(
	X, y, test_size=0.2, random_state=42
)

# Entrena el modelo usando los cinco vecinos más cercanos.
model = KNeighborsClassifier(n_neighbors=5)
model.fit(X_train, y_train)

# Evalúa y muestra la precisión sobre los datos de prueba.
y_pred = model.predict(X_test)
print(f"Precisión: {accuracy_score(y_test, y_pred):.2f}")


def recommend(feature1, feature2, feature3):
	"""Predice la etiqueta recomendada para las características recibidas."""
	product = pd.DataFrame([[feature1, feature2, feature3]], columns=FEATURES)
	return model.predict(product)[0]


# Ejemplo de uso con un producto de muestra.
recommended_label = recommend(0.7, 0.4, 0.2)
print(f"Etiqueta recomendada para el producto de ejemplo: {recommended_label}")

