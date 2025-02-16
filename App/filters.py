import pandas as pd

def filtrer_donnees(df, filtres):
    """Applique les filtres sélectionnés sur le DataFrame."""
    if df.empty:
        return df  # Évite les erreurs si le DataFrame est vide

    df_filtre = df.copy()

    # Filtre par marque
    if "Marque" in df.columns and filtres.get("marque"):
        df_filtre = df_filtre[df_filtre["Marque"].isin(filtres["marque"])]

    # Filtre par prix
    if "Prix Actuel" in df.columns:
        if filtres.get("prix_min") is not None:
            df_filtre = df_filtre[df_filtre["Prix Actuel"] >= filtres["prix_min"]]
        if filtres.get("prix_max") is not None:
            df_filtre = df_filtre[df_filtre["Prix Actuel"] <= filtres["prix_max"]]

    # Filtres avancés pour les ordinateurs portables
    if "Marque du processeur" in df.columns and filtres.get("processeur"):
        df_filtre = df_filtre[df_filtre["Marque du processeur"].isin(filtres["processeur"])]

    if "Taille de l'écran" in df.columns and filtres.get("taille_ecran"):
        df_filtre = df_filtre[df_filtre["Taille de l'écran"].isin(filtres["taille_ecran"])]

    if "Mémoire maximale" in df.columns and filtres.get("ram"):
        df_filtre = df_filtre[df_filtre["Mémoire maximale"].isin(filtres["ram"])]

    if "Évaluation moyenne" in df.columns and filtres.get("rating") is not None:
        df_filtre = df_filtre[df_filtre["Évaluation moyenne"] >= filtres["rating"]]

    # Décalage de la virgule pour le prix, si le prix est sous forme de chaîne de caractères
    if "Prix Actuel" in df.columns:
        df_filtre["Prix Actuel"] = df_filtre["Prix Actuel"].replace({'€': '', ',': ''}, regex=True)
        df_filtre["Prix Actuel"] = pd.to_numeric(df_filtre["Prix Actuel"], errors='coerce') / 100

    return df_filtre
