import logging
import os
import pandas as pd

logger = logging.getLogger(__name__)

def sauvegarder_fichier(df, fichier_csv):
    logger.info(f"[INFO] Sauvegarde du fichier nettoyé: {fichier_csv}")
    df.to_csv(fichier_csv, index=False, encoding='utf-8')
    logger.info(f"[SUCCESS] Fichier CSV '{fichier_csv}' sauvegardé avec succès.")


def sauvegarder_kpis_details(kpi_jour, kpi_semaine, kpi_mois, kpi_heure, output_dir):
    os.makedirs(output_dir, exist_ok=True)

    fichier_kpi_jour = os.path.join(output_dir, 'kpi_jour.csv')
    fichier_kpi_semaine = os.path.join(output_dir, 'kpi_semaine.csv')
    fichier_kpi_mois = os.path.join(output_dir, 'kpi_mois.csv')
    fichier_kpi_heure = os.path.join(output_dir, 'kpi_heure.csv')

    logger.info("[INFO] Sauvegarde des KPIs journaliers...")
    kpi_jour.to_csv(fichier_kpi_jour, index=False)

    logger.info("[INFO] Sauvegarde des KPIs hebdomadaires...")
    kpi_semaine.to_csv(fichier_kpi_semaine, index=False)

    logger.info("[INFO] Sauvegarde des KPIs mensuels...")
    kpi_mois.to_csv(fichier_kpi_mois, index=False)

    logger.info("[INFO] Sauvegarde des KPIs horaires...")
    kpi_heure.to_csv(fichier_kpi_heure, index=False)

    logger.info("[INFO] Tous les KPIs ont été sauvegardés avec succès.")

def sauvegarder_kpis_combines(kpi_jour, kpi_semaine, kpi_mois, kpi_heure, dossier_sortie, nom_fichier='KPIs_global.csv'):
    os.makedirs(dossier_sortie, exist_ok=True)
    fichier_kpis_combines = os.path.join(dossier_sortie, nom_fichier)

    logger.info("[INFO] Combinaison des KPIs en un seul fichier...")

    kpis_combines = pd.concat([kpi_jour, kpi_semaine, kpi_mois, kpi_heure], axis=0)
    kpis_combines.to_csv(fichier_kpis_combines, index=False, encoding='utf-8')

    logger.info(f"[SUCCESS] Fichier CSV combiné '{fichier_kpis_combines}' sauvegardé avec succès.")

