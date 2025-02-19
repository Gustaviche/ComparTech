import numpy as np
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer, make_column_selector
from sklearn.neighbors import NearestNeighbors


url = r'Table_produits_withname.csv' # à modifier
df = pd.read_csv(url)

clean_func = lambda nom: "Google" if "Google" in nom else "Apple"
clean_names = df.loc[(df["Marque"]=="LENOVO") & (df["Catégorie produit"]=="Smartphone"), 'Nom'].apply(clean_func)
df.loc[(df["Marque"]=="LENOVO") & (df["Catégorie produit"]=="Smartphone"), "Marque"] = clean_names

cols_to_keep = ["Prix Actuel", "Catégorie produit", "Couleur", "Marque"]
df_knn = df.loc[:, cols_to_keep]


# Pipeline
numeric_transformer = Pipeline(steps=[
    ('scaler', StandardScaler())
    ])
# One Hot Encoding sur les catégories
categorical_transformer = Pipeline(steps=[
    ('onehot', OneHotEncoder(handle_unknown='ignore'))
    ])
# On applique les transformations précédentes
preprocessor = ColumnTransformer(transformers=[
    ('num', numeric_transformer, make_column_selector(dtype_include=np.number)),
    ('cat', categorical_transformer, make_column_selector(dtype_include=object))
    ])
# On entraîne le modèle
preprocess_pipeline = Pipeline(steps=[
    ('preprocessor', preprocessor)
    ])


data_knn = preprocess_pipeline.fit_transform(df_knn)

knn = NearestNeighbors(n_neighbors=6)
knn.fit(data_knn)


def similarity_search(asin):
    product_index = df.loc[df['ASIN']==asin].index
    product = data_knn[product_index]
    index_similarity = knn.kneighbors(product)[1].tolist()[0][1:]
    return df.loc[index_similarity, ['ASIN', 'Nom', 'Prix Actuel', 'Catégorie produit', 'Couleur', 'Marque']]