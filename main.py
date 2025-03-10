import os
import logging
from save import sauvegarder_fichier, sauvegarder_kpis_details, sauvegarder_kpis_combines
from load import charger_fichier_csv
from cleaning import (
    nettoyer_texte_sauf_liens,
    nettoyer_date,
    nettoyer_identifiants,
    extraire_informations,
    ajouter_mots,
    calculer_kpis
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def nettoyer_et_traiter(fichier_entree, fichier_csv_sortie, mots_cles, mots_cles_critiques):
    logger.info(f"[INFO] Chargement du fichier : {fichier_entree}")
    df = charger_fichier_csv(fichier_entree)

    logger.info("[INFO] Nettoyage du texte des tweets...")
    df['full_text'] = df['full_text'].apply(nettoyer_texte_sauf_liens)

    logger.info("[INFO] Nettoyage et standardisation des dates...")
    df = nettoyer_date(df)

    logger.info("[INFO] Nettoyage des identifiants...")
    df = nettoyer_identifiants(df)

    logger.info("[INFO] Extraction d'informations supplémentaires (heure, longueur)...")
    df = extraire_informations(df)

    logger.info("[INFO] Détection des mots-clés standards...")
    df = ajouter_mots(df, 'presence_mots_cles', mots_cles)

    logger.info("[INFO] Détection des mots-clés critiques...")
    df = ajouter_mots(df, 'presence_mots_cles_critiques', mots_cles_critiques)

    logger.info("[INFO] Calcul des KPI détaillés...")
    df, kpi_jour, kpi_semaine, kpi_mois, kpi_heure = calculer_kpis(df)

    logger.info(f"[INFO] Sauvegarde du fichier nettoyé : {fichier_csv_sortie}")
    sauvegarder_fichier(df, fichier_csv_sortie)

    return df, kpi_jour, kpi_semaine, kpi_mois, kpi_heure


if __name__ == "__main__":
    output_dir = './output'
    kpi_output_dir = os.path.join(output_dir, 'KPIs')
    os.makedirs(output_dir, exist_ok=True)

    fichier_entree = 'filtered_tweets_engie.csv'
    fichier_csv_sortie = os.path.join(output_dir, 'filtered_tweets_engie_cleaned.csv')

    mots_cles = ['énergie', 'transition', 'engie']
    mots_cles_critiques = ['délai', 'panne', 'urgence', 'scandale']

    df, kpi_jour, kpi_semaine, kpi_mois, kpi_heure = nettoyer_et_traiter(
        fichier_entree,
        fichier_csv_sortie,
        mots_cles,
        mots_cles_critiques
    )

    sauvegarder_kpis_details(kpi_jour, kpi_semaine, kpi_mois, kpi_heure, kpi_output_dir)
    sauvegarder_kpis_combines(kpi_jour, kpi_semaine, kpi_mois, kpi_heure, output_dir)
