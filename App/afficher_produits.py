# afficher_produit.py

import streamlit as st

def afficher_produit(df):
    # Afficher l'image du produit
    st.image(df["Images"].iloc[0], width=400)
    
    # Afficher le nom du produit
    st.title(df["Nom"].iloc[0])
    
    # Afficher le prix
    st.subheader(f"Prix : {df['Prix Actuel'].iloc[0]}€")
    
    # Afficher les évaluations et avis
    st.write(f"**Évaluation** : {df['Évaluation moyenne'].iloc[0]} ⭐ ({df['total_ratings'].iloc[0]} avis)")
    
    # Afficher les caractéristiques principales
    st.write("### Caractéristiques principales :")
    st.write(f"- **Processeur** : {df['Marque du processeur'].iloc[0]} {df['Type de processeur'].iloc[0]} à {df['Vitesse du processeur'].iloc[0]} GHz")
    st.write(f"- **Mémoire vive** : {df['Mémoire maximale'].iloc[0]} Go")
    st.write(f"- **Taille de l'écran** : {df['Taille de lécran'].iloc[0]} pouces")
    st.write(f"- **Carte graphique** : {df['GPU'].iloc[0]}")
    
    # Afficher la description complète du produit
    st.write("### Description du produit :")
    st.write(df["Description complète"].iloc[0])