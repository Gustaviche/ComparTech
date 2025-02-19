
import streamlit as st
from load_data import load_product_table, load_reviews
from similarity import create_model, similarity_search, search_products
from filters import apply_common_filters, apply_specific_filters
from display import display_product, display_reviews, display_seller

# Chargement des données
df_products = load_product_table()
df_reviews = load_reviews()

# Création du modèle de similarité
cols_to_keep = ["Prix Actuel", "Catégorie produit", "Couleur", "Marque"]
df_knn = df_products.loc[:, cols_to_keep]
preprocess_pipeline, knn, data_knn = create_model(df_knn)

st.title("📱💻📺 Comparateur de produits")

# Barre de recherche
search_query = st.text_input("🔍 Recherchez un produit")

if search_query:
    matching_products = search_products(df_products, search_query)
    if not matching_products.empty:
        st.write("Produits correspondants :")
        st.dataframe(matching_products[['ASIN', 'Nom', 'Prix Actuel', 'Catégorie produit', 'Couleur', 'Marque']])
        
        selected_asin = st.selectbox("Sélectionnez un produit pour voir les détails et les similaires", matching_products['ASIN'])
        if selected_asin:
            selected_product = df_products[df_products['ASIN'] == selected_asin].iloc[0]
            display_product(selected_product, selected_product['Catégorie produit'])
            display_reviews(df_reviews, selected_product)
            display_seller(selected_product)
            
            st.write("Produits similaires :")
            similar_products = similarity_search(selected_asin, df_products, knn, data_knn)
            for _, row in similar_products.iterrows():
                display_product(row, row['Catégorie produit'])
    else:
        st.error("Aucun produit trouvé. Essayez d'autres mots-clés.")

# Filtres
st.sidebar.header("🔍 Filtres")

type_produit = st.sidebar.selectbox("Type de produit", 
    ["Tous", "Écrans", "Smartphones", "TVs", "Tablettes", "Ordinateurs"])

if type_produit != "Tous":
    df_filtered = df_products[df_products['Catégorie produit'] == type_produit]
else:
    df_filtered = df_products

# Double slider pour le prix
prix_min = float(df_filtered['Prix Actuel'].min())
prix_max = float(df_filtered['Prix Actuel'].max())
prix_range = st.sidebar.slider("Fourchette de prix (€)", prix_min, prix_max, (prix_min, prix_max))
evaluation_min = st.sidebar.slider("Évaluation minimale ⭐", 1.0, 5.0, 3.0)

filter_params = {}
if type_produit in ["Écrans", "TVs", "Tous"]:
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

df_filtré = apply_common_filters(df_filtered, prix_range[0], prix_range[1], evaluation_min)
df_filtré = apply_specific_filters(df_filtré, type_produit, **filter_params)

st.subheader(f"🎯 Produits filtrés")

if not df_filtré.empty:
    for _, row in df_filtré.iterrows():
        display_product(row, row['Catégorie produit'])
        display_reviews(df_reviews, row)
        display_seller(row)
else:
    st.write("⚠ Aucun produit ne correspond à vos critères.")