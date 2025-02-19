import streamlit as st
import pandas as pd
import ast

# Titre de l'application
st.title("📱💻📺 Comparateur de produits")

# Sidebar pour les filtres
st.sidebar.header("🔍 Filtres")

# Sélection du type de produit
type_produit = st.sidebar.selectbox("Type de produit", 
    ["Écrans", "Smartphones", "TVs", "Tablettes", "Ordinateurs"])

# Chargement conditionnel des données
if type_produit == "Écrans":
    df = pd.read_csv("https://raw.githubusercontent.com/Gustaviche/ComparTech/refs/heads/main/DataFrame/ecrans.csv")
elif type_produit == "Smartphones":
    df = pd.read_csv("https://raw.githubusercontent.com/Gustaviche/ComparTech/refs/heads/main/DataFrame/smartphones.csv")
elif type_produit == "TVs":
    df = pd.read_csv("https://raw.githubusercontent.com/Gustaviche/ComparTech/refs/heads/main/DataFrame/tvs.csv")
elif type_produit == "Tablettes":
    df = pd.read_csv("https://raw.githubusercontent.com/Gustaviche/ComparTech/refs/heads/main/DataFrame/tablettes.csv")
elif type_produit == "Ordinateurs":
    df = pd.read_csv("https://raw.githubusercontent.com/Gustaviche/ComparTech/refs/heads/main/DataFrame/ordinateurs.csv")

df_reviews = pd.read_csv("https://raw.githubusercontent.com/Gustaviche/ComparTech/refs/heads/main/DataFrame/reviews.csv")

# Filtres communs
prix_min = st.sidebar.slider("Prix minimum (€)", 0, int(df['Prix Actuel'].max()), 0)
prix_max = st.sidebar.slider("Prix maximum (€)", 0, int(df['Prix Actuel'].max()), int(df['Prix Actuel'].max()))
evaluation_min = st.sidebar.slider("Évaluation minimale ⭐", 1.0, 5.0, 3.0)

# Filtres spécifiques
if type_produit == "Écrans":
    taille_ecran = st.sidebar.slider("Taille d'écran (pouces)", 10, 75, (15, 30))
    type_ecran = st.sidebar.selectbox("Type d'écran", options=['Tous', 'IPS', 'VA', 'LCD', 'OLED'])
elif type_produit == "TVs":
    taille_ecran = st.sidebar.slider("Taille d'écran (pouces)", 10, 75, (15, 30))
    technologie_affichage = st.sidebar.selectbox("Technologie d'affichage", options=['Tous', 'LED', 'OLED', 'QLED'])
elif type_produit in ["Smartphones", "Tablettes"]:
    taille_ecran = st.sidebar.slider("Taille d'écran (pouces)", 5, 13, (6, 10))
    os = st.sidebar.selectbox("Système d'exploitation", options=['Tous', 'Android', 'iOS'])
elif type_produit == "Ordinateurs":
    ram = st.sidebar.slider("RAM minimale (Go)", 4, 64, 8)
    stockage = st.sidebar.slider("Stockage minimal (Go)", 128, 2048, 256)

# Application des filtres
df_filtré = df[
    (df['Prix Actuel'] >= prix_min) & 
    (df['Prix Actuel'] <= prix_max) &
    (df['Évaluation moyenne'] >= evaluation_min)
]

if type_produit == "Écrans":
    df_filtré = df_filtré[
        (df_filtré['Taille de l\'écran'].between(taille_ecran[0], taille_ecran[1])) &
        ((df_filtré['Type d\'écran'] == type_ecran) | (type_ecran == 'Tous'))
    ]
elif type_produit == "TVs":
    df_filtré = df_filtré[
        (df_filtré['Taille de l\'écran'].between(taille_ecran[0], taille_ecran[1])) &
        ((df_filtré['Technologie d\'affichage'] == technologie_affichage) | (technologie_affichage == 'Tous'))
    ]
elif type_produit in ["Smartphones", "Tablettes"]:
    df_filtré = df_filtré[
        (df_filtré['Taille de l\'écran'].between(taille_ecran[0], taille_ecran[1])) &
        ((df_filtré['Système d\'exploitation'] == os) | (os == 'Tous'))
    ]
elif type_produit == "Ordinateurs":
    df_filtré = df_filtré[
        (df_filtré['Mémoire maximale'] >= ram) &
        (df_filtré['Taille du disque dur'] >= stockage)
    ]

# Affichage des produits
st.subheader(f"🎯 {type_produit} filtrés")

if not df_filtré.empty:
    num_columns = 1
    columns = st.columns(num_columns)

    for i, (_, row) in enumerate(df_filtré.iterrows()):
        # Conversion des colonnes stockées sous forme de string en listes
        for col in ['Vendeur', 'Lien', 'Feature Bullets', 'Prix']:
            if isinstance(row[col], str):
                try:
                    row[col] = ast.literal_eval(row[col])
                except:
                    row[col] = []

        col = columns[i % num_columns]
        with col:
            st.image(row['Images'], width=150)
            st.write(f"**{row['Nom']}**")
            st.write(f"**Marque :** {row['Marque']}")
            st.write(f"**Prix Amazon :** {row['Prix Actuel']} €")
            st.write(f"**Évaluation :** {row['Évaluation moyenne']} ⭐")
            
            # Affichage des caractéristiques spécifiques
            if type_produit == "Écrans":
                st.write(f"**Type d'écran :** {row['Type d\'écran']}")
                st.write(f"**Taille :** {row['Taille de l\'écran']} pouces")
            elif type_produit == "TVs":
                st.write(f"**Technologie d'affichage :** {row['Technologie d\'affichage']}")
                st.write(f"**Taille :** {row['Taille de l\'écran']} pouces")
            elif type_produit in ["Smartphones", "Tablettes"]:
                st.write(f"**Système d'exploitation :** {row['Système d\'exploitation']}")
                st.write(f"**Taille :** {row['Taille de l\'écran']} pouces")
                if 'Capacité de stockage de la mémoire' in row:
                    st.write(f"**Stockage :** {row['Capacité de stockage de la mémoire']} Go")
            elif type_produit == "Ordinateurs":
                st.write(f"**Processeur :** {row['Type de processeur']}")
                st.write(f"**RAM :** {row['Mémoire maximale']} Go")
                st.write(f"**Stockage :** {row['Taille du disque dur']} Go")
            
            st.write(f"**Description :** {row['Feature Bullets'][0]}")

            # Affichage des résumés de reviews
            st.write("**Ce que pensent les utilisateurs :**")
            product_reviews = df_reviews[df_reviews['ASIN'] == row['ASIN']]
            if not product_reviews.empty:
                for _, review in product_reviews.iterrows():
                    st.write(f"- {review['Summary']}")
            else:
                st.write("Aucune review disponible pour ce produit.")
            
            # Affichage des vendeurs avec leurs liens
            st.write("**Produits sur d'autres sites :**")
            for nom_site, lien, prix in zip(row['Vendeur'], row['Lien'], row['Prix']):
                st.markdown(f"- [{nom_site}]({lien}) - {prix}€", unsafe_allow_html=True)
            st.markdown("---")

else:
    st.write("⚠ Aucun produit ne correspond à vos critères.")
