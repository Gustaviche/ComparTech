import streamlit as st
import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer, make_column_selector
from sklearn.neighbors import NearestNeighbors

@st.cache_resource
def create_model(df_knn):
    numeric_transformer = Pipeline(steps=[('scaler', StandardScaler())])
    categorical_transformer = Pipeline(steps=[('onehot', OneHotEncoder(handle_unknown='ignore'))])
    preprocessor = ColumnTransformer(transformers=[
        ('num', numeric_transformer, make_column_selector(dtype_include=np.number)),
        ('cat', categorical_transformer, make_column_selector(dtype_include=object))
    ])
    preprocess_pipeline = Pipeline(steps=[('preprocessor', preprocessor)])
    
    data_knn = preprocess_pipeline.fit_transform(df_knn)
    
    knn = NearestNeighbors(n_neighbors=6)
    knn.fit(data_knn)
    
    return preprocess_pipeline, knn, data_knn

def similarity_search(asin, df, knn, data_knn):
    product_index = df.loc[df['ASIN']==asin].index
    product = data_knn[product_index]
    index_similarity = knn.kneighbors(product)[1].tolist()[0][1:]
    return df.loc[index_similarity, ['ASIN', 'Nom', 'Prix Actuel', 'Catégorie produit', 'Couleur', 'Marque']]

def search_products(df, query):
    return df[df['Nom'].str.contains(query, case=False, na=False)]
