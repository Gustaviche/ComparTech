import streamlit as st
import pandas as pd

@st.cache_data
def load_product_table():
    df = pd.read_csv("Table_produits_withname.csv")
    
    clean_func = lambda nom: "Google" if "Google" in nom else "Apple"
    clean_names = df.loc[(df["Marque"]=="LENOVO") & (df["Catégorie produit"]=="Smartphone"), 'Nom'].apply(clean_func)
    df.loc[(df["Marque"]=="LENOVO") & (df["Catégorie produit"]=="Smartphone"), "Marque"] = clean_names
    
    return df

def load_reviews():
    return pd.read_csv("https://raw.githubusercontent.com/Gustaviche/ComparTech/refs/heads/main/DataFrame/reviews.csv")
