import logging

logger = logging.getLogger(__name__)

def sauvegarder_fichier(df, fichier_csv):
    logger.info(f"[INFO] Sauvegarde du fichier nettoyé: {fichier_csv}")
    df.to_csv(fichier_csv, index=False, encoding='utf-8')
    logger.info(f"[SUCCESS] Fichier CSV '{fichier_csv}' sauvegardé avec succès.")

def sauvegarder_kpis(df, fichier_kpi_csv):
    logger.info(f"[INFO] Sauvegarde des KPI dans '{fichier_kpi_csv}'...")
    kpi_df = df[['date', 'nombre_tweets_par_jour', 'semaine', 'nombre_tweets_par_semaine', 'mois', 'nombre_tweets_par_mois', 
                 'mentions_engie', 'tweets_critiques', 'tweets_mots_cles', 'heure', 'nombre_tweets_par_heure']]
    kpi_df.to_csv(fichier_kpi_csv, index=False, encoding='utf-8')
    logger.info(f"[SUCCESS] KPI CSV '{fichier_kpi_csv}' sauvegardé avec succès.")
