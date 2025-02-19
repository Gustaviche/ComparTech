import streamlit as st
from load_data import load_data, load_reviews
from filters import apply_common_filters, apply_specific_filters
from display import display_product, display_reviews, display_seller

st.title("📱💻📺 Comparateur de produits")

st.sidebar.header("🔍 Filtres")

type_produit = st.sidebar.selectbox("Type de produit", 
    ["Écrans", "Smartphones", "TVs", "Tablettes", "Ordinateurs"])

df = load_data(type_produit)
df_reviews = load_reviews()

prix_min = st.sidebar.slider("Prix minimum (€)", 0, int(df['Prix Actuel'].max()), 0)
prix_max = st.sidebar.slider("Prix maximum (€)", 0, int(df['Prix Actuel'].max()), int(df['Prix Actuel'].max()))
evaluation_min = st.sidebar.slider("Évaluation minimale ⭐", 1.0, 5.0, 3.0)

filter_params = {}
if type_produit in ["Écrans", "TVs"]:
    filter_params['taille_ecran'] = st.sidebar.slider("Taille d'écran (pouces)", 10, 75, (15, 30))
    filter_params['type_ecran' if type_produit == "Écrans" else 'technologie_affichage'] = st.sidebar.selectbox(
        "Type d'écran" if type_produit == "Écrans" else "Technologie d'affichage", 
        options=['Tous', 'IPS', 'VA', 'LCD', 'OLED'] if type_produit == "Écrans" else ['Tous', 'LED', 'OLED', 'QLED']
    )
elif type_produit in ["Smartphones", "Tablettes"]:
    filter_params['taille_ecran'] = st.sidebar.slider("Taille d'écran (pouces)", 5, 13, (6, 10))
    filter_params['os'] = st.sidebar.selectbox("Système d'exploitation", options=['Tous', 'Android', 'iOS'])
elif type_produit == "Ordinateurs":
    filter_params['ram'] = st.sidebar.slider("RAM minimale (Go)", 4, 64, 8)
    filter_params['stockage'] = st.sidebar.slider("Stockage minimal (Go)", 128, 2048, 256)

df_filtré = apply_common_filters(df, prix_min, prix_max, evaluation_min)
df_filtré = apply_specific_filters(df_filtré, type_produit, **filter_params)

st.subheader(f"🎯 {type_produit} filtrés")

if not df_filtré.empty:
    for _, row in df_filtré.iterrows():
        display_product(row, type_produit)
        display_reviews(df_reviews, row)
        display_seller(row)
else:
    st.write("⚠ Aucun produit ne correspond à vos critères.")
