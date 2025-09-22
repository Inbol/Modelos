##Decision log y riesgos

A continuación se presentan las principales decisiones tomadas durante el desarrollo del proyecto:

25/08/2025 – Equipo completo
Decisión: Plan de negocio enfocado en usuarios y empresas de bienes raíces.
Alternativa considerada: Enfoque exclusivo a agencias de bienes raíces.
Motivo: Ampliar el mercado objetivo y viabilidad comercial.

27/08/2025 – Marisol Ramírez
Decisión: Desarrollar un mapa de calor para visualizar las zonas con mayor y menor valor en el mercado
Alternativas consideradas: Tabla comparativa de precios, histogramas interactivos.
Motivo: Visualización rápida e intuitiva y mejora en la experiencia de usuario.

03/09/2025 – Yael Pérez, Daniel Bernal, Marisol Ramírez, Maximiliano de la Cruz
Decisión: Desarrollo de una página web para visibilidad del proyecto.
Alternativa considerada: Prototipo de aplicación móvil.
Motivo: Accesibilidad y difusión a usuarios externos y potenciales clientes.

03/09/2025 – Yael Pérez
Decisión: Utilizar React para el FrontEnd y Fast API para el backend.
Alternativa considerada: -
Motivo: Dominio del lenguaje y capacidad de enseñar relativamente rápida.

05/09/2025   – Marisol Ramírez
Decisión: Creación de variables dummy para las coordenadas de las propiedades usando Google Maps
par definir los vecindarios y asignar posibles puntos en un grid. 
Alternativas consideradas: Coordenadas random, geolocalización con base en landmarks, quitar mapa de calor.
Motivo: Visualización lo más cercana a la realidad.


9/09/2025  – Equipo completo
Decisión: Desarrollar modelos de predicción con menos variables para comprar su desempeño. 
Alternativa considerada: Variables categóricas y/o numéricas para entrenar los modelos.
Motivo: La experiencia del usuario puede disminuir si el cuestionario a contestar contiene 
alrededor de 70 preguntas. Explorar las variables más significativas para las preguntas de 
avalúo rápido. 

12/09/2025  – Daniel Bernal
Decisión: Realizar dos cuetsionarios para el avalúo, correspondiente al modelo con 15 variables
de entrada y modelo completo.
Alternativa considerada: -
Motivo: El usuario puede escoger la opción que más le interese en el momento. Se incluye un
disclaimer con el rango de error en la predicción.


16/09/2025 – Daniel Jiménez, Omar López
Decisión: Ensamble de árboles de decisión para competencia en Kaggle.
Alternativa considerada: Random Forest.
Motivo: Alto desempeño en clasificación tabular y facilidad de ajuste de hiperparámetros.


18/09/2025 – Maximiliano de la Cruz, Daniel Bernal
Decisión: Implementar Random Forest como modelo principal en la aplicación.
Alternativas consideradas: Modelo de Kaggle, regresión lineal.
Motivo: Balance entre explicabilidad, desempeño y compatibilidad con la aplicación.


19/09/2025   – Marisol Ramírez, Maximiliano Cruz 
Decisión: Incluir mapa de propiedades disponibles por vecindario en la página web.
Alternativas consideradas: Asociación por precio, sin mapa
Motivo: EXperiencia de usuario. 


19/09/2025   – Equipo completo
Decisión: Mantener la sección de informes trimestrales en una versión beta.
Alternativas consideradas: quitar la opción del modelo de negocios.
Motivo: Tiempo. 


