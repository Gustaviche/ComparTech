import streamlit as st
from load_data import load_data, load_reviews
from filters import apply_common_filters, apply_specific_filters
from display import display_product, display_reviews, display_seller

# Définir le CSS pour mettre l'image en arrière-plan
page_bg_img = """
<style>
[data-testid="stAppViewContainer"] {
    background-image: url("file://assets/background.png");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}
</style>
"""

# Appliquer le CSS
st.markdown(page_bg_img, unsafe_allow_html=True)

# Contenu de l'application
st.title("Mon site e-commerce")
st.write("Bienvenue sur notre boutique de matériel informatique !")


st.title("📱💻📺 Comparateur de produits")

st.sidebar.header("🔍 Filtres")

type_produit = st.sidebar.selectbox("Type de produit", 
    ["Écrans", "Smartphones", "TVs", "Tablettes", "Ordinateurs"])

df = load_data(type_produit)
df_reviews = load_reviews()

# Double slider pour le prix
prix_min = int(df['Prix Actuel'].min())
prix_max = int(df['Prix Actuel'].max())
prix_range = st.sidebar.slider("Fourchette de prix (€)", prix_min, prix_max, (prix_min, prix_max))
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

# Utilisez les valeurs de prix_range ici
df_filtré = apply_common_filters(df, prix_range[0], prix_range[1], evaluation_min)
df_filtré = apply_specific_filters(df_filtré, type_produit, **filter_params)

st.subheader(f"🎯 {type_produit} filtrés")

if not df_filtré.empty:
    for _, row in df_filtré.iterrows():
        display_product(row, type_produit)
        display_reviews(df_reviews, row)
        display_seller(row)
else:
    st.write("⚠ Aucun produit ne correspond à vos critères.")
