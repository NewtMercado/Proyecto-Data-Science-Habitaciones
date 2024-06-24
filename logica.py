
# 1. SETUP
import numpy as np
import pandas as pd
from sklearn.preprocessing import OneHotEncoder

# 2. CARGA DE DATOS
df = pd.read_csv('dataset_inquilinos.csv', index_col = 'id_inquilino')

df.columns = [
'horario', 'bioritmo', 'nivel_educativo', 'leer', 'animacion', 
'cine', 'mascotas', 'cocinar', 'deporte', 'dieta', 'fumador',
'visitas', 'orden', 'musica_tipo', 'musica_alta', 'plan_perfecto', 'instrumento'
]

# 3. ONE HOT ENCODING
# Realizar el one-hot encoding
encoder = OneHotEncoder(sparse=False)
df_encoded = encoder.fit_transform(df)

# Obtener los nombres de las variables codificadas después de realizar el one-hot encoding
encoded_feature_names = encoder.get_feature_names_out()

# 4. MATRIZ DE SIMILIARIDAD
# Calcular la matriz de similaridad utilizando el punto producto
matriz_s = np.dot(df_encoded, df_encoded.T)

# Define el rango de destino
rango_min = -100
rango_max = 100

# Encontrar el mínimo y máximo valor en matriz_s
min_original = np.min(matriz_s)
max_original = np.max(matriz_s)

# Reescalar la matriz
matriz_s_reescalada = ((matriz_s - min_original) / (max_original - min_original)) * (rango_max - rango_min) + rango_min

# Pasar a Pandas
df_similaridad = pd.DataFrame(matriz_s_reescalada,
        index = df.index,
        columns = df.index)


# 5. BÚSQUEDA DE INQUILINOS COMPATIBLES
'''
Input:
* id_inquilinos: el o los inquilinos actuales DEBE SER UNA LISTA aunque sea solo un dato
* topn: el número de inquilinos compatibles a buscar

Output:
Lista con 2 elementos.
Elemento 0: las características de los inquilinos compatibles
Elemento 1: el dato de similaridad
'''

def inquilinos_compatibles(id_inquilinos, topn):
    # Verificar si todos los ID de inquilinos existen en la matriz de similaridad
    for id_inquilino in id_inquilinos:
        if id_inquilino not in df_similaridad.index:
            return 'Al menos uno de los inquilinos no encontrado'

    # Obtener las filas correspondientes a los inquilinos dados
    filas_inquilinos = df_similaridad.loc[id_inquilinos]

    # Calcular la similitud promedio entre los inquilinos
    similitud_promedio = filas_inquilinos.mean(axis=0)

    # Ordenar los inquilinos en función de su similitud promedio
    inquilinos_similares = similitud_promedio.sort_values(ascending=False)

    # Excluir los inquilinos de referencia (los que están en la lista)
    inquilinos_similares = inquilinos_similares.drop(id_inquilinos)

    # Tomar los topn inquilinos más similares
    topn_inquilinos = inquilinos_similares.head(topn)

    # Obtener los registros de los inquilinos similares
    registros_similares = df.loc[topn_inquilinos.index]

    # Obtener los registros de los inquilinos buscados
    registros_buscados = df.loc[id_inquilinos]

    # Concatenar los registros buscados con los registros similares en las columnas
    resultado = pd.concat([registros_buscados.T, registros_similares.T], axis=1)

    # Crear un objeto Series con la similitud de los inquilinos similares encontrados
    similitud_series = pd.Series(data=topn_inquilinos.values, index=topn_inquilinos.index, name='Similitud')

    # Devolver el resultado y el objeto Series
    return(resultado, similitud_series)

