def apply_common_filters(df, prix_min, prix_max, evaluation_min):
    return df[
        (df['Prix Actuel'] >= prix_min) & 
        (df['Prix Actuel'] <= prix_max) &
        (df['Évaluation moyenne'] >= evaluation_min)
    ]

def apply_specific_filters(df, type_produit, **kwargs):
    if type_produit == "Écrans":
        return df[
            (df['Taille de l\'écran'].between(kwargs['taille_ecran'][0], kwargs['taille_ecran'][1])) &
            ((df['Type d\'écran'] == kwargs['type_ecran']) | (kwargs['type_ecran'] == 'Tous'))
        ]
    elif type_produit == "TVs":
        return df[
            (df['Taille de l\'écran'].between(kwargs['taille_ecran'][0], kwargs['taille_ecran'][1])) &
            ((df['Technologie d\'affichage'] == kwargs['technologie_affichage']) | (kwargs['technologie_affichage'] == 'Tous'))
        ]
    elif type_produit in ["Smartphones", "Tablettes"]:
        return df[
            (df['Taille de l\'écran'].between(kwargs['taille_ecran'][0], kwargs['taille_ecran'][1])) &
            ((df['Système d\'exploitation'] == kwargs['os']) | (kwargs['os'] == 'Tous'))
        ]
    elif type_produit == "Ordinateurs":
        return df[
            (df['Mémoire maximale'] >= kwargs['ram']) &
            (df['Taille du disque dur'] >= kwargs['stockage'])
        ]
    return df
