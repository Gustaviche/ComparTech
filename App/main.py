import streamlit as st
from load_data import load_data, load_reviews
from filters import apply_common_filters, apply_specific_filters
from display import display_product, display_reviews, display_seller
from chatbots import chatbot_response, init_chat  # Importer la fonction d'initialisation du chat


# Définir le CSS avec overlay semi-transparent
def background():
    st.markdown("""
    <style>
    /* Fond global pour l'application */
    .stApp {
        background-image: url('https://raw.githubusercontent.com/Gustaviche/ComparTech/refs/heads/main/App/DALL%C2%B7E%202025-02-19%2016.08.57%20-%20A%20modern%20and%20sleek%20background%20for%20an%20e-commerce%20website%20specializing%20in%20computer%20hardware.%20The%20image%20features%20a%20futuristic%2C%20tech-inspired%20design%20with%20.webp');
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }
    
    .stSidebar {
        background: rgba(255, 255, 255, 0.7) !important; /* Fond semi-transparent */
        backdrop-filter: blur(10px); /* Flou pour un effet élégant */
    }
                
    /* Ciblage des widgets (conteneur principal) */
    div.block-container {
        background: rgba(255, 255, 255, 0.90); /* Transparence blanche */
        border-radius: 15px; /* Coins arrondis */
        padding: 20px; /* Espacement interne */
    }
                
    div.data-v-5af006b8 {
        border-radius: 15px;
    }
    </style>
    """, unsafe_allow_html=True)

st.set_page_config(
    page_title="ComparTech",
    page_icon="💻",
    layout="centered",
    initial_sidebar_state="expanded"
)

background()

st.title("📱💻📺 Welcome to ComparTech !")
st.write("**Enfin un site où vous allez pouvoir filtrer vos produits tech préférés !**")

st.sidebar.header("🔍 Filtres")

# Sélectionner le type de produit avec "Tous"
type_produit = st.sidebar.selectbox("**Type de produit**", 
    ["Tous", "Écrans", "Smartphones", "TVs", "Tablettes", "Ordinateurs"])

# Charger les données
if type_produit == "Tous":
    df = load_data("all")  # Charge toutes les catégories
else:
    df = load_data(type_produit)

df_reviews = load_reviews()

# Double slider pour le prix
prix_min = int(df['Prix Actuel'].min())
prix_max = int(df['Prix Actuel'].max())
prix_range = st.sidebar.slider("**Fourchette de prix (€)**", prix_min, prix_max, (prix_min, prix_max))
evaluation_min = st.sidebar.slider("**Évaluation minimale** ⭐", 1.0, 5.0, 3.0)

# Paramètres de filtre spécifiques au type de produit (uniquement si ce n'est pas "Tous")
filter_params = {}
if type_produit in ["Écrans", "TVs"]:
    filter_params['taille_ecran'] = st.sidebar.slider("**Taille d'écran (pouces)**", 10, 100, (15, 30))
    filter_params['type_ecran' if type_produit == "Écrans" else 'technologie_affichage'] = st.sidebar.selectbox(
        "**Type d'écran**" if type_produit == "Écrans" else "Technologie d'affichage", 
        options=['Tous', 'IPS', 'VA', 'LCD', 'OLED'] if type_produit == "Écrans" else ['Tous', 'LED', 'OLED', 'QLED']
    )
elif type_produit in ["Smartphones", "Tablettes"]:
    filter_params['taille_ecran'] = st.sidebar.slider("**Taille d'écran (pouces)**", 5, 13, (6, 10))
    filter_params['os'] = st.sidebar.selectbox("**Système d'exploitation**", options=['Tous', 'Android', 'iOS'])
elif type_produit == "Ordinateurs":
    filter_params['ram'] = st.sidebar.slider("**RAM minimale (Go)**", 4, 64, 8)
    filter_params['stockage'] = st.sidebar.slider("**Stockage minimal (Go)**", 128, 2048, 256)

# Filtrer les marques disponibles dans les données
marques_disponibles = ["Toutes"] + sorted(df["Marque"].dropna().unique().tolist())
marque_selectionnee = st.sidebar.selectbox("**Marque**", marques_disponibles)

# Appliquer le filtre sur la marque
if marque_selectionnee != "Toutes":
    df = df[df["Marque"] == marque_selectionnee]

# Appliquer les filtres globaux
df_filtré = apply_common_filters(df, prix_range[0], prix_range[1], evaluation_min)

# Appliquer les filtres spécifiques si un type est sélectionné (hors "Tous")
if type_produit != "Tous":
    df_filtré = apply_specific_filters(df_filtré, type_produit, **filter_params)

# Afficher les produits filtrés après recherche
if not df_filtré.empty:
    for _, row in df_filtré.iterrows():
        display_product(row, row["Catégorie produit"])  # Adapté à toutes les catégories
        display_reviews(df_reviews, row)
        display_seller(row)
else:
    st.write("⚠ Aucun produit ne correspond à votre recherche.")

# Afficher les produits filtrés
st.subheader(f"🎯 {type_produit if type_produit != 'Tous' else 'Tous les produits'} filtrés")

if not df_filtré.empty:
    for _, row in df_filtré.iterrows():
        display_product(row, row["Catégorie produit"])  # Prend en compte toutes les catégories
        display_reviews(df_reviews, row)
        display_seller(row)
else:
    st.write("⚠ Aucun produit ne correspond à vos critères.")

# Initialiser la session du chatbot
init_chat()  # Assure-toi que le chat est initialisé depuis chatbots.py

# Initialiser l'historique des messages si nécessaire
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Bonjour ! Comment puis-je vous aider ? 🤖"}
    ]

# Interface du chatbot dans la barre latérale
with st.sidebar:
    st.title("💬 Chatbot")

    # Afficher tout l'historique des messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):  # Affichage propre des messages
            st.markdown(message["content"])

    # Champ de saisie pour que l'utilisateur puisse répondre
    user_input = st.chat_input("Écrivez votre message ici...")

    if user_input:
        # Ajouter le message utilisateur à l'historique
        st.session_state.messages.append({"role": "user", "content": user_input})

        # Obtenir la réponse du chatbot
        bot_response = chatbot_response(user_input)

        # Ajouter la réponse du chatbot à l'historique
        st.session_state.messages.append({"role": "assistant", "content": bot_response})

        # Afficher immédiatement la réponse du chatbot
        with st.chat_message("assistant"):
            st.markdown(bot_response)

        # Relancer l'application pour rafraîchir l'interface
        st.rerun()
