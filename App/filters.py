import pandas as pd

def apply_common_filters(df, prix_min, prix_max, evaluation_min):
    return df[
        (df['Prix Actuel'] >= prix_min) & 
        (df['Prix Actuel'] <= prix_max) &
        (df['Évaluation moyenne'] >= evaluation_min)
    ]

def apply_specific_filters(df, type_produit, **kwargs):
    # Convertir les colonnes nécessaires en numérique si besoin
    if 'Taille de l\'écran' in df.columns:
        df['Taille de l\'écran'] = pd.to_numeric(df['Taille de l\'écran'], errors='coerce')
    if 'Mémoire maximale' in df.columns:
        df['Mémoire maximale'] = pd.to_numeric(df['Mémoire maximale'], errors='coerce')
    if 'Taille du disque dur' in df.columns:
        df['Taille du disque dur'] = pd.to_numeric(df['Taille du disque dur'], errors='coerce')

    # Appliquer des filtres spécifiques selon le type de produit
    if type_produit in ["Écrans", "TVs"]:
        # Filtrer par taille d'écran
        df = df[
            (df['Taille de l\'écran'].between(kwargs['taille_ecran'][0], kwargs['taille_ecran'][1]))
        ]
        if type_produit == "Écrans":
            # Filtrer par type d'écran
            df = df[
                (df['Type d\'écran'] == kwargs['type_ecran']) | (kwargs['type_ecran'] == 'Tous')
            ]
        elif type_produit == "TVs":
            # Filtrer par technologie d'affichage
            df = df[
                (df['Technologie d\'affichage'] == kwargs['technologie_affichage']) | (kwargs['technologie_affichage'] == 'Tous')
            ]

    elif type_produit in ["Smartphones", "Tablettes"]:
        # Filtrer par taille d'écran et système d'exploitation
        df = df[
            (df['Taille de l\'écran'].between(kwargs['taille_ecran'][0], kwargs['taille_ecran'][1])) &
            ((df['Système d\'exploitation'] == kwargs['os']) | (kwargs['os'] == 'Tous'))
        ]

    elif type_produit == "Ordinateurs":
        # Filtrer par RAM et stockage minimum
        df = df[
            (df['Mémoire maximale'] >= kwargs['ram']) &
            (df['Taille du disque dur'] >= kwargs['stockage'])
        ]

    elif type_produit == "Tous":
        # Aucun filtre spécifique pour "Tous", on retourne le DataFrame tel quel
        pass

    return df

