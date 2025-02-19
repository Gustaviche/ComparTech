import pandas as pd

def apply_common_filters(df, prix_min, prix_max, evaluation_min):
    return df[
        (df['Prix Actuel'] >= prix_min) & 
        (df['Prix Actuel'] <= prix_max) &
        (df['Évaluation moyenne'] >= evaluation_min)
    ]

def apply_specific_filters(df, type_produit, **kwargs):
    # Convertir la colonne 'Taille de l\'écran' en numérique
    df['Taille de l\'écran'] = pd.to_numeric(df['Taille de l\'écran'], errors='coerce')

    if type_produit in ["Écrans", "TVs", "Tous"]:
        df = df[
            (df['Taille de l\'écran'].between(kwargs['taille_ecran'][0], kwargs['taille_ecran'][1]))
        ]
        if type_produit == "Écrans":
            df = df[
                (df['Type d\'écran'] == kwargs['type_ecran']) | (kwargs['type_ecran'] == 'Tous')
            ]
        elif type_produit == "TVs":
            df = df[
                (df['Technologie d\'affichage'] == kwargs['technologie_affichage']) | (kwargs['technologie_affichage'] == 'Tous')
            ]
    elif type_produit in ["Smartphones", "Tablettes"]:
        df = df[
            (df['Taille de l\'écran'].between(kwargs['taille_ecran'][0], kwargs['taille_ecran'][1])) &
            ((df['Système d\'exploitation'] == kwargs['os']) | (kwargs['os'] == 'Tous'))
        ]
    elif type_produit == "Ordinateurs":
        df = df[
            (df['Mémoire maximale'] >= kwargs['ram']) &
            (df['Taille du disque dur'] >= kwargs['stockage'])
        ]
    return df
