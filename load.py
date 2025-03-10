import pandas as pd

def charger_fichier_csv(fichier):
    """Charge un fichier CSV dans un DataFrame."""
    return pd.read_csv(fichier, encoding='utf-8', sep=';')
