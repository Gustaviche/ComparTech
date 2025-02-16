import streamlit as st
import pandas as pd

# Charger les DataFrames (remplace par tes propres chemins)
ordinateurs = pd.read_csv("ordinateurs.csv")
telephones = pd.read_csv("telephones.csv")

def filtrer_et_afficher(df, filtres):
    # Applique les filtres ici (exemple)
    df_filtre = df
    if filtres["marque"]:
        df_filtre = df_filtre[df_filtre["marque"].isin(filtres["marque"])]
    if filtres["prix_min"]:
        df_filtre = df_filtre[df_filtre["prix"] >= filtres["prix_min"]]
    if filtres["prix_max"]:
        df_filtre = df_filtre[df_filtre["prix"] <= filtres["prix_max"]]
    # ... autres filtres

    return df_filtre

st.title("Comparateur de Prix d'Electronique")

type_produit = st.selectbox("Sélectionner le type de produit", ["Ordinateur portable", "Téléphone"])

if type_produit == "Ordinateur portable":
    df = ordinateurs
elif type_produit == "Téléphone":
    df = telephones

# Filtres
filtres = {"marque": st.multiselect("Marque", df["marque"].unique()),
           "prix_min": st.number_input("Prix minimum", value=0),
           "prix_max": st.number_input("Prix maximum", value=10000)}

#Tri
tri = st.radio("Trier par :", ["Prix croissant", "Prix décroissant"])

df_filtre = filtrer_et_afficher(df, filtres)

if tri == "Prix croissant":
    df_filtre = df_filtre.sort_values("prix")
else:
    df_filtre = df_filtre.sort_values("prix", ascending=False)

st.dataframe(df_filtre)

# ... ajouter des visualisations si besoin