import pandas as pd

def charger_donnees(fichier):
    try:
        df = pd.read_csv(fichier)
        return df
    except FileNotFoundError:
        print(f"⚠️ Fichier {fichier} introuvable.")
        return pd.DataFrame()  # Retourne un DataFrame vide en cas d'erreur
    except Exception as e:
        print(f"Erreur lors du chargement de {fichier} : {e}")
        return pd.DataFrame()

# Chargement des données
ordinateurs = charger_donnees("df_ordi_cleaned.csv")
telephones = charger_donnees("df_smartphones_cleaned.csv")
ecrans = charger_donnees("df_ecrans_cleaned.csv")
tablettes = charger_donnees("df_tablettes_cleaned.csv")
tvs = charger_donnees("df_tvs_cleaned.csv")
