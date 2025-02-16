import streamlit as st
import pandas as pd
import ast  # Pour convertir les chaînes en listes

# Charger les données
df = pd.read_csv("DataFrame/ecrans.csv")

# Titre de l'application
st.title("📺 Comparateur de produits")

# Sidebar pour les filtres
st.sidebar.header("🔍 Filtres")

# Filtrer par prix
prix_min = st.sidebar.slider("Prix minimum (€)", 0, int(df['Prix Actuel'].max()), 0)
prix_max = st.sidebar.slider("Prix maximum (€)", 0, int(df['Prix Actuel'].max()), int(df['Prix Actuel'].max()))

# Filtrer par taille d'écran
taille_ecran = st.sidebar.slider("Taille d'écran (pouces)", 10, 75, (15, 30))

# Filtrer par type d'écran
type_ecran = st.sidebar.selectbox("Type d'écran", options=['Tous', 'IPS', 'VA', 'LCD', 'OLED'])

# Filtrer par évaluation
evaluation_min = st.sidebar.slider("Évaluation minimale ⭐", 1.0, 5.0, 3.0)

# Appliquer les filtres
df_filtré = df[
    (df['Prix Actuel'] >= prix_min) & 
    (df['Prix Actuel'] <= prix_max) &
    (df['Taille de l\'écran'].between(taille_ecran[0], taille_ecran[1])) &
    (df['Évaluation moyenne'] >= evaluation_min) &
    ((df['Type d\'écran'] == type_ecran) | (type_ecran == 'Tous'))
]

# Affichage des produits sous forme de cartes en colonnes
st.subheader("🎯 Produits filtrés")

if not df_filtré.empty:
    # Diviser l'écran en 3 colonnes
    num_columns = 1
    columns = st.columns(num_columns)

    for i, (_, row) in enumerate(df_filtré.iterrows()):
        # Convertir les colonnes stockées sous forme de string en listes
        for col in ['Vendeur', 'Lien', 'Feature Bullets','Prix']:
            if isinstance(row[col], str):
                try:
                    row[col] = ast.literal_eval(row[col])
                except:
                    row[col] = []

        # Vérifier que les listes ont bien la même longueur
        if len(row['Vendeur']) == len(row['Lien']):
            # Sélectionner la colonne pour chaque produit
            col = columns[i % num_columns]  # Répartir sur les 3 colonnes

            with col:
                st.image(row['Images'], width=150)
                st.write(f"**{row['Nom']}**")
                st.write(f"**Marque :** {row['Marque']}")
                st.write(f"**Type d'écran :** {row['Type d\'écran']}")
                st.write(f"**Taille :** {row['Taille de l\'écran']} pouces")
                st.write(f"**Prix Amazon :** {row['Prix Actuel']} €")
                st.write(f"**Évaluation :** {row['Évaluation moyenne']} ⭐")
                st.write(f"**Resumé :** {row['Feature Bullets'][0]}")
                # Affichage des vendeurs avec leurs liens
                st.write("**Produits sur d'autres sites :**")
                for nom_site, lien, prix in zip(row['Vendeur'], row['Lien'], row['Prix']):
                    st.markdown(f"- [{nom_site}]({lien}) - {prix}€", unsafe_allow_html=True)
                st.markdown("---")  # Séparateur entre chaque ligne de produits

else:
    st.write("⚠ Aucun produit ne correspond à vos critères.")
