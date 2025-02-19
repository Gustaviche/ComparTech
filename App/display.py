import streamlit as st
import ast

def convert_string_to_list(row):
    for col in ['Vendeur', 'Lien', 'Feature Bullets', 'Prix']:
        if isinstance(row[col], str):
            try:
                row[col] = ast.literal_eval(row[col])
            except:
                row[col] = []
    return row

def display_product(row, type_produit):
    row = convert_string_to_list(row)
    
    st.image(row['Images'], width=150)
    st.write(f"**{row['Nom']}**")
    st.write(f"**Marque :** {row['Marque']}")
    st.write(f"**Prix Amazon :** {row['Prix Actuel']} €")
    st.write(f"**Évaluation :** {row['Évaluation moyenne']} ⭐")
    
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

def display_reviews(df_reviews, row):
    st.write("**Ce que pensent les utilisateurs (IA):**")
    product_reviews = df_reviews[df_reviews['ASIN'] == row['ASIN']]
    if not product_reviews.empty:
        for _, review in product_reviews.iterrows():
            st.write(f"- {review['Summary']}")
    else:
        st.write("Aucune review disponible pour ce produit.")

def display_seller(row):
    row = convert_string_to_list(row)
    
    st.write("**Produits sur d'autres sites :**")
    for nom_site, lien, prix in zip(row['Vendeur'], row['Lien'], row['Prix']):
        st.markdown(f"- [{nom_site}]({lien}) - {prix}€", unsafe_allow_html=True)
    st.markdown("---")
