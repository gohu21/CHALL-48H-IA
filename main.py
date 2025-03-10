import os
import logging
from save import sauvegarder_fichier, sauvegarder_kpis
from load import charger_fichier_csv
from cleaning import (nettoyer_texte_sauf_liens, nettoyer_date, nettoyer_identifiants, 
                      extraire_informations, ajouter_mots, calculer_kpis)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def nettoyer_et_traiter(fichier_entree, fichier_csv_sortie, mots_cles, mots_cles_critiques):
    df = charger_fichier_csv(fichier_entree)

    logger.info("[INFO] Nettoyage du texte des tweets...")
    df['full_text'] = df['full_text'].apply(nettoyer_texte_sauf_liens)

    df = nettoyer_date(df)
    df = nettoyer_identifiants(df)
    df = extraire_informations(df)
    df = ajouter_mots(df, 'presence_mots_cles', mots_cles)
    df = ajouter_mots(df, 'presence_mots_cles_critiques', mots_cles_critiques)

    df = calculer_kpis(df)

    sauvegarder_fichier(df, fichier_csv_sortie)
    return df

if __name__ == "__main__":
    output_dir = './output'
    os.makedirs(output_dir, exist_ok=True)

    fichier_csv_sortie = os.path.join(output_dir, 'filtered_tweets_engie_cleaned.csv')
    fichier_kpi_csv = os.path.join(output_dir, 'kpis_tweets.csv')

    mots_cles = ['énergie', 'transition', 'engie']
    mots_cles_critiques = ['délai', 'panne', 'urgence', 'scandale']

    df = nettoyer_et_traiter(
        'filtered_tweets_engie.csv',
        fichier_csv_sortie,
        mots_cles,
        mots_cles_critiques
    )

    sauvegarder_kpis(df, fichier_kpi_csv)
