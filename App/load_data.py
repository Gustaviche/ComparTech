import pandas as pd

def load_data(type_produit):
    base_url = "https://raw.githubusercontent.com/Gustaviche/ComparTech/refs/heads/main/DataFrame/"
    if type_produit == "Écrans":
        return pd.read_csv(f"{base_url}ecrans.csv")
    elif type_produit == "Smartphones":
        return pd.read_csv(f"{base_url}smartphones.csv")
    elif type_produit == "TVs":
        return pd.read_csv(f"{base_url}tvs.csv")
    elif type_produit == "Tablettes":
        return pd.read_csv(f"{base_url}tablettes.csv")
    elif type_produit == "Ordinateurs":
        return pd.read_csv(f"{base_url}ordinateurs.csv")

def load_reviews():
    return pd.read_csv("https://raw.githubusercontent.com/Gustaviche/ComparTech/refs/heads/main/DataFrame/reviews.csv")
