def sort_products(df, sort_by, ascending=True):
    """Trie les produits selon le critère sélectionné."""
    if sort_by == "Prix":
        return df.sort_values(by="Prix Actuel", ascending=ascending)
    elif sort_by == "Évaluation":
        return df.sort_values(by="Évaluation moyenne", ascending=not ascending)
    elif sort_by == "Marque":
        return df.sort_values(by="Marque", ascending=ascending)
    elif sort_by == "Taille d'écran" and "Taille de l'écran" in df.columns:
        return df.sort_values(by="Taille de l'écran", ascending=ascending)
    return df
